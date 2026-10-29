#!/usr/bin/env python3
"""Report whether Ship APs Enum, location, and Item definitions are up to date with the generated RLS output and gen_ship_data.py

Usage: python3 worlds/oot_soh/tools/check_contract.py
"""
import ast
import importlib
import pathlib
import sys

WORLD = pathlib.Path(__file__).resolve().parent.parent
REPO = WORLD.parent.parent
sys.path.insert(0, str(REPO))
GENERATED = ["functions_gen.py", "regions_gen.py"]


def definitions(path: pathlib.Path) -> set[str]:
    """Every function, class and assigned name anywhere in `path`."""
    found: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text())):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            found.add(node.name)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            found.add(node.id)
    return found


def imported_names() -> dict[tuple[str, str], set[str]]:
    """(module, name) for every name the generated files import from a world module, mapped to the
    generated files that import it."""
    wanted: dict[tuple[str, str], set[str]] = {}
    for name in GENERATED:
        for node in ast.walk(ast.parse((WORLD / name).read_text())):
            if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module:
                for alias in node.names:
                    wanted.setdefault((node.module, alias.name), set()).add(name)
    return wanted


def main() -> int:
    for name in GENERATED:
        if not (WORLD / name).exists():
            print(f"error: {name} not generated. Run tools/gen_logic.sh", file=sys.stderr)
            return 2

    wanted = imported_names()
    missing: list[tuple[str, str]] = []
    for (module, name), _files in sorted(wanted.items()):
        if module in {path.removesuffix(".py") for path in GENERATED} | {"enums_gen"}:
            provided = name in definitions(WORLD / f"{module}.py")
        else:
            provided = hasattr(importlib.import_module(f"worlds.oot_soh.{module}"), name)
        if not provided:
            missing.append((module, name))

    print(f"host contract: {len(wanted)} names imported by generated logic, "
          f"from {len({module for module, _ in wanted})} modules")
    print(f"  MISSING ({len(missing)}):")
    for module, name in missing:
        print(f"    {name:38s} <- .{module} ({', '.join(sorted(wanted[(module, name)]))})")

    uses = attribute_uses()
    print()
    print(enum_member_report(uses))
    print()
    print(alias_report())
    print()
    print(item_table_report(uses["Items"]))
    return 1 if missing else 0


def enum_members(path: pathlib.Path) -> dict[str, set[str]]:
    """Map each enum class defined in `path` to its member names."""
    return {node.name: {t.id for stmt in node.body if isinstance(stmt, ast.Assign)
                        for t in stmt.targets if isinstance(t, ast.Name)}
            for node in ast.walk(ast.parse(path.read_text())) if isinstance(node, ast.ClassDef)}


def attribute_uses() -> dict[str, set[str]]:
    """`Name.attr` accesses in the generated logic, as name -> attrs."""
    uses: dict[str, set[str]] = {}
    for name in GENERATED:
        for node in ast.walk(ast.parse((WORLD / name).read_text())):
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
                uses.setdefault(node.value.id, set()).add(node.attr)
    return uses


def enum_member_report(uses: dict[str, set[str]]) -> str:
    """Check every `Enum.MEMBER` the generated logic uses actually exists.

    The enums are glob-declared in RLS (`extern enum Trick { RT_* }`), so a misspelt member
    transpiles cleanly; this is where it surfaces.
    """
    available: dict[str, set[str]] = {}
    for mod in ["Enums.py", "enums_gen.py", "ship_data_gen.py", "LogicHelpers.py"]:
        for cls, members in enum_members(WORLD / mod).items():
            available.setdefault(cls, set()).update(members)
    used = {cls: attrs for cls, attrs in uses.items() if cls in available}

    lines = ["enum members referenced by generated logic:"]
    for cls in sorted(used):
        absent = sorted(used[cls] - available[cls])
        status = "ok" if not absent else f"{len(absent)} MISSING"
        lines.append(f"  {cls:22s} used={len(used[cls]):5d}  {status}")
        for member in absent[:5]:
            lines.append(f"      e.g. {member}")
        if len(absent) > 5:
            lines.append(f"      ... and {len(absent) - 5} more")
    return "\n".join(lines)


def item_table_report(used: set[str]) -> str:
    """Check every item the generated logic asks for actually exists in the item pool.

    Separate from the enum check: Items.RG_X can be a perfectly good enum member and still name
    an item the world has no data row for, in which case the rule can never be satisfied. Most
    of the gap is Ship's item-ified abilities (RG_OPEN_CHEST, RG_CLIMB, the RG_SPEAK_* tongues,
    bean souls), which the world models as always-available rather than as items.
    """
    try:
        from worlds.oot_soh.Items import item_data_table  # noqa: PLC0415
        from worlds.oot_soh.ship_data_gen import Items  # noqa: PLC0415
    except Exception as e:  # noqa: BLE001 - importing the world drags in all of AP
        return f"item table: skipped ({type(e).__name__}: {e})"

    # Pseudo-items: real enum members with ids, but has_item resolves them to a rule rather than
    # ever placing them (LogicHelpers.py), so their names never reach the client.
    logic_only = {"SCARECROW", "DISTANT_SCARECROW"}

    table = {str(key) for key in item_data_table}
    absent = sorted(m for m in used - logic_only if str(getattr(Items, m, "")) not in table)
    lines = [f"items referenced by generated logic: {len(used)}, "
             f"{len(absent)} absent from item_data_table"]
    lines += [f"    {m:38s} {str(getattr(Items, m))!r}" for m in absent]
    return "\n".join(lines)


def alias_report() -> str:
    """Find generated StrEnum members that share a value.

    Python makes the second declaration an *alias* of the first, so two distinct RLS regions
    with the same `name:` silently become one AP region and their locations and exits merge.
    Ship never sees this -- its C++ enum keys by the member name -- so it is an AP-only trap,
    and an upstream copy-paste in a `name:` is all it takes.
    """
    lines = ["generated enum value collisions:"]
    found = False
    for node in (n for mod in ("enums_gen.py", "ship_data_gen.py")
                 for n in ast.walk(ast.parse((WORLD / mod).read_text()))):
        if not (isinstance(node, ast.ClassDef) and any(getattr(b, "id", None) == "StrEnum" for b in node.bases)):
            continue
        seen: dict[str, str] = {}
        for stmt in node.body:
            if not (isinstance(stmt, ast.Assign) and isinstance(stmt.targets[0], ast.Name)
                    and isinstance(stmt.value, ast.Constant)):
                continue
            name, value = stmt.targets[0].id, stmt.value.value
            if value in seen:
                lines.append(f"  {node.name}: {name} aliases {seen[value]} -- both are {value!r}")
                found = True
            else:
                seen[value] = name
    if not found:
        lines.append("  none")
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
