"""Module entry point: python3 -m metrics_starter_collector ROOT [--report PATH].

Exit codes: 0 completed report, 1 unreadable input, 2 usage error.
"""
import sys

from metrics_starter_collector.derivation_core import derive_report
from metrics_starter_collector.report_renderer import render_report
from metrics_starter_collector.shell_reader import (
    UnreadableInputError, UsageError, capture_read, deliver_report)

USAGE = ("usage: metrics-starter-collector ROOT [--report PATH]")


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    root = None
    report_path = None
    idx = 0
    while idx < len(args):
        arg = args[idx]
        if arg == "--report":
            if report_path is not None:
                sys.stderr.write(USAGE + "\n")
                return 2
            if idx + 1 >= len(args):
                sys.stderr.write(USAGE + "\n")
                return 2
            report_path = args[idx + 1]
            idx += 2
            continue
        if arg.startswith("-"):
            sys.stderr.write(USAGE + "\n")
            return 2
        if root is not None:
            sys.stderr.write(USAGE + "\n")
            return 2
        root = arg
        idx += 1
    if root is None:
        sys.stderr.write(USAGE + "\n")
        return 2
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
