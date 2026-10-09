from collections import deque
from BaseClasses import CollectionState, MultiWorld
from worlds.AutoWorld import LogicMixin
from .LogicHelpers import IsChild, IsAdult
from .Enums import Ages
from .enums_gen import Regions
import copy


class SohAgeLogic(LogicMixin):
    def init_mixin(self, parent: MultiWorld):
        game = "Ship of Harkinian"
        self._soh_stale = {player: True for player in parent.worlds.keys()
                           if parent.worlds[player].game == game}
        players = parent.get_game_groups(game) + parent.get_game_players(game)
        self._soh_child_reachable_regions = {
            player: set() for player in players}
        self._soh_adult_reachable_regions = {
            player: set() for player in players}
        self._soh_child_blocked_regions = {player: set() for player in players}
        self._soh_adult_blocked_regions = {player: set() for player in players}
        self._soh_age = {player: Ages.null for player in players}
        self._soh_widen = {player: None for player in players}
        self._soh_widen_pending = {player: {} for player in players}

    def copy_mixin(self, ret) -> CollectionState:
        ret._soh_stale = {player: stale for player,
                          stale in self._soh_stale.items()}
        ret._soh_child_reachable_regions = {player: copy.copy(
            regions) for player, regions in self._soh_child_reachable_regions.items()}
        ret._soh_adult_reachable_regions = {player: copy.copy(
            regions) for player, regions in self._soh_adult_reachable_regions.items()}
        ret._soh_child_blocked_regions = {player: copy.copy(
            regions) for player, regions in self._soh_child_blocked_regions.items()}
        ret._soh_adult_blocked_regions = {player: copy.copy(
            regions) for player, regions in self._soh_adult_blocked_regions.items()}
        ret._soh_age = {player: age for player, age in self._soh_age.items()}
        ret._soh_widen = {player: widen for player,
                          widen in self._soh_widen.items()}
        ret._soh_widen_pending = {player: {} for player in self._soh_widen_pending}
        return ret

    def _soh_invalidate(self, player):
        self._soh_child_reachable_regions[player] = set()
        self._soh_adult_reachable_regions[player] = set()
        self._soh_child_blocked_regions[player] = set()
        self._soh_adult_blocked_regions[player] = set()
        self._soh_stale[player] = True

    def _soh_update_age_reachable_regions(self, player):
        self._soh_stale[player] = False
        pending = self._soh_widen_pending[player]
        while True:
            pending.clear()
            for age in [Ages.CHILD, Ages.ADULT]:
                self._soh_age[player] = age
                start = self.multiworld.get_region(
                    Regions.RR_ROOT, player)  # type: ignore

                if age == Ages.CHILD:
                    reachable = self._soh_child_reachable_regions[player]
                    blocked = self._soh_child_blocked_regions[player]
                    queue = deque(self._soh_child_blocked_regions[player])
                else:
                    reachable = self._soh_adult_reachable_regions[player]
                    blocked = self._soh_adult_blocked_regions[player]
                    queue = deque(self._soh_adult_blocked_regions[player])

                # init on first call
                if start not in reachable:
                    reachable.add(start)
                    blocked.update(start.exits)
                    queue.extend(start.exits)

                # run breadth first search
                while queue:
                    connection = queue.popleft()
                    new_region = connection.connected_region
                    if new_region is None:
                        continue
                    if new_region in reachable:
                        blocked.remove(connection)
                    elif connection.can_reach(self):
                        reachable.add(new_region)
                        blocked.remove(connection)
                        blocked.update(new_region.exits)
                        queue.extend(new_region.exits)
                        self.path[new_region] = (new_region.name, self.path.get(
                            connection, None))  # type: ignore

            # Continue searching after the first 
            # Needed so an if Adult unlocks something for Child, it is found in this region search instead of a subsequent one
            if all(self._soh_region_ages(region, player) == read for region, read in pending.items()):
                break

    def _soh_region_ages(self, region: Regions, player: int) -> tuple[bool, bool]:
        reg = self.multiworld.get_region(region.value, player)  # type: ignore
        return (reg in self._soh_child_reachable_regions[player],
                reg in self._soh_adult_reachable_regions[player])

    def _soh_can_reach_as_age(self, region: Regions, age: Ages, player: int):
        if self._soh_age[player] == Ages.null:
            # first layer of recursion
            self._soh_age[player] = age
            can_reach = self.multiworld.get_region(
                region.value, player).can_reach(self)  # type: ignore
            self._soh_age[player] = Ages.null
            return can_reach
        return self._soh_age[player] == age
