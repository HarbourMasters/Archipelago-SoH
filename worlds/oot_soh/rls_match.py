"""Runtime support for RLS `match` expressions in the Archipelago (RuleBuilder) target.

A `match` lowers to one of two helpers, chosen at transpile time by the value class of its
arm bodies (see docs/AP-Function-Generation.md):

  * `rls_match_value` -- arms produce build-time Python values (e.g. distance_to_int's
    integers). Returns the first matching arm's value, or `default` if none match.

  * `rls_match_rule` -- arms produce RuleBuilder rules. A rule is not a Python bool
    (`bool(rule)` raises), so rule arms cannot be combined with Python `or`; matched arms
    are `|`-combined instead. `or`-fallthrough in the source means a matched arm also pulls
    in the arms it falls through into, so the combined rule accumulates down the chain.

Each arm is passed as a flat (condition, body, fallthrough) triple: `condition()` is a
zero-arg predicate over the (build-time) discriminant, `body()` yields the arm's value or
rule, and `fallthrough` is True when the source arm ended with a trailing `or`.
"""
from typing import Any

from rule_builder.rules import False_


def rls_match_value(default: Any, *arms: Any) -> Any:
	"""Return the first matching arm's value, or `default` if no arm matches."""
	for i in range(0, len(arms), 3):
		condition, body = arms[i], arms[i + 1]
		if condition():
			return body()
	return default


def rls_match_rule(*arms: Any) -> Any:
	"""`|`-combine the matched arm with the arms it falls through into.

	Returns `False_()` (an always-closed rule) when no arm matches.
	"""
	result = None
	matched = False
	for i in range(0, len(arms), 3):
		condition, body, fallthrough = arms[i], arms[i + 1], arms[i + 2]
		if not matched and condition():
			matched = True
		if matched:
			result = body() if result is None else result | body()
			if not fallthrough:
				break
	return result if result is not None else False_()
