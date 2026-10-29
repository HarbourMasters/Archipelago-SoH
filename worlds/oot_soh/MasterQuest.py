from typing import TYPE_CHECKING

from .Options import MQDungeons, DekuTreeQuest

if TYPE_CHECKING:
    from . import SohWorld

# Dungeon -> (options field, Ship scene).
MQ_DUNGEONS: dict[str, tuple[str, str]] = {
    "Deku Tree": ("deku_tree_quest", "SCENE_DEKU_TREE"),
    "Dodongo's Cavern": ("dodongos_cavern_quest", "SCENE_DODONGOS_CAVERN"),
    "Jabu Jabu's Belly": ("jabu_jabus_belly_quest", "SCENE_JABU_JABU"),
    "Forest Temple": ("forest_temple_quest", "SCENE_FOREST_TEMPLE"),
    "Fire Temple": ("fire_temple_quest", "SCENE_FIRE_TEMPLE"),
    "Water Temple": ("water_temple_quest", "SCENE_WATER_TEMPLE"),
    "Spirit Temple": ("spirit_temple_quest", "SCENE_SPIRIT_TEMPLE"),
    "Shadow Temple": ("shadow_temple_quest", "SCENE_SHADOW_TEMPLE"),
    "Bottom of the Well": ("bottom_of_the_well_quest", "SCENE_BOTTOM_OF_THE_WELL"),
    "Ice Cavern": ("ice_cavern_quest", "SCENE_ICE_CAVERN"),
    "Gerudo Training Ground": ("gerudo_training_ground_quest", "SCENE_GERUDO_TRAINING_GROUND"),
    "Ganon's Castle": ("ganons_castle_quest", "SCENE_INSIDE_GANONS_CASTLE"),
}

MQ_SCENES: frozenset[str] = frozenset(scene for _, scene in MQ_DUNGEONS.values())


def resolve_mq_dungeons(world: "SohWorld") -> list[str]:
    """The dungeons that are Master Quest this seed, as MQ_DUNGEONS keys."""
    mode = world.options.mq_dungeons

    if mode == MQDungeons.option_none:
        return []

    forced: list[str] = []
    eligible: list[str] = []
    for dungeon, (field, _scene) in MQ_DUNGEONS.items():
        choice = getattr(world.options, field).value
        if choice == DekuTreeQuest.option_master_quest:
            forced.append(dungeon)
        elif choice == DekuTreeQuest.option_random_quest:
            eligible.append(dungeon)
        # option_vanilla: never chosen, in any mode.

    if mode == MQDungeons.option_selection_only:
        return sorted(forced + [d for d in eligible if world.random.randint(0, 1)])

    if mode == MQDungeons.option_random_number:
        target = world.random.randint(0, len(MQ_DUNGEONS))
    else:
        target = world.options.mq_dungeon_count.value

    remaining = max(0, target - len(forced))
    world.random.shuffle(eligible)
    return sorted(forced + eligible[:remaining])


def mq_scenes(dungeons: list[str]) -> frozenset[str]:
    return frozenset(MQ_DUNGEONS[dungeon][1] for dungeon in dungeons if dungeon in MQ_DUNGEONS)


def small_key_count(world: "SohWorld", key) -> int:
    """How many of a dungeon's small keys exist. Vanilla VS MQ"""
    from .ship_data_gen import DUNGEON_SMALL_KEYS  # noqa: PLC0415 - keep this module import-light
    dungeon, vanilla, mq = DUNGEON_SMALL_KEYS[key]
    return mq if dungeon in world.mq_dungeons else vanilla
