from typing import NamedTuple
from enum import IntEnum, IntFlag
from BaseClasses import Item, ItemClassification as IC
from .Enums import *


class SohItem(Item):
    game = "Ship of Harkinian"


# for convenience for things like songs and magic
class ItemType(IntEnum):
    none = 0
    song = 1
    magic = 2  # things that cost magic

class GroupTag(IntFlag):
    Sword = auto()
    Melee_Weapon = auto()
    Ranged_Weapon = auto()
    Stun_Weapon = auto()
    Shield = auto()
    Tunic = auto()
    Boots = auto()
    Magic_Item = auto()
    Magic_Arrows = auto()
    Magic_Spell = auto()
    Beans = auto()
    Token = auto()
    Letter = auto()
    Explosives_Upgrade = auto()
    Bag_Upgrade = auto()
    Wallet = auto()
    Magic_Meter = auto()
    Ocarina = auto()
    Bottle = auto()
    Song = auto()
    Map = auto()
    Compass = auto()
    Key = auto()
    Boss_Key = auto()
    Small_Key = auto()
    Key_Ring = auto()
    Dungeon_Reward = auto()
    Spiritual_Stone = auto()
    Medallion = auto()
    Greg = auto()
    Health_Upgrade = auto()
    Trap = auto()
    Boss_Soul = auto()
    Ocarina_Button = auto()
    Overworld_Key = auto()
    Trade_Item = auto()
    Consumable_Item = auto()
    Money = auto()
    Purchasable_Item = auto()
    Secret_Finder = auto()
    Item_Retriever = auto()
    Golden_Item = auto()
    Movement_Upgrade = auto()
    Ability_Upgrade = auto()
    Deku_Tree_Item = auto()
    Dodongos_Cavern_Item = auto()
    Jabu_Jabus_Item = auto()
    Forest_Temple_Item = auto()
    Fire_Temple_Item = auto()
    Water_Temple_Item = auto()
    Ice_Cavern_Item = auto()
    Spirit_Temple_Item = auto()
    Shadow_Temple_Item = auto()
    Bottom_of_the_Well_Item = auto()
    Traning_Ground_Item = auto()
    Gerudo_Fortress_Item = auto()
    Ganons_Castle_Item = auto()
    Graveyard_Item = auto()

class SohItemData(NamedTuple):
    # None means it's just here for the data, and won't be added to the datapackage
    item_id: int | None
    classification: IC = IC.progression
    # balanced amount
    quantity_in_item_pool: int = 0
    item_type: int = ItemType.none
    child_only: bool = False
    adult_only: bool = False
    # todo: fill out more item groups
    tags: GroupTag | None = None
    plentiful_quantity: int = -1
    scarce_quantity: int = -1
    minimal_quantity: int = -1


item_data_table: dict[Items, SohItemData] = {
    # Items commented out that can never appear in the item pool and are only used on Ship internally

    Items.KOKIRI_SWORD: SohItemData(1, IC.progression | IC.useful, 0, child_only=True, tags=GroupTag.Sword | GroupTag.Melee_Weapon, plentiful_quantity=2),
    Items.MASTER_SWORD: SohItemData(2, IC.progression | IC.useful, 0, adult_only=True, tags=GroupTag.Sword | GroupTag.Melee_Weapon, plentiful_quantity=2),
    Items.GIANTS_KNIFE: SohItemData(3, IC.progression, 0, adult_only=True, tags=GroupTag.Sword | GroupTag.Melee_Weapon),
    Items.BIGGORONS_SWORD: SohItemData(4, IC.progression | IC.useful, 1, adult_only=True, tags=GroupTag.Sword | GroupTag.Melee_Weapon, plentiful_quantity=2, minimal_quantity=0),
    Items.DEKU_SHIELD: SohItemData(5, IC.useful, 1, child_only=True, tags=GroupTag.Shield),
    Items.HYLIAN_SHIELD: SohItemData(6, IC.useful, 1, tags=GroupTag.Shield),
    Items.MIRROR_SHIELD: SohItemData(7, IC.progression | IC.useful, 1, adult_only=True, tags=GroupTag.Shield, plentiful_quantity=2),
    Items.GORON_TUNIC: SohItemData(8, IC.progression | IC.useful, 1, adult_only=True, tags=GroupTag.Tunic, plentiful_quantity=2),
    Items.ZORA_TUNIC: SohItemData(9, IC.progression | IC.useful, 1, adult_only=True, tags=GroupTag.Tunic, plentiful_quantity=2),
    Items.IRON_BOOTS: SohItemData(10, IC.progression | IC.useful, 1, adult_only=True, tags=GroupTag.Boots, plentiful_quantity=2),
    Items.HOVER_BOOTS: SohItemData(11, IC.progression | IC.useful, 1, adult_only=True, tags=GroupTag.Boots, plentiful_quantity=2),
    Items.BOOMERANG: SohItemData(12, IC.progression | IC.useful, 1, child_only=True, tags=GroupTag.Ranged_Weapon | GroupTag.Stun_Weapon | GroupTag.Item_Retriever, plentiful_quantity=2),
    Items.LENS_OF_TRUTH: SohItemData(13, IC.progression | IC.useful, 1, item_type=ItemType.magic, tags=GroupTag.Magic_Item | GroupTag.Secret_Finder, plentiful_quantity=2),
    Items.MEGATON_HAMMER: SohItemData(14, IC.progression | IC.useful, 1, adult_only=True, tags=GroupTag.Melee_Weapon, plentiful_quantity=2),
    Items.STONE_OF_AGONY: SohItemData(15, IC.progression | IC.useful, 1, tags=GroupTag.Secret_Finder, plentiful_quantity=2),
    Items.DINS_FIRE: SohItemData(16, IC.progression, 1, item_type=ItemType.magic, tags=GroupTag.Magic_Item | GroupTag.Magic_Spell, plentiful_quantity=2),
    Items.FARORES_WIND: SohItemData(17, IC.progression, 1, item_type=ItemType.magic, tags=GroupTag.Magic_Item | GroupTag.Magic_Spell, plentiful_quantity=2, minimal_quantity=0),
    Items.NAYRUS_LOVE: SohItemData(18, IC.progression, 1, item_type=ItemType.magic, tags=GroupTag.Magic_Item | GroupTag.Magic_Spell, plentiful_quantity=2, minimal_quantity=0),
    Items.FIRE_ARROW: SohItemData(19, IC.progression, 1, adult_only=True, item_type=ItemType.magic, tags=GroupTag.Magic_Arrows | GroupTag.Magic_Item, plentiful_quantity=2),
    Items.ICE_ARROW: SohItemData(20, IC.progression | IC.useful, 1, adult_only=True, item_type=ItemType.magic, tags=GroupTag.Magic_Arrows | GroupTag.Magic_Item, plentiful_quantity=2),
    Items.LIGHT_ARROW: SohItemData(21, IC.progression, 1, adult_only=True, item_type=ItemType.magic, tags=GroupTag.Magic_Arrows | GroupTag.Magic_Item, plentiful_quantity=2),
    Items.GERUDO_MEMBERSHIP_CARD: SohItemData(22, IC.progression, 0, tags=GroupTag.Gerudo_Fortress_Item, plentiful_quantity=2),
    Items.MAGIC_BEAN: SohItemData(23, IC.progression, 0, child_only=True, tags=GroupTag.Beans),
    Items.MAGIC_BEAN_PACK: SohItemData(24, IC.progression, 0, child_only=True, tags=GroupTag.Beans, plentiful_quantity=2),
    Items.DOUBLE_DEFENSE: SohItemData(25, IC.useful, 1, tags=GroupTag.Health_Upgrade, plentiful_quantity=2, scarce_quantity=0, minimal_quantity=0),
    Items.WEIRD_EGG: SohItemData(26, IC.progression, 0, child_only=True, tags=GroupTag.Trade_Item, plentiful_quantity=2),
    Items.ZELDAS_LETTER: SohItemData(27, IC.progression, 0, child_only=True, tags=GroupTag.Trade_Item | GroupTag.Letter),
    Items.POCKET_EGG: SohItemData(28, IC.progression, 0, adult_only=True, tags=GroupTag.Trade_Item, plentiful_quantity=2),
    Items.COJIRO: SohItemData(29, IC.progression, 0, adult_only=True, tags=GroupTag.Trade_Item, plentiful_quantity=2),
    Items.ODD_MUSHROOM: SohItemData(30, IC.progression, 0, adult_only=True, tags=GroupTag.Trade_Item, plentiful_quantity=2),
    Items.ODD_POTION: SohItemData(31, IC.progression, 0, adult_only=True, tags=GroupTag.Trade_Item, plentiful_quantity=2),
    Items.POACHERS_SAW: SohItemData(32, IC.progression, 0, adult_only=True, tags=GroupTag.Trade_Item, plentiful_quantity=2),
    Items.BROKEN_GORONS_SWORD: SohItemData(33, IC.progression, 0, adult_only=True, tags=GroupTag.Trade_Item, plentiful_quantity=2),
    Items.PRESCRIPTION: SohItemData(34, IC.progression, 0, adult_only=True, tags=GroupTag.Trade_Item, plentiful_quantity=2),
    Items.EYEBALL_FROG: SohItemData(35, IC.progression, 0, adult_only=True, tags=GroupTag.Trade_Item, plentiful_quantity=2),
    Items.WORLDS_FINEST_EYEDROPS: SohItemData(36, IC.progression, 0, adult_only=True, tags=GroupTag.Trade_Item, plentiful_quantity=2),
    Items.CLAIM_CHECK: SohItemData(37, IC.progression, 1, adult_only=True, tags=GroupTag.Trade_Item, plentiful_quantity=2),
    Items.GOLD_SKULLTULA_TOKEN: SohItemData(38, IC.progression_deprioritized_skip_balancing, 0, tags=GroupTag.Token | GroupTag.Golden_Item),
    Items.PROGRESSIVE_HOOKSHOT: SohItemData(39, IC.progression | IC.useful, 2, tags=GroupTag.Item_Retriever | GroupTag.Movement_Upgrade | GroupTag.Graveyard_Item),
    Items.STRENGTH_UPGRADE: SohItemData(40, IC.progression | IC.useful, 3, tags=GroupTag.Ability_Upgrade, plentiful_quantity=4),
    Items.PROGRESSIVE_BOMB_BAG: SohItemData(41, IC.progression | IC.useful, 3, tags=GroupTag.Explosives_Upgrade | GroupTag.Bag_Upgrade, plentiful_quantity=4, scarce_quantity=2, minimal_quantity=1),
    Items.PROGRESSIVE_BOW: SohItemData(42, IC.progression | IC.useful, 3, tags=GroupTag.Ranged_Weapon, plentiful_quantity=4, scarce_quantity=2, minimal_quantity=1),
    Items.PROGRESSIVE_SLINGSHOT: SohItemData(43, IC.progression | IC.useful, 3, tags=GroupTag.Ranged_Weapon , plentiful_quantity=4, scarce_quantity=2, minimal_quantity=1),
    Items.PROGRESSIVE_WALLET: SohItemData(44, IC.progression, 2, tags=GroupTag.Wallet, plentiful_quantity=3),
    Items.PROGRESSIVE_SCALE: SohItemData(45, IC.progression | IC.useful, 2, tags=GroupTag.Movement_Upgrade | GroupTag.Ability_Upgrade, plentiful_quantity=3),
    Items.PROGRESSIVE_NUT_CAPACITY: SohItemData(46, IC.progression | IC.useful, 2, tags=GroupTag.Stun_Weapon | GroupTag.Bag_Upgrade, plentiful_quantity=3, scarce_quantity=1, minimal_quantity=0),
    Items.PROGRESSIVE_STICK_CAPACITY: SohItemData(47, IC.progression | IC.useful, 2, tags=GroupTag.Melee_Weapon | GroupTag.Bag_Upgrade, plentiful_quantity=3, scarce_quantity=1, minimal_quantity=0),
    Items.BOMBCHU_BAG: SohItemData(48, IC.progression | IC.useful, 0, tags=GroupTag.Explosives_Upgrade | GroupTag.Bag_Upgrade),
    Items.PROGRESSIVE_MAGIC_METER: SohItemData(49, IC.progression | IC.useful, 2, tags=GroupTag.Magic_Meter | GroupTag.Ability_Upgrade, plentiful_quantity=3, scarce_quantity=1, minimal_quantity=1),
    # Items.MAGIC_SINGLE: SohItemData( 50, IC.filler, 0 ),
    # Items.MAGIC_DOUBLE: SohItemData( 51, IC.filler, 0 ),
    Items.PROGRESSIVE_OCARINA: SohItemData(52, IC.progression | IC.useful, 0, tags=GroupTag.Ocarina),
    # Items.PROGRESSIVE_GORON_SWORD: SohItemData(53, IC.progression, 0),
    Items.EMPTY_BOTTLE: SohItemData(54, IC.progression | IC.useful, 0, tags=GroupTag.Bottle),
    Items.BOTTLE_WITH_MILK: SohItemData(55, IC.progression | IC.useful, 0, tags=GroupTag.Bottle),
    Items.BOTTLE_WITH_RED_POTION: SohItemData(56, IC.progression | IC.useful, 0, tags=GroupTag.Bottle),
    Items.BOTTLE_WITH_GREEN_POTION: SohItemData(57, IC.progression | IC.useful, 0, tags=GroupTag.Bottle),
    Items.BOTTLE_WITH_BLUE_POTION: SohItemData(58, IC.progression | IC.useful, 0, tags=GroupTag.Bottle),
    Items.BOTTLE_WITH_FAIRY: SohItemData(59, IC.progression | IC.useful, 0, tags=GroupTag.Bottle),
    Items.BOTTLE_WITH_FISH: SohItemData(60, IC.progression | IC.useful, 0, tags=GroupTag.Bottle),
    Items.BOTTLE_WITH_BLUE_FIRE: SohItemData(61, IC.progression | IC.useful, 0, tags=GroupTag.Bottle),
    Items.BOTTLE_WITH_BUGS: SohItemData(62, IC.progression | IC.useful, 0, tags=GroupTag.Bottle),
    Items.BOTTLE_WITH_POE: SohItemData(63, IC.progression | IC.useful, 0, tags=GroupTag.Bottle),
    Items.BOTTLE_WITH_RUTOS_LETTER: SohItemData(64, IC.progression | IC.useful, 1, child_only=True, tags=GroupTag.Bottle | GroupTag.Letter),
    Items.BOTTLE_WITH_BIG_POE: SohItemData(65, IC.progression | IC.useful, 1, tags=GroupTag.Bottle),
    Items.ZELDAS_LULLABY: SohItemData(66, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song, plentiful_quantity=2),
    Items.EPONAS_SONG: SohItemData(67, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song, plentiful_quantity=2),
    Items.SARIAS_SONG: SohItemData(68, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song, plentiful_quantity=2),
    Items.SUNS_SONG: SohItemData(69, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song | GroupTag.Graveyard_Item, plentiful_quantity=2),
    Items.SONG_OF_TIME: SohItemData(70, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song, plentiful_quantity=2),
    Items.SONG_OF_STORMS: SohItemData(71, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song, plentiful_quantity=2),
    Items.MINUET_OF_FOREST: SohItemData(72, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song, plentiful_quantity=2),
    Items.BOLERO_OF_FIRE: SohItemData(73, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song, plentiful_quantity=2),
    Items.SERENADE_OF_WATER: SohItemData(74, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song, plentiful_quantity=2),
    Items.REQUIEM_OF_SPIRIT: SohItemData(75, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song, plentiful_quantity=2),
    Items.NOCTURNE_OF_SHADOW: SohItemData(76, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song, plentiful_quantity=2),
    Items.PRELUDE_OF_LIGHT: SohItemData(77, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song, plentiful_quantity=2),
    Items.GREAT_DEKU_TREE_MAP: SohItemData(78, IC.filler, 0, tags=GroupTag.Map | GroupTag.Deku_Tree_Item),
    Items.DODONGOS_CAVERN_MAP: SohItemData(79, IC.filler, 0, tags=GroupTag.Map | GroupTag.Dodongos_Cavern_Item),
    Items.JABU_JABUS_BELLY_MAP: SohItemData(80, IC.filler, 0, tags=GroupTag.Map | GroupTag.Jabu_Jabus_Item),
    Items.FOREST_TEMPLE_MAP: SohItemData(81, IC.filler, 0, tags=GroupTag.Map | GroupTag.Forest_Temple_Item),
    Items.FIRE_TEMPLE_MAP: SohItemData(82, IC.filler, 0, tags=GroupTag.Map | GroupTag.Fire_Temple_Item),
    Items.WATER_TEMPLE_MAP: SohItemData(83, IC.filler, 0, tags=GroupTag.Map | GroupTag.Water_Temple_Item),
    Items.SPIRIT_TEMPLE_MAP: SohItemData(84, IC.filler, 0, tags=GroupTag.Map | GroupTag.Spirit_Temple_Item),
    Items.SHADOW_TEMPLE_MAP: SohItemData(85, IC.filler, 0, tags=GroupTag.Map | GroupTag.Shadow_Temple_Item),
    Items.BOTTOM_OF_THE_WELL_MAP: SohItemData(86, IC.filler, 0, tags=GroupTag.Map | GroupTag.Bottom_of_the_Well_Item),
    Items.ICE_CAVERN_MAP: SohItemData(87, IC.filler, 0, tags=GroupTag.Map | GroupTag.Ice_Cavern_Item),
    Items.GREAT_DEKU_TREE_COMPASS: SohItemData(88, IC.filler, 0, tags=GroupTag.Compass | GroupTag.Deku_Tree_Item),
    Items.DODONGOS_CAVERN_COMPASS: SohItemData(89, IC.filler, 0, tags=GroupTag.Compass | GroupTag.Dodongos_Cavern_Item),
    Items.JABU_JABUS_BELLY_COMPASS: SohItemData(90, IC.filler, 0, tags=GroupTag.Compass | GroupTag.Jabu_Jabus_Item),
    Items.FOREST_TEMPLE_COMPASS: SohItemData(91, IC.filler, 0, tags=GroupTag.Compass | GroupTag.Forest_Temple_Item),
    Items.FIRE_TEMPLE_COMPASS: SohItemData(92, IC.filler, 0, tags=GroupTag.Compass | GroupTag.Fire_Temple_Item),
    Items.WATER_TEMPLE_COMPASS: SohItemData(93, IC.filler, 0, tags=GroupTag.Compass | GroupTag.Water_Temple_Item),
    Items.SPIRIT_TEMPLE_COMPASS: SohItemData(94, IC.filler, 0, tags=GroupTag.Compass | GroupTag.Spirit_Temple_Item),
    Items.SHADOW_TEMPLE_COMPASS: SohItemData(95, IC.filler, 0, tags=GroupTag.Compass | GroupTag.Shadow_Temple_Item),
    Items.BOTTOM_OF_THE_WELL_COMPASS: SohItemData(96, IC.filler, 0, tags=GroupTag.Compass | GroupTag.Bottom_of_the_Well_Item),
    Items.ICE_CAVERN_COMPASS: SohItemData(97, IC.filler, 0, tags=GroupTag.Compass | GroupTag.Ice_Cavern_Item),
    Items.FOREST_TEMPLE_BOSS_KEY: SohItemData(98, IC.progression, 1, tags=GroupTag.Boss_Key | GroupTag.Key | GroupTag.Forest_Temple_Item, plentiful_quantity=2),
    Items.FIRE_TEMPLE_BOSS_KEY: SohItemData(99, IC.progression, 1, tags=GroupTag.Boss_Key | GroupTag.Key | GroupTag.Fire_Temple_Item, plentiful_quantity=2),
    Items.WATER_TEMPLE_BOSS_KEY: SohItemData(100, IC.progression, 1, tags=GroupTag.Boss_Key | GroupTag.Key | GroupTag.Water_Temple_Item, plentiful_quantity=2),
    Items.SPIRIT_TEMPLE_BOSS_KEY: SohItemData(101, IC.progression, 1, tags=GroupTag.Boss_Key | GroupTag.Key | GroupTag.Spirit_Temple_Item, plentiful_quantity=2),
    Items.SHADOW_TEMPLE_BOSS_KEY: SohItemData(102, IC.progression, 1, tags=GroupTag.Boss_Key | GroupTag.Key | GroupTag.Shadow_Temple_Item, plentiful_quantity=2),
    Items.GANONS_CASTLE_BOSS_KEY: SohItemData(103, IC.progression, 0, tags=GroupTag.Boss_Key | GroupTag.Key | GroupTag.Ganons_Castle_Item, plentiful_quantity=2),
    Items.FOREST_TEMPLE_SMALL_KEY: SohItemData(104, IC.progression, 5, tags=GroupTag.Small_Key | GroupTag.Key | GroupTag.Forest_Temple_Item, plentiful_quantity=6),
    Items.FIRE_TEMPLE_SMALL_KEY: SohItemData(105, IC.progression, 8, tags=GroupTag.Small_Key | GroupTag.Key | GroupTag.Fire_Temple_Item, plentiful_quantity=9),
    Items.WATER_TEMPLE_SMALL_KEY: SohItemData(106, IC.progression, 6, tags=GroupTag.Small_Key | GroupTag.Key | GroupTag.Water_Temple_Item, plentiful_quantity=7),
    Items.SPIRIT_TEMPLE_SMALL_KEY: SohItemData(107, IC.progression, 5, tags=GroupTag.Small_Key | GroupTag.Key | GroupTag.Spirit_Temple_Item, plentiful_quantity=6),
    Items.SHADOW_TEMPLE_SMALL_KEY: SohItemData(108, IC.progression, 5, tags=GroupTag.Small_Key | GroupTag.Key | GroupTag.Shadow_Temple_Item, plentiful_quantity=6),
    Items.BOTTOM_OF_THE_WELL_SMALL_KEY: SohItemData(109, IC.progression, 3, tags=GroupTag.Small_Key | GroupTag.Key | GroupTag.Bottom_of_the_Well_Item, plentiful_quantity=4),
    Items.TRAINING_GROUND_SMALL_KEY: SohItemData(110, IC.progression, 9, tags=GroupTag.Small_Key | GroupTag.Key | GroupTag.Traning_Ground_Item, plentiful_quantity=10),
    Items.GERUDO_FORTRESS_SMALL_KEY: SohItemData(111, IC.progression, 4, tags=GroupTag.Small_Key | GroupTag.Key | GroupTag.Gerudo_Fortress_Item),
    Items.GANONS_CASTLE_SMALL_KEY: SohItemData(112, IC.progression, 2, tags=GroupTag.Small_Key | GroupTag.Key | GroupTag.Ganons_Castle_Item, plentiful_quantity=3),
    Items.TREASURE_GAME_SMALL_KEY: SohItemData(113, IC.progression, 0, tags=GroupTag.Small_Key | GroupTag.Key),
    Items.FOREST_TEMPLE_KEY_RING: SohItemData(114, IC.progression, 0, tags=GroupTag.Key_Ring | GroupTag.Key | GroupTag.Forest_Temple_Item, plentiful_quantity=2),
    Items.FIRE_TEMPLE_KEY_RING: SohItemData(115, IC.progression, 0, tags=GroupTag.Key_Ring | GroupTag.Key | GroupTag.Fire_Temple_Item, plentiful_quantity=2),
    Items.WATER_TEMPLE_KEY_RING: SohItemData(116, IC.progression, 0, tags=GroupTag.Key_Ring | GroupTag.Key | GroupTag.Water_Temple_Item, plentiful_quantity=2),
    Items.SPIRIT_TEMPLE_KEY_RING: SohItemData(117, IC.progression, 0, tags=GroupTag.Key_Ring | GroupTag.Key | GroupTag.Spirit_Temple_Item, plentiful_quantity=2),
    Items.SHADOW_TEMPLE_KEY_RING: SohItemData(118, IC.progression, 0, tags=GroupTag.Key_Ring | GroupTag.Key | GroupTag.Shadow_Temple_Item, plentiful_quantity=2),
    Items.BOTTOM_OF_THE_WELL_KEY_RING: SohItemData(119, IC.progression, 0, tags=GroupTag.Key_Ring | GroupTag.Key | GroupTag.Bottom_of_the_Well_Item, plentiful_quantity=2),
    Items.TRAINING_GROUND_KEY_RING: SohItemData(120, IC.progression, 0, tags=GroupTag.Key_Ring | GroupTag.Key | GroupTag.Traning_Ground_Item, plentiful_quantity=2),
    Items.GERUDO_FORTRESS_KEY_RING: SohItemData(121, IC.progression, 0, tags=GroupTag.Key_Ring | GroupTag.Key | GroupTag.Gerudo_Fortress_Item),
    Items.GANONS_CASTLE_KEY_RING: SohItemData(122, IC.progression, 0, tags=GroupTag.Key_Ring | GroupTag.Key | GroupTag.Ganons_Castle_Item, plentiful_quantity=2),
    Items.TREASURE_GAME_KEY_RING: SohItemData(123, IC.progression, 0, tags=GroupTag.Key_Ring | GroupTag.Key),
    Items.KOKIRIS_EMERALD: SohItemData(124, IC.progression, 0, tags=GroupTag.Spiritual_Stone | GroupTag.Dungeon_Reward | GroupTag.Deku_Tree_Item),
    Items.GORONS_RUBY: SohItemData(125, IC.progression, 0, tags=GroupTag.Spiritual_Stone | GroupTag.Dungeon_Reward | GroupTag.Dodongos_Cavern_Item),
    Items.ZORAS_SAPPHIRE: SohItemData(126, IC.progression, 0, tags=GroupTag.Spiritual_Stone | GroupTag.Dungeon_Reward | GroupTag.Jabu_Jabus_Item),
    Items.FOREST_MEDALLION: SohItemData(127, IC.progression, 0, tags=GroupTag.Medallion | GroupTag.Dungeon_Reward | GroupTag.Forest_Temple_Item),
    Items.FIRE_MEDALLION: SohItemData(128, IC.progression, 0, tags=GroupTag.Medallion | GroupTag.Dungeon_Reward | GroupTag.Fire_Temple_Item),
    Items.WATER_MEDALLION: SohItemData(129, IC.progression, 0, tags=GroupTag.Medallion | GroupTag.Dungeon_Reward | GroupTag.Water_Temple_Item),
    Items.SPIRIT_MEDALLION: SohItemData(130, IC.progression, 0, tags=GroupTag.Medallion | GroupTag.Dungeon_Reward | GroupTag.Spirit_Temple_Item),
    Items.SHADOW_MEDALLION: SohItemData(131, IC.progression, 0, tags=GroupTag.Medallion | GroupTag.Dungeon_Reward | GroupTag.Shadow_Temple_Item),
    Items.LIGHT_MEDALLION: SohItemData(132, IC.progression, 0, tags=GroupTag.Medallion | GroupTag.Dungeon_Reward),
    Items.RECOVERY_HEART: SohItemData(133, IC.filler, 0, tags=GroupTag.Consumable_Item),
    Items.GREEN_RUPEE: SohItemData(134, IC.filler, 0, tags=GroupTag.Money),
    Items.GREG_THE_GREEN_RUPEE: SohItemData(135, IC.progression_skip_balancing, 1, tags=GroupTag.Greg),
    Items.BLUE_RUPEE: SohItemData(136, IC.filler, 0, tags=GroupTag.Money),
    Items.RED_RUPEE: SohItemData(137, IC.filler, 0, tags=GroupTag.Money),
    Items.PURPLE_RUPEE: SohItemData(138, IC.filler, 0, tags=GroupTag.Money),
    Items.HUGE_RUPEE: SohItemData(139, IC.filler, 0, tags=GroupTag.Money),
    # 35
    Items.PIECE_OF_HEART: SohItemData(140, IC.progression_skip_balancing, 0, tags=GroupTag.Health_Upgrade),
    # 8
    Items.HEART_CONTAINER: SohItemData(141, IC.progression_skip_balancing, 0, tags=GroupTag.Health_Upgrade),
    Items.ICE_TRAP: SohItemData(142, IC.trap, 0, tags=GroupTag.Trap),
    # Items.MILK: SohItemData( 143, ),
    # Items.FISH: SohItemData( 144, ),
    Items.BOMBS_5: SohItemData(145, IC.filler, 0, tags=GroupTag.Consumable_Item),
    Items.BOMBS_10: SohItemData(146, IC.filler, 0, tags=GroupTag.Consumable_Item),
    Items.BOMBS_20: SohItemData(147, IC.filler, 0, tags=GroupTag.Consumable_Item),
    Items.BOMBCHUS_5: SohItemData(148, IC.filler, 1, tags=GroupTag.Consumable_Item),
    Items.BOMBCHUS_10: SohItemData(149, IC.filler, 3, tags=GroupTag.Consumable_Item, scarce_quantity=2, minimal_quantity=0),
    Items.BOMBCHUS_20: SohItemData(150, IC.filler, 1, tags=GroupTag.Consumable_Item, plentiful_quantity=2, scarce_quantity=0, minimal_quantity=0),
    Items.ARROWS_5: SohItemData(151, IC.filler, 0, tags=GroupTag.Consumable_Item),
    Items.ARROWS_10: SohItemData(152, IC.filler, 0, tags=GroupTag.Consumable_Item),
    Items.ARROWS_30: SohItemData(153, IC.filler, 0, tags=GroupTag.Consumable_Item),
    Items.DEKU_NUTS_5: SohItemData(154, IC.filler, 0, tags=GroupTag.Consumable_Item),
    Items.DEKU_NUTS_10: SohItemData(155, IC.filler, 0, tags=GroupTag.Consumable_Item),
    Items.DEKU_SEEDS_30: SohItemData(156, IC.filler, 0, tags=GroupTag.Consumable_Item),
    Items.DEKU_STICK_1: SohItemData(157, IC.filler, 0, tags=GroupTag.Consumable_Item),
    # Items.RED_POTION_REFILL: SohItemData( 158, IC.filler, 0 ),
    # Items.GREEN_POTION_REFILL: SohItemData( 159, IC.filler, 0 ),
    # Items.BLUE_POTION_REFILL: SohItemData( 160, IC.filler, 0 ),
    # 1
    Items.PIECE_OF_HEART_WINNER: SohItemData(161, IC.progression_skip_balancing, 0, tags=GroupTag.Health_Upgrade),
    # Items.TREASURE_GAME_GREEN_RUPEE: SohItemData( 162, IC.filler, 0 ),
    Items.BUY_DEKU_NUTS5: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_ARROWS30: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_ARROWS50: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_BOMBS525: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_DEKU_NUTS10: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_DEKU_STICK1: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_BOMBS10: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_FISH: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_RED_POTION30: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_GREEN_POTION: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_BLUE_POTION: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_HYLIAN_SHIELD: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_DEKU_SHIELD: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_GORON_TUNIC: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_ZORA_TUNIC: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_HEART: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_BOMBCHUS10: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_BOMBCHUS20: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_DEKU_SEEDS30: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    # Items.SOLD_OUT: SohItemData( None, IC.progression, 0 ),
    Items.BUY_BLUE_FIRE: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_BOTTLE_BUG: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_POE: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_FAIRYS_SPIRIT: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_ARROWS10: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_BOMBS20: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_BOMBS30: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_BOMBS535: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_RED_POTION40: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.BUY_RED_POTION50: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    # Items.TRIFORCE: SohItemData( 193, IC.progression, 0 ),
    Items.TRIFORCE_PIECE: SohItemData(194, IC.progression_skip_balancing, 0, tags=GroupTag.Golden_Item),
    Items.GOHMAS_SOUL: SohItemData(195, IC.progression, 0, tags=GroupTag.Boss_Soul | GroupTag.Deku_Tree_Item, plentiful_quantity=2),
    Items.KING_DODONGOS_SOUL: SohItemData(196, IC.progression, 0, tags=GroupTag.Boss_Soul | GroupTag.Dodongos_Cavern_Item, plentiful_quantity=2),
    Items.BARINADES_SOUL: SohItemData(197, IC.progression, 0, tags=GroupTag.Boss_Soul | GroupTag.Jabu_Jabus_Item, plentiful_quantity=2),
    Items.PHANTOM_GANONS_SOUL: SohItemData(198, IC.progression, 0, tags=GroupTag.Boss_Soul | GroupTag.Forest_Temple_Item, plentiful_quantity=2),
    Items.VOLVAGIAS_SOUL: SohItemData(199, IC.progression, 0, tags=GroupTag.Boss_Soul | GroupTag.Fire_Temple_Item, plentiful_quantity=2),
    Items.MORPHAS_SOUL: SohItemData(200, IC.progression, 0, tags=GroupTag.Boss_Soul | GroupTag.Water_Temple_Item, plentiful_quantity=2),
    Items.BONGO_BONGOS_SOUL: SohItemData(201, IC.progression, 0, tags=GroupTag.Boss_Soul | GroupTag.Shadow_Temple_Item, plentiful_quantity=2),
    Items.TWINROVAS_SOUL: SohItemData(202, IC.progression, 0, tags=GroupTag.Boss_Soul | GroupTag.Spirit_Temple_Item, plentiful_quantity=2),
    Items.GANONS_SOUL: SohItemData(203, IC.progression, 0, tags=GroupTag.Boss_Soul | GroupTag.Ganons_Castle_Item, plentiful_quantity=2),
    Items.OCARINA_A_BUTTON: SohItemData(204, IC.progression, 0, tags=GroupTag.Ocarina_Button, plentiful_quantity=2),
    Items.OCARINA_CUP_BUTTON: SohItemData(205, IC.progression, 0, tags=GroupTag.Ocarina_Button, plentiful_quantity=2),
    Items.OCARINA_CDOWN_BUTTON: SohItemData(206, IC.progression, 0, tags=GroupTag.Ocarina_Button, plentiful_quantity=2),
    Items.OCARINA_CLEFT_BUTTON: SohItemData(207, IC.progression, 0, tags=GroupTag.Ocarina_Button, plentiful_quantity=2),
    Items.OCARINA_CRIGHT_BUTTON: SohItemData(208, IC.progression, 0, tags=GroupTag.Ocarina_Button, plentiful_quantity=2),
    Items.SKELETON_KEY: SohItemData(209, IC.progression, 0, tags=GroupTag.Key),
    Items.FISHING_POLE: SohItemData(210, IC.progression, 0, tags=GroupTag.Item_Retriever, plentiful_quantity=2),
    Items.DEKU_STICK_BAG: SohItemData(None),
    Items.DEKU_NUT_BAG: SohItemData(None),
    # Items.HINT: SohItemData( 213, IC.filler, 0 ),
    Items.TYCOON_WALLET: SohItemData(None),
    Items.BRONZE_SCALE: SohItemData(None),
    Items.CHILD_WALLET: SohItemData(None),
    # Items.BOMBCHU_BAG: SohItemData(None),
    # Items.QUIVER_INF: SohItemData( 218, IC.filler, 0 ),
    # Items.BOMB_BAG_INF: SohItemData( 219, IC.filler, 0 ),
    # Items.BULLET_BAG_INF: SohItemData( 220, IC.filler, 0 ),
    # Items.STICK_UPGRADE_INF: SohItemData( 221, IC.filler, 0 ),
    # Items.NUT_UPGRADE_INF: SohItemData( 222, IC.filler, 0 ),
    # Items.MAGIC_INF: SohItemData( 223, IC.filler, 0 ),
    # Items.BOMBCHU_INF: SohItemData( 224, IC.filler, 0 ),
    # Items.WALLET_INF: SohItemData( 225, IC.filler, 0 ),
    Items.FAIRY_OCARINA: SohItemData(None),
    Items.OCARINA_OF_TIME: SohItemData(None),
    Items.BOMB_BAG: SohItemData(None),
    # Items.BIG_BOMB_BAG: SohItemData( 229, IC.filler, 0 ),
    # Items.BIGGEST_BOMB_BAG: SohItemData( 230, IC.filler, 0 ),
    Items.FAIRY_BOW: SohItemData(None, adult_only=True),
    # Items.BIG_QUIVER: SohItemData( 232, IC.filler, 0 ),
    # Items.BIGGEST_QUIVER: SohItemData( 233, IC.filler, 0 ),
    Items.FAIRY_SLINGSHOT: SohItemData(None, child_only=True),
    # Items.BIG_BULLET_BAG: SohItemData( 235, IC.filler, 0 ),
    # Items.BIGGEST_BULLET_BAG: SohItemData( 236, IC.filler, 0 ),
    Items.GORONS_BRACELET: SohItemData(None),
    Items.SILVER_GAUNTLETS: SohItemData(None, adult_only=True),
    Items.GOLDEN_GAUNTLETS: SohItemData(None, adult_only=True),
    Items.SILVER_SCALE: SohItemData(None),
    Items.GOLDEN_SCALE: SohItemData(None),
    Items.ADULT_WALLET: SohItemData(None),
    Items.GIANT_WALLET: SohItemData(None),
    # Items.DEKU_NUT_CAPACITY30: SohItemData( 244, IC.filler, 0 ),
    # Items.DEKU_NUT_CAPACITY40: SohItemData( 245, IC.filler, 0 ),
    # Items.DEKU_STICK_CAPACITY20: SohItemData( 246, IC.filler, 0 ),
    # Items.DEKU_STICK_CAPACITY30: SohItemData( 247, IC.filler, 0 ),
    Items.HOOKSHOT: SohItemData(None, adult_only=True),
    Items.LONGSHOT: SohItemData(None, adult_only=True),
    Items.SCARECROW: SohItemData(250, IC.progression, 0, adult_only=True),
    Items.GUARD_HOUSE_KEY: SohItemData(251, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.MARKET_BAZAAR_KEY: SohItemData(252, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.MARKET_POTION_SHOP_KEY: SohItemData(253, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.MASK_SHOP_KEY: SohItemData(254, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.MARKET_SHOOTING_GALLERY_KEY: SohItemData(255, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.BOMBCHU_BOWLING_KEY: SohItemData(256, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.TREASURE_CHEST_GAME_BUILDING_KEY: SohItemData(257, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.BOMBCHU_SHOP_KEY: SohItemData(258, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RICHARDS_HOUSE_KEY: SohItemData(259, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.ALLEY_HOUSE_KEY: SohItemData(260, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.KAK_BAZAAR_KEY: SohItemData(261, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.KAK_POTION_SHOP_KEY: SohItemData(262, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.BOSS_HOUSE_KEY: SohItemData(263, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.GRANNYS_POTION_SHOP_KEY: SohItemData(264, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.SKULLTULA_HOUSE_KEY: SohItemData(265, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.IMPAS_HOUSE_KEY: SohItemData(266, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.WINDMILL_KEY: SohItemData(267, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.KAK_SHOOTING_GALLERY_KEY: SohItemData(268, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.DAMPES_HUT_KEY: SohItemData(269, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.TALONS_HOUSE_KEY: SohItemData(270, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.STABLES_KEY: SohItemData(271, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.BACK_TOWER_KEY: SohItemData(272, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.HYLIA_LAB_KEY: SohItemData(273, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.FISHING_HOLE_KEY: SohItemData(274, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.DISTANT_SCARECROW: SohItemData(275, IC.progression, 0, adult_only=True),
    Items.ROCS_FEATHER: SohItemData(276, IC.progression, 0, tags=GroupTag.Movement_Upgrade, plentiful_quantity=2),
    Items.STICKS: SohItemData(None, child_only=True),
    Items.NUTS: SohItemData(None),
    Items.EPONA: SohItemData(None),
    Items.RESERVATION: SohItemData(None),
    # Items.MAX: SohItemData( 279, IC.filler, 0 ),
    # Intentionally place the glitched item without a value. Everything else should be above this.
    Items.GLITCHED: SohItemData(None),
}

item_table = {name.value: data.item_id for name,
              data in item_data_table.items() if data.item_id}

filler_items = [
    Items.RECOVERY_HEART,
    Items.BLUE_RUPEE,
    Items.RED_RUPEE,
    Items.PURPLE_RUPEE,
    Items.HUGE_RUPEE,
    Items.BOMBS_5,
    Items.BOMBS_10,
    Items.ARROWS_5,
    Items.ARROWS_10,
    Items.DEKU_NUTS_5,
    Items.DEKU_NUTS_10,
    Items.DEKU_STICK_1,
    Items.DEKU_SEEDS_30
]

no_rules_bottles = [
    Items.EMPTY_BOTTLE,
    Items.BOTTLE_WITH_MILK,
    Items.BOTTLE_WITH_RED_POTION,
    Items.BOTTLE_WITH_GREEN_POTION,
    Items.BOTTLE_WITH_BLUE_POTION,
    Items.BOTTLE_WITH_FAIRY,
    Items.BOTTLE_WITH_FISH,
    Items.BOTTLE_WITH_BLUE_FIRE,
    Items.BOTTLE_WITH_BUGS,
    Items.BOTTLE_WITH_POE
]

progressive_items: dict[str, tuple[str, ...]] = {
    Items.PROGRESSIVE_SCALE: (Items.BRONZE_SCALE, Items.SILVER_SCALE, Items.GOLDEN_SCALE),
    Items.PROGRESSIVE_OCARINA: (Items.FAIRY_OCARINA, Items.OCARINA_OF_TIME),
    Items.STRENGTH_UPGRADE: (Items.GORONS_BRACELET, Items.SILVER_GAUNTLETS, Items.GOLDEN_GAUNTLETS),
    Items.PROGRESSIVE_HOOKSHOT: (Items.HOOKSHOT, Items.LONGSHOT),
    Items.PROGRESSIVE_WALLET: (Items.CHILD_WALLET, Items.ADULT_WALLET, Items.GIANT_WALLET, Items.TYCOON_WALLET),
    Items.PROGRESSIVE_SLINGSHOT: (Items.FAIRY_SLINGSHOT,),
    Items.PROGRESSIVE_BOW: (Items.FAIRY_BOW,),
    Items.PROGRESSIVE_BOMB_BAG: (Items.BOMB_BAG,),
    Items.PROGRESSIVE_STICK_CAPACITY: (Items.DEKU_STICK_BAG,),
    Items.PROGRESSIVE_NUT_CAPACITY: (Items.DEKU_NUT_BAG,),
    Items.PROGRESSIVE_MAGIC_METER: (Items.MAGIC_SINGLE, Items.MAGIC_DOUBLE)
}

