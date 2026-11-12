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
