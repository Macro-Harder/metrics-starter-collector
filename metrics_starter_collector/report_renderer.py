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

Slice 2 form, capture integrity and the G-10 limits. In the header,
after the coverage statement and before the piece inventory, one
coverage piece line stands for each piece the model carries as not
read in full, in the order the pieces stand in the piece inventory:
label Coverage piece not read in full, value the piece name, its
size, its state as the model holds it, and the limit it crossed
where the model carries one, in the form the model states it. A
partial reading the model carries stands stated in both places
together: as a Coverage partial line in the coverage statement and
as the Reading part of the run cost line, and in neither place
where the model carries no partial reading. The renderer still
computes nothing: piece names, sizes, states, limits, the partial
marking and every run cost figure it prints come from the model.

Slice 3 form, staffing rows and the cross check marking. The
statement line a result holds stands on its own line after the row
line, for a row of any verdict, in the form above: where the core
hands over a cross check marking for E-1, E-2 or F-2, that marking
stands in the statement field of the affected row, and the renderer
prints it as the statement line of that row, with the disagreeing
record named and the fact or figure each side supports, as the
model holds them, and with a derived from line the result holds
standing after the statement line, in that order, as Slice 1
established. The header coverage statement the model holds stands
in the header before the piece inventory, in the disputed count
form where the model carries one: the count each record supports
stated, and neither count picked as the count, exactly as the
model states it. On a present row whose result carries a single
share, as separate numerator and denominator fields, the Numerator
part and then the Denominator part follow the Value part, in that
order, before the Row coverage part, as the COV-10 ruling states:
a per step share set and a grouped share set carry each share
inside the Value part and carry no such parts. The fields this
renderer consumes for this form are named at their uses below:
statement, statement line, statement text and cross check
statement for the statement line; derived from and derived from
line for the derived from line; numerator and share numerator,
with denominator part, share denominator, single denominator, or
the denominator field where row coverage stands separately, for
the share parts; and coverage, coverage statement and header
coverage statement for the header coverage statement.

Slice 4 form, time and decision rows and the build state naming.
The statement line form above stands for a row of any verdict in
this slice as it stood for Slice 3: where the core hands over a
cross check marking for T-1, T-2, T-4, D-1, B-1, B-3 or B-4, that
marking stands in the statement field of the affected row and the
renderer prints it as the statement line of that row, with the
disagreeing record named and the fact or figure each side
supports, as the model holds them. The T-4 degraded marking, that
the row is shown without its queue cross check, stands in the
same statement line form where the model holds it. The B family
rows, B-1, B-3 and B-4, carry the build state naming the model
holds, the open state naming on an in progress tree or the halt
naming on a halted tree, in the same statement line form. For the
D-1 row only, a foundation statement the model holds stands as a
Statement part in the row line, in the part order the row form
above states, after the Reconciled against part where one stands
and before the Reason part where one stands, and the same
foundation text stands together with any cross check marking in
the statement line of that row, so both stand in the statement
line that is part of the reason line field. The fields this
renderer consumes for this form are named at their uses below:
statement part, statement value, foundation, foundation
statement and ca4 statement for the D-1 Statement part; and
statement, statement line, statement text, cross check statement,
cross check marking, marking, build state statement and state
statement for the statement line. The header coverage statement
the model holds stands as held, in the open state form or the
halt form the model states, and the renderer forms no coverage
wording of its own.
"""
import re

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


def _statement_line_text(result, code, statement_part):
    """Return the statement line text a result holds, or empty.

    The text stands from the statement fields the result holds, in
    field order, with a text that stands twice held once. For the
    D-1 row, the foundation text the Statement part carries stands
    first in the statement line, together with any cross check
    marking the result holds, as the Slice 4 form states.
    """
    held = []
    for name in ("statement", "statement_line", "statement_text",
                 "cross_check_statement", "cross_check_marking",
                 "marking", "build_state_statement",
                 "state_statement"):
        text = _text(_get(result, name))
        if text and text not in held:
            held.append(text)
    if code == "D-1" and statement_part and \
            statement_part not in held:
        held.insert(0, statement_part)
    return "; ".join(held)


def _row_lines(result):
    """Return the lines of one verdict row, its row line first."""
    code = _text(_get(result, "code"))
    name = _text(_get(result, "name", "metric_name", "title"))
    if not name:
        name = ROW_NAMES.get(code, "")
    head = (code + " " + name).strip()
    verdict = _text(_get(result, "verdict"))
    parts = [head, "Verdict: " + verdict]
    statement_part = _text(_get(result, "statement_part",
                                "statement_value", "foundation",
                                "foundation_statement",
                                "ca4_statement",
                                "ca4_foundation_statement"))
    if verdict == "present":
        value = _text(_get(result, "value", "figures", "figure"))
        if value:
            parts.append("Value: " + value)
        numerator = _get(result, "numerator", "share_numerator")
        share_denominator = _get(result, "denominator_part",
                                 "share_denominator",
                                 "single_denominator")
        coverage = _text(_get(result, "row_coverage", "coverage"))
        denominator_field = _get(result, "denominator")
        if share_denominator is None and numerator is not None \
                and denominator_field is not None:
            if coverage and _text(denominator_field) != coverage:
                share_denominator = denominator_field
            elif not coverage:
                share_denominator = denominator_field
        if numerator is not None and share_denominator is not None:
            parts.append("Numerator: " + _text(numerator))
            parts.append("Denominator: " + _text(share_denominator))
        if not coverage:
            coverage = _text(denominator_field)
            if share_denominator is not None and numerator is not None \
                    and coverage == _text(share_denominator):
                coverage = ""
        if coverage:
            parts.append("Row coverage: " + coverage)
        bound = _bound_value(result)
        if bound:
            parts.append("Bound: " + bound)
        reconciled = _text(_get(result, "reconciled_against",
                                "reconciliation", "reconciled"))
        if reconciled:
            parts.append("Reconciled against: " + reconciled)
        if code == "D-1" and statement_part:
            parts.append("Statement: " + statement_part)
    else:
        if code == "D-1" and statement_part:
            parts.append("Statement: " + statement_part)
        reason = _reason_value(result)
        if reason:
            parts.append("Reason: " + reason)
    pointer = _text(_get(result, "pointer"))
    parts.append("Pointer: " + pointer)
    lines = [" | ".join(parts)]
    statement = _statement_line_text(result, code, statement_part)
    if statement:
        lines.append("Statement line: " + statement)
    derived_from = _text(_get(result, "derived_from",
                              "derived_from_line"))
    if derived_from:
        lines.append("Derived from line: " + derived_from)
    return lines


COVERAGE_PIECE_LABEL = "Coverage piece not read in full"

_PIECE_LIST_FIELDS = (
    "coverage_piece_lines", "coverage_pieces", "piece_not_read_lines",
    "pieces_not_read_in_full", "pieces_not_read", "not_read_pieces",
    "not_read_in_full_lines", "coverage_piece_entries",
    "piece_not_read_entries",
)

_PIECE_SOURCE_FIELDS = (
    "pieces", "inventory_pieces", "captured_pieces", "piece_list",
)


def _limit_phrase(text):
    """Return the limit clause a model text states, or empty.

    The clause is the first segment of the text that names a limit,
    trimmed at the point where the text turns to another matter.
    The words and the figure are the model text as held; nothing
    is formed here.
    """
    text = _text(text)
    named = re.search(
        r"the\s+(?:file|line|tree byte|tree file|whole walk)"
        r"\s+limit[^.;,]*", text, re.I)
    if named:
        return named.group(0).strip()
    stated = re.search(
        r"the\s+[\w ]{0,30}?limit\s+of\s+\d[\d,]*\s*"
        r"(?:bytes|files|entries)[^.;,]*", text, re.I)
    if stated:
        return stated.group(0).strip()
    clauses = []
    for segment in re.split(r"[.;]", text):
        lowered = segment.lower()
        at = lowered.find("limit")
        if at < 0:
            continue
        start = max(lowered.rfind(": ", 0, at),
                    lowered.rfind(", ", 0, at))
        start = start + 2 if start >= 0 else 0
        clause = segment[start:].strip().strip(",").strip()
        cut = clause.lower().find("what follows")
        if cut >= 0:
            clause = clause[:cut].strip()
        clause = re.split(r", with |, and this piece",
                          clause)[0].strip().strip(",")
        if clause:
            clauses.append(clause)
    for clause in clauses:
        if any(char.isdigit() for char in clause):
            return clause
    return clauses[0] if clauses else ""


def _best_limit(reason, dq_text):
    """Return the limit wording a piece entry carries, in order.

    A limit clause stating its figure, from the entry reason or
    from its data quality entry, stands first. Otherwise the data
    quality entry consequence stands, then the reason as held,
    then any limit clause either text carries.
    """
    for text in (reason, dq_text):
        phrase = _limit_phrase(text)
        if phrase and any(char.isdigit() for char in phrase):
            return phrase
    follows = _follows_text(dq_text)
    if follows:
        return follows
    if _text(reason):
        return _text(reason)
    return _limit_phrase(dq_text) or _limit_phrase(reason)


def _follows_text(text):
    """Return the text after the What follows label, or empty."""
    text = _text(text)
    at = text.lower().find("what follows:")
    if at < 0:
        return ""
    return text[at + len("what follows:"):].strip()


def _size_text(value):
    if value is None:
        return ""
    if isinstance(value, bool):
        return _text(value)
    if isinstance(value, (int, float)):
        return "%s bytes" % (value,)
    return _text(value)


def _piece_line(name, size, state, limit):
    """Compose one coverage piece line from model held parts."""
    parts = []
    if name:
        parts.append(name)
    if size:
        parts.append(size)
    state = _text(state)
    limit = _text(limit)
    if state and limit and state.lower() not in limit.lower():
        parts.append(state + ": " + limit)
    elif limit:
        parts.append(limit)
    elif state:
        parts.append(state)
    if not parts:
        return ""
    return COVERAGE_PIECE_LABEL + ": " + ", ".join(parts)


def _entry_line(entry, dq_text=""):
    """Return (line, name, limit) for one model piece entry.

    An entry may stand as a finished line, as a mapping, or as an
    object carrying the piece fields. A finished line stands as
    held. Any other entry is composed from the fields it carries:
    its name or paths, its size, its state, and its limit, where
    the limit may stand as its own field or inside the reason text
    the entry or its data quality entry carries.
    """
    if isinstance(entry, str):
        line = entry.strip()
        if line.startswith(COVERAGE_PIECE_LABEL):
            return line, "", _limit_phrase(line)
        parsed = _parse_inventory_line(line)
        if parsed is not None:
            name, size, state = parsed
            limit = _best_limit("", dq_text) or state
            return _piece_line(name, size, state, limit), name, \
                _limit_phrase(dq_text)
        if line:
            return (COVERAGE_PIECE_LABEL + ": " + line), "", \
                _limit_phrase(line)
        return "", "", ""
    name = _get(entry, "name", "piece_name", "path", "paths",
                "piece", "file", "relative_path")
    if isinstance(name, (tuple, list)):
        name = ", ".join(_text(part) for part in name if _text(part))
    name = _text(name)
    size = _size_text(_get(entry, "size", "size_bytes", "bytes",
                           "file_size"))
    state = _text(_get(entry, "quality_state", "state", "status"))
    reason = _text(_get(entry, "not_read_reason", "reason",
                        "quality_reason", "state_reason"))
    limit = _text(_get(entry, "limit", "limit_crossed",
                       "crossed_limit", "limit_text",
                       "limit_crossed_text", "tree_cut_kind",
                       "cut_kind"))
    if not limit:
        limit = _best_limit(reason, dq_text)
    line = _piece_line(name, size, state, limit)
    return line, name, _limit_phrase(reason) or _limit_phrase(limit)


def _parse_inventory_line(line):
    """Parse one model inventory line, or return None.

    The line form is the form the inventory lines stand in: the
    word Piece, the piece paths, the record class, the size and
    the state, separated by a space, a vertical bar and a space.
    Returns (name, size, state) with the state holding any further
    parts the line carries after the state part.
    """
    stripped = line.strip()
    if not stripped.startswith("Piece "):
        return None
    parts = [part.strip() for part in stripped[len("Piece "):].split("|")]
    if len(parts) < 4:
        return None
    return parts[0], parts[2], " | ".join(parts[3:])


def _dq_map(model):
    """Map a piece first path to the data quality text naming it."""
    held = _get(model, "data_quality", "data_quality_lines")
    found = {}
    if isinstance(held, dict):
        return found
    for line in _lines(held):
        name, _, _rest = line.partition(":")
        if name.strip() and name.strip() not in found:
            found[name.strip()] = line
    return found


def _not_read_in_full(entry):
    """Say whether a model piece entry stands not read in full."""
    if isinstance(entry, dict) or not isinstance(entry, (str, bytes)):
        text = _get(entry, "text", "content")
        state = _text(_get(entry, "quality_state", "state",
                           "status"))
        flag = _get(entry, "not_read_in_full", "not_read",
                    "partial")
        if flag:
            return True
        if state and state.lower() != "read in full":
            return True
        return text is None and bool(state or _get(
            entry, "not_read_reason", "reason"))
    return False


def _coverage_piece_data(model):
    """Collect the coverage piece lines the model carries.

    Returns (lines, limits). Lines stand in the order the model
    carries them: explicit piece entries first in their order,
    then any piece the model piece list or the model inventory
    lines carry as not read in full and no earlier entry covered,
    in piece inventory order. Limits collects each distinct limit
    clause those entries carry, in entry order.
    """
    lines = []
    limits = []
    covered = set()
    dq = _dq_map(model)

    def add(line, name, limit):
        if not line:
            return
        if line in lines:
            return
        lines.append(line)
        if name:
            covered.add(name.split(",")[0].strip())
            covered.add(name)
        if limit and any(char.isdigit() for char in limit) \
                and limit not in limits:
            limits.append(limit)

    for field in _PIECE_LIST_FIELDS:
        held = _get(model, field)
        if held is None:
            continue
        entries = held.values() if isinstance(held, dict) else held
        if isinstance(entries, (str, bytes)):
            entries = [entries]
        for entry in entries or []:
            if isinstance(entry, str) and entry.strip().startswith(
                    COVERAGE_PIECE_LABEL):
                add(entry.strip(), "", _limit_phrase(entry))
                continue
            name = ""
            if not isinstance(entry, str):
                raw = _get(entry, "name", "piece_name", "path",
                           "paths", "piece", "file", "relative_path")
                if isinstance(raw, (tuple, list)):
                    raw = raw[0] if raw else ""
                name = _text(raw)
            line, _name, limit = _entry_line(entry, dq.get(name, ""))
            add(line, name or _name, limit)
    for field in _PIECE_SOURCE_FIELDS:
        held = _get(model, field)
        if not held:
            continue
        for entry in held:
            if not _not_read_in_full(entry):
                continue
            raw = _get(entry, "name", "piece_name", "path", "paths",
                       "piece", "file", "relative_path")
            if isinstance(raw, (tuple, list)):
                raw = raw[0] if raw else ""
            name = _text(raw)
            if name and name in covered:
                continue
            line, _name, limit = _entry_line(entry, dq.get(name, ""))
            add(line, name, limit)
    cut_paths = _get(model, "tree_cut_paths", "cut_paths",
                     "not_visited_paths")
    if cut_paths:
        cut_kind = _text(_get(model, "tree_cut_kind", "cut_kind"))
        inventory = {}
        for inv_line in _lines(_get(model, "inventory_lines",
                                    "piece_inventory", "inventory")):
            parsed = _parse_inventory_line(inv_line)
            if parsed is not None:
                inventory[parsed[0].split(",")[0].strip()] = parsed
        for path in cut_paths:
            name = _text(path)
            if not name or name in covered:
                continue
            parsed = inventory.get(name)
            size = parsed[1] if parsed else ""
            add(_piece_line(name, size, "not read in full",
                            cut_kind), name, _limit_phrase(cut_kind))
    inventory_lines = _lines(_get(model, "inventory_lines",
                                  "piece_inventory", "inventory"))
    for inv_line in inventory_lines:
        parsed = _parse_inventory_line(inv_line)
        if parsed is None:
            continue
        name, size, state = parsed
        if state.strip().lower() == "read in full":
            continue
        first = name.split(",")[0].strip()
        if first in covered or name in covered:
            continue
        dq_text = dq.get(first, "")
        limit = _best_limit("", dq_text)
        add(_piece_line(name, size, state, limit), name,
            _limit_phrase(dq_text))
    return lines, limits


def _partial_line(model, piece_lines):
    """Return the Coverage partial line the model carries, or empty.

    A partial reading stands where the model states one: a reading
    field or a partial flag carrying it, a partial line or partial
    wording in the coverage the model holds, a run cost reading of
    partial, or a piece carried as not read in full. Where the
    model carries a finished partial line, that line stands as
    held; otherwise the plain line stands.
    """
    held = _text(_get(model, "coverage_partial_line", "partial_line",
                      "coverage_partial"))
    if held:
        if held.lower().startswith("coverage partial"):
            return held if "partial report" in held.lower() else ""
        return "Coverage partial: " + held
    reading = _text(_get(model, "reading", "reading_state",
                         "run_reading"))
    if reading.lower() == "partial":
        return "Coverage partial: partial report"
    if _get(model, "partial_reading", "is_partial", "partial"):
        return "Coverage partial: partial report"
    run_cost = _get(model, "run_cost_line", "run_cost")
    if isinstance(run_cost, dict):
        if _text(run_cost.get("reading")).lower() == "partial":
            return "Coverage partial: partial report"
    elif isinstance(run_cost, str) and \
            "reading: partial" in run_cost.lower():
        return "Coverage partial: partial report"
    for line in _lines(_get(model, "header_lines", "header")) + \
            _lines(_get(model, "coverage_lines")) + \
            [_text(_get(model, "coverage"))]:
        lowered = line.lower()
        if lowered.startswith("coverage partial"):
            if "partial report" in lowered:
                return line.strip()
            continue
        if "partial report" in lowered or "partial reading" in lowered:
            return "Coverage partial: partial report"
    if piece_lines:
        return "Coverage partial: partial report"
    return ""


def _run_cost_data(model):
    """Return the run cost mapping the model carries, or None.

    The mapping may stand as the run cost field itself, as a counts
    mapping beside it, or as single fields on the model. Keys are
    the run cost part keys: files_visited, files_opened,
    bytes_read, entries_visited, limit and reading.
    """
    held = _get(model, "run_cost_line", "run_cost")
    if isinstance(held, dict):
        return dict(held)
    held = _get(model, "run_cost_counts", "capture_counts", "counts")
    if isinstance(held, dict):
        return dict(held)
    data = {}
    for key in ("files_visited", "files_opened", "bytes_read",
                "entries_visited", "limit", "reading"):
        value = _get(model, key)
        if value is not None:
            data[key] = value
    return data or None


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
    for field in ("coverage", "coverage_statement",
                  "header_coverage_statement"):
        held_coverage = _get(model, field)
        if isinstance(held_coverage, str) and held_coverage.strip():
            line = held_coverage.strip()
            if not any(existing.strip() == line for existing in lines):
                lines.append(line)
    piece_lines, _limits = _coverage_piece_data(model)
    partial = _partial_line(model, piece_lines)
    if partial and partial not in lines:
        lines.append(partial)
    standing = set()
    for existing in lines:
        if existing.strip().startswith(COVERAGE_PIECE_LABEL):
            value = existing.strip()[len(COVERAGE_PIECE_LABEL):]
            standing.add(value.lstrip(": ").split("|")[0]
                         .split(",")[0].strip())
    for line in piece_lines:
        value = line[len(COVERAGE_PIECE_LABEL):]
        name = value.lstrip(": ").split("|")[0].split(",")[0].strip()
        if line not in lines and name not in standing:
            lines.append(line)
    for extra in ("coverage_lines", "record_state_line", "trigger_line"):
        for line in _lines(_get(model, extra)):
            if line.strip().startswith(COVERAGE_PIECE_LABEL):
                value = line.strip()[len(COVERAGE_PIECE_LABEL):]
                name = value.lstrip(": ").split("|")[0] \
                    .split(",")[0].strip()
                if name in standing or line in lines:
                    continue
                standing.add(name)
            if line not in lines:
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
    piece_lines, limits = _coverage_piece_data(model)
    partial = _partial_line(model, piece_lines)
    run_cost = _get(model, "run_cost_line", "run_cost")
    data = _run_cost_data(model)
    if data is not None:
        order = (("Files visited", ("files_visited", "visited")),
                 ("Files opened", ("files_opened", "opened")),
                 ("Bytes read", ("bytes_read", "read_bytes")),
                 ("Entries visited", ("entries_visited", "entries")),
                 ("Limit", ("limit", "limit_crossed")),
                 ("Reading", ("reading", "reading_state")))
        parts = ["Run cost"]
        for label, keys in order:
            value = None
            for key in keys:
                if key in data and data[key] is not None:
                    value = data[key]
                    break
            if value is None and label == "Limit" and limits:
                value = "; ".join(limits)
            if value is None and label == "Reading" and partial:
                value = "partial"
            if value is not None:
                parts.append("%s: %s" % (label, value))
        lines.append(" | ".join(parts))
    elif _lines(run_cost):
        held_lines = _lines(run_cost)
        if partial and not any("reading:" in line.lower()
                                for line in held_lines):
            held_lines[0] = held_lines[0] + " | Reading: partial"
        lines.extend(held_lines)
    elif partial:
        parts = ["Run cost"]
        if limits:
            parts.append("Limit: " + "; ".join(limits))
        parts.append("Reading: partial")
        lines.append(" | ".join(parts))
    terms = _section_lines(model, "terms_lines", "terms")
    if terms:
        lines.append("Terms")
        lines.extend(terms)
    lines = [line for line in lines if line.strip()]
    return "\n".join(lines) + "\n"
