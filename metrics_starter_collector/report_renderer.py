"""Module 5: report renderer.

Prints the finished ReportModel the derivation core hands over, in
the plain text line grammar the plan states: one content line after
another with no blank lines, each multi part line carrying its parts
as labelled parts separated by a space, a vertical bar and a space,
and the last line ending with the line feed. The renderer computes
nothing: every verdict, figure, coverage statement and reason it
prints comes from the model it is handed, in the order the model
carries it.

Row form, in part order. The row head stands first, the metric code
and the metric name in words. Then the Verdict part. On a present
row, the Value part follows, carrying the figure in its defined
unit as the result holds it; where the result carries a single
share for the row as a whole, as separate numerator and denominator
fields of the result, a Numerator part and then a Denominator part
follow the Value part, in that order, and on no other row: a per
step share set and a grouped share set carry each share inside the
Value part, and a row that is not present carries no Value part and
no Numerator or Denominator part. Then the Row coverage part, where
the result carries step coverage or a denominator. Then the Bound
part, where the result carries one, and the Reconciled against
part, where the result carries one. On a row that is not present,
the Reason part stands in place of the value parts, carrying the
reason line the result holds: where the result holds its reason in
the three named subparts, in the grammar form the reason value
states below, and where it holds only the two part fields, in that
form. The Pointer part stands last on every
row. A statement the result holds stands on its own line after the
row line, in the statement line form, and a derived from line the
result holds stands after it, in that order.
"""

ROW_NAMES = {
    "T-1": "Step elapsed time",
    "T-2": "Step active time",
    "T-4": "Wait on a decision",
    "T-7": "Loop rounds",
    "E-1": "Agents staffed against base",
    "E-2": "Spin-ups per step",
    "E-3": "Tokens per step",
    "E-4": "Money cost per step",
    "F-2": "First-time approval rate",
    "Q-1": "Findings per audit round, by severity",
    "Q-3": "Escaped defects",
    "Q-4": "Fold-in trace landed at first trace",
    "D-1": "Decision latency",
    "B-1": "Total build elapsed and active time",
    "B-2": "Total cost against budget",
    "B-3": "Slowest three steps",
    "B-4": "Fastest three steps",
}

DATA_QUALITY_KIND_ORDER = (
    "missing record",
    "missing field",
    "wrong form",
    "unreconciled",
    "not producible",
)


def _get(obj, *names):
    """Return the first named field the object or mapping carries."""
    for name in names:
        if isinstance(obj, dict):
            value = obj.get(name)
        else:
            value = getattr(obj, name, None)
        if value is not None:
            return value
    return None


def _text(value):
    if value is None:
        return ""
    return str(value).strip()


def _lines(value):
    """Return the non blank lines of a line list or a text block."""
    if value is None:
        return []
    if isinstance(value, str):
        raw = value.splitlines()
    else:
        raw = []
        for item in value:
            raw.extend(str(item).splitlines())
    return [line for line in raw if line.strip()]


_SUBPART_MARKERS = ("broken link,", "form required,", "form held,")


def _subparts_from_container(container):
    """Return the three named subparts a container holds, or None.

    A mapping container names the subparts by their field names. A
    sequence container of three carries them in the grammar order:
    broken link, form required, form held.
    """
    if isinstance(container, dict):
        broken = _get(container, "broken_link", "link_broken",
                      "broken_link_text", "broken")
        required = _get(container, "form_required", "required_form",
                        "form_required_text", "required")
        held = _get(container, "form_held", "held_form",
                    "form_held_text", "held")
        parts = (broken, required, held)
    elif isinstance(container, (tuple, list)) and len(container) == 3:
        parts = tuple(container)
    else:
        return None
    if all(_text(part) for part in parts):
        return tuple(_text(part).rstrip(";").strip() for part in parts)
    return None


def _parse_anatomy(text):
    """Return the three named subparts a finished reason text holds.

    The markers may stand in the grammar order or in the composed
    line order, broken link and form held before form required.
    Each subpart text runs from its marker to the next marker, to
    a what follows label, or to the end of the text.
    """
    text = _text(text)
    lowered = text.lower()
    found = []
    for marker in _SUBPART_MARKERS:
        at = lowered.find(marker)
        if at < 0:
            return None
        found.append((at, marker))
    found.sort()
    parts = {}
    for index, (at, marker) in enumerate(found):
        start = at + len(marker)
        end = found[index + 1][0] if index + 1 < len(found) else len(text)
        segment = _text(text)[start:end]
        cut = segment.lower().find("what follows")
        if cut >= 0:
            segment = segment[:cut]
        parts[marker] = segment.strip().rstrip(";").strip()
    if all(parts[marker] for marker in _SUBPART_MARKERS):
        return (parts["broken link,"], parts["form required,"],
                parts["form held,"])
    return None


def _subparts(result):
    """Return the three named subparts a result holds, or None.

    The subparts may stand as their own fields on the result, as a
    container field, as a mapping in the reason field, or composed
    inside a finished reason text the result holds. All three must
    stand for the result to hold its reason in this form.
    """
    for name in ("reason_parts", "reason_subparts", "subparts",
                 "anatomy", "reason_anatomy"):
        parts = _subparts_from_container(_get(result, name))
        if parts is not None:
            return parts
    broken = _get(result, "broken_link", "link_broken",
                  "broken_link_text", "broken")
    required = _get(result, "form_required", "required_form",
                    "form_required_text", "required")
    held = _get(result, "form_held", "held_form",
                "form_held_text", "held")
    if all(_text(part) for part in (broken, required, held)):
        return tuple(_text(part).rstrip(";").strip()
                     for part in (broken, required, held))
    parts = _subparts_from_container(_get(result, "reason"))
    if parts is not None:
        return parts
    reason = _get(result, "reason")
    if isinstance(reason, str) and "what the record shows" not in \
            reason.lower() and "what follows" not in reason.lower():
        parts = _parse_anatomy(reason)
        if parts is not None:
            return parts
    method = getattr(result, "reason_text", None)
    if callable(method):
        value = method()
        if value and "what the record shows" not in value.lower() \
                and "what follows" not in value.lower():
            return _parse_anatomy(value)
    return None


def _consequence(follows, code, required):
    """Return the consequence text of a follows field, cleaned.

    A leading reason code is dropped, because the code stands once,
    at the start of the second part. A leading form required segment
    that repeats the required subpart the result already holds is
    dropped, so the subpart stands once, in the grammar form.
    """
    body = _text(follows)
    if code and body.lower().startswith(code.lower()):
        body = body[len(code):].lstrip(" :")
    if body.lower().startswith("form required,"):
        segment, _, rest = body.partition(";")
        if _text(required) and _text(required) in segment:
            body = rest.lstrip()
    return body


def _reason_value(result):
    """Return the reason line text a result holds, or an empty text.

    Field form selects printed form. A result that holds its reason
    in the three named subparts prints them in the grammar form, in
    their order: broken link, form required, form held, separated
    by a semicolon and a space. Where that result also holds the
    two part fields, the grammar form stands inside the first
    labelled part, what the record shows, and the second labelled
    part, what follows, opens with the reason code the result
    holds, followed by the consequence the follows field holds:
    the code stands at the start of the second part and no code
    stands in the first part. A result that holds the three
    subparts and no code and no follows field prints the grammar
    form alone. A result that holds a finished reason line,
    through its reason text method or its reason field, stands as
    it is held. A result that holds only the two part fields
    stands composed from them in the two part form.
    """
    parts = _subparts(result)
    if parts is not None:
        anatomy = "broken link, %s; form required, %s; form held, %s" % (
            parts)
        code = _text(_get(result, "code_token", "reason_code"))
        follows = _get(result, "follows")
        if follows is None and not code:
            return anatomy
        body = _consequence(follows, code, parts[1])
        tail = (code + " " + body).strip() if code else body
        if not tail:
            return anatomy
        return ("What the record shows: " + anatomy +
                " What follows: " + tail)
    method = getattr(result, "reason_text", None)
    if callable(method):
        value = method()
        if value:
            return _text(value)
    reason = _get(result, "reason")
    if reason is not None:
        return _text(reason)
    shows = _get(result, "shows")
    if shows is not None:
        code = _text(_get(result, "code_token", "reason_code"))
        body = _text(_get(result, "follows"))
        if code and body.lower().startswith(code.lower()):
            body = body[len(code):].lstrip()
        tail = (code + " " + body).strip() if code else body
        text = "What the record shows: " + _text(shows)
        if tail:
            text += " What follows: " + tail
        return text
    return ""


def _bound_value(result):
    """Return the Bound part text a result holds, or an empty text."""
    bound = _get(result, "bound", "bound_text", "bound_part")
    if bound is None:
        return ""
    if isinstance(bound, dict):
        return "excepted, %s; link excepted, %s; cleared by, %s" % (
            _text(bound.get("excepted")), _text(bound.get("link_excepted")),
            _text(bound.get("cleared_by")))
    if isinstance(bound, (tuple, list)):
        parts = [_text(part) for part in bound]
        if len(parts) == 3:
            return ("excepted, %s; link excepted, %s; cleared by, %s"
                    % tuple(parts))
        return "; ".join(part for part in parts if part)
    return _text(bound)


def _row_lines(result):
    """Return the lines of one verdict row, its row line first."""
    code = _text(_get(result, "code"))
    name = _text(_get(result, "name", "metric_name", "title"))
    if not name:
        name = ROW_NAMES.get(code, "")
    head = (code + " " + name).strip()
    verdict = _text(_get(result, "verdict"))
    parts = [head, "Verdict: " + verdict]
    if verdict == "present":
        value = _text(_get(result, "value", "figures", "figure"))
        if value:
            parts.append("Value: " + value)
        numerator = _get(result, "numerator", "share_numerator")
        denominator = _get(result, "denominator_part", "share_denominator",
                           "single_denominator")
        if numerator is not None and denominator is not None:
            parts.append("Numerator: " + _text(numerator))
            parts.append("Denominator: " + _text(denominator))
        coverage = _text(_get(result, "row_coverage", "coverage",
                              "denominator"))
        if coverage:
            parts.append("Row coverage: " + coverage)
        bound = _bound_value(result)
        if bound:
            parts.append("Bound: " + bound)
        reconciled = _text(_get(result, "reconciled_against",
                                "reconciliation", "reconciled"))
        if reconciled:
            parts.append("Reconciled against: " + reconciled)
        statement_part = _text(_get(result, "statement_part"))
        if code == "D-1" and statement_part:
            parts.append("Statement: " + statement_part)
    else:
        reason = _reason_value(result)
        if reason:
            parts.append("Reason: " + reason)
    pointer = _text(_get(result, "pointer"))
    parts.append("Pointer: " + pointer)
    lines = [" | ".join(parts)]
    statement = _text(_get(result, "statement"))
    if statement:
        lines.append("Statement line: " + statement)
    derived_from = _text(_get(result, "derived_from"))
    if derived_from:
        lines.append("Derived from line: " + derived_from)
    return lines


def _header_lines(model):
    """Return the header lines in grammar position.

    The root identity line stands first and the build identity line
    second. Where the model carries its header as finished lines,
    those lines stand as held, in their order, with any title line
    and any blank line dropped, and the two identity lines moved to
    their places at the head. Where the model carries the identity
    facts as fields, the two lines stand composed from them and the
    remaining header lines follow as held.
    """
    held = _lines(_get(model, "header_lines", "header"))
    root_line = None
    build_line = None
    rest = []
    for line in held:
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if stripped.startswith("Root:") and root_line is None:
            root_line = stripped
        elif stripped.startswith("Build identity:") and build_line is None:
            build_line = stripped
        else:
            rest.append(line)
    if root_line is None:
        root = _text(_get(model, "root"))
        if root:
            root_line = "Root: " + root
    if build_line is None:
        identity = _text(_get(model, "build_identity"))
        if identity:
            build_line = "Build identity: " + identity
    lines = []
    if root_line is not None:
        lines.append(root_line)
    if build_line is not None:
        lines.append(build_line)
    lines.extend(rest)
    for extra in ("coverage_lines", "record_state_line", "trigger_line"):
        for line in _lines(_get(model, extra)):
            if line not in lines:
                lines.append(line)
    coverage = _get(model, "coverage")
    if isinstance(coverage, str) and coverage.strip():
        line = coverage.strip()
        if not any(existing.strip() == line for existing in lines):
            lines.append(line)
    return lines


def _inventory_lines(model):
    """Return the piece inventory lines, heading in its plain form."""
    held = _lines(_get(model, "inventory_lines", "piece_inventory",
                       "inventory"))
    lines = []
    for line in held:
        stripped = line.strip()
        if stripped.startswith("## "):
            stripped = stripped[3:].strip()
        lines.append(stripped if stripped.lower() == "piece inventory"
                     else line)
    return lines


def _section_lines(model, *names):
    return _lines(_get(model, *names))


def _data_quality_lines(model):
    """Return the data quality lines the model holds.

    A model that holds its entries as a list of entry lines stands
    as held, one entry to a line. A model that holds a count per
    broken link kind stands in the kind order the grammar states,
    one line for each kind, the kind as its label and its count as
    its value.
    """
    held = _get(model, "data_quality", "data_quality_lines")
    if isinstance(held, dict):
        lines = []
        for kind in DATA_QUALITY_KIND_ORDER:
            if kind in held:
                lines.append("%s: %s" % (kind, held[kind]))
        for kind in held:
            if kind not in DATA_QUALITY_KIND_ORDER:
                lines.append("%s: %s" % (kind, held[kind]))
        return lines
    return _lines(held)


def _floor_lines(model):
    """Return the no usable records form: three lines, no rows."""
    header = _header_lines(model)
    lines = header[:2]
    floor = _text(_get(model, "no_usable_line", "floor_line"))
    if not floor:
        for line in header[2:] + _data_quality_lines(model):
            if line.strip().startswith("No usable records"):
                floor = line.strip()
                break
    if not floor:
        root = ""
        if lines and lines[0].startswith("Root:"):
            root = lines[0][len("Root:"):].strip()
        floor = ("No usable records: the root read, %s, was looked "
                 "through for the recognised record pieces, and none "
                 "was found" % (root or "the root as given"))
    elif not floor.startswith("No usable records"):
        floor = "No usable records: " + floor
    lines.append(floor)
    return lines


def render_report(model):
    """Print the ReportModel and return the report text."""
    if _get(model, "no_usable"):
        return "\n".join(_floor_lines(model)) + "\n"
    lines = []
    lines.extend(_header_lines(model))
    lines.extend(_inventory_lines(model))
    results = _get(model, "results", "rows", "derivations") or []
    for result in results:
        lines.extend(_row_lines(result))
    disagreements = _section_lines(model, "disagreements_lines",
                                   "disagreements")
    if disagreements:
        lines.append("Disagreements")
        lines.extend(disagreements)
    data_quality = _data_quality_lines(model)
    if data_quality:
        lines.append("Data quality")
        lines.extend(data_quality)
    record_cost = _section_lines(model, "record_cost_lines", "record_cost")
    if record_cost:
        lines.append("Record cost")
        lines.extend(record_cost)
    run_cost = _get(model, "run_cost_line", "run_cost")
    if isinstance(run_cost, dict):
        order = (("Files visited", "files_visited"),
                 ("Files opened", "files_opened"),
                 ("Bytes read", "bytes_read"),
                 ("Entries visited", "entries_visited"),
                 ("Limit", "limit"),
                 ("Reading", "reading"))
        parts = ["Run cost"]
        for label, key in order:
            if key in run_cost:
                parts.append("%s: %s" % (label, run_cost[key]))
        lines.append(" | ".join(parts))
    else:
        lines.extend(_lines(run_cost))
    terms = _section_lines(model, "terms_lines", "terms")
    if terms:
        lines.append("Terms")
        lines.extend(terms)
    lines = [line for line in lines if line.strip()]
    return "\n".join(lines) + "\n"
