from rule_builder.rules import *
from .Enums import *
from .Items import no_rules_bottles, all_bottles, item_data_table, ItemType

if TYPE_CHECKING:
    from . import SohWorld


@dataclasses.dataclass()
class soh_rule(Rule["SohWorld"], game=SohWorld.game):
    @override
    def _instantiate(self, world: "SohWorld") -> Rule.Resolved:
        return self.Resolved(
                world=world,
                caching_enabled=getattr(world, "rule_caching_enabled", False),
            )
    
    class Resolved(Rule.Resolved):
        world: "SohWorld"

        @override
        def _evaluate(self, state):
            return True


@dataclasses.dataclass()
class can_use_rule(soh_rule["SohWorld"], game=SohWorld.game):
    item: Items
    
    @override
    def _instantiate(self, world: "SohWorld") -> Rule.Resolved:
        return self.Resolved(
                self.item,
                world=world,
                caching_enabled=getattr(world, "rule_caching_enabled", False),
            )

    class Resolved(soh_rule.Resolved):
        item: Items

        @override
        def _evaluate(self, state):
                if not has_item_rule(self.item).resolve(self.world):
                    return False

                data = item_data_table

                if self.item in data:
                    if data[self.item].adult_only and not is_adult(bundle):
                        return False

                    if data[self.item].child_only and not is_child(bundle):
                        return False

                    if data[self.item].item_type == ItemType.magic and not has_item_rule(Items.PROGRESSIVE_MAGIC_METER).resolve(self.world):
                        return False

                    if data[self.item].item_type == ItemType.song:
                        return can_play_song(item, bundle)

                if self.item in (Items.FIRE_ARROW, Items.ICE_ARROW, Items.LIGHT_ARROW):
                    return can_use_rule(Items.FAIRY_BOW).resolve(self.world)

                if self.item in (Items.BOMBCHU_BAG, Items.BOMBCHUS_5, Items.BOMBCHUS_10, Items.BOMBCHUS_20):
                    return bombchu_refill_rule().resolve(self.world)

                if self.item == Items.FISHING_POLE:
                    return has_item_rule(Items.CHILD_WALLET).resolve(self.world)

                if self.item == Items.EPONA:
                    return is_adult(bundle) and can_use_rule(Items.EPONAS_SONG).resolve(self.world)

                return True
        
        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            # TODO Some of this is duplicate across has_item_rule. Fix it
            item_groupings = [
                (Items.BOMBCHU_BAG, Items.BOMBCHUS_5, Items.BOMBCHUS_10, Items.BOMBCHUS_20),
                (Items.POCKET_EGG, Items.COJIRO, Items.ODD_MUSHROOM, Items.ODD_POTION, Items.POACHERS_SAW, Items.BROKEN_GORONS_SWORD, Items.PRESCRIPTION, Items.EYEBALL_FROG, Items.WORLDS_FINEST_EYEDROPS)
                (Items.BOTTLE_WITH_MILK, Items.BOTTLE_WITH_POE, Items.BOTTLE_WITH_RED_POTION, Items.EMPTY_BOTTLE),
                (Items.FIRE_ARROW, Items.ICE_ARROW, Items.LIGHT_ARROW)
            ]

            for item_group in item_groupings:
                if self.item in item_group:
                    return {item: {id(self)} for item in item_group}
        
            return {self.item: set()}


@dataclasses.dataclass()
class has_item_rule(Has["SohWorld"], game=SohWorld.game):
    class Resolved(Has.Resolved):
        #override skip cache
        def __init__(self):
            super().skip_cache = False

        @override
        def _evaluate(self, state) -> bool:
            world = state.multiworld.worlds[self.player]

            if super().item_name == Items.STICKS:
                return state.has_all((Events.CAN_FARM_STICKS, Items.DEKU_STICK_BAG), self.player)

            if super().item_name in (Items.BOMBCHU_BAG, Items.BOMBCHUS_5, Items.BOMBCHUS_10, Items.BOMBCHUS_20):
                return bombchus_enabled_rule.resolve(world)._evaluate()

            if super().item_name == Items.NUTS:
                return state.has_all((Events.CAN_FARM_NUTS, Items.DEKU_NUT_BAG), self.player)

            if super().item_name == Items.MAGIC_BEAN:
                return state.has_any({Items.MAGIC_BEAN_PACK, Events.CAN_BUY_BEANS}, self.player)

            if super().item_name == Items.DEKU_SHIELD:
                return state.has(Items.BUY_DEKU_SHIELD, self.player)

            if super().item_name == Items.HYLIAN_SHIELD:
                return state.has(Items.BUY_HYLIAN_SHIELD, self.player)

            if super().item_name == Items.GORON_TUNIC:
                return state.has_any({Items.BUY_GORON_TUNIC, Items.GORON_TUNIC}, self.player)

            if super().item_name == Items.ZORA_TUNIC:
                return state.has_any({Items.BUY_ZORA_TUNIC, Items.ZORA_TUNIC}, self.player)

            if super().item_name == Items.SCARECROW:
                return scarecrows_song_rule.resolve(world) and can_use_rule(Items.HOOKSHOT).resolve(world)

            if super().item_name == Items.DISTANT_SCARECROW:
                return scarecrows_song_rule.resolve(world) and can_use_rule(Items.LONGSHOT).resolve(world)

            if super().item_name == Items.FISHING_POLE:
                return (not world.options.shuffle_fishing_pole) or state.has(Items.FISHING_POLE, self.player)

            if super().item_name == Items.EPONA:
                return state.has(Events.FREED_EPONA, self.player)

            if super().item_name in {Items.POCKET_EGG, Items.COJIRO, Items.ODD_MUSHROOM, Items.ODD_POTION, Items.POACHERS_SAW,
                        Items.BROKEN_GORONS_SWORD, Items.PRESCRIPTION, Items.EYEBALL_FROG, Items.WORLDS_FINEST_EYEDROPS}:
                return not world.options.shuffle_adult_trade_items or state.has(super().item_name, self.player)

            if super().item_name == Items.BOTTLE_WITH_BLUE_FIRE:
                return has_bottle_rule().resolve(world) and (state.has(Events.CAN_ACCESS_BLUE_FIRE, self.player) or state.has(Items.BUY_BLUE_FIRE, self.player))

            if super().item_name == Items.BOTTLE_WITH_BLUE_POTION:
                return has_bottle_rule().resolve(world) and state.has(Items.BUY_BLUE_POTION, self.player)

            if super().item_name == Items.BOTTLE_WITH_BUGS:
                return has_bottle_rule().resolve(world) and (state.has(Events.CAN_ACCESS_BUGS, self.player) or state.has(Items.BUY_BOTTLE_BUG, self.player))

            if super().item_name == Items.BOTTLE_WITH_FAIRY:
                return has_bottle_rule().resolve(world) and (state.has(Events.CAN_ACCESS_FAIRIES, self.player) or state.has(Items.BUY_FAIRYS_SPIRIT, self.player))

            if super().item_name == Items.BOTTLE_WITH_FISH:
                return has_bottle_rule().resolve(world) and (state.has(Events.CAN_ACCESS_FISH, self.player) or state.has(Items.BUY_FISH, self.player))

            if super().item_name == Items.BOTTLE_WITH_GREEN_POTION:
                return has_bottle_rule().resolve(world) and state.has(Items.BUY_GREEN_POTION, self.player)

            if super().item_name in (Items.BOTTLE_WITH_MILK, Items.BOTTLE_WITH_POE, Items.BOTTLE_WITH_RED_POTION, Items.EMPTY_BOTTLE):
                return has_bottle_rule().resolve(world)

            return state.has(super().item_name, self.player, self.count)
        
        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            item_groupings = [
                (Items.BOMBCHU_BAG, Items.BOMBCHUS_5, Items.BOMBCHUS_10, Items.BOMBCHUS_20),
                (Items.POCKET_EGG, Items.COJIRO, Items.ODD_MUSHROOM, Items.ODD_POTION, Items.POACHERS_SAW, Items.BROKEN_GORONS_SWORD, Items.PRESCRIPTION, Items.EYEBALL_FROG, Items.WORLDS_FINEST_EYEDROPS)
                (Items.BOTTLE_WITH_MILK, Items.BOTTLE_WITH_POE, Items.BOTTLE_WITH_RED_POTION, Items.EMPTY_BOTTLE)
            ]

            for item_group in item_groupings:
                if self.item in item_group:
                    return {item: {id(self)} for item in item_group}
        
            return {self.item: set()}



@dataclasses.dataclass()
class bombchu_refill_rule(soh_rule["SohWorld"], game=SohWorld.game):
    @override
    def _instantiate(self, world: "SohWorld") -> Rule.Resolved:
        return self.Resolved(
                world=world,
                caching_enabled=getattr(world, "rule_caching_enabled", False),
            )

    class Resolved(soh_rule.Resolved):
        @override
        def _evaluate(self, state):
            return state.has_any([Items.BUY_BOMBCHUS10, Items.BUY_BOMBCHUS20, Events.COULD_PLAY_BOWLING, Events.CARPET_MERCHANT], self.world.player) or bool(self.world.options.bombchu_drops)
        
        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            if not self.world.options.bombchu_drops:
                return {item: {id(self)} for item in (Items.BUY_BOMBCHUS10, Items.BUY_BOMBCHUS20, Events.COULD_PLAY_BOWLING, Events.CARPET_MERCHANT)}
            return None
        

@dataclasses.dataclass()
class bombchus_enabled_rule(soh_rule["SohWorld"], game=SohWorld.game):
    class Resolved(soh_rule.Resolved):
        @override
        def _evaluate(self, state):
            if self.world.options.bombchu_bag:
                return state.has(Items.BOMBCHU_BAG, self.world.player)
            return state.has(Items.BOMB_BAG, self.world.player)
        
        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            if self.world.options.bombchu_bag:
                return {Items.BOMBCHU_BAG: set()}
            return {Items.BOMB_BAG: set()}
        

@dataclasses.dataclass()
class scarecrows_song_rule(soh_rule["SohWorld"], game=SohWorld.game):
    class Resolved(soh_rule.Resolved):
        @override
        def _evaluate(self, state):
            return (
                (bool(self.world.options.skip_scarecrows_song) and has_item_rule(Items.FAIRY_OCARINA).resolve(self.world) and (ocarina_button_count(state, self.world) >= 2))
                or (has_item_rule(Events.CHILD_SCARECROW_UNLOCKED).resolve(self.world) and has_item_rule(Events.ADULT_SCARECROW_UNLOCKED).resolve(self.world))
            )
        
        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {item: {id(self)} for item in 
                (
                    Items.FAIRY_OCARINA,
                    Events.CHILD_SCARECROW_UNLOCKED,
                    Events.ADULT_SCARECROW_UNLOCKED,
                    Items.OCARINA_A_BUTTON,
                    Items.OCARINA_CDOWN_BUTTON,
                    Items.OCARINA_CLEFT_BUTTON,
                    Items.OCARINA_CRIGHT_BUTTON,
                    Items.OCARINA_CUP_BUTTON
                )
            }
               

@dataclasses.dataclass()
class can_play_song_rule(soh_rule["SohWorld"], game=SohWorld.game):
    song: Items

    @override
    def _instantiate(self, world: "SohWorld") -> Rule.Resolved:
        return self.Resolved(
                self.song,
                world=world,
                caching_enabled=getattr(world, "rule_caching_enabled", False),
            )

    class Resolved(soh_rule.Resolved):
        song: Items

        @override
        def _evaluate(self, state):
            if not (has_item_rule(Items.FAIRY_OCARINA).resolve(self.world) and has_item_rule(self.song).resolve(self.world)):
                return False
            if not self.world.options.shuffle_ocarina_buttons:
                return True
            else:
                return state.has_all(ocarina_buttons_required[self.song], self.world.player)
        
        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {item: {id(self)} for item in 
                (Items.FAIRY_OCARINA, ocarina_buttons_required.keys(), self.song) 
            }
                
        
@dataclasses.dataclass()
class has_bottle_rule(soh_rule["SohWorld"], game=SohWorld.game):
    @override
    def _instantiate(self, world: "SohWorld") -> Rule.Resolved:
        return has_bottle_count_rule(1).resolve(world)


@dataclasses.dataclass()
class has_bottle_count_rule(soh_rule["SohWorld"], game=SohWorld.game):
    target_count: int = 1

    @override
    def _instantiate(self, world: "SohWorld") -> Rule.Resolved:
        return self.Resolved(
                self.target_count,
                world=world,
                caching_enabled=getattr(world, "rule_caching_enabled", False),
            )

    class Resolved(soh_rule.Resolved):
        target_count: int

        @override
        def _evaluate(self, state):
            count = 0
            for bottle in no_rules_bottles:
                count += state.count(bottle.value, self.world.player)
                if count >= self.target_count:
                    return True
            if state.has(Events.DELIVER_LETTER, self.world.player):
                count += state.count(Items.BOTTLE_WITH_RUTOS_LETTER, self.world.player)
                if count >= self.target_count:
                    return True
            if state.has(Events.CAN_EMPTY_BIG_POES, self.world.player):
                count += state.count(Items.BOTTLE_WITH_BIG_POE, self.world.player)
                if count >= self.target_count:
                    return True
            return False
        
        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {item: {id(self)} for item in all_bottles}
        

# Modified Helpers
def item_group_count(state: CollectionState, world: "SohWorld", item_group: str) -> int:
    return state.count_group_unique(item_group, world.player)


def ocarina_button_count(state: CollectionState, world: "SohWorld") -> int:
    if world.options.shuffle_ocarina_buttons:
        return item_group_count(state, world, "Ocarina Buttons")
    return 5


def stone_count(state: CollectionState, world: "SohWorld") -> int:
    return item_group_count(state, world, "Stones")


def medallion_count(state: CollectionState, world: "SohWorld") -> int:
    return item_group_count(state, world, "Medallions")


def get_gs_count(state: CollectionState, world: "SohWorld") -> int:
    return state.count(Items.GOLD_SKULLTULA_TOKEN, world.player)


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

#TODO might not need
ocarina_buttons: tuple[Items] = (Items.OCARINA_A_BUTTON, Items.OCARINA_CDOWN_BUTTON, Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CUP_BUTTON)