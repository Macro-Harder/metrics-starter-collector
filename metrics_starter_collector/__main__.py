"""Module entry point for the metrics starter set collector.

The command grammar, stated once in the design plan and applied
here exactly: the command name first, then the one root argument,
then the optional report argument in its two word form, the word
--report followed by its file path as the next argument. No
argument, an extra argument, an unknown option, a repeated report
argument, and a report argument with no file path after it are
usage errors and exit 2. Help and version forms are barred in
version 1 and count as unknown options. A completed report exits
0, and a root that cannot be read at all exits 1.
"""
import sys

from metrics_starter_collector.derivation_core import derive_report
from metrics_starter_collector.report_renderer import render_report
from metrics_starter_collector.shell_reader import (
    UnreadableInputError, UsageError, capture_read, deliver_report)

USAGE = "usage: metrics-starter-collector ROOT [--report PATH]"


def _usage_error():
    sys.stderr.write(USAGE + "\n")
    return 2


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        return _usage_error()
    root = args[0]
    if root.startswith("-"):
        return _usage_error()
    report_path = None
    index = 1
    while index < len(args):
        word = args[index]
        if word != "--report":
            return _usage_error()
        if report_path is not None:
            return _usage_error()
        if index + 1 >= len(args):
            return _usage_error()
        report_path = args[index + 1]
        index += 2
    try:
        captured = capture_read(root)
    except UnreadableInputError as exc:
        sys.stderr.write("error: %s\n" % (exc,))
        return 1
    model = derive_report(captured)
    text = render_report(model)
    try:
        deliver_report(text, root, report_path)
    except UsageError as exc:
        sys.stderr.write("error: %s\n" % (exc,))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
