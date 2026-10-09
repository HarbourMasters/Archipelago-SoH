#!/usr/bin/env python3
"""Generate ship_data_gen.py: the enums and data tables the world mirrors from Shipwright.

- Locations / Items / Tricks: Ship's names, which the client resolves checks, items and
  tricks_in_logic by. Only tricks the logic uses; ones with no OPT_TRICK are in DISABLED_TRICKS.
- Enemies / EnemyDistance / TrialKey: Ship's enums, in Ship's order.
- RandomizerSettingKey: Ship's RO_* values; each is its index in its RANDO_ENUM group, which
  must equal the AP `option_*` value.

Also verifies the RSK_* option classes, MQ dungeon names and slot-data keys against Ship.
Run after gen_logic.sh (the trick filter reads the generated logic).

Usage: python3 worlds/oot_soh/tools/gen_ship_data.py path/to/Shipwright
"""
import ast
import json
import pathlib
import re
import sys

WORLD = pathlib.Path(__file__).resolve().parent.parent
OUT = WORLD / "ship_data_gen.py"
RANDO = "soh/soh/Enhancements/randomizer"

# Items with no Ship itemTable row
ITEM_OVERRIDES = {
    "RG_STICKS": "Sticks",
    "RG_NUTS": "Nuts",
    "RG_SCARECROW": "Scarecrow",
    "RG_DISTANT_SCARECROW": "Distant Scarecrow",
    "RG_EPONA": "Epona",
    "RG_GLITCHED": "Glitched Item",
    "RG_RESERVATION": "Prefill Reservation",
}


def strip_comments(src: str) -> str:
    """Drop C++ comments. Ship keeps retired enum values and OPT_TRICKs as commented-out lines."""
    return re.sub(r"//[^\n]*", "", re.sub(r"/\*.*?\*/", "", src, flags=re.S))


def rando_enum(rando: pathlib.Path, header: str, group: str) -> list[str]:
    """Members of one RANDO_ENUM_BEGIN(group) block, in order, minus the *_MAX sentinel."""
    text = strip_comments((rando / "randomizerEnums" / header).read_text())
    block = re.search(rf"RANDO_ENUM_BEGIN\({group}\)(.*?)RANDO_ENUM_END", text, re.S).group(1)
    return [m for m in re.findall(r"RANDO_ENUM_ITEM\((\w+)\)", block) if not m.endswith("_MAX")]


def call_args(text: str, start: int) -> str:
    """The argument text of a call whose opening paren has just been consumed."""
    depth = 1
    for i, c in enumerate(text[start:]):
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return text[start : start + i]
    return text[start:]


# == Locations / Items ==========================================================================

def area_prefixes(ship: pathlib.Path, rando: pathlib.Path) -> dict[str, str]:
    """RCAREA_* -> display prefix ("KF", "Market", ...), zipped in declaration order."""
    areas = rando_enum(rando, "RandomizerMiscEnums.h", "RandomizerCheckArea")
    util = strip_comments((ship / "soh/soh/util.cpp").read_text())
    arr = re.search(r"std::array<std::string, RA_MAX> rcareaPrefixes = \{(.*?)\};", util, re.S)
    return dict(zip(areas, re.findall(r'"([^"]*)"', arr.group(1))))


def scene_areas(rando: pathlib.Path) -> dict[str, str]:
    """SCENE_* -> RCAREA_*, from the GetAreaFromScene switch."""
    fn = re.search(
        r"RandomizerCheckArea GetAreaFromScene\(uint8_t scene\) \{(.*?)\n\}",
        strip_comments((rando / "location.cpp").read_text()),
        re.S,
    ).group(1)
    mapping: dict[str, str] = {}
    pending: list[str] = []
    for m in re.finditer(r"case (SCENE_\w+):|return (RCAREA_\w+);", fn):
        if m.group(1):
            pending.append(m.group(1))
        else:
            for scene in pending:
                mapping[scene] = m.group(2)
            pending = []
    return mapping


def factory_types(rando: pathlib.Path) -> dict[str, str]:
    """Location factory -> the RCTYPE it fixes (Location::Pot -> RCTYPE_POT). Base, Chest and
    Collectable take the type as an argument instead."""
    text = strip_comments((rando / "location.cpp").read_text())
    types: dict[str, str] = {}
    for m in re.finditer(r"Rando::Location Rando::Location::(\w+)\(.*?\)\s*\{(.*?)\n\}", text, re.S):
        found = re.search(r"\b(RCTYPE_\w+)", m.group(2))
        if found:
            types[m.group(1)] = found.group(1)
    return types


def scene_order(ship: pathlib.Path) -> dict[str, int]:
    text = (ship / "soh/include/tables/scene_table.h").read_text()
    return {scene: i for i, scene in enumerate(re.findall(r"DEFINE_SCENE\(\w+,\s*\w+,\s*(SCENE_\w+)", text))}


def is_dungeon(rc: str, check_type: str, scene: str, order: dict[str, int]) -> bool:
    """Ship's Location::IsDungeon (location.cpp), which compares scene ids by range."""
    s = order.get(scene, len(order))
    if check_type == "RCTYPE_SKULL_TOKEN":
        return s <= order["SCENE_ICE_CAVERN"]
    return (s <= order["SCENE_GERUDO_TRAINING_GROUND"] or scene == "SCENE_INSIDE_GANONS_CASTLE"
            or order["SCENE_DEKU_TREE_BOSS"] <= s <= order["SCENE_GANONDORF_BOSS"]
            or rc in ("RC_SPIRIT_TEMPLE_SILVER_GAUNTLETS_CHEST", "RC_SPIRIT_TEMPLE_MIRROR_SHIELD_CHEST"))


def ship_locations(ship: pathlib.Path, rando: pathlib.Path) -> dict[str, dict]:
    """Every locationTable row: its display name, check type, quest, area, scene, actor, dungeon-ness
    and vanilla item. Rows are matched by argument prefix (RCQUEST_/RCTYPE_/RCAREA_/SCENE_/RG_), which
    holds across every factory overload."""
    prefixes, scenes, types, order = area_prefixes(ship, rando), scene_areas(rando), factory_types(rando), scene_order(ship)
    rows: dict[str, dict] = {}
    for f in sorted(rando.glob("*.cpp")):
        text = strip_comments(f.read_text())
        for m in re.finditer(r"locationTable\[(RC_\w+)\]\s*=\s*Location::(\w+)\(", text):
            rc, factory = m.group(1), m.group(2)
            args = call_args(text, m.end())
            strings = re.findall(r'"([^"]*)"', args)
            if not strings:
                continue
            first = lambda prefix: (re.findall(rf"\b({prefix}_\w+)", args) or [None])[0]
            scene = first("SCENE") or ""
            area = first("RCAREA") or scenes.get(scene, "RCAREA_INVALID")
            # The Base overload taking an explicit spoilerName passes two strings; the
            # second is already the finished name and must not be prefixed again.
            if factory == "Base" and len(strings) >= 2:
                name = strings[1]
            else:
                prefix = prefixes.get(area)
                name = f"{prefix} {strings[0]}" if prefix else strings[0]
            check_type = types.get(factory) or first("RCTYPE")
            rows[rc] = dict(name=name, type=check_type, quest=first("RCQUEST"), area=area, scene=scene,
                            actor=first("ACTOR") or "", dungeon=is_dungeon(rc, check_type, scene, order), item=first("RG"))
    return rows


def area_names(rando: pathlib.Path) -> dict[str, str]:
    """RCAREA_* -> Ship's display name ("Kokiri Forest"), from rcAreaNames."""
    text = strip_comments((rando / "randomizer_check_objects.cpp").read_text())
    return dict(re.findall(r'\{\s*(RCAREA_\w+),\s*"([^"]*)"\s*\}', text))


def dungeon_infos(rando: pathlib.Path) -> dict[str, list[str]]:
    """Dungeon name -> the rest of its DungeonInfo(...) arguments, from dungeon.cpp."""
    text = strip_comments((rando / "dungeon.cpp").read_text())
    return {m.group(1): [a.strip() for a in m.group(2).split(",")]
            for m in re.finditer(r'DungeonInfo\(\s*"([^"]*)",(.*?)\);', text, re.S)}


def dungeon_small_keys(rando: pathlib.Path) -> dict[str, tuple[str, int, int]]:
    """Small key item -> (dungeon name, vanilla count, MQ count)."""
    return {args[3]: (name, int(args[7]), int(args[8]))
            for name, args in dungeon_infos(rando).items() if args[3] != "RG_NONE"}


def item_names(rando: pathlib.Path) -> dict[str, str]:
    src = strip_comments((rando / "item_list.cpp").read_text())
    found = dict(
        re.findall(r'itemTable\[(RG_\w+)\]\s*=\s*\w+\(\s*RG_\w+,\s*Text\{\s*"([^"]*)"', src)
    )
    return found | ITEM_OVERRIDES


# == Tricks =====================================================================================

def trick_names(rando: pathlib.Path) -> tuple[dict[str, str], list[str]]:
    """(used trick -> Ship's name, used tricks Ship has disabled).

    OPT_TRICK(rsk, quest, area, {tags}, "Name", "Tag", "Description"): the name is the first
    string. "Used" means referenced by the world's Python (the generated logic plus helpers).
    """
    text = strip_comments((rando / "settings.cpp").read_text())
    names: dict[str, str] = {}
    for m in re.finditer(r"OPT_TRICK\(\s*(RT_\w+)\s*,", text):
        names[m.group(1)] = re.findall(r'"((?:[^"\\]|\\.)*)"', call_args(text, m.start() + len("OPT_TRICK(")))[0]
    used = set()
    for path in WORLD.glob("*.py"):
        if path != OUT:
            used |= set(re.findall(r"\bTricks\.(RT_\w+)", path.read_text()))
    declared = rando_enum(rando, "RandomizerTrick.h", "RandomizerTrick")
    unknown = used - set(declared)
    if unknown:
        sys.exit(f"error: logic uses tricks Ship does not declare: {sorted(unknown)}")
    if len(set(names.values())) != len(names):
        sys.exit("error: two OPT_TRICKs share a name; the StrEnum would alias them")
    kept = {rt: names[rt] for rt in declared if rt in used and rt in names}
    return kept, [rt for rt in declared if rt in used and rt not in names]


# == RandomizerSettingKey =======================================================================

def ship_options(rando: pathlib.Path) -> dict[str, int]:
    """Every RO_* name mapped to its index within its own RANDO_ENUM group."""
    values: dict[str, int] = {}
    index = 0
    for line in strip_comments((rando / "randomizerEnums/RandomizerOptions.h").read_text()).split("\n"):
        if "RANDO_ENUM_BEGIN" in line:
            index = 0
        member = re.search(r"RANDO_ENUM_ITEM\((RO_\w+)\)", line)
        if member:
            values[member.group(1)] = index
            index += 1
    return values


# == Output =====================================================================================

def str_enum(name: str, members: dict[str, str] | list[str], sort: bool = True) -> str:
    """A list of members becomes an enum whose values are its member names."""
    if isinstance(members, list):
        members = dict(zip(members, members))
    # json.dumps yields a valid double-quoted Python literal, matching the transpiler's output.
    items = sorted(members.items()) if sort else members.items()
    body = [f"    {key} = {json.dumps(value, ensure_ascii=False)}" for key, value in items]
    return "\n".join([f"class {name}(StrEnum):", *body, "", ""])


def int_enum(name: str, members: list[str]) -> str:
    body = [f"    {key} = {i}" for i, key in enumerate(members)]
    return "\n".join([f"class {name}(IntEnum):", *body, "", ""])


def location_table(rows: dict[str, dict], ids: list[str], items: dict[str, str]) -> str:
    """SHIP_LOCATIONS: each location's Ship data, keyed by Locations member. The id is the
    location's index in Ship's RandomizerCheck enum."""
    lines = [
        "class ShipLocation(NamedTuple):",
        "    id: int",
        "    type: CheckType",
        "    quest: CheckQuest",
        "    area: CheckArea",
        "    scene: str",
        "    actor: str  # empty when the factory implies it (tokens, pots, grass, ...)",
        "    dungeon: bool  # Ship's Location::IsDungeon",
        "    vanilla_item: Items | None",
        "",
        "",
        "SHIP_LOCATIONS: dict[Locations, ShipLocation] = {",
    ]
    index = {rc: i for i, rc in enumerate(ids)}
    for rc in sorted(rows, key=lambda rc: index[rc]):
        r = rows[rc]
        item = f"Items.{r['item']}" if r["item"] in items and r["item"] != "RG_NONE" else "None"
        lines.append(f"    Locations.{rc}: ShipLocation({index[rc]}, CheckType.{r['type']}, "
                     f"CheckQuest.{r['quest']}, CheckArea.{r['area']}, {json.dumps(r['scene'])}, {json.dumps(r['actor'])}, "
                     f"{r['dungeon']}, {item}),")
    return "\n".join([*lines, "}", "", ""])


def write(ship: pathlib.Path, rando: pathlib.Path) -> None:
    # Ship names each dungeon's check area exactly as it names the dungeon.
    areas = area_names(rando)
    area_by_name = {name: area for area, name in areas.items()}
    rows = ship_locations(ship, rando)
    locations = {rc: row["name"] for rc, row in rows.items()}
    check_ids = rando_enum(rando, "RandomizerCheck.h", "RandomizerCheck")
    missing = set(rows) - set(check_ids)
    if missing:
        sys.exit(f"error: locationTable rows with no RandomizerCheck member: {sorted(missing)}")
    items = item_names(rando)
    tricks, disabled = trick_names(rando)
    enemies = rando_enum(rando, "RandomizerMiscEnums.h", "RandomizerEnemy")
    options = ship_options(rando)

    parts = [
        "# Generated by tools/gen_ship_data.py from Shipwright. Do not edit.",
        "from enum import IntEnum, StrEnum",
        "from typing import NamedTuple",
        "",
        "",
        str_enum("Locations", locations),
        str_enum("Items", items),
        str_enum("CheckType", rando_enum(rando, "RandomizerMiscEnums.h", "RandomizerCheckType"), sort=False),
        str_enum("CheckQuest", rando_enum(rando, "RandomizerMiscEnums.h", "RandomizerCheckQuest"), sort=False),
        # Values are Ship's area names (rcAreaNames), which double as location group names.
        str_enum("CheckArea", areas, sort=False),
        location_table(rows, check_ids, items),
        "# Small key item -> (dungeon, vanilla count, Master Quest count), from Ship's DungeonInfo.",
        "DUNGEON_SMALL_KEYS: dict[Items, tuple[CheckArea, int, int]] = {",
        *[f"    Items.{key}: (CheckArea.{area_by_name[name]}, {vanilla}, {mq}),"
          for key, (name, vanilla, mq) in dungeon_small_keys(rando).items()],
        "}",
        "",
        "",
        # Disabled tricks keep their RT_ name as the value: Ship gives them no display name.
        str_enum("Tricks", tricks | {rt: rt for rt in disabled}, sort=False),
        f"# Declared by Ship but with no OPT_TRICK: never in logic, even under enable_all_tricks.\n"
        f"DISABLED_TRICKS = frozenset({{{', '.join(f'Tricks.{rt}' for rt in disabled)}}})\n\n",
        str_enum("Enemies", enemies, sort=False),
        int_enum("EnemyDistance", rando_enum(rando, "RandomizerMiscEnums.h", "EnemyDistance")),
        int_enum("TrialKey", rando_enum(rando, "RandomizerMiscEnums.h", "TrialKey")),
        "class RandomizerSettingKey:",
        '    """Ship\'s RO_* option values, flattened into one namespace.',
        "",
        "    Plain ints rather than an IntEnum on purpose: these numbers are per-option-group",
        "    indices, so they repeat (RO_CLOSED_FOREST_ON and RO_DOOROFTIME_CLOSED are both 0),",
        "    and an IntEnum would quietly fold the repeats into aliases of each other.",
        '    """',
        *[f"    {name} = {value}" for name, value in options.items()],
        "",
    ]
    OUT.write_text("\n".join(parts))
    print(f"wrote {OUT.name}: {len(locations)} locations, {len(items)} items, "
          f"{len(tricks)} tricks (+{len(disabled)} disabled), {len(enemies)} enemies, "
          f"{len(options)} RO_* values")


# == Verification ===============================================================================

def options_classes() -> list[ast.ClassDef]:
    return [node for node in ast.parse((WORLD / "Options.py").read_text()).body
            if isinstance(node, ast.ClassDef)]


def ship_settings(rando: pathlib.Path) -> dict[str, list[str]]:
    """RSK_* mapped to its ordered value labels. OPT_BOOL options have no labels."""
    text = strip_comments((rando / "settings.cpp").read_text())
    settings: dict[str, list[str]] = {}
    for m in re.finditer(r'OPT_U8\((RSK_\w+),\s*"(?:[^"\\]|\\.)*"\s*,\s*\{([^}]*)\}', text):
        settings.setdefault(m.group(1), re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(2)))
    for m in re.finditer(r'OPT_BOOL\((RSK_\w+),', text):
        settings.setdefault(m.group(1), [])
    return settings


def ap_option_count() -> dict[str, int]:
    """Each Options.py class mapped to how many values it accepts. A Toggle declares no
    option_* of its own and counts as 2."""
    counts: dict[str, int] = {}
    for node in options_classes():
        declared = sum(1 for stmt in node.body
                       if isinstance(stmt, ast.Assign) and isinstance(stmt.targets[0], ast.Name)
                       and stmt.targets[0].id.startswith("option_"))
        bases = {b.id for b in node.bases if isinstance(b, ast.Name)}
        counts[node.name] = declared or (2 if bases & {"Toggle", "DefaultOnToggle"} else 0)
    return counts


def verify_options(settings: dict[str, list[str]]) -> int:
    """Compare each RSK_* option class's value count against Ship's. Counts, not labels: the two
    spell the same value differently often enough that comparing text would be noise, and a
    count that drifts is what silently changes a rule's meaning."""
    counts = ap_option_count()
    problems = 0
    for key in sorted(name for name in counts if name.startswith("RSK_")):
        labels, count = settings.get(key), counts[key]
        if labels is None:
            print(f"  {key}: not an option in Ship's settings.cpp")
            problems += 1
        elif labels and count != len(labels):
            print(f"  {key}: Ship has {len(labels)} values {labels}, Options.py takes {count}")
            problems += 1
    return problems


def verify_dungeon_names(rando: pathlib.Path) -> int:
    """MasterQuest.py's dungeon names cross the wire: the client matches them by string, and a
    mismatch silently leaves the dungeon vanilla while the logic assumed MQ."""
    ship = list(dungeon_infos(rando))
    sys.path.insert(0, str(WORLD.parent.parent))
    from worlds.oot_soh.MasterQuest import MQ_DUNGEONS  # noqa: PLC0415

    missing = [name for name in MQ_DUNGEONS if name not in ship]
    extra = [name for name in ship if name not in MQ_DUNGEONS]
    for name in missing:
        print(f"  {name!r} is not a Ship dungeon name")
    for name in extra:
        print(f"  Ship has dungeon {name!r}, which MasterQuest.py does not list")
    return len(missing) + len(extra)


# Keys AP deliberately sends that the client has no reason to read.
AP_ONLY_SLOT_DATA = {
    "ice_trap_count",           # AP filler shaping; the client only sees the resulting items
    "ice_trap_filler_replacement",
}


def verify_slot_data(ship: pathlib.Path) -> int:
    """fill_slot_data's keys vs every slotData["x"] the client reads. A key the client reads but AP
    stops sending does not raise: nlohmann's operator[] inserts a null, so the comparison against it
    quietly takes the wrong branch. A key AP sends that the client ignores is harmless, but is
    usually the other half of a rename done on one side only."""
    reads: set[str] = set()
    for path in (ship / "soh/soh").rglob("*.cpp"):
        # slotData["x"], and the GetSlotData()["x"] form used before the local is bound.
        reads |= set(re.findall(r'(?:slotData|GetSlotData\(\))\s*\[\s*"([^"]+)"\s*\]',
                                strip_comments(path.read_text(errors="ignore"))))
    fn = next(n for n in ast.walk(ast.parse((WORLD / "__init__.py").read_text()))
              if isinstance(n, ast.FunctionDef) and n.name == "fill_slot_data")
    returned = next(n.value for n in ast.walk(fn) if isinstance(n, ast.Return) and isinstance(n.value, ast.Dict))
    sends = {k.value for k in returned.keys if isinstance(k, ast.Constant)}
    for key in sorted(reads - sends):
        print(f"  {key!r} is read by the client but not sent -- silently wrong")
    for key in sorted(sends - reads - AP_ONLY_SLOT_DATA):
        print(f"  {key!r} is sent but unread by the client -- fine if AP-side or not implemented client-side")
    return len(reads - sends)


def report_stubs() -> None:
    stubs = sorted(node.name for node in options_classes() if node.name.startswith("RSK_")
                   and any(getattr(base, "id", None) == "NotImplementedChoice" for base in node.bases))
    print(f"\nRSK_* not implemented (yaml may only pick the default): {len(stubs)}")
    for key in stubs:
        print(f"  {key}")


def main() -> int:
    if len(sys.argv) < 2:
        sys.exit("error: pass the path to a Shipwright checkout.")
    ship = pathlib.Path(sys.argv[1])
    rando = ship / RANDO
    if not (rando / "location_list.cpp").exists():
        sys.exit(f"error: no Shipwright checkout at {ship}")

    write(ship, rando)
    print("\nverifying RSK_* option classes against Ship:")
    problems = verify_options(ship_settings(rando))
    print("verifying MasterQuest.py dungeon names against Ship:")
    problems += verify_dungeon_names(rando)
    print("verifying slot data against the client:")
    problems += verify_slot_data(ship)
    print(f"  {problems} problem(s)")
    report_stubs()
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
