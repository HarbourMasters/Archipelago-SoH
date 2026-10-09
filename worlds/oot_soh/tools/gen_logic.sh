#!/usr/bin/env bash
# Regenerate the RLS-derived logic for the oot_soh world.
#
# Builds the RandoLogicScript compiler from the logic/ submodule and transpiles logic/src/*.rls into Python
#
# Usage: worlds/oot_soh/tools/gen_logic.sh
set -euo pipefail

WORLD="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOGIC="$WORLD/logic"
COMPILER="$LOGIC/RandoLogicScript"
BUILD="$COMPILER/build"

if [[ ! -f "$LOGIC/rls.json" ]]; then
    echo "error: logic submodule not checked out. Run: git submodule update --init --recursive" >&2
    exit 1
fi

echo "==> Building RandoLogicScript"
cmake -S "$COMPILER" -B "$BUILD" -G Ninja >/dev/null
cmake --build "$BUILD" --target RandoLogicScript -j"$(nproc)"

echo "==> Transpiling logic -> $WORLD"
"$BUILD/console/RandoLogicScript" -p "$LOGIC/rls.json" -t soh_ap -o "$WORLD"

# copy rls_match/rls_conditional
echo "==> Syncing runtime support modules"
for f in rls_match.py rls_conditional.py; do
    src="$COMPILER/transpilers/soh_ap/src/$f"
    if ! cmp -s "$src" "$WORLD/$f"; then
        cp "$src" "$WORLD/$f"
        echo "    updated $f"
    fi
done

echo "==> Done. Generated: enums_gen.py functions_gen.py regions_gen.py"
