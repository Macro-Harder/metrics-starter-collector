"""Live line tests: the header names the latest timestamp in the tree.

These cases pin finding H-1 of the Step 14 product audit. The shell
reader comparison once carried the date and the hour only, so within
the latest hour the first timestamp met in walk order won whatever
its minutes. Each synthetic case below places the true latest
timestamp where that comparison cannot reach it, and the golden case
pins the value on the real subject tree.
"""
import unittest

from tests.fixture_builder import (FixtureTestCase, GOLDEN_ROOT,
                                     base_case, build_tree, run_tool)


def live_line(report):
    """Return the report live line, or empty if no such line stands."""
    for line in report.splitlines():
        if line.startswith("Live line:"):
            return line
    return ""


class TestLiveLine(FixtureTestCase):

    def test_live_line_later_hour_in_earlier_walked_file_wins(self):
        table = base_case()
        table["audit/step20-a-first.md"] = (
            "# Audit paper\n\n"
            "First note at 2026-11-12 06:10. "
            "Later note at 2026-11-12 06:50.\n")
        table["audit/step20-b-second.md"] = (
            "# Audit paper\n\nRecorded at 2026-11-12 05:55.\n")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            live_line(result.stdout),
            "Live line: latest record timestamp: 2026-11-12 06:50")

    def test_live_line_later_minute_in_later_walked_file_wins(self):
        table = base_case()
        table["audit/step20-a-first.md"] = (
            "# Audit paper\n\nRecorded at 2026-11-12 05:03.\n")
        table["audit/step20-b-second.md"] = (
            "# Audit paper\n\nRun at: 2026-11-12T05:07Z.\n")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            live_line(result.stdout),
            "Live line: latest record timestamp: 2026-11-12T05:07")

    def test_live_line_later_second_in_later_walked_file_wins(self):
        table = base_case()
        table["audit/step20-a-first.md"] = (
            "# Audit paper\n\nRecorded at 2026-11-12 05:07:10.\n")
        table["audit/step20-b-second.md"] = (
            "# Audit paper\n\nRecorded at 2026-11-12 05:07:45.\n")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            live_line(result.stdout),
            "Live line: latest record timestamp: 2026-11-12 05:07:45")

    def test_live_line_on_golden_tree_names_latest_timestamp(self):
        result = run_tool(GOLDEN_ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            live_line(result.stdout),
            "Live line: latest record timestamp: 2026-11-12T05:07")


if __name__ == "__main__":
    unittest.main()
