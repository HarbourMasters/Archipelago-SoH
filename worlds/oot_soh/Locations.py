from typing import Callable, NamedTuple
from BaseClasses import CollectionState, Location
from .Enums import Locations, Ages
from .ship_data_gen import SHIP_LOCATIONS, CheckType, CheckArea, Items, ShipLocation


class SohLocation(Location):
    game = "Ship of Harkinian"

    def can_reach(self, state: CollectionState) -> bool:
        can_reach = False
        # check if we can reach this as either age
        stored_age = state._soh_age[self.player]  # type: ignore
        for age in [Ages.CHILD, Ages.ADULT]:
            state._soh_age[self.player] = age  # type: ignore
            can_reach |= super().can_reach(state)
        state._soh_age[self.player] = stored_age  # type: ignore
        return can_reach


class SohLocData(NamedTuple):
    loc_id: int
    dungeon_tag: CheckArea | None = None  # the dungeon it belongs to, by Ship's IsDungeon


# Not AP locations
EXCLUDED_TYPES = {CheckType.RCTYPE_GOSSIP_STONE, CheckType.RCTYPE_STATIC_HINT, CheckType.RCTYPE_CHEST_GAME}
EXCLUDED = {Locations.RC_UNKNOWN_CHECK, Locations.RC_GANON, Locations.RC_TRIFORCE_COMPLETED,
            Locations.RC_LH_CHILD_LOACH_1, Locations.RC_LH_CHILD_LOACH_2, Locations.RC_LH_ADULT_LOACH,
            Locations.RC_LH_HYRULE_LOACH}

location_data_table: dict[Locations, SohLocData] = {
    location: SohLocData(data.id, data.area if data.dungeon else None)
    for location, data in SHIP_LOCATIONS.items()
    if location not in EXCLUDED and data.type not in EXCLUDED_TYPES
}

location_table = {str(name): data.loc_id for name, data in location_data_table.items()}


SHOOTING_MINIGAMES = {Locations.RC_LW_TARGET_IN_WOODS, Locations.RC_MARKET_SHOOTING_GALLERY_REWARD,
                      Locations.RC_KAK_SHOOTING_GALLERY_REWARD, Locations.RC_GF_HBA_1000_POINTS,
                      Locations.RC_GF_HBA_1500_POINTS}
MINIGAMES = SHOOTING_MINIGAMES | {Locations.RC_LW_OCARINA_MEMORY_GAME, Locations.RC_MARKET_BOMBCHU_BOWLING_FIRST_PRIZE,
                                  Locations.RC_MARKET_BOMBCHU_BOWLING_SECOND_PRIZE,
                                  Locations.RC_MARKET_TREASURE_CHEST_GAME_REWARD,
                                  Locations.RC_ZR_FROGS_OCARINA_GAME, Locations.RC_ZD_DIVING_MINIGAME}

# Groups derived from Ship's data rather than listed.
GROUP_RULES: dict[str, Callable[[Locations, ShipLocation], bool]] = {
    "Boss": lambda loc, d: d.type == CheckType.RCTYPE_DUNGEON_REWARD and d.scene.endswith("_BOSS"),
    "Heart Container": lambda loc, d: d.vanilla_item == Items.RG_HEART_CONTAINER,
    "Piece Of Heart": lambda loc, d: d.vanilla_item == Items.RG_PIECE_OF_HEART,
    "House of Skulltula Reward": lambda loc, d: d.scene == "SCENE_HOUSE_OF_SKULLTULA",
    "Chest": lambda loc, d: d.actor == "ACTOR_EN_BOX",
    "Great Fairy Reward": lambda loc, d: d.actor == "ACTOR_BG_DY_YOSEIZO",
    "Shooting Minigame": lambda loc, d: loc in SHOOTING_MINIGAMES,
    "Minigame": lambda loc, d: loc in MINIGAMES,
}


def _groups() -> dict[str, set[str]]:
    """Ship's area names ("Kokiri Forest"), check types ("Skull Token") and GROUP_RULES as location groups."""
    groups: dict[str, set[str]] = {}
    for location in location_data_table:
        data = SHIP_LOCATIONS[location]
        for group in (str(data.area), data.type.name.removeprefix("RCTYPE_").replace("_", " ").title(),
                      *(name for name, rule in GROUP_RULES.items() if rule(location, data))):
            groups.setdefault(group, set()).add(str(location))
    return groups


location_name_groups = _groups()

scrubs_one_time_only: tuple = (Locations.RC_LW_DEKU_SCRUB_NEAR_BRIDGE, Locations.RC_LW_DEKU_SCRUB_GROTTO_FRONT,
                               Locations.RC_HF_DEKU_SCRUB_GROTTO)

scrubs_location_table = {name: data for name, data in location_data_table.items()
                         if SHIP_LOCATIONS[name].type == CheckType.RCTYPE_SCRUB}
merchants_items_location_table = {name: data for name, data in location_data_table.items()
                                  if SHIP_LOCATIONS[name].type == CheckType.RCTYPE_MERCHANT}

token_amounts: dict[str, int] = {
    Locations.RC_KAK_50_GOLD_SKULLTULA_REWARD: 50,
    Locations.RC_KAK_40_GOLD_SKULLTULA_REWARD: 40,
    Locations.RC_KAK_30_GOLD_SKULLTULA_REWARD: 30,
    Locations.RC_KAK_20_GOLD_SKULLTULA_REWARD: 20,
    Locations.RC_KAK_10_GOLD_SKULLTULA_REWARD: 10
}
