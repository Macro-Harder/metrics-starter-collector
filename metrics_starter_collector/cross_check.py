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

Slice 5 form. This module builds the marking for the rows Slice 5
certifies, T-7, Q-1, Q-3 and Q-4, under decisions D-18 and proposal
CA-1, in the same form Slice 4 uses for the D-1 row: any
disagreement stands in the statement line of the affected row, the
disagreeing record is named, the fact or figure each side supports
is stated, and, where CA-1 applies, both figures and the cause are
stated. The feeder figure always stands and no marking overrides a
feeder result. The functions below are the seam the derivation
core addresses, in the forms the core consumes:

rounds_quality_cross_check_statements(captured, feeder_figures)
returns a mapping of metric code to statement text, for the Slice
5 rows. captured is the CapturedRead, whose assembled metrics
record text is the record compared. feeder_figures maps a metric
code to its feeder figure, as a single figure text or number, a
mapping of step to figure, or a sequence of (step, figure) pairs,
where a figure may stand as a share in the form N of M, as a
number, or as a (landed, total) pair. Where the metrics record
states a figure for a row, in the form CODE for Step S as F or
CODE as F, and that figure differs from the feeder figure for the
same step or for the row, the statement for that code names the
metrics record, states both figures, and states that the feeder
figure stands. A row whose feeder figure the caller does not
supply carries no marking from this function.

q4_cross_check_statement(captured, covered) returns one statement
text or None, the Q-4 limb of the form above in the signature the
earlier slices landed. covered is the Q-4 feeder standing, as a
mapping of step to a (landed, total) pair or a share text, a
sequence of (step, landed, total) entries, or a single share.

Slice 6 form. This module builds the marking for the rows Slice 6
certifies, E-3, E-4 and B-2, under decisions D-18 and proposal
CA-1, in the same form Slice 4 uses for the D-1 row: any
disagreement stands in the statement line of the affected row,
the disagreeing record is named, the fact or figure each side
supports is stated, and, where CA-1 applies, both figures and
the cause are stated. The feeder figure always stands and no
marking overrides a feeder result, and no standalone comparison
table stands anywhere in the report for these rows. The seam the
derivation core addresses stands in these forms:

cost_cross_check_statements(captured, feeder_figures=None,
**legacy_figures) returns a mapping of metric code to statement
text, for E-3, E-4 and B-2. feeder_figures maps a code to its
feeder figure, a single figure or a mapping of step to figure,
and for B-2 a mapping holding its money spent and token spent
figures under money and token named keys, the two sides stated
separately.

b2_cross_check_statement(captured, money_spent=None,
token_spent=None) returns one statement text or None, the B-2
limb of the form above, each side stated separately.

cost_row_cross_check_statement(captured, code, feeder_figure)
returns one statement text or None, the single row limb of the
form above for E-3 and E-4.

The comparison reads the one CapturedRead, its assembled metrics
record text and its metrics record path, and no source outside
it. A placeholder zero is never printed as a value for E-4 in
any marking this module forms: a marking states only figures
the record and the feeder each support.

Slice 7 form. This slice lands no new cross check function and
changes no marking form the earlier slices settled. The final
printed standing of every marking this module forms stands as
the earlier slices settled it: a disagreement stands recorded
inside the row statement line of the row it touches only, the
disagreeing record named, the fact or figure each side supports
stated, the feeder figure always standing, no marking overriding
a feeder result, and no standalone comparison table standing
anywhere in the report. The seam the derivation core addresses
stands in the landed signatures stated above and in the module
head forms for Slices 4, 5 and 6, unchanged in this slice, and
the golden full comparison carriage in this slice rests on those
markings standing in that printed form and on no new comparison
function.

q3_contested_statement(captured, universe, origin_steps) returns
one statement text or None, in the signature the earlier slices
landed. universe is the StepUniverse the core built, or an
iterable of evidenced steps. origin_steps is the set of origin
steps the register entries state, as step numbers or Step S texts.
Where an origin step stands outside the evidenced universe, the
statement names the metrics record as the disagreeing record,
states the universe the record supports and the origin step the
register entry supports, and states that the feeder figure stands.
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


def _share_text(value):
    """Return one feeder figure as a share or number text, or None."""
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return _fmt_num(value)
    if isinstance(value, str):
        found = re.search(r"(\d+)\s+of\s+(\d+)", value)
        if found:
            return "%s of %s" % (found.group(1), found.group(2))
        found = re.search(r"(\d+(?:\.\d+)?)", value)
        return _fmt_num(float(found.group(1))) if found else None
    if isinstance(value, (tuple, list)):
        numbers = [v for v in value
                   if isinstance(v, (int, float))
                   and not isinstance(v, bool)]
        if len(numbers) >= 2:
            return "%s of %s" % (_fmt_num(numbers[0]),
                                 _fmt_num(numbers[-1]))
        if len(numbers) == 1:
            return _fmt_num(numbers[0])
    return None


def _share_figures(value):
    """Return a mapping of step to feeder figure text, where held so."""
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
            figure = _share_text(held)
            if step is not None and figure is not None:
                found[step] = figure
        return found
    if isinstance(value, (tuple, list)):
        for entry in value:
            if isinstance(entry, (tuple, list)) and len(entry) >= 2:
                step = entry[0]
                if isinstance(step, str):
                    match = re.search(r"(\d+)", step)
                    step = int(match.group(1)) if match else None
                figure = _share_text(entry[1:] if len(entry) > 2
                                     else entry[1])
                if step is not None and figure is not None:
                    found[int(step)] = figure
    return found


def _record_figures(text, code):
    """Return (per step figures, row figure) the record states."""
    per_step = {}
    row = None
    if not text:
        return per_step, row
    for found in re.finditer(
            re.escape(code) +
            r"\s+for\s+Step\s+(\d+)\s+as\s+(\d+\s+of\s+\d+|"
            r"\d+(?:\.\d+)?)", str(text)):
        per_step[int(found.group(1))] = _share_text(found.group(2))
    found = re.search(
        re.escape(code) + r"\s+as\s+(\d+\s+of\s+\d+|\d+(?:\.\d+)?)",
        str(text))
    if found:
        row = _share_text(found.group(1))
    return per_step, row


def rounds_quality_cross_check_statements(captured, feeder_figures):
    """Return the Slice 5 markings for T-7, Q-1, Q-3 and Q-4.

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
    for code in ("T-7", "Q-1", "Q-3", "Q-4"):
        if code not in feeder_figures:
            continue
        held = feeder_figures[code]
        per_step = _share_figures(held)
        single = _share_text(held) if not per_step else None
        stated_steps, stated_row = _record_figures(text, code)
        marking = None
        for step in sorted(stated_steps):
            feeder = per_step.get(step, single)
            if feeder is not None and stated_steps[step] != feeder:
                marking = ("record disagrees: %s states %s for "
                           "Step %d as %s, while the feeder records "
                           "state %s for Step %d; the feeder figure "
                           "stands and the record figure is not "
                           "followed"
                           % (name, code, step, stated_steps[step],
                              feeder, step))
                break
        if marking is None and stated_row is not None \
                and single is not None and stated_row != single:
            marking = ("record disagrees: %s states %s as %s, while "
                       "the feeder records state %s; the feeder "
                       "figure stands and the record figure is not "
                       "followed"
                       % (name, code, stated_row, single))
        if marking is not None:
            statements[code] = marking
    return statements


def q4_cross_check_statement(captured, covered):
    """Return the Q-4 record disagrees marking, or None.

    covered is the Q-4 feeder standing the core derived, as a
    mapping of step to a (landed, total) pair or a share text, a
    sequence of (step, landed, total) entries, or a single share.
    Where the metrics record states a Q-4 figure for a step that
    differs from the feeder share for that step, the marking names
    the metrics record, states both figures, and states that the
    feeder figure stands, under D-18 and CA-1.
    """
    if captured is None:
        return None
    statements = rounds_quality_cross_check_statements(
        captured, {"Q-4": covered})
    return statements.get("Q-4")


def q3_contested_statement(captured, universe, origin_steps):
    """Return the Q-3 contested origin step marking, or None.

    Where a register entry states an origin step that stands
    outside the evidenced step universe, the marking names the
    metrics record as the disagreeing record, states the universe
    the record supports and the origin step the entry supports,
    and states that the feeder figure stands, under D-18 and CA-1.
    """
    evidenced = set()
    if universe is not None:
        held = getattr(universe, "evidenced", None)
        if held is None:
            held = getattr(universe, "steps", None)
        if held is None:
            held = universe
        try:
            for item in held:
                if isinstance(item, int):
                    evidenced.add(item)
                elif isinstance(item, str):
                    match = re.search(r"(\d+)", item)
                    if match:
                        evidenced.add(int(match.group(1)))
                else:
                    number = getattr(item, "step", None)
                    if isinstance(number, int):
                        evidenced.add(number)
        except TypeError:
            evidenced = set()
    origins = []
    if origin_steps is not None:
        values = origin_steps if isinstance(
            origin_steps, (list, tuple, set)) else [origin_steps]
        for value in values:
            if isinstance(value, int):
                origins.append(value)
            elif isinstance(value, str):
                match = re.search(r"(\d+)", value)
                if match:
                    origins.append(int(match.group(1)))
    if not evidenced or not origins:
        return None
    name = _record_name(getattr(captured, "metrics_single_path", None)
                        if captured is not None else None)
    for step in origins:
        if step not in evidenced:
            return ("record disagrees: %s states the step universe "
                    "as %d step%s, while the register entry states "
                    "origin step Step %d; the feeder figure stands "
                    "and the record figure is not followed"
                    % (name, len(evidenced),
                       "" if len(evidenced) == 1 else "s", step))
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


def _cost_record_figures(text, code):
    """Return (per step figures, labelled figures) the record states.

    Labelled figures stand in the forms CODE money spent as N,
    CODE token total as N and CODE as N. Per step figures stand in
    the form CODE for Step S as N.
    """
    per_step = {}
    labelled = {}
    if not text:
        return per_step, labelled
    text = str(text)
    for found in re.finditer(
            re.escape(code) +
            r"(?:\s+[A-Za-z]+)?\s+for\s+Step\s+(\d+)\s+as\s+"
            r"(\d+(?:\.\d+)?)", text):
        per_step[int(found.group(1))] = float(found.group(2))
    for label, pattern in (
            ("money", r"\s+money\s+(?:spent\s+)?as\s+(\d+(?:\.\d+)?)"),
            ("token", r"\s+tokens?\s+(?:total\s+)?as\s+(\d+(?:\.\d+)?)"),
            ("row", r"\s+as\s+(\d+(?:\.\d+)?)")):
        found = re.search(re.escape(code) + pattern, text)
        if found:
            labelled[label] = float(found.group(1))
    return per_step, labelled


def _b2_side_figures(feeder_figures):
    """Return (money spent, token spent) from a B-2 feeder holding."""
    money = None
    token = None
    if isinstance(feeder_figures, dict):
        for key, value in feeder_figures.items():
            lowered = str(key).lower()
            figure = _figure_value(value)
            if figure is None:
                continue
            if "money" in lowered and "spent" in lowered:
                money = figure
            elif "token" in lowered and "spent" in lowered:
                token = figure
            elif "money" in lowered and money is None:
                money = figure
            elif "token" in lowered and token is None:
                token = figure
    else:
        figure = _figure_value(feeder_figures)
        if figure is not None:
            money = figure
    return money, token


def b2_cross_check_statement(captured, money_spent=None,
                             token_spent=None):
    """Return the B-2 record disagrees marking, or None.

    Where the assembled metrics record states a B-2 money spent
    figure or a B-2 token total figure that differs from the
    feeder figure for that side, the marking names the metrics
    record, states both figures for that side, and states that
    the feeder figure stands, under D-18 and CA-1. The money side
    and the token side stand stated separately in the marking.
    """
    if captured is None:
        return None
    text = getattr(captured, "assembled_metrics", None) or ""
    if not text:
        return None
    name = _record_name(getattr(captured, "metrics_single_path", None))
    _per_step, labelled = _cost_record_figures(text, "B-2")
    parts = []
    if money_spent is not None and "money" in labelled:
        feeder = _figure_value(money_spent)
        if feeder is not None and labelled["money"] != feeder:
            parts.append(
                "record disagrees: %s states B-2 money spent as %s, "
                "while the feeder records state money spent %s; the "
                "feeder figure stands and the record figure is not "
                "followed"
                % (name, _fmt_num(labelled["money"]), _fmt_num(feeder)))
    if token_spent is not None and "token" in labelled:
        feeder = _figure_value(token_spent)
        if feeder is not None and labelled["token"] != feeder:
            parts.append(
                "record disagrees: %s states B-2 token total as %s, "
                "while the feeder records state token total %s; the "
                "feeder figure stands and the record figure is not "
                "followed"
                % (name, _fmt_num(labelled["token"]), _fmt_num(feeder)))
    if not parts:
        return None
    return "; ".join(parts)


def cost_row_cross_check_statement(captured, code, feeder_figure):
    """Return the record disagrees marking for one cost row, or None.

    feeder_figure stands as a single figure for the row, or as a
    mapping of step to figure. Where the assembled metrics record
    states a figure for the row, per step or as a row figure, that
    differs from the feeder figure, the marking names the metrics
    record, states both figures, and states that the feeder figure
    stands, under D-18 and CA-1.
    """
    if captured is None:
        return None
    text = getattr(captured, "assembled_metrics", None) or ""
    if not text:
        return None
    name = _record_name(getattr(captured, "metrics_single_path", None))
    per_step = _step_figures(feeder_figure)
    single = _figure_value(feeder_figure) if not per_step else None
    stated_steps, labelled = _cost_record_figures(text, code)
    for step in sorted(stated_steps):
        feeder = per_step.get(step, single)
        if feeder is not None and stated_steps[step] != feeder:
            return ("record disagrees: %s states %s for Step %d as "
                    "%s, while the feeder records state %s for "
                    "Step %d; the feeder figure stands and the "
                    "record figure is not followed"
                    % (name, code, step, _fmt_num(stated_steps[step]),
                       _fmt_num(feeder), step))
    stated_row = labelled.get("row")
    if stated_row is not None and single is not None \
            and stated_row != single:
        return ("record disagrees: %s states %s as %s, while the "
                "feeder records state %s; the feeder figure stands "
                "and the record figure is not followed"
                % (name, code, _fmt_num(stated_row), _fmt_num(single)))
    return None


def cost_cross_check_statements(captured, feeder_figures=None,
                                **legacy_figures):
    """Return the Slice 6 markings for E-3, E-4 and B-2.

    feeder_figures maps a metric code to its feeder figure: for
    E-3 and E-4 a single figure or a mapping of step to figure,
    and for B-2 a mapping holding its money spent and token spent
    figures under money and token named keys, the two sides stated
    separately. The legacy keyword forms e3_tokens, e4_money,
    b2_money_spent and b2_token_spent stand accepted in the same
    places. A marking stands only where the assembled metrics
    record states a figure for the row that differs from the
    feeder figure. Each marking names the metrics record, states
    both figures, and states that the feeder figure stands, under
    D-18 and CA-1. The comparison reads the one CapturedRead and
    no source outside it.
    """
    statements = {}
    if captured is None:
        return statements
    held = {}
    if isinstance(feeder_figures, dict):
        held.update(feeder_figures)
    if "e3_tokens" in legacy_figures:
        held.setdefault("E-3", legacy_figures["e3_tokens"])
    if "e4_money" in legacy_figures:
        held.setdefault("E-4", legacy_figures["e4_money"])
    b2_money = legacy_figures.get("b2_money_spent")
    b2_token = legacy_figures.get("b2_token_spent")
    if "B-2" in held:
        side_money, side_token = _b2_side_figures(held["B-2"])
        if b2_money is None:
            b2_money = side_money
        if b2_token is None:
            b2_token = side_token
    for code in ("E-3", "E-4"):
        if code in held:
            marking = cost_row_cross_check_statement(
                captured, code, held[code])
            if marking is not None:
                statements[code] = marking
    marking = b2_cross_check_statement(captured, b2_money, b2_token)
    if marking is not None:
        statements["B-2"] = marking
    return statements


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
