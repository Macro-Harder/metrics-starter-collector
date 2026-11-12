"""Module 4: cross check, part of the derivation core.

Compares a feeder derived result with the metrics record where that
record holds the figure, and records any disagreement for the row
statement line. It never overrides a feeder result. Where the metrics
record is absent or holds no figure, no marking is made on that ground.
"""


def _median_of(items):
    from metrics_starter_collector.derivation_core import _item_latency_hours, _median
    latencies = []
    for item in items or []:
        value = _item_latency_hours(item)
        if value is not None:
            latencies.append(value)
    if not latencies:
        return None
    return _median(latencies)


def _metrics_name(captured):
    if captured.metrics_single_path:
        return captured.metrics_single_path.rsplit("/", 1)[-1]
    return "build-metrics-record.md"


def _contested_steps(captured, universe):
    claim = getattr(universe, "metrics_count_claim", None)
    if claim is None or claim >= len(universe.evidenced):
        return []
    return list(universe.evidenced)[claim:]


def staffing_cross_check_statements(captured, universe, covered,
                                    totals, f2_counted):
    """Return record disagrees statements for the Slice 3 rows.

    covered maps a step to its feeder (staffed, base) pair for E-1,
    totals maps a step to its feeder total spins for E-2, and
    f2_counted holds the steps counted in the F-2 denominator. A
    statement is returned per row code only where the metrics record
    figure or the contested step instance disagrees with the feeder
    result the row follows.
    """
    import re
    name = _metrics_name(captured)
    statements = {}
    text = captured.assembled_metrics or ""
    for m in re.finditer(r"E-1 for Step (\d+) as (\d+) of (\d+)", text):
        step = int(m.group(1))
        stated = (int(m.group(2)), int(m.group(3)))
        if step in covered and covered[step] != stated:
            statements.setdefault("E-1", []).append(
                "record disagrees: %s states E-1 for Step %d as %d of "
                "%d while the feeder records support %d of %d; the row "
                "follows the feeder records."
                % (name, step, stated[0], stated[1], covered[step][0],
                   covered[step][1]))
    for m in re.finditer(r"E-2 for Step (\d+) as (\d+)", text):
        step = int(m.group(1))
        if step in totals and totals[step] != int(m.group(2)):
            statements.setdefault("E-2", []).append(
                "record disagrees: %s states E-2 for Step %d as %d "
                "while the feeder records support total spins %d; the "
                "row follows the feeder records."
                % (name, step, int(m.group(2)), totals[step]))
    claim = getattr(universe, "metrics_count_claim", None)
    for step in _contested_steps(captured, universe):
        if step in covered:
            statements.setdefault("E-1", []).append(
                "record disagrees: %s states the step universe as %d "
                "steps and does not include Step %d, while the feeder "
                "records support Step %d staffed %d of base %d; the "
                "figure for the contested instance is carried on the "
                "evidenced universe and the row follows the feeder "
                "records."
                % (name, claim, step, step, covered[step][0],
                   covered[step][1]))
        if step in totals:
            statements.setdefault("E-2", []).append(
                "record disagrees: %s states the step universe as %d "
                "steps and does not include Step %d, while the feeder "
                "records support total spins Step %d: %d; the figure "
                "for the contested instance is carried on the "
                "evidenced universe and the row follows the feeder "
                "records."
                % (name, claim, step, step, totals[step]))
        if step in f2_counted:
            statements.setdefault("F-2", []).append(
                "record disagrees: %s states the step universe as %d "
                "steps and does not include Step %d, while the gate "
                "files support a first ruling for Step %d counted in "
                "the denominator on the evidenced universe; the row "
                "follows the feeder records."
                % (name, claim, step, step))
    return statements


def d1_cross_check_statement(feeder_result, table_items):
    """Return a record disagrees statement for the D-1 row, or None.

    Applies where the queue file governed the row and the metrics
    record decision table, standing as the cross check, supports a
    different median figure.
    """
    if table_items is None:
        return None
    if feeder_result.verdict != "present":
        return None
    table_median = _median_of(table_items)
    if table_median is None:
        return None
    import re
    m = re.search(r"median ([0-9.]+) hours", feeder_result.figures)
    if not m:
        return None
    feeder_median = float(m.group(1))
    if feeder_median == table_median:
        return None
    from metrics_starter_collector.derivation_core import _fmt_num
    return ("record disagrees: the metrics record "
            "decision table supports a median of %s hours while the "
            "governing feeder supports a median of %s hours; the row "
            "follows the governing feeder."
            % (_fmt_num(table_median), _fmt_num(feeder_median)))
