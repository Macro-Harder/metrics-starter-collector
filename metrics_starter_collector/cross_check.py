"""Module 4: cross check, part of the derivation core.

Slice 1 standing, stated plainly: the tracer slice names no cross
check content. Its delivery list carries no comparison with the
metrics record, and its non delivery list names no cross check as
part of the slice. This module therefore stands at a minimal form
in Slice 1: it performs no comparison, records no disagreement and
marks no row. The family slices build the comparison for the rows
each of them certifies, inside their own slices, on the footing
this module states here and in no other place: a comparison reads
the one assembled metrics record and the feeder result it is
checked against, it never overrides a feeder result, and a
disagreement it finds stands recorded inside the row it touches,
in that row statement line, with the disagreeing record named and
the fact or figure each side supports.

The names below stand as placeholders at that minimal form, so the
module seam the core addresses by metric family stands in place
from the first slice. Each returns the empty marking: no statement
for a single row name, and no statements for a family name. No
derivation in Slice 1 calls them, and no marking of any row in
Slice 1 comes from this module.
"""


def staffing_cross_check_statements(captured, universe, covered,
                                    totals, f2_counted):
    """Return no statements: Slice 1 carries no staffing marking."""
    return {}


def q4_cross_check_statement(captured, covered):
    """Return no statement: Slice 1 carries no Q-4 marking."""
    return None


def q3_contested_statement(captured, universe, origin_steps):
    """Return no statement: Slice 1 carries no Q-3 marking."""
    return None


def d1_cross_check_statement(feeder_result, table_items,
                             feeder_items=None, metrics_name=None):
    """Return no statement: Slice 1 carries no D-1 marking."""
    return None


def cost_cross_check_statements(captured, e3_tokens, e4_money,
                                b2_money_spent, b2_token_spent):
    """Return no statements: Slice 1 carries no cost marking."""
    return {}


def t4_cross_check_statement(feeder_durations, metrics_text,
                             metrics_name=None):
    """Return no statement: Slice 1 carries no T-4 marking."""
    return None
