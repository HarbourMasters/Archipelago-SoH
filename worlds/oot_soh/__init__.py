import orjson
import pkgutil

from typing import Any, ClassVar, Callable

from BaseClasses import CollectionState, Item, Tutorial, ItemClassification, Location
from worlds.AutoWorld import WebWorld, World
from Fill import fill_restrictive
from .location_access.overworld.castle_grounds import LocalEvents
from .Items import SohItem, item_data_table, item_table, SohItemData, progressive_items
from .Locations import location_table, token_amounts, SohLocData, location_data_table
from .Options import SohOptions, soh_option_groups
from .Regions import create_regions_and_locations, place_locked_items
from .Enums import *
from .ItemPool import create_item_pool, create_filler_item_pool, create_triforce_pieces, get_filler_item, give_starting_items
from . import RegionAgeAccess
from .DungeonRewardShuffle import pre_fill_dungeon_rewards, get_pre_fill_rewards
from .KeyShuffle import pre_fill_own_dungeon_items, pre_fill_any_dungeon_keys, pre_fill_overworld_items, get_own_dungeon_prefill_items, get_dungeon_item_prefill_items
from .SongShuffle import pre_fill_songs, get_prefill_songs
from .ShopItems import fill_shop_items, generate_prices
from .Presets import oot_soh_options_presets
from .UniversalTracker import setup_options_from_slot_data
from settings import Group, Bool
from Options import OptionError
from .LogicHelpers import wallet_capacities
from .Hints import CreateNonlocalHints, StaticHint
from worlds.LauncherComponents import Component, components, Type, launch as launch_component

import logging
logger = logging.getLogger("SOH_OOT")


class SohWebWorld(WebWorld):
    theme = "ice"
    options_presets = oot_soh_options_presets

    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Ship of Harkinian.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["aMannus"]
    )

    tutorials = [setup_en]
    game_info_languages = ["en"]
    option_groups = soh_option_groups


class SohSettings(Group):
    class AllowTrueNoLogic(Bool):
        """
        Allows SoH players to enable the true_no_logic hidden option, which makes every region and logically accessible.
        Do not enable this if you are not ready to use /send, !getitem, or similar commands.
        Do not enable this if you don't trust the players using it to play responsibly.
        """

    class DisableFillOverflow(Bool):
        """
        A debugging option for disabling our fill overflow for prefills. Typical users likely shouldn't enable this as it allows for generation failures.
        By default when an item can't be placed in prefill it will be added to the item pool as a backup. This disables that behavoir.
        """

    class SOHInstallPath(str):
        """
        Where the game is installed. Used for opening the game through the AP launcher or Webhost
        """

    allow_true_no_logic: AllowTrueNoLogic | bool = False
    disable_fill_overflow: DisableFillOverflow | bool = False
    soh_install_path: SOHInstallPath | None = None


@staticmethod
def create_groups(obj: dict[Items, SohItemData] | dict[str, SohLocData]) -> dict[str, set[str]]:
    groups: dict[str, set[str]] = dict()
    for key, data in obj.items():
        if data.tags is None:
            continue
        for tag in data.tags:
            tag_name = tag.name.replace('_', ' ')
            if tag_name not in groups:
                groups[tag_name] = set()
            groups[tag_name].add(str(key))
    return groups

class SohWorld(World):
    """A PC Port of Ocarina of Time"""

    game = "Ship of Harkinian"
    web = SohWebWorld()
    options: SohOptions
    options_dataclass = SohOptions
    settings: ClassVar[SohSettings]
    location_name_to_id = location_table
    item_name_to_id = item_table
    item_name_groups = create_groups(item_data_table)
    location_name_groups = create_groups(location_data_table)

    # Universal Tracker stuff, does not do anything in normal gen
    glitches_item_name = Items.GLITCHED
    using_ut: bool  # so we can check if we're using UT only once
    passthrough: dict[str, Any]  # slot data that got passed through
    ut_can_gen_without_yaml = True  # class var that tells it to ignore the player yaml

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.item_pool = list[SohItem]()
        self.preplaced_items = list[SohItem]()
        self.included_locations = dict[str, SohLocData]()
        self.shop_prices = dict[Locations, int]()
        self.shop_vanilla_items = dict[str, str]()
        self.triforce_pieces_required: int = 0
        self.randomized_progressive_skulltula_count: int = 0
        self.ganons_trials = list[GanonsTrials]()
        self.pre_fill_pool = list[Items]()
        self.reserved_pre_fill_locations = list[Locations]()
        self.static_hints = dict[str, list[list[int, int]]]()

        apworld_manifest = orjson.loads(pkgutil.get_data(
            __name__, "archipelago.json").decode("utf-8"))
        self.apworld_version: str = apworld_manifest["world_version"]
        # The version is stored on Worlds, so when we're ready to bump our min AP version to 0.6.4, we can use this directly in our slot data:
        # slot_data["apworld_version"] = self.world_version

    def generate_early(self) -> None:
        # for use with Universal Tracker, doesn't do anything otherwise
        setup_options_from_slot_data(self)

        if self.options.true_no_logic and not self.settings.allow_true_no_logic:
            raise OptionError(f"Player {self.player_name} enabled True No Logic, but the corresponding host.yaml "
                              "setting has not been enabled. Either have them disable that option, or enable it in "
                              "your host.yaml settings.")

        self.options.apply_any_required_option_adjustments()

        # Figure out how many Skulltula tokens need to be progressive
        # Max amount from KAK turn ins
        turn_in_amount: int = 0

        if self.options.shuffle_100_gs_reward:
            turn_in_amount = 100
        elif self.options.accessibility == "full":
            turn_in_amount = 50
        else:
            for location, amount in token_amounts.items():
                if str(location) not in self.options.exclude_locations:
                    turn_in_amount = amount
                    break

        progressive_skulltula_count: int = max(self.options.rainbow_bridge_skull_tokens_required.value if self.options.rainbow_bridge.value == 6 else 0,
                                               self.options.ganons_castle_boss_key_skull_tokens_required.value if self.options.ganons_castle_boss_key.value == 7 else 0, turn_in_amount)

        if self.options.shuffle_skull_tokens:
            vanilla_progressive_skulltula_count = 0
            if self.options.shuffle_skull_tokens == "dungeon":
                vanilla_progressive_skulltula_count = max(progressive_skulltula_count - int(TokenCounts.DUNGEON), 0)
            elif self.options.shuffle_skull_tokens == "overworld":
                vanilla_progressive_skulltula_count = max(progressive_skulltula_count - int(TokenCounts.OVERWORLD), 0)
                
            self.randomized_progressive_skulltula_count = progressive_skulltula_count - vanilla_progressive_skulltula_count

        # Figure out Keyring Situation
        key_ring_options: list = [self.options.gerudo_fortress_key_ring, self.options.forest_temple_key_ring, self.options.fire_temple_key_ring, self.options.water_temple_key_ring,
                                  self.options.spirit_temple_key_ring, self.options.shadow_temple_key_ring, self.options.bottom_of_the_well_key_ring, self.options.gerudo_training_ground_key_ring, self.options.ganons_castle_key_ring]

        if self.options.key_rings != "selection":
            for option in key_ring_options:
                option.value = False

        if self.options.key_rings == "count":
            # Fix count if Gerudo Fortress Keys aren't allowed
            if self.options.fortress_carpenters == "normal" and self.options.gerudo_fortress_key_shuffle == "vanilla":
                if self.options.key_rings_count.value > 8:
                    self.options.key_rings_count.value = 8
                key_ring_options.remove(self.options.gerudo_fortress_key_ring)

            self.random.shuffle(key_ring_options)

            # Set only the chosen
            for index in range(self.options.key_rings_count.value):
                key_ring_options[index].value = True
        elif self.options.key_rings == "selection" and self.options.fortress_carpenters == "normal" and self.options.gerudo_fortress_key_shuffle == "vanilla":
            self.options.gerudo_fortress_key_ring.value = False

        # generate the prefill pool
        self.pre_fill_pool += get_pre_fill_rewards(self)
        self.pre_fill_pool += get_prefill_songs(self)
        for key_shuffle in get_own_dungeon_prefill_items(self).values():
            self.pre_fill_pool += key_shuffle
        self.pre_fill_pool += get_dungeon_item_prefill_items(self, False)
        self.pre_fill_pool += get_dungeon_item_prefill_items(self, True)
        self.pre_fill_pool += ShopItems.get_vanilla_shop_pool(self)

        if self.options.ganons_trials == "set_number" and self.options.ganons_trials_count.value > 0:
            self.ganons_trials = [str(trial) for trial in GanonsTrials]
            if self.options.ganons_trials_count.value < 6:
                self.random.shuffle(self.ganons_trials)
                self.ganons_trials = self.ganons_trials[:self.options.ganons_trials_count.value]

        # These things get modified after we call setup_options_from_slot_data, so we need to set them here.
        if self.using_ut:
            self.ganons_trials = self.passthrough.get("required_trials", 6)
            self.options.gerudo_fortress_key_ring.value = self.passthrough.get("gerudo_fortress_key_ring", False)
            self.options.forest_temple_key_ring.value = self.passthrough.get("forest_temple_key_ring", False)
            self.options.fire_temple_key_ring.value = self.passthrough.get("fire_temple_key_ring", False)
            self.options.water_temple_key_ring.value = self.passthrough.get("water_temple_key_ring", False)
            self.options.spirit_temple_key_ring.value = self.passthrough.get("spirit_temple_key_ring", False)
            self.options.shadow_temple_key_ring.value = self.passthrough.get("shadow_temple_key_ring", False)
            self.options.bottom_of_the_well_key_ring.value = self.passthrough.get("bottom_of_the_well_key_ring", False)
            self.options.gerudo_training_ground_key_ring.value = self.passthrough.get("gerudo_training_ground_key_ring", False)
            self.options.ganons_castle_key_ring.value = self.passthrough.get("ganons_castle_key_ring", False)


    def create_regions(self) -> None:
        create_regions_and_locations(self)
        place_locked_items(self)
        self.reserve_prefill_locations()
        for location in self.get_locations():
            location.name = str(location.name)
        for region in self.get_regions():
            region.name = str(region.name)

        if self.using_ut:
            # Put vanilla items in shop
            fill_shop_items(self)

    def reserve_prefill_locations(self) -> None:
        # songs and medalion locations get a soft reservation, by adding them to the reserved location list
        # pre-fill is not allowed to place items there, but plando is allowed
        DungeonRewardShuffle.reserve_dungeon_reward_locations(self)
        SongShuffle.reserve_song_locations(self)

        # vanilla shop locations get a hard reservation, by placing a RESERVATION item there
        # pre-fill and plando are not allowed to place items there
        ShopItems.reserve_vanilla_shop_locations(self)

    def create_item(self, name: str, create_as_event: bool = False, classification: ItemClassification = None) -> SohItem:
        item_entry = Items(name)
        return SohItem(str(name), item_data_table[item_entry].classification if classification == None else classification,
                       None if create_as_event else item_data_table[item_entry].item_id, self.player)

    def get_pre_fill_items(self) -> list[Item]:
        return [self.create_item(item) for item in self.pre_fill_pool]

    def get_filler_item_name(self) -> str:
        return get_filler_item(self)

    def set_completion_rule(self) -> None:
        if not self.options.true_no_logic:
            # Actual completion condition.
            self.multiworld.completion_condition[self.player] = lambda state: state.has(
                Events.GAME_COMPLETED.value, self.player)

    def get_empty_locations_from_list_shuffled(self, location_list: list[Locations]) -> list[Location]:
        locations = []
        for location in location_list:
            loc = self.get_location(str(location))
            if loc.item != None or loc.locked or location in self.reserved_pre_fill_locations:
                continue
            locations.append(loc)
        self.random.shuffle(locations)

        return locations

    def get_pre_fill_state(self) -> CollectionState:
        my_locations = list(self.multiworld.get_locations(self.player))
        prefill_state = CollectionState(self.multiworld)
        for item in self.item_pool:
            prefill_state.collect(item, True)
        for item in self.pre_fill_pool:
            prefill_state.collect(self.create_item(item), True)
        prefill_state.sweep_for_advancements(my_locations)
        return prefill_state
    
    def set_rules(self) -> None:
        # Set price rules in advance
        generate_prices(self)

        # disregard all rules if no logic is in effect
        if self.options.true_no_logic:
            for entrance in self.get_entrances():
                entrance.access_rule = lambda state: True
            for location in self.get_locations():
                location.access_rule = lambda state: True

    def create_items(self) -> None:
        # these are for making the progressive items collect/remove work properly
        if not self.options.shuffle_swim:
            self.push_precollected(self.create_item(
                Items.PROGRESSIVE_SCALE, create_as_event=True))
        if not self.options.shuffle_deku_stick_bag:
            self.push_precollected(self.create_item(
                Items.PROGRESSIVE_STICK_CAPACITY, create_as_event=True))
        if not self.options.shuffle_deku_nut_bag:
            self.push_precollected(self.create_item(
                Items.PROGRESSIVE_NUT_CAPACITY, create_as_event=True))
        if not self.options.shuffle_childs_wallet:
            self.push_precollected(self.create_item(
                Items.PROGRESSIVE_WALLET, create_as_event=True))

        # Pre-Collect Extra Fire Temple Small Key
        if self.options.small_key_shuffle in ("vanilla", "own_dungeon"):
            self.multiworld.push_precollected(
                self.create_item(str(Items.FIRE_TEMPLE_SMALL_KEY), True))
            
        give_starting_items(self)

        create_item_pool(self)

        if self.options.triforce_hunt:
            create_triforce_pieces(self)

        create_filler_item_pool(self)

        self.set_completion_rule()

    def pre_fill(self) -> None:
        original_completion_goal = self.multiworld.completion_condition[self.player]

        pre_fill_own_dungeon_items(self)
        pre_fill_dungeon_rewards(self)
        pre_fill_songs(self)
        pre_fill_any_dungeon_keys(self)
        pre_fill_overworld_items(self)
        fill_shop_items(self)

        self.multiworld.completion_condition[self.player] = original_completion_goal

    def post_fill(self) -> None:
        hints = CreateNonlocalHints(self)
        for hint in hints:
            self.static_hints.update(hint.serialize())
            
    def run_prefill(self, item_pool: list[Items], locations: list[Locations], prefill_state: CollectionState | None = None, goal: Callable[[CollectionState], bool] | None = None):
        # check if we're using specific collectionstate
        if prefill_state is None:
            for item in item_pool:
                if item in self.pre_fill_pool: 
                    self.pre_fill_pool.remove(item)
            
            prefill_state = self.get_pre_fill_state()
        
        if goal is None:
            # set region accessability of locations as the goal
            accessibility_goal = {self.get_location(loc) for loc in locations}
            goal = lambda state: all([state.can_reach(reg) for reg in accessibility_goal])

        self.multiworld.completion_condition[self.player] = goal

        # get empty, non reserved locations
        empty_locations = self.get_empty_locations_from_list_shuffled(locations)
        items = [self.create_item(str(item)) for item in item_pool]
        self.preplaced_items.extend(items)

        if self.settings.disable_fill_overflow:
            fill_restrictive(self.multiworld, prefill_state, empty_locations, items, single_player_placement=True, lock=True)
        else:
            # Add any unplaced items to the item pool
            fill_restrictive(self.multiworld, prefill_state, empty_locations, items, single_player_placement=True, lock=True, allow_partial=True)
            self.add_items_to_item_pool_list(items)
        
        for item in items:
            self.preplaced_items.remove(item)


    def collect(self, state: CollectionState, item: Item) -> bool:
        changed = super().collect(state, item)
        state._soh_stale[self.player] = True  # type: ignore

        if item.name in progressive_items:
            current_count = state.prog_items[self.player][item.name]
            for non_prog_version in progressive_items[item.name]:
                state.prog_items[self.player][non_prog_version] = 1
                current_count -= 1
                if not current_count:
                    break

        if item.name == Items.HEART_CONTAINER:
            state.soh_heart_count[self.player] += 1  # type: ignore

        if item.name in (Items.PIECE_OF_HEART, Items.PIECE_OF_HEART_WINNER):
            state.soh_piece_of_heart_count[self.player] += 1  # type: ignore
            # type: ignore
            if state.soh_piece_of_heart_count[self.player] == 4:
                state.soh_piece_of_heart_count[self.player] = 0  # type: ignore
                state.soh_heart_count[self.player] += 1  # type: ignore

        return changed
    
    def add_items_to_item_pool_list(self, items: list[SohItem]) -> None:
        if len(items) > 0:
            self.item_pool.extend(items)
            self.multiworld.itempool.extend(items)

    def remove(self, state: CollectionState, item: Item) -> bool:
        changed = super().remove(state, item)
        if changed:
            state._soh_invalidate(self.player)  # type: ignore

        if item.name in progressive_items:
            current_count = state.prog_items[self.player][item.name]
            for i, non_prog_version in enumerate(progressive_items[item.name]):
                if i + 1 > current_count:
                    state.prog_items[self.player][non_prog_version] = 0

        if item.name == Items.HEART_CONTAINER:
            state.soh_heart_count[self.player] -= 1  # type: ignore

        if item.name in (Items.PIECE_OF_HEART, Items.PIECE_OF_HEART_WINNER):
            state.soh_piece_of_heart_count[self.player] -= 1  # type: ignore
            # type: ignore
            if state.soh_piece_of_heart_count[self.player] == -1:
                state.soh_piece_of_heart_count[self.player] = 3  # type: ignore
                state.soh_heart_count[self.player] -= 1  # type: ignore

        return changed

    # For debugging purposes
    # def generate_output(self, output_directory: str):
    #    from Utils import visualize_regions
    #    visualize_regions(self.get_region(self.origin_region_name), f"SOH-Player{self.player}.puml",
    #                      show_entrance_names=True,
    #                      regions_to_highlight=self.multiworld.get_all_state().reachable_regions[self.player])

    def fill_slot_data(self) -> dict[str, Any]:
        return {
            "closed_forest": self.options.closed_forest.value,
            "kakariko_gate": self.options.kakariko_gate.value,
            "door_of_time": self.options.door_of_time.value,
            "zoras_fountain": self.options.zoras_fountain.value,
            "sleeping_waterfall": self.options.sleeping_waterfall.value,
            "jabu_jabu": self.options.jabu_jabu.value,
            "lock_overworld_doors": self.options.lock_overworld_doors.value,
            "fortress_carpenters": self.options.fortress_carpenters.value,
            "rainbow_bridge": self.options.rainbow_bridge.value,
            "rainbow_bridge_greg_modifier": self.options.rainbow_bridge_greg_modifier.value,
            "rainbow_bridge_stones_required": self.options.rainbow_bridge_stones_required.value,
            "rainbow_bridge_medallions_required": self.options.rainbow_bridge_medallions_required.value,
            "rainbow_bridge_dungeon_rewards_required": self.options.rainbow_bridge_dungeon_rewards_required.value,
            "rainbow_bridge_dungeons_required": self.options.rainbow_bridge_dungeons_required.value,
            "rainbow_bridge_skull_tokens_required": self.options.rainbow_bridge_skull_tokens_required.value,
            "ganons_trials": self.options.ganons_trials.value,
            "ganons_trials_count": self.options.ganons_trials_count.value,
            "required_trials": self.ganons_trials,
            "triforce_hunt": self.options.triforce_hunt.value,
            "triforce_hunt_pieces_total": self.options.triforce_hunt_pieces_total.value,
            "triforce_hunt_pieces_required": self.triforce_pieces_required,
            "shuffle_songs": self.options.shuffle_songs.value,
            "shuffle_skull_tokens": self.options.shuffle_skull_tokens.value,
            "skulls_sun_song": self.options.skulls_sun_song.value,
            "shuffle_kokiri_sword": self.options.shuffle_kokiri_sword.value,
            "shuffle_master_sword": self.options.shuffle_master_sword.value,
            "shuffle_childs_wallet": self.options.shuffle_childs_wallet.value,
            "shuffle_tycoon_wallet": self.options.shuffle_tycoon_wallet.value,
            "shuffle_ocarinas": self.options.shuffle_ocarina_buttons.value,
            "shuffle_ocarina_buttons": self.options.shuffle_ocarina_buttons.value,
            "shuffle_swim": self.options.shuffle_swim.value,
            "shuffle_gerudo_membership_card": self.options.shuffle_gerudo_membership_card.value,
            "shuffle_weird_egg": self.options.shuffle_weird_egg.value,
            "shuffle_fishing_pole": self.options.shuffle_fishing_pole.value,
            "shuffle_deku_stick_bag": self.options.shuffle_deku_stick_bag.value,
            "shuffle_deku_nut_bag": self.options.shuffle_deku_nut_bag.value,
            "shuffle_freestanding_items": self.options.shuffle_freestanding_items.value,
            "shuffle_shops": self.options.shuffle_shops.value,
            "shuffle_shops_item_amount": self.options.shuffle_shops_item_amount.value,
            "shop_prices": self.shop_prices,
            "shop_vanilla_items": self.shop_vanilla_items,
            "shuffle_fish": self.options.shuffle_fish.value,
            "shuffle_scrubs": self.options.shuffle_scrubs.value,
            "shuffle_beehives": self.options.shuffle_beehives.value,
            "shuffle_cows": self.options.shuffle_cows.value,
            "shuffle_pots": self.options.shuffle_pots.value,
            "shuffle_crates": self.options.shuffle_crates.value,
            "shuffle_trees": self.options.shuffle_trees.value,
            "shuffle_merchants": self.options.shuffle_merchants.value,
            "shuffle_frog_song_rupees": self.options.shuffle_frog_song_rupees.value,
            "shuffle_adult_trade_items": self.options.shuffle_adult_trade_items.value,
            "shuffle_boss_souls": self.options.shuffle_boss_souls.value,
            "shuffle_fountain_fairies": self.options.shuffle_fountain_fairies.value,
            "shuffle_stone_fairies": self.options.shuffle_stone_fairies.value,
            "shuffle_bean_fairies": self.options.shuffle_bean_fairies.value,
            "shuffle_song_fairies": self.options.shuffle_song_fairies.value,
            "shuffle_grass": self.options.shuffle_grass.value,
            "shuffle_dungeon_rewards": self.options.shuffle_dungeon_rewards.value,
            "maps_and_compasses": self.options.maps_and_compasses.value,
            "ganons_castle_boss_key": self.options.ganons_castle_boss_key.value,
            "ganons_castle_boss_key_greg_modifier": self.options.ganons_castle_boss_key_greg_modifier.value,
            "ganons_castle_boss_key_stones_required": self.options.ganons_castle_boss_key_stones_required.value,
            "ganons_castle_boss_key_medallions_required": self.options.ganons_castle_boss_key_medallions_required.value,
            "ganons_castle_boss_key_dungeon_rewards_required": self.options.ganons_castle_boss_key_dungeon_rewards_required.value,
            "ganons_castle_boss_key_dungeons_required": self.options.ganons_castle_boss_key_dungeons_required.value,
            "ganons_castle_boss_key_skull_tokens_required": self.options.ganons_castle_boss_key_skull_tokens_required.value,
            "small_key_shuffle": self.options.small_key_shuffle.value,
            "gerudo_fortress_key_shuffle": self.options.gerudo_fortress_key_shuffle.value,
            "boss_key_shuffle": self.options.boss_key_shuffle.value,
            "key_rings": self.options.key_rings.value,
            "key_rings_count": self.options.key_rings_count.value,
            "gerudo_fortress_key_ring": self.options.gerudo_fortress_key_ring.value,
            "forest_temple_key_ring": self.options.forest_temple_key_ring.value,
            "fire_temple_key_ring": self.options.fire_temple_key_ring.value,
            "water_temple_key_ring": self.options.water_temple_key_ring.value,
            "spirit_temple_key_ring": self.options.spirit_temple_key_ring.value,
            "shadow_temple_key_ring": self.options.shadow_temple_key_ring.value,
            "bottom_of_the_well_key_ring": self.options.bottom_of_the_well_key_ring.value,
            "gerudo_training_ground_key_ring": self.options.gerudo_training_ground_key_ring.value,
            "ganons_castle_key_ring": self.options.ganons_castle_key_ring.value,
            "big_poe_target_count": self.options.big_poe_target_count.value,
            "skip_child_zelda": self.options.skip_child_zelda.value,
            "skip_epona_race": self.options.skip_epona_race.value,
            "complete_mask_quest": self.options.complete_mask_quest.value,
            "skip_scarecrows_song": self.options.skip_scarecrows_song.value,
            "start_with_links_pocket": self.options.start_with_links_pocket.value,
            "start_with_kokiri_sword": self.options.start_with_kokiri_sword.value,
            "start_with_deku_shield": self.options.start_with_deku_shield.value,
            "start_with_master_sword": self.options.start_with_master_sword.value,
            "start_with_ocarina": self.options.start_with_ocarina.value,
            "start_with_stick_ammo": self.options.start_with_stick_ammo.value,
            "start_with_nut_ammo": self.options.start_with_nut_ammo.value,
            "start_with_magic_beans": self.options.start_with_magic_beans.value,
            "start_with_zeldas_lullaby": self.options.start_with_zeldas_lullaby.value,
            "start_with_eponas_song": self.options.start_with_eponas_song.value,
            "start_with_sarias_song": self.options.start_with_sarias_song.value,
            "start_with_suns_song": self.options.start_with_suns_song.value,
            "start_with_song_of_time": self.options.start_with_song_of_time.value,
            "start_with_song_of_storms": self.options.start_with_song_of_storms.value,
            "start_with_minuet": self.options.start_with_minuet.value,
            "start_with_bolero": self.options.start_with_bolero.value,
            "start_with_serenade": self.options.start_with_serenade.value,
            "start_with_requiem": self.options.start_with_requiem.value,
            "start_with_nocturne": self.options.start_with_nocturne.value,
            "start_with_prelude": self.options.start_with_prelude.value,
            "full_wallets": self.options.full_wallets.value,
            "bombchu_bag": self.options.bombchu_bag.value,
            "bombchu_drops": self.options.bombchu_drops.value,
            "blue_fire_arrows": self.options.blue_fire_arrows.value,
            "sunlight_arrows": self.options.sunlight_arrows.value,
            "rocs_feather": self.options.rocs_feather.value,
            "infinite_upgrades": self.options.infinite_upgrades.value,
            "skeleton_key": self.options.skeleton_key.value,
            "slingbow_break_beehives": self.options.slingbow_break_beehives.value,
            "starting_age": self.options.starting_age.value,
            "shuffle_100_gs_reward": self.options.shuffle_100_gs_reward.value,
            "ice_trap_count": self.options.ice_trap_count.value,
            "ice_trap_filler_replacement": self.options.ice_trap_filler_replacement.value,
            "no_logic": self.options.true_no_logic.value,
            "apworld_version": self.apworld_version,
            "enable_all_tricks": self.options.enable_all_tricks.value,
            "tricks_in_logic": self.options.tricks_in_logic.value,
            "medallion_locked_trials": self.options.medallion_locked_trials.value,
            "starting_hearts": self.options.starting_hearts.value,
            "hint_clarity": self.options.hint_clarity.value,
            "tot_altar_hint": self.options.tot_altar_hint.value,
            "ganondorf_hint": self.options.ganondorf_hint.value,
            "sheik_la_hint": self.options.sheik_la_hint.value,
            "boss_key_hint": self.options.boss_key_hint.value,
            "dampe_diary_hint": self.options.dampe_diary_hint.value,
            "greg_hint": self.options.greg_hint.value,
            #"hyrule_loach_hint": self.options.hyrule_loach_hint.value,
            "saria_hint": self.options.saria_hint.value,
            "mido_hint": self.options.mido_hint.value,
            "frog_game_hint": self.options.frog_game_hint.value,
            "ocarina_of_time_hint": self.options.ocarina_of_time_hint.value,
            "big_goron_hint": self.options.big_goron_hint.value,
            "big_poe_hint": self.options.big_poe_hint.value,
            "chicken_hint": self.options.chicken_hint.value,
            "malon_hint": self.options.malon_hint.value,
            "horseback_archery_hint": self.options.horseback_archery_hint.value,
            "fishing_pole_hint": self.options.fishing_pole_hint.value,
            "warp_song_hint": self.options.warp_song_hint.value,
            "scrub_hints": self.options.scrub_hints.value,
            "merchant_hints": self.options.merchant_hints.value,
            "gs_10_hint": self.options.gs_10_hint.value,
            "gs_20_hint": self.options.gs_20_hint.value,
            "gs_30_hint": self.options.gs_30_hint.value,
            "gs_40_hint": self.options.gs_40_hint.value,
            "gs_50_hint": self.options.gs_50_hint.value,
            "gs_100_hint": self.options.gs_100_hint.value,
            "mask_shop_hint": self.options.mask_shop_hint.value,
            "static_hints": self.static_hints,
            "hintable_items": {item.code for item in self.item_pool + self.preplaced_items if item.code is not None},
            "starting_hearts": self.options.starting_hearts.value,
            "archipelago_seed": self.random.randint(0, 4294967295) #This is a uint32_t in ship
        }

def launch_client(*args: str):
    from .Client import launch
    launch_component(launch, name="Ship of Harkinian Client", args=args)

components.append(Component("Ship Of Harkinian Client", game_name="Ship of Harkinian", func=launch_client, component_type=Type.CLIENT, supports_uri=True))