from collections import Counter
import math
from typing import TYPE_CHECKING, Callable
from collections import Counter

from BaseClasses import CollectionState, ItemClassification as IC, MultiWorld, Location, Region
from .Locations import SohLocation
from worlds.AutoWorld import LogicMixin, World
from .Enums import *
from .Items import SohItem, item_data_table, ItemType, no_rules_bottles, GroupTag, progressive_items
from rule_builder.rules import *
from rule_builder.field_resolvers import *
from .Options import *

if TYPE_CHECKING:
    from . import SohWorld

import logging
logger = logging.getLogger("SOH_OOT.Logic")

child_age_dependent_rules: dict[Regions, list[Rule.Resolved]] = {}
adult_age_dependent_rules: dict[Regions, list[Rule.Resolved]] = {}

class rule_wrapper:
    def __init__(self, parent_region: Regions, rule: Callable[[tuple[Regions, "SohWorld"]], Rule], world: "SohWorld"):
        self.parent_region = parent_region
        self.world = world
        self.rule = rule

    @staticmethod
    def wrap(parent_region: Regions, rule: Callable[[tuple[Regions, "SohWorld"]], Rule], world: "SohWorld") -> Rule:
        wrapper = rule_wrapper(parent_region, rule, world)
        return wrapper.evaluate()

    def evaluate(self) -> Rule:
        rule = self.rule((self.parent_region, self.world))
        return rule 


def test_for_age_check(rule: Rule, parent_region: Regions, world: "SohWorld") -> set[Ages]:
        ages: set[Ages] = set()
        if isinstance(rule, IsChild):
            ages.add(Ages.CHILD)
        elif isinstance(rule, IsAdult):
            ages.add(Ages.ADULT)
        elif isinstance(rule, WrapperRule):
            ages = test_for_age_check(rule.child, parent_region, world)
        elif isinstance(rule, NestedRule):
            ages = set()
            for sub_rule in rule.children:
                ages.update(test_for_age_check(sub_rule, parent_region, world))
        if Ages.CHILD in ages:
            if parent_region in child_age_dependent_rules:
                child_age_dependent_rules[parent_region].append(rule.resolve(world))
            else:
                child_age_dependent_rules[parent_region] = [rule.resolve(world)]
        if Ages.ADULT in ages:
            if parent_region in adult_age_dependent_rules:
                adult_age_dependent_rules[parent_region].append(rule.resolve(world))
            else:
                adult_age_dependent_rules[parent_region] = [rule.resolve(world)]
        return ages

def add_locations(parent_region: Regions, world: "SohWorld", locations: list[tuple[Locations, Rule | Callable[[tuple[Regions, "SohWorld"]], Rule]]]) -> None:
    mLocations : list[tuple[str, int | None, Rule | Callable[[CollectionState], bool]]] = list()
    for loc in locations:
        locationName = str(loc[0])
        if locationName in world.included_locations:
            locationAddress = world.included_locations.pop(loc[0]).loc_id
            if len(loc) > 1 and not world.options.true_no_logic:
                locationRule = loc[1]((parent_region, world)) if callable(loc[1]) else loc[1]
            else:
                locationRule = True_()
            mLocations.append((locationName, locationAddress, locationRule))

    if len(mLocations) > 0:
        # Create the whole batch of locations at once
        world.get_region(str(parent_region)).add_locations({mLoc[0]: mLoc[1] for mLoc in mLocations}, SohLocation)

        # Set rules
        for mLocation in mLocations:
            locationRule = mLocation[2]
            location: Location = world.get_location(mLocation[0])
            world.set_rule(location, locationRule)


def connect_regions(parent_region: Regions, world: "SohWorld", child_regions: list[tuple[Regions, Rule | Callable[[tuple[Regions, "SohWorld"]], Rule]]]) -> None:
    parentRegion: Region = world.get_region(str(parent_region))

    for region in child_regions:
        childRegion = world.get_region(region[0])
        
        if len(region) > 1 and not world.options.true_no_logic:
            regionRule = region[1]((parent_region, world)) if callable(region[1]) else region[1]  # type: ignore # noqa
        else:
            regionRule = True_()
        world.create_entrance(parentRegion, childRegion, regionRule)


def add_events(parent_region: Regions, world: "SohWorld", events: list[tuple[StrEnum, Events | StrEnum, Rule | Callable[[tuple[Regions, "SohWorld"]], Rule]]]) -> None:
    parentRegion: Region = world.get_region(str(parent_region))

    for event in events:
        eventName = str(event[0])
        eventItemName = str(event[1])
        eventRule = event[2]((parent_region, world)) if callable(event[2]) else event[2]
        # test_for_age_check(eventRule, parent_region, world)
        parentRegion.add_event(eventName, eventItemName, eventRule, SohLocation, SohItem)


def can_use(item: Items, bundle: tuple[Regions, "SohWorld"]) -> Rule:
    rule : Rule = has_item(item, bundle)
    data = item_data_table

    if item in data:
        if data[item].adult_only:
            rule &= is_adult(bundle)

        if data[item].child_only:
            rule &= is_child(bundle)

        if data[item].item_type == ItemType.magic:
            rule &= has_item(Items.MAGIC_SINGLE, bundle)

        if data[item].item_type == ItemType.song:
            rule &= can_play_song(item, bundle)

    if item in (Items.FIRE_ARROW, Items.ICE_ARROW, Items.LIGHT_ARROW):
        rule &= can_use(Items.FAIRY_BOW, bundle)

    if item in (Items.BOMBCHU_BAG, Items.BOMBCHUS_5, Items.BOMBCHUS_10, Items.BOMBCHUS_20):
        rule &= bombchu_refill(bundle)

    if item == Items.FISHING_POLE:
        rule &= has_item(Items.CHILD_WALLET, bundle)

    if item == Items.EPONA:
        rule &= is_adult(bundle) & can_use(Items.EPONAS_SONG, bundle)
    
    return rule

def can_use_any(names: list[Items], bundle: tuple[Regions, "SohWorld"]) -> Rule:
    rule: Rule
    for i in range(len(names)):
        if i == 0:
            rule = can_use(names[i], bundle)
        else:
            rule |= can_use(names[i], bundle) # type: ignore
    return rule # type: ignore


def has_item(item: Items | Events | StrEnum, bundle: tuple[Regions, "SohWorld"], count: int = 1) -> Rule:
    if item == Items.STICKS:
        return has_item(Events.CAN_FARM_STICKS, bundle) & has_item(Items.DEKU_STICK_BAG, bundle)

    if item in (Items.BOMBCHU_BAG, Items.BOMBCHUS_5, Items.BOMBCHUS_10, Items.BOMBCHUS_20):
        return bombchus_enabled(bundle)

    if item == Items.NUTS:
        return has_item(Events.CAN_FARM_NUTS, bundle) & has_item(Items.DEKU_NUT_BAG, bundle)

    if item == Items.MAGIC_BEAN:
        return HasAny(Items.MAGIC_BEAN_PACK, Events.CAN_BUY_BEANS)

    if item == Items.DEKU_SHIELD:
        return Has(Items.BUY_DEKU_SHIELD)

    if item == Items.HYLIAN_SHIELD:
        return Has(Items.BUY_HYLIAN_SHIELD)

    if item == Items.GORON_TUNIC:
        return HasAny(Items.BUY_GORON_TUNIC, Items.GORON_TUNIC)

    if item == Items.ZORA_TUNIC:
        return HasAny(Items.BUY_ZORA_TUNIC, Items.ZORA_TUNIC)

    if item == Items.SCARECROW:
        return scarecrows_song(bundle) & can_use(Items.HOOKSHOT, bundle)

    if item == Items.DISTANT_SCARECROW:
        return scarecrows_song(bundle) & can_use(Items.LONGSHOT, bundle)

    if item == Items.FISHING_POLE:
        return OptionFilter(ShuffleFishingPole, False) | Has(Items.FISHING_POLE)

    if item == Items.EPONA:
        return Has(Events.FREED_EPONA)

    if item in {Items.POCKET_EGG, Items.COJIRO, Items.ODD_MUSHROOM, Items.ODD_POTION, Items.POACHERS_SAW,
                Items.BROKEN_GORONS_SWORD, Items.PRESCRIPTION, Items.EYEBALL_FROG, Items.WORLDS_FINEST_EYEDROPS}:
        return OptionFilter(ShuffleAdultTradeItems, False) | Has(item)

    if item == Items.BOTTLE_WITH_BLUE_FIRE:
        return has_bottle(bundle) & (Has(Events.CAN_ACCESS_BLUE_FIRE) | Has(Items.BUY_BLUE_FIRE))

    if item == Items.BOTTLE_WITH_BLUE_POTION:
        return has_bottle(bundle) & Has(Items.BUY_BLUE_POTION)

    if item == Items.BOTTLE_WITH_BUGS:
        return has_bottle(bundle) & (Has(Events.CAN_ACCESS_BUGS) | Has(Items.BUY_BOTTLE_BUG))

    if item == Items.BOTTLE_WITH_FAIRY:
        return has_bottle(bundle) & (Has(Events.CAN_ACCESS_FAIRIES) | Has(Items.BUY_FAIRYS_SPIRIT))

    if item == Items.BOTTLE_WITH_FISH:
        return has_bottle(bundle) & (Has(Events.CAN_ACCESS_FISH) | Has(Items.BUY_FISH))

    if item == Items.BOTTLE_WITH_GREEN_POTION:
        return has_bottle(bundle) & Has(Items.BUY_GREEN_POTION)

    if item in (Items.BOTTLE_WITH_MILK, Items.BOTTLE_WITH_POE, Items.BOTTLE_WITH_RED_POTION, Items.EMPTY_BOTTLE):
        return has_bottle(bundle)

    for prog,non_progs in progressive_items.items():
        if item in non_progs:
            return Has(prog, non_progs.index(item) + 1)

    return Has(item, count)



@dataclasses.dataclass
class CanAffordSlot(Rule, game="Ship of Harkinian"):
    location: Locations

    def _instantiate(self, world: "SohWorld") -> Rule.Resolved: # type: ignore
        return self.Resolved(location = self.location, player = world.player,
                             caching_enabled=getattr(world, "rule_caching_enabled", False))

    class Resolved(Rule.Resolved):
        location: Locations
        #player: int
        
        def _evaluate(self, state: CollectionState) -> bool:
            world = state.multiworld.worlds[self.player]
            wallet = get_wallet_for_shop_slot(self.location, world)[0] #type: ignore
            prog_wallet_count = progressive_items[Items.PROGRESSIVE_WALLET].index(wallet) + 1
            return state.has(Items.PROGRESSIVE_WALLET, self.player, prog_wallet_count)

        def item_dependencies(self) -> dict[str, set[int]]:
            return {str(Items.PROGRESSIVE_WALLET): {id(self)}}
        
        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            data = get_wallet_for_shop_slot(self.location, state.multiworld.worlds[self.player])
            verb = "Missing " if state and not self(state) else "Has "
            messages: list[JSONMessagePart] = [{"type": "text", "text": verb}]
            if state:
                color = "green" if self(state) else "salmon"
                messages.append({"type": "color", "color": color, "text": data[0]})
                messages.append({"type": "text", "text": f" to buy item for "})
                messages.append({"type": "color", "color": "cyan", "text": str(data[1])})
                messages.append({"type": "text", "text": f" rupees"})
            else:
                messages.append({"type": "item_name", "flags": 0b001, "text": data[0], "player": self.player})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            data = get_wallet_for_shop_slot(self.location, state.multiworld.worlds[self.player])
            if state is None:
                return str(self)
            prefix = "Has" if self(state) else "Missing"
            return f"{prefix} {data[0]} to buy item for {str(data[1])} rupees"

        @override
        def __str__(self) -> str:
            return f"Has wallet large enough to buy the item at {str(self.location)}"


def get_wallet_for_shop_slot(location: Locations, world: "SohWorld") -> tuple[str, int]:
    assert location in world.shop_prices, f'Shop location "{str(location)}" does not have a price assigned'

    price = world.shop_prices.get(location, 500)
    for wallet, amount in wallet_capacities.items():
        if amount >= price:
            return str(wallet), price

def can_afford_slot(slot: Locations, bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return CanAffordSlot(slot)


def scarecrows_song(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return ((OptionFilter(SkipScarecrowsSong, True) & has_item(Items.FAIRY_OCARINA, bundle)
            & has_enough_ocarina_buttons(bundle, 2))
            | (has_item(Events.CHILD_SCARECROW_UNLOCKED, bundle) & has_item(Events.ADULT_SCARECROW_UNLOCKED, bundle)))


def has_bottle(bundle: tuple[Regions, "SohWorld"]) -> Rule:  # soup
    return has_bottle_count(1)

#Exists just to make the bottle rule somewhat more understandable in explains
@dataclasses.dataclass()
class HasBottleCount(WrapperRule, game="Ship of Harkinian"):
    count: int

    def _instantiate(self, world: World) -> Rule.Resolved:
        return self.Resolved(
            self.child.resolve(world),
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
            count = self.count
        )

    class Resolved(WrapperRule.Resolved):
        count: int
        
        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            verb = "Does not have " if state and not self(state) else "Has "
            messages: list[JSONMessagePart] = [{"type": "text", "text": verb}]
            bottles = "bottles" if self.count > 1 else "bottle"
            if state:
                messages.append({"type": "color", "color": "cyan", "text": f"{self.count} "})
                messages.append({"type": "text", "text": f"emptiable {bottles}"})
            else:
                messages.append({"type": "text", "text": f"at least {self.count} emptiable {bottles}"})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            return f"{"Has" if self(state) else "Does not have"} {self.count} emptiable bottle{"s" if self.count > 1 else ""}"

        @override
        def __str__(self) -> str:
            return f"Has {self.count} bottle{"s" if self.count>1 else ""}"


def has_bottle_count(target_count: int) -> Rule:
    return HasBottleCount( \
        (HasAll(Events.DELIVER_LETTER, Events.CAN_EMPTY_BIG_POES) & HasFromList(*no_rules_bottles, Items.BOTTLE_WITH_BIG_POE, Items.BOTTLE_WITH_RUTOS_LETTER, count=target_count)) \
            | (Has(Events.DELIVER_LETTER) & HasFromList(*no_rules_bottles, Items.BOTTLE_WITH_RUTOS_LETTER, count=target_count)) \
            | (Has(Events.CAN_EMPTY_BIG_POES) & HasFromList(*no_rules_bottles, Items.BOTTLE_WITH_BIG_POE, count=target_count)) \
            | HasFromList(*no_rules_bottles, count=target_count) \
        , count = target_count)


def bombchu_refill(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return OptionFilter(BombchuDrops, True) | HasAny(Items.BUY_BOMBCHUS10, Items.BUY_BOMBCHUS20, Events.COULD_PLAY_BOWLING, Events.CARPET_MERCHANT)


def bombchus_enabled(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return Has(Items.BOMBCHU_BAG) | Has(Items.PROGRESSIVE_BOMB_BAG, options=[OptionFilter(BombchuBag, False)])


ocarina_buttons_required: dict[str, list[str]] = {
    Items.ZELDAS_LULLABY: [Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CUP_BUTTON],
    Items.EPONAS_SONG: [Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CUP_BUTTON],
    Items.PRELUDE_OF_LIGHT: [Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CUP_BUTTON],
    Items.SARIAS_SONG: [Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CDOWN_BUTTON],
    Items.SUNS_SONG: [Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CUP_BUTTON, Items.OCARINA_CDOWN_BUTTON],
    Items.SONG_OF_TIME: [Items.OCARINA_A_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CDOWN_BUTTON],
    Items.BOLERO_OF_FIRE: [Items.OCARINA_A_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CDOWN_BUTTON],
    Items.REQUIEM_OF_SPIRIT: [Items.OCARINA_A_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CDOWN_BUTTON],
    Items.SONG_OF_STORMS: [Items.OCARINA_A_BUTTON, Items.OCARINA_CUP_BUTTON, Items.OCARINA_CDOWN_BUTTON],
    Items.MINUET_OF_FOREST: [Items.OCARINA_A_BUTTON, Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CUP_BUTTON],
    Items.SERENADE_OF_WATER: [Items.OCARINA_A_BUTTON, Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CDOWN_BUTTON],
    Items.NOCTURNE_OF_SHADOW: [Items.OCARINA_A_BUTTON, Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CDOWN_BUTTON],
}


def can_play_song(song: StrEnum, bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return has_item(Items.FAIRY_OCARINA, bundle) & has_item(song, bundle) & (OptionFilter(ShuffleOcarinaButtons, False) | HasAll(*ocarina_buttons_required[song]))


def has_explosives(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    """Check if Link has access to explosives (bombs or bombchus)."""
    return can_use_any([Items.BOMB_BAG, Items.BOMBCHU_BAG], bundle)


def blast_or_smash(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    """Check if Link can blast or smash obstacles."""
    return has_explosives(bundle) | can_use(Items.MEGATON_HAMMER, bundle)


def blue_fire(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    """Check if Link has access to blue fire."""
    return ((has_bottle(bundle) &
             (has_item(Events.CAN_ACCESS_BLUE_FIRE, bundle) |
              has_item(Items.BUY_BLUE_FIRE, bundle))) |
            (can_use(Items.ICE_ARROW, bundle) &
             OptionFilter(BlueFireArrows, True)))


def can_use_sword(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    """Check if Link can use any sword."""
    return can_use_any([Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD], bundle)


def has_projectile(bundle: tuple[Regions, "SohWorld"], age: Ages = Ages.null) -> Rule:
    """Check if Link has access to projectiles."""
    if age == Ages.CHILD:
        return has_explosives(bundle) | can_use_any([Items.FAIRY_SLINGSHOT, Items.BOOMERANG], bundle)
    elif age == Ages.ADULT:
        return has_explosives(bundle) | can_use_any([Items.HOOKSHOT, Items.FAIRY_BOW], bundle)
    else:  # "either"
        return has_explosives(bundle) | can_use_any([Items.FAIRY_SLINGSHOT, Items.BOOMERANG, Items.HOOKSHOT, Items.FAIRY_BOW], bundle)


def can_use_projectile(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return has_projectile(bundle)


def can_break_mud_walls(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return blast_or_smash(bundle) | (can_do_trick(Tricks.BLUE_FIRE_MUD_WALLS, bundle) & blue_fire(bundle))


def can_get_deku_baba_sticks(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return can_use_sword(bundle) | can_use(Items.BOOMERANG, bundle)


def can_get_deku_baba_nuts(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return can_use_any([Items.FAIRY_SLINGSHOT, Items.FAIRY_BOW, Items.DINS_FIRE], bundle) | can_jump_slash(bundle) | has_explosives(bundle)


@dataclasses.dataclass
class IsAdult(Rule, game="Ship of Harkinian"):
    parent_region: Regions

    def _instantiate(self, world: "SohWorld") -> Rule.Resolved: # type: ignore
        return self.Resolved(parent_region = self.parent_region, player = world.player, caching_enabled=getattr(world, "rule_caching_enabled", False))

    class Resolved(Rule.Resolved):
        parent_region: Regions
        force_recalculate = True
        def _evaluate(self, state: CollectionState) -> bool:
            return state._soh_can_reach_as_age(self.parent_region, Ages.ADULT, self.player) # type: ignore

        def item_dependencies(self) -> dict[str, set[int]]:
            return {}
        
        def region_dependencies(self) -> dict[str, set[int]]:
            return {self.parent_region.value: {id(self)}}
        
        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            verb = "Can not " if state and not self(state) else "Can "
            messages: list[JSONMessagePart] = [{"type": "text", "text": verb}]
            if state:
                color = "green" if self(state) else "salmon"
                messages.append({"type": "text", "text": "reach "})
                messages.append({"type": "color", "color": "cyan", "text": f"{self.parent_region} "})
                messages.append({"type": "text", "text": "as "})
                messages.append({"type": "color", "color": color, "text": "Adult Link"})
            return messages
        
        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            prefix = "Can" if self(state) else "Can not"
            return f"{prefix} reach {str(self.parent_region)} as Adult Link"

        @override
        def __str__(self) -> str:
            return f"Can reach {str(self.parent_region)} as Adult Link"

@dataclasses.dataclass
class IsChild(Rule, game="Ship of Harkinian"):
    parent_region: Regions

    def _instantiate(self, world: "SohWorld") -> Rule.Resolved: # type: ignore
        return self.Resolved(parent_region = self.parent_region, player = world.player, caching_enabled=getattr(world, "rule_caching_enabled", False))

    class Resolved(Rule.Resolved):
        parent_region: Regions
        force_recalculate = True
        def _evaluate(self, state: CollectionState) -> bool:
            return state._soh_can_reach_as_age(self.parent_region, Ages.CHILD, self.player) # type: ignore

        def item_dependencies(self) -> dict[str, set[int]]:
            return {}
        
        def region_dependencies(self) -> dict[str, set[int]]:
            return {self.parent_region.value: {id(self)}}
        
        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            verb = "Can not " if state and not self(state) else "Can "
            messages: list[JSONMessagePart] = [{"type": "text", "text": verb}]
            if state:
                color = "green" if self(state) else "salmon"
                messages.append({"type": "text", "text": "reach "})
                messages.append({"type": "color", "color": "cyan", "text": f"{self.parent_region} "})
                messages.append({"type": "text", "text": "as "})
                messages.append({"type": "color", "color": color, "text": "Child Link"})
            return messages
        
        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            prefix = "Can" if self(state) else "Can not"
            return f"{prefix} reach {self.parent_region} as Child Link"

        @override
        def __str__(self) -> str:
            return f"Can reach {self.parent_region} as Child Link"

#Build the rules
def is_child(bundle: tuple[Regions, "SohWorld"]):
    return IsChild(bundle[0])

def is_adult(bundle: tuple[Regions, "SohWorld"]):
    return IsAdult(bundle[0])

def at_day(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return ((is_child(bundle) & has_item(Events.CHILD_CAN_PASS_TIME, bundle))
            | (is_adult(bundle) & has_item(Events.ADULT_CAN_PASS_TIME, bundle)))
    # TODO: Implement starting time of day if that ever gets added


def at_night(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return ((is_child(bundle) & has_item(Events.CHILD_CAN_PASS_TIME, bundle))
            | (is_adult(bundle) & has_item(Events.ADULT_CAN_PASS_TIME, bundle)))
    # TODO: Implement starting time of day if that ever gets added

def starting_age(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return IsChild(bundle[0], options=[OptionFilter(StartingAge, StartingAge.option_child)]) | IsAdult(bundle[0], options=[OptionFilter(StartingAge, StartingAge.option_adult)])


def can_damage(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    """Check if Link can deal damage to enemies."""
    return (can_jump_slash(bundle) |
            has_explosives(bundle) |
            can_use_any([Items.FAIRY_SLINGSHOT, Items.FAIRY_BOW, Items.DINS_FIRE], bundle))


def can_attack(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    """Check if Link can attack enemies (damage or stun)."""
    return (can_damage(bundle) |
            can_use_any([Items.BOOMERANG, Items.HOOKSHOT], bundle))


def can_standing_shield(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    """Check if Link can use a shield for standing blocks."""
    return (can_use_any([Items.MIRROR_SHIELD, Items.DEKU_SHIELD], bundle) |
            (is_adult(bundle) & can_use(Items.HYLIAN_SHIELD, bundle)))


def can_shield(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    """Check if Link can use a shield for blocking or stunning."""
    return can_use_any([Items.MIRROR_SHIELD, Items.HYLIAN_SHIELD, Items.DEKU_SHIELD], bundle)


def take_damage(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return (can_use_any([Items.BOTTLE_WITH_FAIRY, Items.NAYRUS_LOVE], bundle)
            | effective_health_at_least(bundle, 1))


def can_do_trick(trick: Tricks, bundle: tuple[Regions, "SohWorld"]) -> Rule:
    # check if we have the trick enabled, the GLITCHED item is for Universal Tracker purposes.
    return OptionFilter(EnableAllTricks, True) | Has(Items.GLITCHED) | OptionFilter(TricksInLogic, trick.value, "contains")


def can_get_nighttime_gs(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return at_night(bundle) & (OptionFilter(SkullsSunSong, False) | can_use(Items.SUNS_SONG, bundle))


def can_break_pots(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    """Check if Link can break pots for items."""
    return True_()


def can_break_crates(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    """Check if Link can break crates."""
    return True_()


def can_break_small_crates(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    """Check if Link can break small crates."""
    return True_()


def can_bonk_trees(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    """Check if Link can bonk trees."""
    return True_()


def can_hit_eye_targets(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    """Check if Link can hit eye switches/targets."""
    return can_use_any([Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT], bundle)


def can_stun_deku(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    """Check if Link can stun Deku Scrubs."""
    return can_attack(bundle) | can_use(Items.NUTS, bundle) | can_reflect_nuts(bundle)


def can_reflect_nuts(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    """Check if Link can reflect Deku Nuts back at enemies."""
    return can_use(Items.DEKU_SHIELD, bundle) | (is_adult(bundle) & has_item(Items.HYLIAN_SHIELD, bundle))


def has_fire_source_with_torch(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    """Check if Link has a fire source that can be used with a torch."""
    return has_fire_source(bundle) | can_use(Items.STICKS, bundle)


def has_fire_source(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    """Check if Link has any fire source."""
    return can_use_any([Items.DINS_FIRE, Items.FIRE_ARROW], bundle)


def can_jump_slash_except_hammer(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    """Check if Link can perform a jump slash with any sword."""
    return can_use(Items.STICKS, bundle) | can_use_sword(bundle)


def can_jump_slash(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    """Check if Link can perform a jump slash at all"""
    return can_jump_slash_except_hammer(bundle) | can_use(Items.MEGATON_HAMMER, bundle)


def call_gossip_fairy_except_suns(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return can_use_any([Items.ZELDAS_LULLABY, Items.EPONAS_SONG, Items.SONG_OF_TIME], bundle)


def call_gossip_fairy(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return (call_gossip_fairy_except_suns(bundle) | can_use(Items.SUNS_SONG, bundle))


def can_break_lower_hives(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return can_break_upper_beehives(bundle) | can_use(Items.BOMB_BAG, bundle)


def can_break_upper_beehives(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return (hookshot_or_boomerang(bundle) | 
            (can_do_trick(Tricks.BOMBCHU_BEEHIVES, bundle) & can_use(Items.BOMBCHU_BAG, bundle)) |
            (OptionFilter(SlingbowBreakBeehives, True) & (can_use_any([Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT], bundle))))


def can_open_storms_grotto(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return (can_use(Items.SONG_OF_STORMS, bundle) & (has_item(Items.STONE_OF_AGONY, bundle) | can_do_trick(Tricks.GROTTOS_WITHOUT_AGONY, bundle)))


def can_hit_at_range(bundle: tuple[Regions, "SohWorld"],
                     distance: EnemyDistance = EnemyDistance.CLOSE,
                     wall_or_floor: bool = True, in_water: bool = False) -> Rule:
    rule = False_()
    if distance == EnemyDistance.CLOSE:
        rule |= can_use(Items.MEGATON_HAMMER, bundle)
    if distance <= EnemyDistance.SHORT_JUMPSLASH:
        rule |= can_use(Items.KOKIRI_SWORD, bundle)
    if distance <= EnemyDistance.MASTER_SWORD_JUMPSLASH:
        rule |= can_use(Items.MASTER_SWORD, bundle)
    if distance <= EnemyDistance.LONG_JUMPSLASH:
        rule |= can_use_any([Items.BIGGORONS_SWORD, Items.STICKS], bundle)
    if distance <= EnemyDistance.BOMB_THROW and not in_water:
        rule |= can_use(Items.BOMB_BAG, bundle)
    if distance <= EnemyDistance.HOOKSHOT:
        wof = True_() if wall_or_floor else False_()
        rule |= can_use(Items.HOOKSHOT, bundle) | (wof & can_use(Items.BOMBCHUS_5, bundle))
    if distance <= EnemyDistance.LONGSHOT:
        rule |= can_use(Items.LONGSHOT, bundle)
    if distance <= EnemyDistance.FAR:
        rule |= can_use_any([Items.FAIRY_SLINGSHOT, Items.FAIRY_BOW], bundle)
    return rule

def can_kill_enemy(bundle: tuple[Regions, "SohWorld"], enemy: Enemies, distance: EnemyDistance = EnemyDistance.CLOSE,
                   wall_or_floor: bool = True, quantity: int = 1, timer: bool = False, in_water: bool = False) -> Rule:
    """
    Check if Link can kill a specific enemy at a given combat range.
    Based on the C++ Logic::CanKillEnemy implementation.

    Args:
        bundle: The standard bundle of state, regions, and the world class
        enemy: Enemy type (e.g., "gold_skulltula", "keese", etc.)
        distance: Combat range - "close", "short_jumpslash", "master_sword_jumpslash",
                     "long_jumpslash", "bomb_throw", "boomerang", "hookshot", "longshot", "far"
        wall_or_floor: Whether enemy is on wall or floor
        quantity: Number of enemies (for ammo considerations)
        timer: Whether there's a timer constraint
        in_water: Whether the fight is underwater
    """

    # Enemy-specific logic based on C++ implementation

    if enemy in [Enemies.GERUDO_GUARD, Enemies.BREAK_ROOM_GUARD]:
        return False_()
    #For some of the cases to use
    rule = False_()
    if enemy == Enemies.GOLD_SKULLTULA:
        rule = can_hit_at_range(bundle, distance, wall_or_floor, in_water)
        if distance <= EnemyDistance.LONGSHOT and wall_or_floor: 
            rule |= can_use(Items.BOMBCHUS_5, bundle)
        if distance <= EnemyDistance.BOOMERANG:
            rule |= can_use_any([Items.DINS_FIRE, Items.BOOMERANG], bundle)
        return rule
    if enemy == Enemies.BIG_SKULLTULA:
        rule = can_hit_at_range(bundle, distance, wall_or_floor, in_water)
        if distance <= EnemyDistance.BOOMERANG:
            rule |= can_use(Items.DINS_FIRE, bundle)
        return rule
    if enemy in [Enemies.GOHMA_LARVA, Enemies.MAD_SCRUB, Enemies.DEKU_BABA]:
        return can_attack(bundle)
    if enemy == Enemies.DODONGO:
        rule = can_use_sword(bundle) \
                | can_use_any([Items.MEGATON_HAMMER, Items.FAIRY_SLINGSHOT, Items.FAIRY_BOW], bundle) \
                | has_explosives(bundle)
        if quantity <= 5:
            rule |= can_use(Items.STICKS, bundle)
        return rule
    if enemy == Enemies.LIZALFOS:
        return (can_jump_slash(bundle)
                | can_use_any([Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT], bundle)
                | has_explosives(bundle))

    if enemy in [Enemies.KEESE, Enemies.FIRE_KEESE]:
        rule = can_hit_at_range(bundle, distance, wall_or_floor, in_water)
        if distance == EnemyDistance.CLOSE:
            rule |= can_use(Items.KOKIRI_SWORD, bundle)
        if distance <= EnemyDistance.BOOMERANG:
            rule |= can_use(Items.BOOMERANG, bundle)
        if distance == EnemyDistance.SHORT_JUMPSLASH:
            rule |= can_use(Items.MEGATON_HAMMER, bundle)
        return rule
    if enemy == Enemies.BLUE_BUBBLE:
        return blast_or_smash(bundle) | can_use(Items.FAIRY_BOW, bundle) | \
            ((can_jump_slash_except_hammer(bundle) | can_use(Items.FAIRY_SLINGSHOT, bundle)) &
             (can_use(Items.NUTS, bundle) | hookshot_or_boomerang(bundle) | can_standing_shield(bundle)))

    if enemy == Enemies.DEAD_HAND:
        return can_use_sword(bundle) | (can_use(Items.STICKS, bundle) & can_do_trick(Tricks.BOTW_CHILD_DEADHAND, bundle))

    if enemy == Enemies.WITHERED_DEKU_BABA:
        return can_attack(bundle) | can_use(Items.BOOMERANG, bundle)

    if enemy in [Enemies.LIKE_LIKE, Enemies.FLOORMASTER]:
        return can_damage(bundle)

    if enemy == Enemies.STALFOS:
        rule = False_()
        if distance <= EnemyDistance.SHORT_JUMPSLASH:
            rule |= can_use_any([Items.MEGATON_HAMMER, Items.KOKIRI_SWORD], bundle)
        if distance <= EnemyDistance.MASTER_SWORD_JUMPSLASH:
            rule |= can_use(Items.MASTER_SWORD, bundle)
        if distance <= EnemyDistance.LONG_JUMPSLASH:
            rule |= can_use(Items.BIGGORONS_SWORD, bundle)
            if quantity <= 1:
                rule |= can_use(Items.STICKS, bundle)
        if distance <= EnemyDistance.BOMB_THROW and quantity <= 2 and not timer and not in_water:
            rule |= (can_use(Items.NUTS, bundle) | hookshot_or_boomerang(bundle)) & can_use(Items.BOMB_BAG, bundle)
        if distance <= EnemyDistance.HOOKSHOT and wall_or_floor:
            rule |= can_use(Items.BOMBCHUS_5, bundle)
        if distance <= EnemyDistance.FAR:
            rule |= can_use(Items.FAIRY_BOW, bundle)
        return rule

    if enemy == Enemies.IRON_KNUCKLE:
        return (can_use_sword(bundle) |
                can_use(Items.MEGATON_HAMMER, bundle) |
                has_explosives(bundle))

    if enemy == Enemies.FLARE_DANCER:
        return (can_use_any([Items.MEGATON_HAMMER, Items.HOOKSHOT], bundle)
                | (has_explosives(bundle)
                    & (can_jump_slash_except_hammer(bundle)
                         | can_use_any([Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT, Items.BOOMERANG], bundle))))

    if enemy in [Enemies.WOLFOS, Enemies.WHITE_WOLFOS, Enemies.WALLMASTER]:
        return (can_jump_slash(bundle)
                | can_use_any([Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT, Items.BOMBCHUS_5, Items.DINS_FIRE], bundle)
                | (can_use(Items.BOMB_BAG, bundle)
                    & can_use_any([Items.NUTS, Items.HOOKSHOT, Items.BOOMERANG], bundle)))

    if enemy == Enemies.GERUDO_WARRIOR:
        return can_jump_slash(bundle) | can_use(Items.FAIRY_BOW, bundle) | \
            (can_do_trick(Tricks.GF_WARRIOR_WITH_DIFFICULT_WEAPON, bundle) &
             can_use_any([Items.FAIRY_SLINGSHOT, Items.BOMBCHUS_5], bundle))

    if enemy in [Enemies.GIBDO, Enemies.REDEAD]:
        return can_jump_slash(bundle) | can_use(Items.DINS_FIRE, bundle)

    if enemy == Enemies.MEG:
        return can_use_any([Items.FAIRY_BOW, Items.HOOKSHOT], bundle) | has_explosives(bundle)

    if enemy == Enemies.ARMOS:
        return (blast_or_smash(bundle)
                | can_use_any([Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.STICKS, Items.FAIRY_BOW], bundle)
                | (can_use_any([Items.NUTS, Items.HOOKSHOT, Items.BOOMERANG], bundle)
                    & can_use_any([Items.KOKIRI_SWORD, Items.FAIRY_SLINGSHOT], bundle)))

    if enemy == Enemies.GREEN_BUBBLE:
        return (can_jump_slash(bundle)
                | can_use_any([Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT], bundle)
                | has_explosives(bundle))

    if enemy == Enemies.DINOLFOS:
        rule = can_jump_slash(bundle) | can_use_any([Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT], bundle)
        if not timer:
            rule |= can_use(Items.BOMBCHUS_5, bundle)
        return rule
    if enemy == Enemies.TORCH_SLUG:
        return can_jump_slash(bundle) | has_explosives(bundle) | can_use(Items.FAIRY_BOW, bundle)

    if enemy == Enemies.FREEZARD:
        return (can_use_any([Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.MEGATON_HAMMER, Items.STICKS,
                             Items.HOOKSHOT, Items.DINS_FIRE, Items.FIRE_ARROW], bundle)
                | has_explosives(bundle))

    if enemy == Enemies.SHELL_BLADE:
        return (can_jump_slash(bundle) | has_explosives(bundle)
                | can_use_any([Items.HOOKSHOT, Items.FAIRY_BOW, Items.DINS_FIRE], bundle))

    if enemy == Enemies.SPIKE:
        return (can_use_any([Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.MEGATON_HAMMER, Items.STICKS,
                            Items.HOOKSHOT, Items.FAIRY_BOW, Items.DINS_FIRE], bundle)
                | has_explosives(bundle))

    if enemy == Enemies.STINGER:
        rule = can_hit_at_range(bundle, distance, wall_or_floor, in_water)
        if distance == EnemyDistance.SHORT_JUMPSLASH:
            rule |= can_use(Items.MEGATON_HAMMER, bundle)
        return rule
    
    if enemy == Enemies.BIG_OCTO:
        # If chasing octo is annoying but with rolls you can catch him, and you need rang to get into this room
        # without shenanigans anyway. Bunny makes it free
        # todo: should this have biggoron sword too?
        return can_use_any([Items.KOKIRI_SWORD, Items.STICKS, Items.MASTER_SWORD], bundle)

    if enemy == Enemies.GOHMA:
        return has_boss_soul(Items.GOHMAS_SOUL, bundle) & can_jump_slash(bundle) & \
            (can_use_any([Items.NUTS, Items.FAIRY_SLINGSHOT, Items.FAIRY_BOW], bundle)
             | hookshot_or_boomerang(bundle))

    if enemy == Enemies.KING_DODONGO:
        return (has_boss_soul(Items.KING_DODONGOS_SOUL, bundle) & can_jump_slash(bundle) &
                (can_use_any([Items.BOMB_BAG, Items.GORONS_BRACELET], bundle) |
                 (can_do_trick(Tricks.DC_DODONGO_CHU, bundle) & is_adult(bundle) & can_use(Items.BOMBCHUS_5, bundle))))

    if enemy == Enemies.BARINADE:
        return (has_boss_soul(Items.BARINADES_SOUL, bundle)
                & can_use(Items.BOOMERANG, bundle) & can_jump_slash_except_hammer(bundle))

    if enemy == Enemies.PHANTOM_GANON:
        return (has_boss_soul(Items.PHANTOM_GANONS_SOUL, bundle) & can_use_sword(bundle)
                & can_use_any([Items.HOOKSHOT, Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT], bundle))

    if enemy == Enemies.VOLVAGIA:
        return has_boss_soul(Items.VOLVAGIAS_SOUL, bundle) & can_use(Items.MEGATON_HAMMER, bundle)

    if enemy == Enemies.MORPHA:
        return (has_boss_soul(Items.MORPHAS_SOUL, bundle) &
                (can_use(Items.HOOKSHOT, bundle) |
                (can_do_trick(Tricks.WATER_MORPHA_WITHOUT_HOOKSHOT, bundle) & has_item(Items.BRONZE_SCALE, bundle))) &
                (can_use_sword(bundle) | can_use(Items.MEGATON_HAMMER, bundle)))

    if enemy == Enemies.BONGO_BONGO:
        return has_boss_soul(Items.BONGO_BONGOS_SOUL, bundle) & \
            (can_use(Items.LENS_OF_TRUTH, bundle) | can_do_trick(Tricks.LENS_BONGO, bundle)) & can_use_sword(bundle) & \
            (can_use_any([Items.HOOKSHOT, Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT], bundle) |
                can_do_trick(Tricks.SHADOW_BONGO, bundle))

    if enemy == Enemies.TWINROVA:
        return has_boss_soul(Items.TWINROVAS_SOUL, bundle) & can_use(Items.MIRROR_SHIELD, bundle) & \
            (can_use_sword(bundle) | can_use(Items.MEGATON_HAMMER, bundle))

    if enemy == Enemies.GANONDORF:
        # RANDOTODO: Trick to use hammer (no jumpslash) or stick (only jumpslash) instead of a sword to reflect the
        # energy ball and either of them regardless of jumpslashing to damage and kill ganondorf

        # Bottle is not taken into account since a sword, hammer or stick are required
        # for killing ganondorf and all of those can reflect the energy ball
        # This will not be the case once ammo logic in taken into account as
        # sticks are limited and using a bottle might become a requirement in that case
        return has_boss_soul(Items.GANONS_SOUL, bundle) & can_use(Items.LIGHT_ARROW, bundle) & can_use_sword(bundle)

    if enemy == Enemies.GANON:
        return has_boss_soul(Items.GANONS_SOUL, bundle) & can_use(Items.MASTER_SWORD, bundle)

    if enemy == Enemies.DARK_LINK:
        # RANDOTODO Dark link is buggy right now, retest when he is not
        return can_jump_slash(bundle) | can_use(Items.FAIRY_BOW, bundle)

    if enemy == Enemies.ANUBIS:
        # there's a restoration that allows beating them with mirror shield + some way to trigger their attack
        return has_fire_source(bundle)

    if enemy == Enemies.BEAMOS:
        return has_explosives(bundle)

    if enemy == Enemies.PURPLE_LEEVER:
        # dies on its own, so this is the conditions to spawn it (killing 10 normal leevers)
        # Sticks and Ice arrows work but will need ammo capacity logic
        # other methods can damage them but not kill them, and they run when hit, making them impractical
        return can_use_any([Items.MASTER_SWORD, Items.BIGGORONS_SWORD], bundle)

    if enemy == Enemies.TENTACLE:
        return can_use(Items.BOOMERANG, bundle)

    if enemy == Enemies.BARI:
        return (hookshot_or_boomerang(bundle)
                | can_use_any([Items.FAIRY_BOW, Items.STICKS, Items.MEGATON_HAMMER, Items.DINS_FIRE], bundle)
                | has_explosives(bundle)
                | (take_damage(bundle) & can_use_sword(bundle)))

    if enemy == Enemies.SHABOM:
        # RANDOTODO when you add better damage logic, you can kill this by taking hits
        return (can_use_any([Items.BOOMERANG, Items.NUTS, Items.DINS_FIRE, Items.ICE_ARROW], bundle)
                | can_jump_slash(bundle))

    if enemy == Enemies.OCTOROK:
        rule = can_reflect_nuts(bundle) | hookshot_or_boomerang(bundle) | can_use_any([Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT, Items.BOMB_BAG], bundle)
        if wall_or_floor:
            rule |= can_use(Items.BOMBCHUS_5, bundle)
        return rule
    return False_()


def has_boss_soul(soul: Items, bundle: tuple[Regions, "SohWorld"]):
    # only check for possesion of gannons soul if the option 'on_plus_ganons' is selected
    if soul == Items.GANONS_SOUL:
        return OptionFilter(ShuffleBossSouls, [ShuffleBossSouls.option_off,ShuffleBossSouls.option_on], operator="in") | has_item(soul, bundle)
        
    return OptionFilter(ShuffleBossSouls, ShuffleBossSouls.option_off) | has_item(soul, bundle)


def can_pass_enemy(bundle: tuple[Regions, "SohWorld"], enemy: Enemies,
                   distance: EnemyDistance = EnemyDistance.CLOSE, wall_or_floor: bool = True) -> Rule:
    if enemy in {Enemies.GOLD_SKULLTULA, Enemies.GOHMA_LARVA, Enemies.LIZALFOS, Enemies.DODONGO, Enemies.MAD_SCRUB,
                 Enemies.KEESE, Enemies.FIRE_KEESE, Enemies.BLUE_BUBBLE, Enemies.DEAD_HAND, Enemies.DEKU_BABA,
                 Enemies.WITHERED_DEKU_BABA, Enemies.STALFOS, Enemies.FLARE_DANCER, Enemies.WOLFOS,
                 Enemies.WHITE_WOLFOS, Enemies.FLOORMASTER, Enemies.MEG, Enemies.ARMOS, Enemies.FREEZARD, Enemies.SPIKE,
                 Enemies.DARK_LINK, Enemies.ANUBIS, Enemies.WALLMASTER, Enemies.PURPLE_LEEVER, Enemies.OCTOROK}:
        return True_()

    if enemy == Enemies.GERUDO_GUARD:
        return (can_do_trick(Tricks.PASS_GUARDS_WITH_NOTHING, bundle)
                | has_item(Items.GERUDO_MEMBERSHIP_CARD, bundle)
                | can_use_any([Items.FAIRY_BOW, Items.HOOKSHOT], bundle))

    if enemy == Enemies.BREAK_ROOM_GUARD:
        return (has_item(Items.GERUDO_MEMBERSHIP_CARD, bundle)
                | can_use_any([Items.FAIRY_BOW, Items.HOOKSHOT], bundle))

    if enemy == Enemies.BIG_SKULLTULA:
        return (can_kill_enemy(bundle, enemy, distance, wall_or_floor)
                | can_use_any([Items.NUTS, Items.BOOMERANG], bundle))

    if enemy == Enemies.LIKE_LIKE:
        return (can_kill_enemy(bundle, enemy, distance, wall_or_floor)
                | can_use_any([Items.HOOKSHOT, Items.BOOMERANG], bundle))

    if enemy in [Enemies.GIBDO, Enemies.REDEAD]:
        return (can_kill_enemy(bundle, enemy, distance, wall_or_floor)
                | can_use_any([Items.HOOKSHOT, Items.SUNS_SONG], bundle))

    if enemy in [Enemies.IRON_KNUCKLE, Enemies.BIG_OCTO]:
        return can_kill_enemy(bundle, enemy, distance, wall_or_floor)

    if enemy == Enemies.GREEN_BUBBLE:
        return (can_kill_enemy(bundle, enemy, distance, wall_or_floor)
                | take_damage(bundle)
                | can_use_any([Items.NUTS, Items.BOOMERANG, Items.HOOKSHOT], bundle))

    return can_kill_enemy(bundle, enemy, distance, wall_or_floor)


def can_cut_shrubs(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    """Check if Link can cut shrubs (grass, bushes)."""
    return (can_use_sword(bundle) |
            has_explosives(bundle) |
            can_use_any([Items.BOOMERANG, Items.GORONS_BRACELET, Items.MEGATON_HAMMER], bundle))


def hookshot_or_boomerang(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    """Check if Link has hookshot or boomerang."""
    return can_use_any([Items.HOOKSHOT, Items.BOOMERANG], bundle)


def can_open_underwater_chest(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return (can_do_trick(Tricks.OPEN_UNDERWATER_CHEST, bundle) &
            can_use(Items.IRON_BOOTS, bundle) &
            can_use(Items.HOOKSHOT, bundle))


def can_open_overworld_door(key: Items, bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return OptionFilter(LockOverworldDoors, False) | has_item(Items.SKELETON_KEY, bundle) | has_item(key, bundle)


key_to_ring: dict[Items, Items] = {
    Items.FOREST_TEMPLE_SMALL_KEY: Items.FOREST_TEMPLE_KEY_RING,
    Items.FIRE_TEMPLE_SMALL_KEY: Items.FIRE_TEMPLE_KEY_RING,
    Items.WATER_TEMPLE_SMALL_KEY: Items.WATER_TEMPLE_KEY_RING,
    Items.BOTTOM_OF_THE_WELL_SMALL_KEY: Items.BOTTOM_OF_THE_WELL_KEY_RING,
    Items.SHADOW_TEMPLE_SMALL_KEY: Items.SHADOW_TEMPLE_KEY_RING,
    Items.GERUDO_FORTRESS_SMALL_KEY: Items.GERUDO_FORTRESS_KEY_RING,
    Items.TRAINING_GROUND_SMALL_KEY: Items.TRAINING_GROUND_KEY_RING,
    Items.SPIRIT_TEMPLE_SMALL_KEY: Items.SPIRIT_TEMPLE_KEY_RING,
    Items.GANONS_CASTLE_SMALL_KEY: Items.GANONS_CASTLE_KEY_RING,
}


def small_keys(key: Items, requiredAmount: int, bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return HasAny(Items.SKELETON_KEY, key_to_ring[key]) | Has(key, requiredAmount)


def can_get_enemy_drop(bundle: tuple[Regions, "SohWorld"], enemy: Enemies,
                       distance: EnemyDistance = EnemyDistance.CLOSE, aboveLink: bool = False) -> Rule:
    rule: Rule = can_kill_enemy(bundle, enemy, distance)
    if distance.value <= EnemyDistance.MASTER_SWORD_JUMPSLASH.value:
        return rule
    match enemy:
        case Enemies.GOLD_SKULLTULA:
            gs_rule: Rule = False_()
            if distance <= EnemyDistance.BOOMERANG:
                gs_rule |= can_use(Items.BOOMERANG, bundle)
            if distance <= EnemyDistance.HOOKSHOT:
                gs_rule |= can_use(Items.HOOKSHOT, bundle)
            if distance <= EnemyDistance.LONGSHOT:
                gs_rule |= can_use(Items.LONGSHOT, bundle)
            return rule & gs_rule
        case Enemies.KEESE:
            return rule
        case Enemies.FIRE_KEESE:
            return rule
        case _:
            if aboveLink:
                return rule
            default_rule: Rule = False_()
            if distance <= EnemyDistance.BOOMERANG:
                default_rule |= can_use(Items.BOOMERANG, bundle)
            if distance <= EnemyDistance.HOOKSHOT:
                default_rule |= can_use(Items.HOOKSHOT, bundle)
            if distance <= EnemyDistance.LONGSHOT:
                default_rule |= can_use(Items.LONGSHOT, bundle)
            return rule & default_rule
    return False_()

def can_detonate_bomb_flowers(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return can_use_any([Items.FAIRY_BOW, Items.DINS_FIRE], bundle) | has_explosives(bundle)


def can_detonate_upright_bomb_flower(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return (can_detonate_bomb_flowers(bundle)
            | has_item(Items.GORONS_BRACELET, bundle)
            | (can_do_trick(Tricks.BLUE_FIRE_MUD_WALLS, bundle)
                & blue_fire(bundle)
                & (effective_health_at_least(bundle, 1)
                     | can_use(Items.NAYRUS_LOVE, bundle))))

  
def get_group_name(item_group: GroupTag) -> str:
    return item_group.name.replace('_', " ")


def item_group_count_enough(item_group: str, count: int):
    return HasGroupUnique(item_group, count)


def has_enough_ocarina_buttons(bundle: tuple[Regions, "SohWorld"], amount: int) -> Rule:
    group_name = get_group_name(GroupTag.Ocarina_Button)
    return OptionFilter(ShuffleOcarinaButtons, False) | HasGroup(group_name, amount)


def has_enough_stones(bundle: tuple[Regions, "SohWorld"], amount: int) -> Rule:
    group_name = get_group_name(GroupTag.Spiritual_Stone)
    return HasGroupUnique(group_name, amount)


def has_enough_medallions(amount: int) -> Rule:
    group_name = get_group_name(GroupTag.Medallion)
    return HasGroupUnique(group_name, amount)


dungeon_events: list[Events] = [Events.DEKU_TREE_COMPLETED, Events.DODONGOS_CAVERN_COMPLETED,
                                Events.JABU_JABUS_BELLY_COMPLETED, Events.FOREST_TEMPLE_COMPLETED,
                                Events.FIRE_TEMPLE_COMPLETED, Events.WATER_TEMPLE_COMPLETED,
                                Events.SPIRIT_TEMPLE_COMPLETED, Events.SHADOW_TEMPLE_COMPLETED]


def cleared_enough_dungeons(amount: int):
    return HasFromList(*dungeon_events, count=amount)


def can_spawn_soil_skull(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return is_child(bundle) & can_use(Items.BOTTLE_WITH_BUGS, bundle)


def fire_timer_at_least(bundle: tuple[Regions, "SohWorld"], amount: int) -> Rule:
    return can_use(Items.GORON_TUNIC, bundle) | (HeartsAtLeast(amount=int(math.ceil(amount/8))) & can_do_trick(Tricks.FEWER_TUNIC_REQUIREMENTS, bundle))


def water_timer_at_least(bundle: tuple[Regions, "SohWorld"], amount: int) -> Rule:
    return can_use(Items.ZORA_TUNIC, bundle) | (HeartsAtLeast(amount=int(math.ceil(amount/8))) & can_do_trick(Tricks.FEWER_TUNIC_REQUIREMENTS, bundle))


@dataclasses.dataclass
class HeartsAtLeast(Rule, game="Ship of Harkinian"):
    amount: int
    def _instantiate(self, world: World) -> Rule.Resolved:
        return self.Resolved(player=world.player, amount = self.amount, caching_enabled=getattr(world, "rule_caching_enabled", False))
    class Resolved(Rule.Resolved):
        player: int
        amount: int
        def _evaluate(self, state: CollectionState) -> bool:
            return state.soh_heart_count[self.player] >= self.amount # type: ignore
        
        def item_dependencies(self) -> dict[str, set[int]]:
            return {str(item_id): {id(self)} for item_id in (Items.HEART_CONTAINER, Items.PIECE_OF_HEART, Items.PIECE_OF_HEART_WINNER)}
        
        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            verb = "Does not have " if state and not self(state) else "Has "
            messages: list[JSONMessagePart] = [{"type": "text", "text": verb}]
            if state:
                color = "green" if self(state) else "salmon"
                messages.append({"type": "color", "color": "cyan", "text": str(self.amount)})

                if self.amount > 1:
                    messages.append({"type": "color", "color": color, "text": " hearts "})
                else:
                    messages.append({"type": "color", "color": color, "text": " heart "})

                messages.append({"type": "text", "text": f"or more"})
            return messages
        
        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            prefix = "Has" if self(state) else "Does not have"
            return f"{prefix} {self.amount} or more"

        @override
        def __str__(self) -> str:
            return f"Has {self.amount} hearts or more"

def hearts_at_least(bundle: tuple[Regions, "SohWorld"], amount) -> Rule:
    return HeartsAtLeast(amount=amount)


def can_open_bomb_grotto(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return blast_or_smash(bundle) & (has_item(Items.STONE_OF_AGONY, bundle) | can_do_trick(Tricks.GROTTOS_WITHOUT_AGONY, bundle))


def trade_quest_step(item: Items, bundle: tuple[Regions, "SohWorld"]) -> Rule:
    # If adult trade shuffle is off, it'll automatically assume the whole trade quest is complete as soon as claim check is obtained.

    rule: Rule = False_()
    # Since the original used fallthrough, we will loop through all trade quest items after this point too
    trade_items = [Items.POCKET_EGG, Items.COJIRO, Items.ODD_MUSHROOM, Items.ODD_POTION, Items.POACHERS_SAW, Items.BROKEN_GORONS_SWORD, Items.PRESCRIPTION, Items.WORLDS_FINEST_EYEDROPS, Items.CLAIM_CHECK]
    if item not in trade_items:
        return rule
    pos = trade_items.index(item)
    for i in range(pos, len(trade_items)):
        rule |= has_item(trade_items[i], bundle)
    return Filtered(has_item(Items.CLAIM_CHECK, bundle), options=[OptionFilter(ShuffleAdultTradeItems, False)]) \
        | Filtered(rule, options=[OptionFilter(ShuffleAdultTradeItems, True)])

@dataclasses.dataclass
class ItemsPlusGregEnough(Rule, game="Ship of Harkinian"):
    target: FieldResolver
    item_tag: GroupTag | list[Events]   # todo figure out a way to change dungeon events to a tag as well
    greg: FieldResolver
    def _instantiate(self, world: World) -> Rule.Resolved:
        world = cast("SohWorld", world)
        items = list()
        if isinstance(self.item_tag, list):
            items.extend(self.item_tag)
        else:
            for tag in self.item_tag:
                items.extend(world.item_name_groups[get_group_name(tag)])
        if self.greg.resolve(world) == 1: #reward, for both classes
            items.append(Items.GREG_THE_GREEN_RUPEE)
        return HasFromList(*items, count=self.target).resolve(world)

def can_build_rainbow_bridge(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    greg = FromOption(RainbowBridgeGregModifier)
    return OptionFilter(RainbowBridge, RainbowBridge.option_always_open) \
         | (OptionFilter(RainbowBridge, RainbowBridge.option_vanilla) & has_item(Items.SHADOW_MEDALLION, bundle) & has_item(Items.SPIRIT_MEDALLION, bundle) & can_use(Items.LIGHT_ARROW, bundle)) \
         | (OptionFilter(RainbowBridge, RainbowBridge.option_stones) & ItemsPlusGregEnough(target=FromOption(RainbowBridgeStonesRequired), item_tag=GroupTag.Spiritual_Stone, greg=greg)) \
         | (OptionFilter(RainbowBridge, RainbowBridge.option_medallions) & ItemsPlusGregEnough(target=FromOption(RainbowBridgeMedallionsRequired), item_tag=GroupTag.Medallion, greg=greg)) \
         | (OptionFilter(RainbowBridge, RainbowBridge.option_dungeon_rewards) & ItemsPlusGregEnough(target=FromOption(RainbowBridgeDungeonRewardsRequired), item_tag=GroupTag.Spiritual_Stone | GroupTag.Medallion, greg=greg)) \
         | (OptionFilter(RainbowBridge, RainbowBridge.option_dungeons) & ItemsPlusGregEnough(target=FromOption(RainbowBridgeDungeonsRequired), item_tag=dungeon_events, greg=greg)) \
         | (OptionFilter(RainbowBridge, RainbowBridge.option_tokens) & Has(Items.GOLD_SKULLTULA_TOKEN, count=FromOption(RainbowBridgeSkullTokensRequired))) \
         | (OptionFilter(RainbowBridge, RainbowBridge.option_greg) & Has(Items.GREG_THE_GREEN_RUPEE))


def can_trigger_lacs(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    greg = FromOption(GanonsCastleBossKeyGregModifier)
    return (OptionFilter(GanonsCastleBossKey, [GanonsCastleBossKey.option_vanilla, GanonsCastleBossKey.option_anywhere, GanonsCastleBossKey.option_lacs_vanilla], operator="in") & has_item(Items.SHADOW_MEDALLION, bundle) & has_item(Items.SPIRIT_MEDALLION, bundle)) \
         | (OptionFilter(GanonsCastleBossKey, GanonsCastleBossKey.option_lacs_stones) & ItemsPlusGregEnough(target=FromOption(GanonsCastleBossKeyStonesRequired), item_tag=GroupTag.Spiritual_Stone, greg=greg))\
         | (OptionFilter(GanonsCastleBossKey, GanonsCastleBossKey.option_lacs_medallions) & ItemsPlusGregEnough(target=FromOption(GanonsCastleBossKeyMedallionsRequired), item_tag=GroupTag.Medallion, greg=greg)) \
         | (OptionFilter(GanonsCastleBossKey, GanonsCastleBossKey.option_lacs_dungeon_rewards) & ItemsPlusGregEnough(target=FromOption(GanonsCastleBossKeyDungeonRewardsRequired), item_tag=GroupTag.Spiritual_Stone | GroupTag.Medallion, greg=greg)) \
         | (OptionFilter(GanonsCastleBossKey, GanonsCastleBossKey.option_lacs_dungeons) & ItemsPlusGregEnough(target=FromOption(GanonsCastleBossKeyDungeonsRequired), item_tag=dungeon_events, greg=greg)) \
         | (OptionFilter(GanonsCastleBossKey, GanonsCastleBossKey.option_lacs_skull_tokens) & Has(Items.GOLD_SKULLTULA_TOKEN, count=FromOption(GanonsCastleBossKeySkullTokensRequired)))



# TODO implement EffectiveHealth(); Returns 2 for now. Requires implementing a damage multiplier option
def effective_health_at_least(bundle: tuple[Regions, "SohWorld"], count: int) -> Rule:
    if count <= 2:
        return True_()
    else:
        return False_()


def is_fire_loop_unlocked(bundle: tuple[Regions, "SohWorld"]) -> Rule:
    return True_(options=[OptionFilter(SmallKeyShuffle, [SmallKeyShuffle.option_anywhere, SmallKeyShuffle.option_overworld, SmallKeyShuffle.option_any_dungeon], operator="in")])


def can_ground_jump(bundle: tuple[Regions, "SohWorld"], hasBombFlower: bool = False) -> Rule:
    if hasBombFlower:
        return (can_do_trick(Tricks.GROUND_JUMP, bundle)
                & can_standing_shield(bundle)
                & (can_use(Items.BOMB_BAG, bundle) | has_item(Items.GORONS_BRACELET, bundle)))
    else:
        return (can_do_trick(Tricks.GROUND_JUMP, bundle)
                & can_standing_shield(bundle)
                & can_use(Items.BOMB_BAG, bundle))

def can_clear_stalagmite(bundle: tuple[Regions, "SohWorld"]):
    return can_jump_slash(bundle) | has_explosives(bundle)


@dataclasses.dataclass
class CanWinTriforceHunt(Rule, game="Ship of Harkinian"):
    def _instantiate(self, world: "SohWorld") -> Rule.Resolved: # type: ignore
        return self.Resolved(player = world.player, caching_enabled=getattr(world, "rule_caching_enabled", False))

    class Resolved(Rule.Resolved):
        item_name: str = str(Items.TRIFORCE_PIECE)
        player: int
        def _evaluate(self, state: CollectionState) -> bool:
            return state.prog_items[self.player][self.item_name] >= cast("SohWorld", state.multiworld.worlds[self.player]).triforce_pieces_required

        def item_dependencies(self) -> dict[str, set[int]]:
            return {self.item_name: {id(self)}}
        
        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            amount = cast("SohWorld", state.multiworld.worlds[self.player]).triforce_pieces_required
            verb = "Does not have " if state and not self(state) else "Has "
            messages: list[JSONMessagePart] = [{"type": "text", "text": verb}]
            if state:
                color = "green" if self(state) else "salmon"
                messages.append({"type": "color", "color": "cyan", "text": str(amount)})

                if amount > 1:
                    messages.append({"type": "color", "color": color, "text": " Triforce Pieces "})
                else:
                    messages.append({"type": "color", "color": color, "text": " Triforce Piece "})

                messages.append({"type": "text", "text": f"or more"})
            return messages
        
        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            prefix = "Has" if self(state) else "Does not have"
            return f"{prefix} {str(cast("SohWorld", state.multiworld.worlds[self.player]).triforce_pieces_required)} Triforce Pieces or more"

        @override
        def __str__(self) -> str:
            return f"Has enough Triforce Pieces to win"


class SohHeartState(LogicMixin):
    # tracking how many hearts the player has instead of checking the collection state every time
    soh_piece_of_heart_count: Counter[int]
    soh_heart_count: Counter[int]

    def init_mixin(self, parent: MultiWorld):
        soh_players = list(parent.get_game_players(
            "Ship of Harkinian") + parent.get_game_groups("Ship of Harkinian"))
        self.soh_piece_of_heart_count = Counter()
        self.soh_heart_count = Counter({player: cast("SohWorld", parent.worlds[player]).options.starting_hearts.value for player in soh_players})

    def copy_mixin(self, ret: CollectionState) -> CollectionState:
        ret.soh_piece_of_heart_count = Counter(self.soh_piece_of_heart_count)  # type: ignore # noqa
        ret.soh_heart_count = Counter(self.soh_heart_count)  # type: ignore # noqa
        return ret
