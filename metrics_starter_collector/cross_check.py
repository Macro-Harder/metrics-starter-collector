"""Module 4: cross check, part of the derivation core.

Standing form, stated plainly. A comparison reads the one assembled
metrics record and the feeder result it is checked against. It never
overrides a feeder result. A disagreement it finds stands recorded
inside the row it touches, in that row statement line, with the
disagreeing record named and the fact or figure each side supports,
and, where proposal CA-1 applies, both figures and the cause. The
one feeder exception for D-1 lives in the D-1 derivation and in this
module role swap, and in no other derivation: where a queue file in
the named form stands, the queue file is the feeder for D-1 and the
metrics record decision table is the cross check, so the D-1 marking
names the decision table as the disagreeing record and the queue
figure stands.

Slice 4 form. This module builds the marking for the rows Slice 4
certifies, T-1, T-2, T-4, D-1, B-1, B-3 and B-4, under decisions D-18
and proposal CA-1. The functions below are the seam the derivation
core addresses, in the forms the core consumes:

d1_cross_check_statement(feeder_result, table_items,
feeder_items=None, metrics_name=None) returns one statement text
or None. feeder_result is the governing feeder item set for D-1,
the queue items where a queue file stands and the decision table
items where it does not. table_items is the decision table item
set standing as the cross check. feeder_items, where given, is the
feeder item set in the same item form, and stands in place of
feeder_result where feeder_result carries no items. An item is a
mapping or object carrying item, raised, presented and ruled
fields, or a sequence of cells in that order. Where the feeder and
the table both hold an item of the same name and state a different
ruled timestamp for it, the statement names the decision table as
the disagreeing record, states the ruled timestamp each side
supports, and states that the feeder figure stands. Where the
feeder is the decision table itself, no cross check stands against
itself and the function returns None.

t4_cross_check_statement(feeder_durations, metrics_text,
metrics_name=None) returns one statement text or None.
feeder_durations is the feeder wait figure for T-4, as a single
number of hours, a sequence of (step, hours) pairs, a mapping of
step to hours, or a text carrying the figure. metrics_text is the
assembled metrics record text. Where that record states a T-4 wait
figure that differs from the feeder figure, the statement names
the metrics record as the disagreeing record, states both figures,
and states that the feeder figure stands.

time_decision_cross_check_statements(captured, feeder_figures)
returns a mapping of metric code to statement text, for the Slice 4
rows other than D-1. captured is the CapturedRead, whose assembled
metrics record text is the record compared. feeder_figures maps a
metric code to its feeder figure, as a single number of hours, a
mapping of step to hours, or a sequence of (step, hours) pairs.
Where the metrics record states a figure for a row, in the form
CODE as N hours, CODE for Step S as N hours, or states CODE wait
as N hours, and that figure differs from the feeder figure for the
same step or for the row, the statement for that code names the
metrics record, states both figures, and states that the feeder
figure stands. A row whose feeder figure the caller does not
supply carries no marking from this function, because no
disagreement can be stated without both sides.

The staffing, Q-3, Q-4 and cost seams below stand in the forms the
earlier slices landed. The staffing derivations carry their own
marking in the core, and this module supplies a staffing marking
only for a row that carries none yet, through
staffing_cross_check_statements in its landed signature.
"""
import re


def _fmt_num(value):
    if value is None:
        return ""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value).strip()
    if number == int(number):
        return str(int(number))
    return ("%.2f" % number).rstrip("0").rstrip(".")


def _record_name(metrics_name):
    if metrics_name:
        return str(metrics_name).rsplit("/", 1)[-1]
    return "build-metrics-record.md"


def _item_field(item, *names):
    if isinstance(item, dict):
        for name in names:
            value = item.get(name)
            if value is not None:
                return value
        return None
    for name in names:
        value = getattr(item, name, None)
        if value is not None:
            return value
    return None


def _item_parts(item):
    """Return (name, ruled) for one decision item, in any held form."""
    if isinstance(item, (tuple, list)):
        name = item[0] if len(item) > 0 else None
        ruled = item[4] if len(item) > 4 else None
        return (str(name).strip() if name is not None else "",
                str(ruled).strip() if ruled is not None else "")
    name = _item_field(item, "item", "name", "id")
    ruled = _item_field(item, "ruled", "ruled_text", "ruling")
    return (str(name).strip() if name is not None else "",
            str(ruled).strip() if ruled is not None else "")


def _item_set(items):
    """Return an ordered mapping of item name to ruled text."""
    found = {}
    if not items:
        return found
    if isinstance(items, dict):
        iterable = items.values()
    else:
        iterable = items
    for item in iterable:
        name, ruled = _item_parts(item)
        if name and name not in found:
            found[name] = ruled
    return found


def _figure_value(value):
    """Return one feeder figure as a float, or None."""
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        found = re.search(r"(\d+(?:\.\d+)?)\s*hours", value)
        if found:
            return float(found.group(1))
        try:
            return float(value.strip())
        except ValueError:
            return None
    if isinstance(value, dict):
        values = [v for v in (_figure_value(v) for v in value.values())
                  if v is not None]
        return values[0] if len(values) == 1 else None
    if isinstance(value, (tuple, list)):
        if len(value) == 2 and isinstance(value[0], (int, float)) \
                and not isinstance(value[0], bool):
            return _figure_value(value[1])
        values = [_figure_value(v) for v in value]
        values = [v for v in values if v is not None]
        return values[0] if len(values) == 1 else None
    return None


def _step_figures(value):
    """Return a mapping of step to feeder figure, where held so."""
    found = {}
    if isinstance(value, dict):
        for key, held in value.items():
            step = None
            if isinstance(key, int):
                step = key
            elif isinstance(key, str):
                match = re.search(r"(\d+)", key)
                if match:
                    step = int(match.group(1))
            figure = _figure_value(held)
            if step is not None and figure is not None:
                found[step] = figure
        return found
    if isinstance(value, (tuple, list)):
        for entry in value:
            if isinstance(entry, (tuple, list)) and len(entry) == 2:
                step = entry[0]
                if isinstance(step, str):
                    match = re.search(r"(\d+)", step)
                    step = int(match.group(1)) if match else None
                figure = _figure_value(entry[1])
                if step is not None and figure is not None:
                    found[int(step)] = figure
    return found


def staffing_cross_check_statements(captured, universe, covered,
                                    totals, f2_counted):
    """Return no statements: the staffing marking stands in the core."""
    return {}


def q4_cross_check_statement(captured, covered):
    """Return no statement: Slice 4 carries no Q-4 marking."""
    return None


def q3_contested_statement(captured, universe, origin_steps):
    """Return no statement: Slice 4 carries no Q-3 marking."""
    return None


def d1_cross_check_statement(feeder_result, table_items,
                             feeder_items=None, metrics_name=None):
    """Return the D-1 record disagrees marking, or None.

    The governing feeder items stand against the decision table
    items. Where both hold the same item and state a different
    ruled timestamp for it, the marking names the decision table
    as the disagreeing record, states the ruled timestamp the
    feeder supports and the ruled timestamp the table supports,
    and states that the feeder figure stands and the record figure
    is not followed, under D-18 and CA-1. Where the feeder item set
    is the table item set itself, no marking stands.
    """
    feeder = _item_set(feeder_items if feeder_items is not None
                       else feeder_result)
    if not feeder and feeder_result is not None and \
            not isinstance(feeder_result, (list, tuple, dict)):
        feeder = _item_set(getattr(feeder_result, "items", None))
    table = _item_set(table_items)
    if not feeder or not table:
        return None
    if feeder == table:
        return None
    for name in table:
        if name not in feeder:
            continue
        feeder_ruled = feeder[name]
        table_ruled = table[name]
        if feeder_ruled and table_ruled and feeder_ruled != table_ruled:
            return ("record disagrees: the decision table in %s "
                    "states %s ruled at %s, while the governing "
                    "feeder states %s ruled at %s; the feeder figure "
                    "stands and the record figure is not followed"
                    % (_record_name(metrics_name), name, table_ruled,
                       name, feeder_ruled))
    return None


def cost_cross_check_statements(captured, e3_tokens, e4_money,
                                b2_money_spent, b2_token_spent):
    """Return no statements: Slice 4 carries no cost marking."""
    return {}


def t4_cross_check_statement(feeder_durations, metrics_text,
                             metrics_name=None):
    """Return the T-4 record disagrees marking, or None.

    Where the metrics record states a T-4 wait figure, in the form
    T-4 wait as N hours or states T-4 wait as N hours, and that
    figure differs from the feeder wait figure, the marking names
    the metrics record, states both figures, and states that the
    feeder figure stands, under D-18 and CA-1.
    """
    feeder = _figure_value(feeder_durations)
    if feeder is None:
        steps = _step_figures(feeder_durations)
        if len(steps) == 1:
            feeder = next(iter(steps.values()))
    if feeder is None or not metrics_text:
        return None
    found = re.search(
        r"T-4\s+wait\s+as\s+(\d+(?:\.\d+)?)\s*hours", str(metrics_text))
    if not found:
        return None
    stated = float(found.group(1))
    if stated == feeder:
        return None
    return ("record disagrees: %s states T-4 wait as %s hours, while "
            "the path ledger BANKED entries state %s hours; the "
            "feeder figure stands and the record figure is not "
            "followed"
            % (_record_name(metrics_name), _fmt_num(stated),
               _fmt_num(feeder)))


def time_decision_cross_check_statements(captured, feeder_figures):
    """Return the Slice 4 markings for T-1, T-2, T-4, B-1, B-3, B-4.

    feeder_figures maps a metric code to the feeder figure the core
    derived for that row. A marking stands only where the assembled
    metrics record states a figure for the row that differs from
    the feeder figure for the same step, or for the row where the
    feeder figure stands as a single figure. Each marking names
    the metrics record, states both figures, and states that the
    feeder figure stands, under D-18 and CA-1.
    """
    statements = {}
    text = ""
    if captured is not None:
        text = getattr(captured, "assembled_metrics", None) or ""
    if not text or not feeder_figures:
        return statements
    name = _record_name(getattr(captured, "metrics_single_path", None)
                        if captured is not None else None)
    for code in ("T-1", "T-2", "T-4", "B-1", "B-3", "B-4"):
        if code not in feeder_figures:
            continue
        held = feeder_figures[code]
        per_step = _step_figures(held)
        single = _figure_value(held)
        marking = None
        for found in re.finditer(
                re.escape(code) +
                r"\s+for\s+Step\s+(\d+)\s+as\s+(\d+(?:\.\d+)?)"
                r"\s*hours", text):
            step = int(found.group(1))
            stated = float(found.group(2))
            feeder = per_step.get(step, single)
            if feeder is not None and stated != feeder:
                marking = ("record disagrees: %s states %s for "
                           "Step %d as %s hours, while the feeder "
                           "records state %s hours for Step %d; the "
                           "feeder figure stands and the record "
                           "figure is not followed"
                           % (name, code, step, _fmt_num(stated),
                              _fmt_num(feeder), step))
                break
        if marking is None and single is not None:
            for pattern in (
                    re.escape(code) +
                    r"\s+as\s+(\d+(?:\.\d+)?)\s*hours",
                    r"states\s+" + re.escape(code) +
                    r"\s+wait\s+as\s+(\d+(?:\.\d+)?)\s*hours",
                    re.escape(code) +
                    r"\s+wait\s+as\s+(\d+(?:\.\d+)?)\s*hours"):
                found = re.search(pattern, text)
                if found and float(found.group(1)) != single:
                    marking = ("record disagrees: %s states %s as "
                               "%s hours, while the feeder records "
                               "state %s hours; the feeder figure "
                               "stands and the record figure is not "
                               "followed"
                               % (name, code,
                                  _fmt_num(float(found.group(1))),
                                  _fmt_num(single)))
                    break
        if marking is not None:
            statements[code] = marking
    return statements
