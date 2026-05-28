from typing import Dict, Tuple, List, Set, cast
import json
import yaml


def get_file_path(folder: str, test: int) -> str:
    return f"{folder}\\{str(test)}\\{str(test)}-0.yaml"

all_tricks = [
	"Visible Collision",
	"Grottos Without Agony",
	"Fewer Tunic Requirements",
	"Rusted Switches",
	"Flaming Chests",
	"Damage Boost Simple",
	"Hover Boost Simple",
	"Bombchu Beehives",
	"Blue Fire Mud Walls",
	"Open Underwater Chest",
	"KF Adult GS",
	"LW Bridge",
	"LW Mido Backflip",
	"LW GS Bean",
	"HC Storms GS",
	"HF Big Poe Without Epona",
	"Kak Man On Roof",
	"Kak Tower GS",
	"Kak Adult Windmill PoH",
	"Kak Child Windmill PoH",
	"Kak Rooftop GS",
	"GY PoH",
	"GY Child Dampe Race PoH",
	"GY Shadow Fire Arrows",
	"DMT Soil GS",
	"DMT Bombable",
	"DMT Hookshot Lower GS",
	"DMT Hovers Lower GS",
	"DMT Bean Lower GS",
	"DMT JS Lower GS",
	"DMT Climb Hovers",
	"DMT Upper GS",
	"GC Pot",
	"GC Pot Strength",
	"GC Rolling Strength",
	"GC Leftmost",
	"GC Grotto",
	"GC Link Goron Dins",
	"DMC Hover Bean PoH",
	"DMC Bolero Jump",
	"DMC Boulder JS",
	"DMC Boulder Skip",
	"ZR Lower",
	"ZR Upper",
	"ZR Hover",
	"ZR Cucco",
	"ZD King Zora Skip",
	"ZD GS",
	"ZF Great Fairy Without Explosives",
	"LH Lab Wall GS",
	"LH Lab Diving",
	"LH Water Hookshot",
	"Pass Guards With Nothing",
	"GF Jump",
	"GF Warrior With Difficult Weapon",
	"GF Ledge Clip into GTG",
	"HW Crossing",
	"Lens HW",
	"HW Reverse",
	"Colossus GS",
	"Deku B1 Skip",
	"Deku B1 Bow Webs",
	"Deku B1 Backflip Over Spiked Log",
	"DC Scarecrow GS",
	"DC Vines GS",
	"DC Stairs With Bow",
	"DC Slingshot Skip",
	"DC Scrub Room",
	"DC Jump",
	"DC Hammer Floor",
	"DC Dodongo Chu",
	"Jabu Alcove Jump Dive",
	"Jabu Boss Hover",
	"Jabu Near Boss Ranged",
	"Jabu Near Boss Explosives",
	"Lens BotW",
	"BotW Child Deadhand",
	"BotW Basement",
	"Forest First GS",
	"Forest Outdoors East GS",
	"Forest Vines",
	"Forest Outdoors Ledge",
	"Forest Doorframe",
	"Forest Outside Backdoor",
	"Forest Outdoors Hearts Boomerang",
	"Fire Boss Door Jump",
	"Fire SoT",
	"Fire Strength",
	"Fire Scarecrow",
	"Fire Flame Maze",
	"Water Longshot Torch",
	"Water Cracked Wall Hovers",
	"Water Cracked Wall",
	"Water BK Region",
	"Water North Basement Ledge Jump",
	"Water BK Jump Dive",
	"Water FW Central GS",
	"Water Irons Central GS",
	"Water Central Bow",
	"Water Hookshot Falling Platform GS",
	"Water Rang Falling Platform GS",
	"Water River GS",
	"Water Dragon Jump Dive",
	"Water Adult Dragon",
	"Water Child Dragon",
	"Water Morpha Without Hookshot",
	"Lens Shadow",
	"Lens Shadow Platform",
	"Lens Bongo",
	"Shadow Umbrella Hover",
	"Shadow Umbrella Clip",
	"Shadow Umbrella GS",
	"Shadow Freestanding Key",
	"Shadow Statue",
	"Shadow Bongo",
	"Lens Spirit",
	"Spirit Child Chu",
	"Spirit Lobby GS",
	"Spirit Lower Adult Switch",
	"Spirit Lobby Jump",
	"Spirit Platform Hookshot",
	"Spirit Map Chest",
	"Spirit Sun Chest",
	"Spirit Wall",
	"Ice Block GS",
	"Lens GTG",
	"GTG Without Hookshot",
	"GTG Fake Wall",
	"Lens Ganon",
	"Ganon Spirit Trial Hookshot",
	"Damage Boost",
	"Ground Jump",
	"Ground Jump Hard",
	"Hookshot Extension",
	"Bottom of the Well Navi Dive",
	"Lost Wood Navi Dive"
]

initial_bools_dict: Dict[str, bool | None] = {
    "closed_forest": None,
    "lock_overworld_doors": None,
    "enable_all_tricks": None,
    "medallion_locked_trials": None,
    "triforce_hunt": None,
    "skulls_sun_song": None,
    "shuffle_kokiri_sword": None,
    "shuffle_master_sword": None,
    "shuffle_childs_wallet": None,
    "shuffle_tycoon_wallet": None,
    "shuffle_ocarinas": None,
    "shuffle_ocarina_buttons": None,
    "shuffle_swim": None,
    "shuffle_weird_egg": None,
    "shuffle_gerudo_membership_card": None,
    "shuffle_fishing_pole": None,
    "shuffle_deku_stick_bag": None,
    "shuffle_deku_nut_bag": None,
    "rocs_feather": None,
    "shuffle_shops": None,
    "shop_affordable_prices": None,
    "scrub_affordable_prices": None,
    "shuffle_beehives": None,
    "shuffle_cows": None,
    "shuffle_trees": None,
    "merchant_affordable_prices": None,
    "shuffle_frog_song_rupees": None,
    "shuffle_adult_trade_items": None,
    "shuffle_100_gs_reward": None,
    "shuffle_fountain_fairies": None,
    "shuffle_stone_fairies": None,
    "shuffle_bean_fairies": None,
    "shuffle_song_fairies": None,
    "shuffle_grass": None,
    "ganons_castle_boss_key_greg_modifier": None,
    "gerudo_fortress_key_ring": None,
    "forest_temple_key_ring": None,
    "fire_temple_key_ring": None,
    "water_temple_key_ring": None,
    "spirit_temple_key_ring": None,
    "shadow_temple_key_ring": None,
    "bottom_of_the_well_key_ring": None,
    "gerudo_training_ground_key_ring": None,
    "ganons_castle_key_ring": None,
    "skip_child_zelda": None,
    "skip_epona_race": None,
    "complete_mask_quest": None,
    "skip_scarecrows_song": None,
    "gossip_stone_hints": None,
    "tot_altar_hint": None,
    "ganondorf_hint": None,
    "sheik_la_hint": None,
    "boss_key_hint": None,
    "dampe_diary_hint": None,
    "greg_hint": None,
    "saria_hint": None,
    "mido_hint": None,
    "frog_game_hint": None,
    "ocarina_of_time_hint": None,
    "big_goron_hint": None,
    "big_poe_hint": None,
    "chicken_hint": None,
    "malon_hint": None,
    "horseback_archery_hint": None,
    "fishing_pole_hint": None,
    "warp_song_hint": None,
    "scrub_hints": None,
    "merchant_hints": None,
    "gs_10_hint": None,
    "gs_20_hint": None,
    "gs_30_hint": None,
    "gs_40_hint": None,
    "gs_50_hint": None,
    "gs_100_hint": None,
    "mask_shop_hint": None,
    "start_with_kokiri_sword": None,
    "start_with_master_sword": None,
    "start_with_deku_shield": None,
    "start_with_stick_ammo": None,
    "start_with_nut_ammo": None,
    "start_with_magic_beans": None,
    "start_with_zeldas_lullaby": None,
    "start_with_eponas_song": None,
    "start_with_sarias_song": None,
    "start_with_suns_song": None,
    "start_with_song_of_time": None,
    "start_with_song_of_storms": None,
    "start_with_minuet": None,
    "start_with_bolero": None,
    "start_with_serenade": None,
    "start_with_requiem": None,
    "start_with_nocturne": None,
    "start_with_prelude": None,
    "full_wallets": None,
    "bombchu_drops": None,
    "blue_fire_arrows": None,
    "sunlight_arrows": None,
    "skeleton_key": None,
    "slingbow_break_beehives": None
}

initial_ints_dict: Dict[str, Tuple[int, int] | None] = {
    "progression_balancing": None,
    "starting_hearts": None,
    "rainbow_bridge_stones_required": None,
    "rainbow_bridge_medallions_required": None,
    "rainbow_bridge_dungeon_rewards_required": None,
    "rainbow_bridge_dungeons_required": None,
    "rainbow_bridge_skull_tokens_required": None,
    "ganons_trials_count": None,
    "triforce_hunt_pieces_total": None,
    "triforce_hunt_pieces_required_percentage": None,
    "shuffle_shops_item_amount": None,
    "shuffle_shops_minimum_price": None,
    "shuffle_shops_maximum_price": None,
    "shuffle_scrubs_minimum_price": None,
    "shuffle_scrubs_maximum_price": None,
    "shuffle_merchants_minimum_price": None,
    "shuffle_merchants_maximum_price": None,
    "ganons_castle_boss_key_stones_required": None,
    "ganons_castle_boss_key_medallions_required": None,
    "ganons_castle_boss_key_dungeon_rewards_required": None,
    "ganons_castle_boss_key_dungeons_required": None,
    "ganons_castle_boss_key_skull_tokens_required": None,
    "key_rings_count": None,
    "big_poe_target_count": None,
    "ice_trap_count": None,
    "ice_trap_filler_replacement": None
}

initial_seen_strings = {
    "accessibility": set(),
    "kakariko_gate": set(),
    "door_of_time": set(),
    "zoras_fountain": set(),
    "sleeping_waterfall": set(),
    "jabu_jabu": set(),
    "starting_age": set(),
    "fortress_carpenters": set(),
    "rainbow_bridge": set(),
    "rainbow_bridge_greg_modifier": set(),
    "ganons_trials": set(),
    "shuffle_songs": set(),
    "shuffle_skull_tokens": set(),
    "shuffle_freestanding_items": set(),
    "shuffle_fish": set(),
    "shuffle_scrubs": set(),
    "shuffle_pots": set(),
    "shuffle_crates": set(),
    "shuffle_merchants": set(),
    "shuffle_boss_souls": set(),
    "shuffle_dungeon_rewards": set(),
    "maps_and_compasses": set(),
    "small_key_shuffle": set(),
    "gerudo_fortress_key_shuffle": set(),
    "boss_key_shuffle": set(),
    "ganons_castle_boss_key": set(),
    "key_rings": set(),
    "item_pool": set(),
    "start_with_links_pocket": set(),
    "start_with_ocarina": set(),
    "bombchu_bag": set(),
    "infinite_upgrades": set(),
}

class ProcessedResults:
    #None will indicate that the value is unchecked and should be treated as matching the first case
    #These should be populated with the option names all pointing to None
    error: str
    int_range_dict: Dict[str, Tuple[int, int] | None]
    consistent_bools: Dict[str, bool | None]
    consistent_tricks: List[str]
    consistent_missing_tricks: List[str]
    seen_strings: Dict[str, Set[str]]

    def __init__(self, error: str, report, startNum = 0, total = 0):
        self.error = error
        #Start by initializing the values
        self.consistent_missing_tricks = all_tricks.copy()
        self.consistent_tricks = all_tricks.copy()
        self.int_range_dict = initial_ints_dict.copy()
        self.consistent_bools = initial_bools_dict.copy()
        self.seen_strings = initial_seen_strings.copy()
        errored = report["errors"]['oot_soh'][error]
        num = startNum
        for testNum in errored:
            num = num + 1
            print(f"{num}/{total} processed")
            yamlPath = get_file_path("fuzz_output\\error\\oot_soh", testNum)
            if error == "<class 'TimeoutError'>":
                yamlPath = get_file_path("fuzz_output\\timeout\\oot_soh", testNum)
            elif error == "success":
                yamlPath = get_file_path("fuzz_output\\success\\oot_soh", testNum)
            errYaml = None
            with open(yamlPath) as fp:
                errYaml = yaml.load(fp, Loader=yaml.Loader)
            for k,v in errYaml["Ship of Harkinian"].items():
                if k == "tricks_in_logic":
                    self.consistent_tricks = [trick for trick in self.consistent_tricks if trick in v]
                    self.consistent_missing_tricks = [trick for trick in self.consistent_missing_tricks if trick not in v]
                elif k in self.consistent_bools.keys():
                    if self.consistent_bools[k] is None:
                        self.consistent_bools[k] = v
                    elif v != self.consistent_bools[k]:
                        del self.consistent_bools[k]
                elif k in self.int_range_dict.keys():
                    if self.int_range_dict[k] is None:
                        self.int_range_dict[k] = (int(v),int(v))
                    else:
                        int_range = cast(Tuple[int, int], self.int_range_dict[k])
                        if v < int_range[0]:
                            self.int_range_dict[k] = (v, int_range[1])
                        elif v > int_range[1]:
                            self.int_range_dict[k] = (int_range[0], v)
                elif k in self.seen_strings.keys():
                    self.seen_strings[k].add(v)
    @staticmethod
    def process_report() -> List["ProcessedResults"]:
        report = None
        with open("fuzz_output\\report.json") as fp:
            report = json.load(fp)
        results = []
        total = report["stats"]["total"]
        count = 0
        for err in report["errors"]["oot_soh"].keys():
            results.append(ProcessedResults(err, report, count, total))
            count += len(report["errors"]["oot_soh"][err])
        return results


results_list = ProcessedResults.process_report()
for result in results_list:
    print(f"Result for {result.error}:")
    print("\tConsistent bool options:")
    for k,v in result.consistent_bools.items():
        print(f"\t\t{k}: {v}")
    print("\tInteger ranges:")
    for k,v in result.int_range_dict.items():
        if v is not None:
            print(f"\t\t{k}: {v[0]} - {v[1]}")
    print("\tConsistently enabled tricks:")
    for trick in result.consistent_tricks:
        print(f"\t\t{trick}")
    print("\tConsistently disabled tricks:")
    for trick in result.consistent_missing_tricks:
        print(f"\t\t{trick}")
    print("\tSeen values for string options:")
    for k, v in result.seen_strings.items():
        print(f"\t\t{k}: {v}")
    print()