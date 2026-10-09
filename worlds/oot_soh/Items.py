from typing import NamedTuple
from enum import IntEnum, IntFlag, auto
from BaseClasses import Item, ItemClassification as IC
from .Enums import Items


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
    Mask_Item = auto()
    Jabbernut = auto()
    

class SohItemData(NamedTuple):
    # None means it's just here for the data, and won't be added to the datapackage
    item_id: int | None
    classification: IC = IC.progression
    # balanced amount
    quantity_in_item_pool: int = 0
    item_type: int = ItemType.none
    child_only: bool = False
    adult_only: bool = False
    tags: GroupTag | None = None
    plentiful_quantity: int = -1
    scarce_quantity: int = -1
    minimal_quantity: int = -1


item_data_table: dict[Items, SohItemData] = {
    # Items commented out that can never appear in the item pool and are only used on Ship internally

    Items.RG_KOKIRI_SWORD: SohItemData(1, IC.progression | IC.useful, 0, child_only=True, tags=GroupTag.Sword | GroupTag.Melee_Weapon, plentiful_quantity=2),
    Items.RG_MASTER_SWORD: SohItemData(2, IC.progression | IC.useful, 0, adult_only=True, tags=GroupTag.Sword | GroupTag.Melee_Weapon, plentiful_quantity=2),
    Items.RG_GIANTS_KNIFE: SohItemData(3, IC.progression, 0, adult_only=True, tags=GroupTag.Sword | GroupTag.Melee_Weapon),
    Items.RG_BIGGORON_SWORD: SohItemData(4, IC.progression | IC.useful, 1, adult_only=True, tags=GroupTag.Sword | GroupTag.Melee_Weapon, plentiful_quantity=2, minimal_quantity=0),
    Items.RG_DEKU_SHIELD: SohItemData(5, IC.useful, 1, child_only=True, tags=GroupTag.Shield),
    Items.RG_HYLIAN_SHIELD: SohItemData(6, IC.useful, 1, tags=GroupTag.Shield),
    Items.RG_MIRROR_SHIELD: SohItemData(7, IC.progression | IC.useful, 1, adult_only=True, tags=GroupTag.Shield, plentiful_quantity=2),
    Items.RG_GORON_TUNIC: SohItemData(8, IC.progression | IC.useful, 1, adult_only=True, tags=GroupTag.Tunic, plentiful_quantity=2),
    Items.RG_ZORA_TUNIC: SohItemData(9, IC.progression | IC.useful, 1, adult_only=True, tags=GroupTag.Tunic, plentiful_quantity=2),
    Items.RG_IRON_BOOTS: SohItemData(10, IC.progression | IC.useful, 1, adult_only=True, tags=GroupTag.Boots, plentiful_quantity=2),
    Items.RG_HOVER_BOOTS: SohItemData(11, IC.progression | IC.useful, 1, adult_only=True, tags=GroupTag.Boots, plentiful_quantity=2),
    Items.RG_BOOMERANG: SohItemData(12, IC.progression | IC.useful, 1, child_only=True, tags=GroupTag.Ranged_Weapon | GroupTag.Stun_Weapon | GroupTag.Item_Retriever, plentiful_quantity=2),
    Items.RG_LENS_OF_TRUTH: SohItemData(13, IC.progression | IC.useful, 1, item_type=ItemType.magic, tags=GroupTag.Magic_Item | GroupTag.Secret_Finder, plentiful_quantity=2),
    Items.RG_MEGATON_HAMMER: SohItemData(14, IC.progression | IC.useful, 1, adult_only=True, tags=GroupTag.Melee_Weapon, plentiful_quantity=2),
    Items.RG_STONE_OF_AGONY: SohItemData(15, IC.progression | IC.useful, 1, tags=GroupTag.Secret_Finder, plentiful_quantity=2),
    Items.RG_DINS_FIRE: SohItemData(16, IC.progression, 1, item_type=ItemType.magic, tags=GroupTag.Magic_Item | GroupTag.Magic_Spell, plentiful_quantity=2),
    Items.RG_FARORES_WIND: SohItemData(17, IC.progression, 1, item_type=ItemType.magic, tags=GroupTag.Magic_Item | GroupTag.Magic_Spell, plentiful_quantity=2, minimal_quantity=0),
    Items.RG_NAYRUS_LOVE: SohItemData(18, IC.progression, 1, item_type=ItemType.magic, tags=GroupTag.Magic_Item | GroupTag.Magic_Spell, plentiful_quantity=2, minimal_quantity=0),
    Items.RG_FIRE_ARROWS: SohItemData(19, IC.progression, 1, adult_only=True, item_type=ItemType.magic, tags=GroupTag.Magic_Arrows | GroupTag.Magic_Item, plentiful_quantity=2),
    Items.RG_ICE_ARROWS: SohItemData(20, IC.progression | IC.useful, 1, adult_only=True, item_type=ItemType.magic, tags=GroupTag.Magic_Arrows | GroupTag.Magic_Item, plentiful_quantity=2),
    Items.RG_LIGHT_ARROWS: SohItemData(21, IC.progression, 1, adult_only=True, item_type=ItemType.magic, tags=GroupTag.Magic_Arrows | GroupTag.Magic_Item, plentiful_quantity=2),
    Items.RG_GERUDO_MEMBERSHIP_CARD: SohItemData(22, IC.progression, 0, tags=GroupTag.Gerudo_Fortress_Item, plentiful_quantity=2),
    Items.RG_MAGIC_BEAN: SohItemData(23, IC.progression, 0, child_only=True, tags=GroupTag.Beans),
    Items.RG_MAGIC_BEAN_PACK: SohItemData(24, IC.progression, 0, child_only=True, tags=GroupTag.Beans, plentiful_quantity=2),
    Items.RG_DOUBLE_DEFENSE: SohItemData(25, IC.useful, 1, tags=GroupTag.Health_Upgrade, plentiful_quantity=2, scarce_quantity=0, minimal_quantity=0),
    Items.RG_WEIRD_EGG: SohItemData(26, IC.progression, 0, child_only=True, tags=GroupTag.Trade_Item, plentiful_quantity=2),
    Items.RG_ZELDAS_LETTER: SohItemData(27, IC.progression, 0, child_only=True, tags=GroupTag.Trade_Item | GroupTag.Letter),
    Items.RG_POCKET_EGG: SohItemData(28, IC.progression, 0, adult_only=True, tags=GroupTag.Trade_Item, plentiful_quantity=2),
    Items.RG_COJIRO: SohItemData(29, IC.progression, 0, adult_only=True, tags=GroupTag.Trade_Item, plentiful_quantity=2),
    Items.RG_ODD_MUSHROOM: SohItemData(30, IC.progression, 0, adult_only=True, tags=GroupTag.Trade_Item, plentiful_quantity=2),
    Items.RG_ODD_POTION: SohItemData(31, IC.progression, 0, adult_only=True, tags=GroupTag.Trade_Item, plentiful_quantity=2),
    Items.RG_POACHERS_SAW: SohItemData(32, IC.progression, 0, adult_only=True, tags=GroupTag.Trade_Item, plentiful_quantity=2),
    Items.RG_BROKEN_SWORD: SohItemData(33, IC.progression, 0, adult_only=True, tags=GroupTag.Trade_Item, plentiful_quantity=2),
    Items.RG_PRESCRIPTION: SohItemData(34, IC.progression, 0, adult_only=True, tags=GroupTag.Trade_Item, plentiful_quantity=2),
    Items.RG_EYEBALL_FROG: SohItemData(35, IC.progression, 0, adult_only=True, tags=GroupTag.Trade_Item, plentiful_quantity=2),
    Items.RG_EYEDROPS: SohItemData(36, IC.progression, 0, adult_only=True, tags=GroupTag.Trade_Item, plentiful_quantity=2),
    Items.RG_CLAIM_CHECK: SohItemData(37, IC.progression, 1, adult_only=True, tags=GroupTag.Trade_Item, plentiful_quantity=2),
    Items.RG_GOLD_SKULLTULA_TOKEN: SohItemData(38, IC.progression_deprioritized_skip_balancing, 0, tags=GroupTag.Token | GroupTag.Golden_Item),
    Items.RG_PROGRESSIVE_HOOKSHOT: SohItemData(39, IC.progression | IC.useful, 2, tags=GroupTag.Item_Retriever | GroupTag.Movement_Upgrade | GroupTag.Graveyard_Item),
    Items.RG_PROGRESSIVE_STRENGTH: SohItemData(40, IC.progression | IC.useful, 3, tags=GroupTag.Ability_Upgrade, plentiful_quantity=4),
    Items.RG_PROGRESSIVE_BOMB_BAG: SohItemData(41, IC.progression | IC.useful, 3, tags=GroupTag.Explosives_Upgrade | GroupTag.Bag_Upgrade, plentiful_quantity=4, scarce_quantity=2, minimal_quantity=1),
    Items.RG_PROGRESSIVE_BOW: SohItemData(42, IC.progression | IC.useful, 3, tags=GroupTag.Ranged_Weapon, plentiful_quantity=4, scarce_quantity=2, minimal_quantity=1),
    Items.RG_PROGRESSIVE_SLINGSHOT: SohItemData(43, IC.progression | IC.useful, 3, tags=GroupTag.Ranged_Weapon , plentiful_quantity=4, scarce_quantity=2, minimal_quantity=1),
    Items.RG_PROGRESSIVE_WALLET: SohItemData(44, IC.progression, 2, tags=GroupTag.Wallet, plentiful_quantity=3),
    Items.RG_PROGRESSIVE_SCALE: SohItemData(45, IC.progression | IC.useful, 2, tags=GroupTag.Movement_Upgrade | GroupTag.Ability_Upgrade, plentiful_quantity=3),
    Items.RG_PROGRESSIVE_NUT_UPGRADE: SohItemData(46, IC.progression | IC.useful, 2, tags=GroupTag.Stun_Weapon | GroupTag.Bag_Upgrade, plentiful_quantity=3, scarce_quantity=1, minimal_quantity=0),
    Items.RG_PROGRESSIVE_STICK_UPGRADE: SohItemData(47, IC.progression | IC.useful, 2, tags=GroupTag.Melee_Weapon | GroupTag.Bag_Upgrade, plentiful_quantity=3, scarce_quantity=1, minimal_quantity=0),
    Items.RG_PROGRESSIVE_BOMBCHU_BAG: SohItemData(48, IC.progression | IC.useful, 0, tags=GroupTag.Explosives_Upgrade | GroupTag.Bag_Upgrade),
    Items.RG_PROGRESSIVE_MAGIC_METER: SohItemData(49, IC.progression | IC.useful, 2, tags=GroupTag.Magic_Meter | GroupTag.Ability_Upgrade, plentiful_quantity=3, scarce_quantity=1, minimal_quantity=1),
    Items.RG_MAGIC_SINGLE: SohItemData(None),
    Items.RG_MAGIC_DOUBLE: SohItemData(None),
    Items.RG_PROGRESSIVE_OCARINA: SohItemData(52, IC.progression | IC.useful, 0, tags=GroupTag.Ocarina),
    # Items.RG_PROGRESSIVE_GORONSWORD: SohItemData(53, IC.progression, 0),
    Items.RG_EMPTY_BOTTLE: SohItemData(54, IC.progression | IC.useful, 0, tags=GroupTag.Bottle),
    Items.RG_BOTTLE_WITH_MILK: SohItemData(55, IC.progression | IC.useful, 0, tags=GroupTag.Bottle),
    Items.RG_BOTTLE_WITH_RED_POTION: SohItemData(56, IC.progression | IC.useful, 0, tags=GroupTag.Bottle),
    Items.RG_BOTTLE_WITH_GREEN_POTION: SohItemData(57, IC.progression | IC.useful, 0, tags=GroupTag.Bottle),
    Items.RG_BOTTLE_WITH_BLUE_POTION: SohItemData(58, IC.progression | IC.useful, 0, tags=GroupTag.Bottle),
    Items.RG_BOTTLE_WITH_FAIRY: SohItemData(59, IC.progression | IC.useful, 0, tags=GroupTag.Bottle),
    Items.RG_BOTTLE_WITH_FISH: SohItemData(60, IC.progression | IC.useful, 0, tags=GroupTag.Bottle),
    Items.RG_BOTTLE_WITH_BLUE_FIRE: SohItemData(61, IC.progression | IC.useful, 0, tags=GroupTag.Bottle),
    Items.RG_BOTTLE_WITH_BUGS: SohItemData(62, IC.progression | IC.useful, 0, tags=GroupTag.Bottle),
    Items.RG_BOTTLE_WITH_POE: SohItemData(63, IC.progression | IC.useful, 0, tags=GroupTag.Bottle),
    Items.RG_RUTOS_LETTER: SohItemData(64, IC.progression | IC.useful, 1, child_only=True, tags=GroupTag.Bottle | GroupTag.Letter),
    Items.RG_BOTTLE_WITH_BIG_POE: SohItemData(65, IC.progression | IC.useful, 1, tags=GroupTag.Bottle),
    Items.RG_ZELDAS_LULLABY: SohItemData(66, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song, plentiful_quantity=2),
    Items.RG_EPONAS_SONG: SohItemData(67, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song, plentiful_quantity=2),
    Items.RG_SARIAS_SONG: SohItemData(68, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song, plentiful_quantity=2),
    Items.RG_SUNS_SONG: SohItemData(69, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song | GroupTag.Graveyard_Item, plentiful_quantity=2),
    Items.RG_SONG_OF_TIME: SohItemData(70, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song, plentiful_quantity=2),
    Items.RG_SONG_OF_STORMS: SohItemData(71, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song, plentiful_quantity=2),
    Items.RG_MINUET_OF_FOREST: SohItemData(72, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song, plentiful_quantity=2),
    Items.RG_BOLERO_OF_FIRE: SohItemData(73, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song, plentiful_quantity=2),
    Items.RG_SERENADE_OF_WATER: SohItemData(74, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song, plentiful_quantity=2),
    Items.RG_REQUIEM_OF_SPIRIT: SohItemData(75, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song, plentiful_quantity=2),
    Items.RG_NOCTURNE_OF_SHADOW: SohItemData(76, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song, plentiful_quantity=2),
    Items.RG_PRELUDE_OF_LIGHT: SohItemData(77, IC.progression | IC.useful, 0, item_type=ItemType.song, tags=GroupTag.Song, plentiful_quantity=2),
    Items.RG_DEKU_TREE_MAP: SohItemData(78, IC.filler, 0, tags=GroupTag.Map | GroupTag.Deku_Tree_Item),
    Items.RG_DODONGOS_CAVERN_MAP: SohItemData(79, IC.filler, 0, tags=GroupTag.Map | GroupTag.Dodongos_Cavern_Item),
    Items.RG_JABU_JABUS_BELLY_MAP: SohItemData(80, IC.filler, 0, tags=GroupTag.Map | GroupTag.Jabu_Jabus_Item),
    Items.RG_FOREST_TEMPLE_MAP: SohItemData(81, IC.filler, 0, tags=GroupTag.Map | GroupTag.Forest_Temple_Item),
    Items.RG_FIRE_TEMPLE_MAP: SohItemData(82, IC.filler, 0, tags=GroupTag.Map | GroupTag.Fire_Temple_Item),
    Items.RG_WATER_TEMPLE_MAP: SohItemData(83, IC.filler, 0, tags=GroupTag.Map | GroupTag.Water_Temple_Item),
    Items.RG_SPIRIT_TEMPLE_MAP: SohItemData(84, IC.filler, 0, tags=GroupTag.Map | GroupTag.Spirit_Temple_Item),
    Items.RG_SHADOW_TEMPLE_MAP: SohItemData(85, IC.filler, 0, tags=GroupTag.Map | GroupTag.Shadow_Temple_Item),
    Items.RG_BOTTOM_OF_THE_WELL_MAP: SohItemData(86, IC.filler, 0, tags=GroupTag.Map | GroupTag.Bottom_of_the_Well_Item),
    Items.RG_ICE_CAVERN_MAP: SohItemData(87, IC.filler, 0, tags=GroupTag.Map | GroupTag.Ice_Cavern_Item),
    Items.RG_DEKU_TREE_COMPASS: SohItemData(88, IC.filler, 0, tags=GroupTag.Compass | GroupTag.Deku_Tree_Item),
    Items.RG_DODONGOS_CAVERN_COMPASS: SohItemData(89, IC.filler, 0, tags=GroupTag.Compass | GroupTag.Dodongos_Cavern_Item),
    Items.RG_JABU_JABUS_BELLY_COMPASS: SohItemData(90, IC.filler, 0, tags=GroupTag.Compass | GroupTag.Jabu_Jabus_Item),
    Items.RG_FOREST_TEMPLE_COMPASS: SohItemData(91, IC.filler, 0, tags=GroupTag.Compass | GroupTag.Forest_Temple_Item),
    Items.RG_FIRE_TEMPLE_COMPASS: SohItemData(92, IC.filler, 0, tags=GroupTag.Compass | GroupTag.Fire_Temple_Item),
    Items.RG_WATER_TEMPLE_COMPASS: SohItemData(93, IC.filler, 0, tags=GroupTag.Compass | GroupTag.Water_Temple_Item),
    Items.RG_SPIRIT_TEMPLE_COMPASS: SohItemData(94, IC.filler, 0, tags=GroupTag.Compass | GroupTag.Spirit_Temple_Item),
    Items.RG_SHADOW_TEMPLE_COMPASS: SohItemData(95, IC.filler, 0, tags=GroupTag.Compass | GroupTag.Shadow_Temple_Item),
    Items.RG_BOTTOM_OF_THE_WELL_COMPASS: SohItemData(96, IC.filler, 0, tags=GroupTag.Compass | GroupTag.Bottom_of_the_Well_Item),
    Items.RG_ICE_CAVERN_COMPASS: SohItemData(97, IC.filler, 0, tags=GroupTag.Compass | GroupTag.Ice_Cavern_Item),
    Items.RG_FOREST_TEMPLE_BOSS_KEY: SohItemData(98, IC.progression, 1, tags=GroupTag.Boss_Key | GroupTag.Key | GroupTag.Forest_Temple_Item, plentiful_quantity=2),
    Items.RG_FIRE_TEMPLE_BOSS_KEY: SohItemData(99, IC.progression, 1, tags=GroupTag.Boss_Key | GroupTag.Key | GroupTag.Fire_Temple_Item, plentiful_quantity=2),
    Items.RG_WATER_TEMPLE_BOSS_KEY: SohItemData(100, IC.progression, 1, tags=GroupTag.Boss_Key | GroupTag.Key | GroupTag.Water_Temple_Item, plentiful_quantity=2),
    Items.RG_SPIRIT_TEMPLE_BOSS_KEY: SohItemData(101, IC.progression, 1, tags=GroupTag.Boss_Key | GroupTag.Key | GroupTag.Spirit_Temple_Item, plentiful_quantity=2),
    Items.RG_SHADOW_TEMPLE_BOSS_KEY: SohItemData(102, IC.progression, 1, tags=GroupTag.Boss_Key | GroupTag.Key | GroupTag.Shadow_Temple_Item, plentiful_quantity=2),
    Items.RG_GANONS_CASTLE_BOSS_KEY: SohItemData(103, IC.progression, 0, tags=GroupTag.Boss_Key | GroupTag.Key | GroupTag.Ganons_Castle_Item, plentiful_quantity=2),
    Items.RG_FOREST_TEMPLE_SMALL_KEY: SohItemData(104, IC.progression, 5, tags=GroupTag.Small_Key | GroupTag.Key | GroupTag.Forest_Temple_Item, plentiful_quantity=6),
    Items.RG_FIRE_TEMPLE_SMALL_KEY: SohItemData(105, IC.progression, 8, tags=GroupTag.Small_Key | GroupTag.Key | GroupTag.Fire_Temple_Item, plentiful_quantity=9),
    Items.RG_WATER_TEMPLE_SMALL_KEY: SohItemData(106, IC.progression, 6, tags=GroupTag.Small_Key | GroupTag.Key | GroupTag.Water_Temple_Item, plentiful_quantity=7),
    Items.RG_SPIRIT_TEMPLE_SMALL_KEY: SohItemData(107, IC.progression, 5, tags=GroupTag.Small_Key | GroupTag.Key | GroupTag.Spirit_Temple_Item, plentiful_quantity=6),
    Items.RG_SHADOW_TEMPLE_SMALL_KEY: SohItemData(108, IC.progression, 5, tags=GroupTag.Small_Key | GroupTag.Key | GroupTag.Shadow_Temple_Item, plentiful_quantity=6),
    Items.RG_BOTTOM_OF_THE_WELL_SMALL_KEY: SohItemData(109, IC.progression, 3, tags=GroupTag.Small_Key | GroupTag.Key | GroupTag.Bottom_of_the_Well_Item, plentiful_quantity=4),
    Items.RG_GERUDO_TRAINING_GROUND_SMALL_KEY: SohItemData(110, IC.progression, 9, tags=GroupTag.Small_Key | GroupTag.Key | GroupTag.Traning_Ground_Item, plentiful_quantity=10),
    Items.RG_GERUDO_FORTRESS_SMALL_KEY: SohItemData(111, IC.progression, 4, tags=GroupTag.Small_Key | GroupTag.Key | GroupTag.Gerudo_Fortress_Item),
    Items.RG_GANONS_CASTLE_SMALL_KEY: SohItemData(112, IC.progression, 2, tags=GroupTag.Small_Key | GroupTag.Key | GroupTag.Ganons_Castle_Item, plentiful_quantity=3),
    Items.RG_TREASURE_GAME_SMALL_KEY: SohItemData(113, IC.progression, 0, tags=GroupTag.Small_Key | GroupTag.Key),
    Items.RG_FOREST_TEMPLE_KEY_RING: SohItemData(114, IC.progression, 0, tags=GroupTag.Key_Ring | GroupTag.Key | GroupTag.Forest_Temple_Item, plentiful_quantity=2),
    Items.RG_FIRE_TEMPLE_KEY_RING: SohItemData(115, IC.progression, 0, tags=GroupTag.Key_Ring | GroupTag.Key | GroupTag.Fire_Temple_Item, plentiful_quantity=2),
    Items.RG_WATER_TEMPLE_KEY_RING: SohItemData(116, IC.progression, 0, tags=GroupTag.Key_Ring | GroupTag.Key | GroupTag.Water_Temple_Item, plentiful_quantity=2),
    Items.RG_SPIRIT_TEMPLE_KEY_RING: SohItemData(117, IC.progression, 0, tags=GroupTag.Key_Ring | GroupTag.Key | GroupTag.Spirit_Temple_Item, plentiful_quantity=2),
    Items.RG_SHADOW_TEMPLE_KEY_RING: SohItemData(118, IC.progression, 0, tags=GroupTag.Key_Ring | GroupTag.Key | GroupTag.Shadow_Temple_Item, plentiful_quantity=2),
    Items.RG_BOTTOM_OF_THE_WELL_KEY_RING: SohItemData(119, IC.progression, 0, tags=GroupTag.Key_Ring | GroupTag.Key | GroupTag.Bottom_of_the_Well_Item, plentiful_quantity=2),
    Items.RG_GERUDO_TRAINING_GROUND_KEY_RING: SohItemData(120, IC.progression, 0, tags=GroupTag.Key_Ring | GroupTag.Key | GroupTag.Traning_Ground_Item, plentiful_quantity=2),
    Items.RG_GERUDO_FORTRESS_KEY_RING: SohItemData(121, IC.progression, 0, tags=GroupTag.Key_Ring | GroupTag.Key | GroupTag.Gerudo_Fortress_Item),
    Items.RG_GANONS_CASTLE_KEY_RING: SohItemData(122, IC.progression, 0, tags=GroupTag.Key_Ring | GroupTag.Key | GroupTag.Ganons_Castle_Item, plentiful_quantity=2),
    Items.RG_TREASURE_GAME_KEY_RING: SohItemData(123, IC.progression, 0, tags=GroupTag.Key_Ring | GroupTag.Key),
    Items.RG_KOKIRI_EMERALD: SohItemData(124, IC.progression, 0, tags=GroupTag.Spiritual_Stone | GroupTag.Dungeon_Reward | GroupTag.Deku_Tree_Item),
    Items.RG_GORON_RUBY: SohItemData(125, IC.progression, 0, tags=GroupTag.Spiritual_Stone | GroupTag.Dungeon_Reward | GroupTag.Dodongos_Cavern_Item),
    Items.RG_ZORA_SAPPHIRE: SohItemData(126, IC.progression, 0, tags=GroupTag.Spiritual_Stone | GroupTag.Dungeon_Reward | GroupTag.Jabu_Jabus_Item),
    Items.RG_FOREST_MEDALLION: SohItemData(127, IC.progression, 0, tags=GroupTag.Medallion | GroupTag.Dungeon_Reward | GroupTag.Forest_Temple_Item),
    Items.RG_FIRE_MEDALLION: SohItemData(128, IC.progression, 0, tags=GroupTag.Medallion | GroupTag.Dungeon_Reward | GroupTag.Fire_Temple_Item),
    Items.RG_WATER_MEDALLION: SohItemData(129, IC.progression, 0, tags=GroupTag.Medallion | GroupTag.Dungeon_Reward | GroupTag.Water_Temple_Item),
    Items.RG_SPIRIT_MEDALLION: SohItemData(130, IC.progression, 0, tags=GroupTag.Medallion | GroupTag.Dungeon_Reward | GroupTag.Spirit_Temple_Item),
    Items.RG_SHADOW_MEDALLION: SohItemData(131, IC.progression, 0, tags=GroupTag.Medallion | GroupTag.Dungeon_Reward | GroupTag.Shadow_Temple_Item),
    Items.RG_LIGHT_MEDALLION: SohItemData(132, IC.progression, 0, tags=GroupTag.Medallion | GroupTag.Dungeon_Reward),
    Items.RG_RECOVERY_HEART: SohItemData(133, IC.filler, 0, tags=GroupTag.Consumable_Item),
    Items.RG_GREEN_RUPEE: SohItemData(134, IC.filler, 0, tags=GroupTag.Money),
    Items.RG_GREG_RUPEE: SohItemData(135, IC.progression_skip_balancing, 1, tags=GroupTag.Greg),
    Items.RG_BLUE_RUPEE: SohItemData(136, IC.filler, 0, tags=GroupTag.Money),
    Items.RG_RED_RUPEE: SohItemData(137, IC.filler, 0, tags=GroupTag.Money),
    Items.RG_PURPLE_RUPEE: SohItemData(138, IC.filler, 0, tags=GroupTag.Money),
    Items.RG_HUGE_RUPEE: SohItemData(139, IC.filler, 0, tags=GroupTag.Money),
    # 35
    Items.RG_PIECE_OF_HEART: SohItemData(140, IC.progression_skip_balancing, 0, tags=GroupTag.Health_Upgrade),
    # 8
    Items.RG_HEART_CONTAINER: SohItemData(141, IC.progression_skip_balancing, 0, tags=GroupTag.Health_Upgrade),
    Items.RG_ICE_TRAP: SohItemData(142, IC.trap, 0, tags=GroupTag.Trap),
    # Items.RG_MILK: SohItemData( 143, ),
    # Items.RG_FISH: SohItemData( 144, ),
    Items.RG_BOMBS_5: SohItemData(145, IC.filler, 0, tags=GroupTag.Consumable_Item),
    Items.RG_BOMBS_10: SohItemData(146, IC.filler, 0, tags=GroupTag.Consumable_Item),
    Items.RG_BOMBS_20: SohItemData(147, IC.filler, 0, tags=GroupTag.Consumable_Item),
    Items.RG_BOMBCHU_5: SohItemData(148, IC.filler, 1, tags=GroupTag.Consumable_Item),
    Items.RG_BOMBCHU_10: SohItemData(149, IC.filler, 3, tags=GroupTag.Consumable_Item, scarce_quantity=2, minimal_quantity=0),
    Items.RG_BOMBCHU_20: SohItemData(150, IC.filler, 1, tags=GroupTag.Consumable_Item, plentiful_quantity=2, scarce_quantity=0, minimal_quantity=0),
    Items.RG_ARROWS_5: SohItemData(151, IC.filler, 0, tags=GroupTag.Consumable_Item),
    Items.RG_ARROWS_10: SohItemData(152, IC.filler, 0, tags=GroupTag.Consumable_Item),
    Items.RG_ARROWS_30: SohItemData(153, IC.filler, 0, tags=GroupTag.Consumable_Item),
    Items.RG_DEKU_NUTS_5: SohItemData(154, IC.filler, 0, tags=GroupTag.Consumable_Item),
    Items.RG_DEKU_NUTS_10: SohItemData(155, IC.filler, 0, tags=GroupTag.Consumable_Item),
    Items.RG_DEKU_SEEDS_30: SohItemData(156, IC.filler, 0, tags=GroupTag.Consumable_Item),
    Items.RG_DEKU_STICK_1: SohItemData(157, IC.filler, 0, tags=GroupTag.Consumable_Item),
    # Items.RG_RED_POTION_REFILL: SohItemData( 158, IC.filler, 0 ),
    # Items.RG_GREEN_POTION_REFILL: SohItemData( 159, IC.filler, 0 ),
    # Items.RG_BLUE_POTION_REFILL: SohItemData( 160, IC.filler, 0 ),
    # 1
    Items.RG_TREASURE_GAME_HEART: SohItemData(161, IC.progression_skip_balancing, 0, tags=GroupTag.Health_Upgrade),
    # Items.RG_TREASURE_GAME_GREEN_RUPEE: SohItemData( 162, IC.filler, 0 ),
    Items.RG_BUY_DEKU_NUTS_5: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_ARROWS_30: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_ARROWS_50: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_BOMBS_525: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_DEKU_NUTS_10: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_DEKU_STICK_1: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_BOMBS_10: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_FISH: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_RED_POTION_30: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_GREEN_POTION: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_BLUE_POTION: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_HYLIAN_SHIELD: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_DEKU_SHIELD: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_GORON_TUNIC: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_ZORA_TUNIC: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_HEART: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_BOMBCHUS_10: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_BOMBCHUS_20: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_DEKU_SEEDS_30: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    # Items.RG_SOLD_OUT: SohItemData( None, IC.progression, 0 ),
    Items.RG_BUY_BLUE_FIRE: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_BOTTLE_BUG: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_POE: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_FAIRYS_SPIRIT: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_ARROWS_10: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_BOMBS_20: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_BOMBS_30: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_BOMBS_535: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_RED_POTION_40: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    Items.RG_BUY_RED_POTION_50: SohItemData(None, IC.progression, 0, tags=GroupTag.Purchasable_Item),
    # Items.RG_TRIFORCE: SohItemData( 193, IC.progression, 0 ),
    Items.RG_TRIFORCE_PIECE: SohItemData(194, IC.progression_skip_balancing, 0, tags=GroupTag.Golden_Item),
    Items.RG_GOHMA_SOUL: SohItemData(195, IC.progression, 0, tags=GroupTag.Boss_Soul | GroupTag.Deku_Tree_Item, plentiful_quantity=2),
    Items.RG_KING_DODONGO_SOUL: SohItemData(196, IC.progression, 0, tags=GroupTag.Boss_Soul | GroupTag.Dodongos_Cavern_Item, plentiful_quantity=2),
    Items.RG_BARINADE_SOUL: SohItemData(197, IC.progression, 0, tags=GroupTag.Boss_Soul | GroupTag.Jabu_Jabus_Item, plentiful_quantity=2),
    Items.RG_PHANTOM_GANON_SOUL: SohItemData(198, IC.progression, 0, tags=GroupTag.Boss_Soul | GroupTag.Forest_Temple_Item, plentiful_quantity=2),
    Items.RG_VOLVAGIA_SOUL: SohItemData(199, IC.progression, 0, tags=GroupTag.Boss_Soul | GroupTag.Fire_Temple_Item, plentiful_quantity=2),
    Items.RG_MORPHA_SOUL: SohItemData(200, IC.progression, 0, tags=GroupTag.Boss_Soul | GroupTag.Water_Temple_Item, plentiful_quantity=2),
    Items.RG_BONGO_BONGO_SOUL: SohItemData(201, IC.progression, 0, tags=GroupTag.Boss_Soul | GroupTag.Shadow_Temple_Item, plentiful_quantity=2),
    Items.RG_TWINROVA_SOUL: SohItemData(202, IC.progression, 0, tags=GroupTag.Boss_Soul | GroupTag.Spirit_Temple_Item, plentiful_quantity=2),
    Items.RG_GANON_SOUL: SohItemData(203, IC.progression, 0, tags=GroupTag.Boss_Soul | GroupTag.Ganons_Castle_Item, plentiful_quantity=2),
    Items.RG_OCARINA_A_BUTTON: SohItemData(204, IC.progression, 0, tags=GroupTag.Ocarina_Button, plentiful_quantity=2),
    Items.RG_OCARINA_C_UP_BUTTON: SohItemData(205, IC.progression, 0, tags=GroupTag.Ocarina_Button, plentiful_quantity=2),
    Items.RG_OCARINA_C_DOWN_BUTTON: SohItemData(206, IC.progression, 0, tags=GroupTag.Ocarina_Button, plentiful_quantity=2),
    Items.RG_OCARINA_C_LEFT_BUTTON: SohItemData(207, IC.progression, 0, tags=GroupTag.Ocarina_Button, plentiful_quantity=2),
    Items.RG_OCARINA_C_RIGHT_BUTTON: SohItemData(208, IC.progression, 0, tags=GroupTag.Ocarina_Button, plentiful_quantity=2),
    Items.RG_SKELETON_KEY: SohItemData(209, IC.progression, 0, tags=GroupTag.Key),
    Items.RG_FISHING_POLE: SohItemData(210, IC.progression, 0, tags=GroupTag.Item_Retriever, plentiful_quantity=2),
    Items.RG_DEKU_STICK_BAG: SohItemData(None),
    Items.RG_DEKU_NUT_BAG: SohItemData(None),
    # Items.RG_HINT: SohItemData( 213, IC.filler, 0 ),
    Items.RG_TYCOON_WALLET: SohItemData(None),
    Items.RG_BRONZE_SCALE: SohItemData(None),
    Items.RG_CHILD_WALLET: SohItemData(None),
    # Items.RG_PROGRESSIVE_BOMBCHU_BAG: SohItemData(None),
    # Items.RG_QUIVER_INF: SohItemData( 218, IC.filler, 0 ),
    # Items.RG_BOMB_BAG_INF: SohItemData( 219, IC.filler, 0 ),
    # Items.RG_BULLET_BAG_INF: SohItemData( 220, IC.filler, 0 ),
    # Items.RG_STICK_UPGRADE_INF: SohItemData( 221, IC.filler, 0 ),
    # Items.RG_NUT_UPGRADE_INF: SohItemData( 222, IC.filler, 0 ),
    # Items.RG_MAGIC_INF: SohItemData( 223, IC.filler, 0 ),
    # Items.RG_BOMBCHU_INF: SohItemData( 224, IC.filler, 0 ),
    # Items.RG_WALLET_INF: SohItemData( 225, IC.filler, 0 ),
    Items.RG_FAIRY_OCARINA: SohItemData(None),
    Items.RG_OCARINA_OF_TIME: SohItemData(None),
    Items.RG_BOMB_BAG: SohItemData(None),
    # Items.RG_BIG_BOMB_BAG: SohItemData( 229, IC.filler, 0 ),
    # Items.RG_BIGGEST_BOMB_BAG: SohItemData( 230, IC.filler, 0 ),
    Items.RG_FAIRY_BOW: SohItemData(None, adult_only=True),
    # Items.RG_BIG_QUIVER: SohItemData( 232, IC.filler, 0 ),
    # Items.RG_BIGGEST_QUIVER: SohItemData( 233, IC.filler, 0 ),
    Items.RG_FAIRY_SLINGSHOT: SohItemData(None, child_only=True),
    # Items.RG_BIG_BULLET_BAG: SohItemData( 235, IC.filler, 0 ),
    # Items.RG_BIGGEST_BULLET_BAG: SohItemData( 236, IC.filler, 0 ),
    Items.RG_GORONS_BRACELET: SohItemData(None),
    Items.RG_POWER_BRACELET: SohItemData(None),
    Items.RG_SILVER_GAUNTLETS: SohItemData(None, adult_only=True),
    Items.RG_GOLDEN_GAUNTLETS: SohItemData(None, adult_only=True),
    Items.RG_SILVER_SCALE: SohItemData(None),
    Items.RG_GOLDEN_SCALE: SohItemData(None),
    Items.RG_ADULT_WALLET: SohItemData(None),
    Items.RG_GIANT_WALLET: SohItemData(None),
    # Items.RG_DEKU_NUT_CAPACITY_30: SohItemData( 244, IC.filler, 0 ),
    # Items.RG_DEKU_NUT_CAPACITY_40: SohItemData( 245, IC.filler, 0 ),
    # Items.RG_DEKU_STICK_CAPACITY_20: SohItemData( 246, IC.filler, 0 ),
    # Items.RG_DEKU_STICK_CAPACITY_30: SohItemData( 247, IC.filler, 0 ),
    Items.RG_HOOKSHOT: SohItemData(None, adult_only=True),
    Items.RG_LONGSHOT: SohItemData(None, adult_only=True),
    Items.RG_SCARECROW: SohItemData(250, IC.progression, 0, adult_only=True),
    Items.RG_GUARD_HOUSE_KEY: SohItemData(251, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_MARKET_BAZAAR_KEY: SohItemData(252, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_MARKET_POTION_SHOP_KEY: SohItemData(253, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_MASK_SHOP_KEY: SohItemData(254, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_MARKET_SHOOTING_GALLERY_KEY: SohItemData(255, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_BOMBCHU_BOWLING_KEY: SohItemData(256, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_TREASURE_CHEST_GAME_BUILDING_KEY: SohItemData(257, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_BOMBCHU_SHOP_KEY: SohItemData(258, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_RICHARDS_HOUSE_KEY: SohItemData(259, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_ALLEY_HOUSE_KEY: SohItemData(260, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_KAK_BAZAAR_KEY: SohItemData(261, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_KAK_POTION_SHOP_KEY: SohItemData(262, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_BOSS_HOUSE_KEY: SohItemData(263, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_GRANNYS_POTION_SHOP_KEY: SohItemData(264, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_SKULLTULA_HOUSE_KEY: SohItemData(265, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_IMPAS_HOUSE_KEY: SohItemData(266, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_WINDMILL_KEY: SohItemData(267, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_KAK_SHOOTING_GALLERY_KEY: SohItemData(268, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_DAMPES_HUT_KEY: SohItemData(269, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_TALONS_HOUSE_KEY: SohItemData(270, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_STABLES_KEY: SohItemData(271, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_BACK_TOWER_KEY: SohItemData(272, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_HYLIA_LAB_KEY: SohItemData(273, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_FISHING_HOLE_KEY: SohItemData(274, IC.progression, 0, tags=GroupTag.Overworld_Key | GroupTag.Key, plentiful_quantity=2),
    Items.RG_DISTANT_SCARECROW: SohItemData(275, IC.progression, 0, adult_only=True),
    Items.RG_ROCS_FEATHER: SohItemData(276, IC.progression, 0, tags=GroupTag.Movement_Upgrade, plentiful_quantity=2),
    Items.RG_STICKS: SohItemData(None, child_only=True),
    Items.RG_NUTS: SohItemData(None),
    Items.RG_EPONA: SohItemData(None),
    Items.RG_CLIMB: SohItemData(277, IC.progression, 0, tags=GroupTag.Ability_Upgrade | GroupTag.Movement_Upgrade),
    Items.RG_CRAWL: SohItemData(278, IC.progression, 0, tags=GroupTag.Ability_Upgrade | GroupTag.Movement_Upgrade),
    Items.RG_OPEN_CHEST: SohItemData(280, IC.progression, 0, tags=GroupTag.Ability_Upgrade),
    Items.RG_SPEAK_DEKU: SohItemData(281, IC.progression, 0, tags=GroupTag.Ability_Upgrade | GroupTag.Jabbernut),
    Items.RG_SPEAK_GERUDO: SohItemData(282, IC.progression, 0, tags=GroupTag.Ability_Upgrade | GroupTag.Jabbernut),
    Items.RG_SPEAK_GORON: SohItemData(283, IC.progression, 0, tags=GroupTag.Ability_Upgrade | GroupTag.Jabbernut),
    Items.RG_SPEAK_HYLIAN: SohItemData(284, IC.progression, 0, tags=GroupTag.Ability_Upgrade | GroupTag.Jabbernut),
    Items.RG_SPEAK_KOKIRI: SohItemData(285, IC.progression, 0, tags=GroupTag.Ability_Upgrade | GroupTag.Jabbernut),
    Items.RG_SPEAK_ZORA: SohItemData(286, IC.progression, 0, tags=GroupTag.Ability_Upgrade | GroupTag.Jabbernut),
    Items.RG_DEATH_MOUNTAIN_CRATER_BEAN_SOUL: SohItemData(287, IC.progression, 0, tags=GroupTag.Beans),
    Items.RG_DEATH_MOUNTAIN_TRAIL_BEAN_SOUL: SohItemData(288, IC.progression, 0, tags=GroupTag.Beans),
    Items.RG_DESERT_COLOSSUS_BEAN_SOUL: SohItemData(289, IC.progression, 0, tags=GroupTag.Beans),
    Items.RG_GRAVEYARD_BEAN_SOUL: SohItemData(290, IC.progression, 0, tags=GroupTag.Beans | GroupTag.Graveyard_Item),
    Items.RG_KOKIRI_FOREST_BEAN_SOUL: SohItemData(291, IC.progression, 0, tags=GroupTag.Beans),
    Items.RG_ZORAS_RIVER_BEAN_SOUL: SohItemData(292, IC.progression, 0, tags=GroupTag.Beans),
    Items.RG_GERUDO_VALLEY_BEAN_SOUL: SohItemData(301, IC.progression, 0, tags=GroupTag.Beans),
    Items.RG_LAKE_HYLIA_BEAN_SOUL: SohItemData(302, IC.progression, 0, tags=GroupTag.Beans),
    Items.RG_LOST_WOODS_BEAN_SOUL: SohItemData(303, IC.progression, 0, tags=GroupTag.Beans),
    Items.RG_LOST_WOODS_BRIDGE_BEAN_SOUL: SohItemData(304, IC.progression, 0, tags=GroupTag.Beans),
    Items.RG_KEATON_MASK: SohItemData(293, IC.useful, 0, child_only=True, tags=GroupTag.Mask_Item),
    Items.RG_SKULL_MASK: SohItemData(294, IC.progression, 0, child_only=True, tags=GroupTag.Mask_Item),
    Items.RG_SPOOKY_MASK: SohItemData(295, IC.useful, 0, child_only=True, tags=GroupTag.Mask_Item),
    Items.RG_BUNNY_HOOD: SohItemData(296, IC.useful, 0, child_only=True, tags=GroupTag.Mask_Item),
    Items.RG_GORON_MASK: SohItemData(297, IC.useful, 0, child_only=True, tags=GroupTag.Mask_Item),
    Items.RG_ZORA_MASK: SohItemData(298, IC.useful, 0, child_only=True, tags=GroupTag.Mask_Item),
    Items.RG_GERUDO_MASK: SohItemData(299, IC.useful, 0, child_only=True, tags=GroupTag.Mask_Item),
    Items.RG_MASK_OF_TRUTH: SohItemData(300, IC.progression, 0, child_only=True, tags=GroupTag.Mask_Item),
    Items.RG_RESERVATION: SohItemData(None),
    # Items.MAX: SohItemData( 279, IC.filler, 0 ),
    # Intentionally place the glitched item without a value. Everything else should be above this.
    Items.RG_GLITCHED: SohItemData(None),
}

item_table = {name.value: data.item_id for name,
              data in item_data_table.items() if data.item_id}

filler_items = [
    Items.RG_RECOVERY_HEART,
    Items.RG_BLUE_RUPEE,
    Items.RG_RED_RUPEE,
    Items.RG_PURPLE_RUPEE,
    Items.RG_HUGE_RUPEE,
    Items.RG_BOMBS_5,
    Items.RG_BOMBS_10,
    Items.RG_ARROWS_5,
    Items.RG_ARROWS_10,
    Items.RG_DEKU_NUTS_5,
    Items.RG_DEKU_NUTS_10,
    Items.RG_DEKU_STICK_1,
    Items.RG_DEKU_SEEDS_30
]

no_rules_bottles = [
    Items.RG_EMPTY_BOTTLE,
    Items.RG_BOTTLE_WITH_MILK,
    Items.RG_BOTTLE_WITH_RED_POTION,
    Items.RG_BOTTLE_WITH_GREEN_POTION,
    Items.RG_BOTTLE_WITH_BLUE_POTION,
    Items.RG_BOTTLE_WITH_FAIRY,
    Items.RG_BOTTLE_WITH_FISH,
    Items.RG_BOTTLE_WITH_BLUE_FIRE,
    Items.RG_BOTTLE_WITH_BUGS,
    Items.RG_BOTTLE_WITH_POE
]

progressive_items: dict[str, tuple[str, ...]] = {
    Items.RG_PROGRESSIVE_SCALE: (Items.RG_BRONZE_SCALE, Items.RG_SILVER_SCALE, Items.RG_GOLDEN_SCALE),
    Items.RG_PROGRESSIVE_OCARINA: (Items.RG_FAIRY_OCARINA, Items.RG_OCARINA_OF_TIME),
    Items.RG_PROGRESSIVE_STRENGTH: (Items.RG_POWER_BRACELET, Items.RG_GORONS_BRACELET, Items.RG_SILVER_GAUNTLETS, Items.RG_GOLDEN_GAUNTLETS),
    Items.RG_PROGRESSIVE_HOOKSHOT: (Items.RG_HOOKSHOT, Items.RG_LONGSHOT),
    Items.RG_PROGRESSIVE_WALLET: (Items.RG_CHILD_WALLET, Items.RG_ADULT_WALLET, Items.RG_GIANT_WALLET, Items.RG_TYCOON_WALLET),
    Items.RG_PROGRESSIVE_SLINGSHOT: (Items.RG_FAIRY_SLINGSHOT,),
    Items.RG_PROGRESSIVE_BOW: (Items.RG_FAIRY_BOW,),
    Items.RG_PROGRESSIVE_BOMB_BAG: (Items.RG_BOMB_BAG,),
    Items.RG_PROGRESSIVE_STICK_UPGRADE: (Items.RG_DEKU_STICK_BAG,),
    Items.RG_PROGRESSIVE_NUT_UPGRADE: (Items.RG_DEKU_NUT_BAG,),
    Items.RG_PROGRESSIVE_MAGIC_METER: (Items.RG_MAGIC_SINGLE, Items.RG_MAGIC_DOUBLE)
}

