"""Runtime support for RLS rule-conditioned ternaries in the Archipelago (RuleBuilder) target.

Every ternary whose condition is a collection rule lowers through here, because the RuleBuilder
has neither a Python `if` over a rule (`bool(rule)` raises) nor a rule negation to express the
condition's complement.

Rule branches go straight in:

    C ? a : b              ->   rls_conditional(bundle, C, a, b)

Value branches -- `CanUse(IsAdult ? RG_HOOKSHOT : RG_LONGSHOT)`, `CanKillEnemy(RE_GS, bronze &&
adult ? ED_SHORT_JUMPSLASH : ED_BOOMERANG)` -- are enum values fed into a call, not rules, so the
transpiler first distributes the call over the branches and hands the two resulting rules here:

    f(.., C ? A : B, ..)   ->   rls_conditional(bundle, C, f(..,A,..), f(..,B,..))

`Conditional` evaluates the condition at solve time and returns whichever branch it selects --
the faithful mirror of the C++ ternary. Unlike the `(cond & a) | b` idiom it replaced, it does not
ungate the else-branch. On the age-pinned forward search is_adult/is_child are a mutually
exclusive scalar, so this matches Ship's per-age evaluation of the ternary.

Copy this module into the oot_soh world alongside rls_match.py; the generated functions file
imports `rls_conditional` from it.
"""
from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from typing_extensions import override

from rule_builder.rules import NestedRule, Rule

if TYPE_CHECKING:
    from . import SohWorld
    from .enums_gen import Regions


class Conditional(NestedRule, game="Ship of Harkinian"):
    """Return the second child's result when the first child (the condition) holds at solve
    time, otherwise the third child's. force_recalculate and the unioned item/region/location/
    entrance dependencies come from NestedRule: any condition that forces recalculation (e.g.
    IsAdult/IsChild) propagates, and cache invalidation conservatively covers all three children."""

    class Resolved(NestedRule.Resolved):
        @override
        def _evaluate(self, state: CollectionState) -> bool:
            condition, if_true, if_false = self.children
            return if_true(state) if condition(state) else if_false(state)


def rls_conditional(
    bundle: "tuple[Regions, SohWorld]", condition: Rule, if_true: Rule, if_false: Rule
) -> Rule:
    """Build a Conditional rule. The bundle is accepted for call-shape consistency with the other
    host helpers; the child rules already closed over it when they were built."""
    return Conditional(condition, if_true, if_false)
