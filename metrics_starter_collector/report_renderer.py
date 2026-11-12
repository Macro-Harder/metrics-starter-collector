"""Module 5: report renderer.

Receives the ReportModel from the core and prints the report in the
settled form: header, coverage statement, piece inventory, 17 rows in
starter set order, and a data quality section. Computes nothing.
"""


def render_report(model):
    """Print the ReportModel and return the report text."""
    lines = []
    lines.extend(model.header_lines)
    lines.append("")
    lines.extend(model.inventory_lines)
    lines.append("")
    if model.no_usable:
        lines.append("No usable records: the tree holds no recognisable "
                     "record pieces, so no metric rows stand.")
        lines.append("")
        lines.append("## Data quality")
        lines.append("")
        lines.extend(model.data_quality)
        return "\n".join(lines) + "\n"
    lines.append("## Metric rows")
    lines.append("")
    for result in model.results:
        lines.append("%s | %s | Pointer: %s | %s | %s"
                     % (result.code, result.verdict, result.pointer,
                        result.figures, result.denominator))
        reason = result.reason_text()
        if reason is not None:
            lines.append("Reason: " + reason)
        if result.statement:
            lines.append("Statement line: " + result.statement)
        if result.derived_from:
            lines.append("Derived from line: " + result.derived_from)
        lines.append("")
    lines.append("## Data quality")
    lines.append("")
    for idx, entry in enumerate(model.data_quality):
        if idx:
            lines.append("")
        lines.append(entry)
    return "\n".join(lines) + "\n"
