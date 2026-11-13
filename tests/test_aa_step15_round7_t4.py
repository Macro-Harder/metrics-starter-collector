"""Step 15 fix round 7 tests: T-4 neighbourhood attribution and counts.

Each case pins one fix round 7 item in the T-4 machinery of
derivation_core.py. F15-48: the F15-40 clause attribution in
_t4_banked_durations took the step named inside the mention own
clause part only, so a step named in an adjacent part of the
mention own sentence scope was dropped and the line first Step
token printed for the wrong step. The attribution scope is the
mention full clause neighbourhood, the before and after fragments
the duration helpers compute for the mention. Precedence, pinned
by the cases below: the mention own part governs first; where the
own part names no step, a step named in an after part governs,
nearest part first, because a part after the figure states what
the figure was recorded for; where no after part names a step, a
step named in a before part governs, nearest part first; where no
part of the neighbourhood names a step, the line first Step token
stands as the fallback. F15-52: _derive_t4 rested the banked item
counts on a queue piece parsing to a decision item table, testing
only that the parse was not None, so a header only table, parsing
to an empty list, set the counts claim while D-1 on the same
report stated the feeder holds 0 decision items. The counts ground
requires a non empty parsed item list, in the canonical and the
duplicate positions alike. Control cases pin the behaviour that
must not move: the F15-40 own clause forms, the two mention line,
the fallback, and a queue with one full item row.
Every case asserts the full printed figures field of its row, and
the full reason or statement line where that line is the evidence,
never a substring of them.
"""
import unittest

from metrics_starter_collector.derivation_core import _t4_banked_durations
from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, path_ledger,
                                     queue_file, row_block, run_tool)

DATE_ONLY_LINE = "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.\n"
QUEUE_ROW_8 = ("| Q-1 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | "
               "2026-11-01 17:00 |")
HEADER_ONLY_QUEUE = ("# Decision queue\n\n"
                     "| Item | Origin step | Raised | Presented | Ruled |\n"
                     "| --- | --- | --- | --- | --- |\n")
SHORT_ROW_QUEUE = HEADER_ONLY_QUEUE + "| Q-1 |\n"
T4_STATEMENT = (
    "Statement line: the row is shown without its queue cross check, "
    "from the BANKED interval durations standing in the feeder "
    "records, with only the decision table cross check absent.")
T4_WEAKER_REASON = (
    "Reason: What the record shows: a decision queue piece stands "
    "in the capture, but no queue piece carries readable decision "
    "items, so no banked item count stands in the feeder records, "
    "and the path ledger holds no banked state What follows: "
    "missing-field no complete decision queue stands, so no banked "
    "item count can form and no wait figure stands")
T4_BANKED_WEAKER_REASON = (
    "Reason: What the record shows: banked states stand in the "
    "feeder records and every duration is absent, and no banked "
    "item count stands because no queue piece carries readable "
    "decision items What follows: missing-field a count of items "
    "is not a time, and the degraded form does not apply because "
    "the durations themselves are absent, not only the cross "
    "check, so no wait figure stands")
T4_COUNTS_REASON = (
    "Reason: What the record shows: banked states and item counts "
    "stand in the feeder records and every duration is absent What "
    "follows: missing-field a count of items is not a time, and the "
    "degraded form does not apply because the durations themselves "
    "are absent, not only the cross check, so no wait figure stands")
D1_ZERO_REASON = (
    "Reason: What the record shows: the governing feeder holds 0 "
    "decision items and no item is ruled: every item stands open "
    "or in date only form, so no latency can form What follows: "
    "missing-field no item is ruled, so no latency, median or "
    "longest can form, and an open item is never counted as a "
    "latency of zero")


def capture(root):
    from metrics_starter_collector.shell_reader import capture_read
    return capture_read(root)


class TestStep15Round7T4(FixtureTestCase):

    # ------------------------------------------------------------ F15-48

    def _date_only_root(self, note):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            DATE_ONLY_LINE + note, steps="1, 2, 3")
        return build_tree(table)

    def _assert_banked(self, note, parsed, figures):
        root = self._date_only_root(note)
        self.assertEqual(_t4_banked_durations(capture(root)), parsed)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "T-4")
        assert_verdict(self, block, "present", "T-4")
        lines = block.splitlines()
        self.assertEqual(
            lines[0],
            "T-4 | present | Pointer: PATH-LEDGER.md | " + figures +
            " | denominator decision items and banked states in the tree")
        self.assertEqual(lines[1], T4_STATEMENT)
        return result.stdout

    def test_f15_48_semicolon_subordinate_step_attributes(self):
        self._assert_banked(
            "Step 1 opened the run; for Step 2, BANKED interval "
            "duration 5 hours stands.",
            [(2, 5.0, True)], "Step 2 banked wait 5 hours")

    def test_f15_48_colon_part_step_attributes(self):
        self._assert_banked(
            "Step 1 summary: Step 3 note: BANKED interval duration "
            "5 hours stands.",
            [(3, 5.0, True)], "Step 3 banked wait 5 hours")

    def test_f15_48_step_after_figure_attributes(self):
        self._assert_banked(
            "Note for Step 2: BANKED interval duration 5 hours, "
            "recorded for Step 1, stands.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_48_step_after_figure_governs_over_before_part(self):
        self._assert_banked(
            "Note for Step 3: BANKED interval duration 5 hours, "
            "recorded for Step 2, stands.",
            [(2, 5.0, True)], "Step 2 banked wait 5 hours")

    def test_f15_48_own_part_governs_over_adjacent_parts(self):
        self._assert_banked(
            "For Step 2, Step 1 BANKED interval duration 5 hours "
            "stands, recorded for Step 3.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_48_control_own_clause_naming_step1(self):
        self._assert_banked(
            "Note: No interval duration was recorded for Step 2, "
            "but Step 1 BANKED interval duration 5 hours stands.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_48_control_two_mentions_each_own_step(self):
        self._assert_banked(
            "Step 2 BANKED interval duration 3 hours stands, and "
            "Step 1 BANKED interval duration 5 hours stands.",
            [(2, 3.0, True), (1, 5.0, True)],
            "Step 2 banked wait 3 hours; Step 1 banked wait 5 hours")

    def test_f15_48_control_fallback_line_first_token_outside_sentence(self):
        self._assert_banked(
            "Step 1 opened the run. BANKED interval duration "
            "5 hours stands.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    # ------------------------------------------------------------ F15-52

    def _assert_zero_item_queue(self, root, d1_pointer):
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        t4 = row_block(result.stdout, "T-4")
        assert_verdict(self, t4, "present but not derivable", "T-4")
        lines = t4.splitlines()
        self.assertEqual(
            lines[0],
            "T-4 | present but not derivable | Pointer: "
            "PATH-LEDGER.md | no figure stands | denominator "
            "decision items and banked states in the tree")
        self.assertEqual(lines[1], T4_WEAKER_REASON)
        d1 = row_block(result.stdout, "D-1")
        assert_verdict(self, d1, "present but not derivable", "D-1")
        dlines = d1.splitlines()
        self.assertEqual(
            dlines[0],
            "D-1 | present but not derivable | Pointer: " +
            d1_pointer + " | no median and no longest figure stands "
            "| denominator decision items in the governing feeder")
        self.assertEqual(dlines[1], D1_ZERO_REASON)
        self.assertEqual(
            dlines[2],
            "Statement line: the in tree " + d1_pointer + " in the "
            "named form supplied the row, as the foundation "
            "statement for this row.")
        return result.stdout

    def test_f15_52_header_only_canonical_weaker_form(self):
        table = base_case()
        table["DECISION-QUEUE.md"] = HEADER_ONLY_QUEUE
        self._assert_zero_item_queue(build_tree(table),
                                     "DECISION-QUEUE.md")

    def test_f15_52_header_plus_short_row_canonical_weaker_form(self):
        table = base_case()
        table["DECISION-QUEUE.md"] = SHORT_ROW_QUEUE
        self._assert_zero_item_queue(build_tree(table),
                                     "DECISION-QUEUE.md")

    def test_f15_52_header_only_duplicate_weaker_form(self):
        table = base_case()
        table["DECISION-QUEUE.md"] = ""
        table["sub/DECISION-QUEUE.md"] = HEADER_ONLY_QUEUE
        self._assert_zero_item_queue(build_tree(table),
                                     "sub/DECISION-QUEUE.md")

    def test_f15_52_header_plus_short_row_duplicate_weaker_form(self):
        table = base_case()
        table["DECISION-QUEUE.md"] = ""
        table["sub/DECISION-QUEUE.md"] = SHORT_ROW_QUEUE
        self._assert_zero_item_queue(build_tree(table),
                                     "sub/DECISION-QUEUE.md")

    def test_f15_52_header_only_beside_banked_state_weaker_form(self):
        table = base_case()
        table["DECISION-QUEUE.md"] = HEADER_ONLY_QUEUE
        table["PATH-LEDGER.md"] = table["PATH-LEDGER.md"] + \
            "\nStep 1 BANKED state is recorded.\n"
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        t4 = row_block(result.stdout, "T-4")
        assert_verdict(self, t4, "present but not derivable", "T-4")
        lines = t4.splitlines()
        self.assertEqual(
            lines[0],
            "T-4 | present but not derivable | Pointer: "
            "PATH-LEDGER.md | banked states stand and no duration "
            "figure stands | denominator decision items and banked "
            "states in the tree")
        self.assertEqual(lines[1], T4_BANKED_WEAKER_REASON)
        d1 = row_block(result.stdout, "D-1")
        assert_verdict(self, d1, "present but not derivable", "D-1")
        self.assertEqual(d1.splitlines()[1], D1_ZERO_REASON)

    def _assert_counts_stand(self, root):
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        t4 = row_block(result.stdout, "T-4")
        assert_verdict(self, t4, "present but not derivable", "T-4")
        lines = t4.splitlines()
        self.assertEqual(
            lines[0],
            "T-4 | present but not derivable | Pointer: "
            "PATH-LEDGER.md | banked item counts stand and no "
            "duration figure stands | denominator decision items "
            "and banked states in the tree")
        self.assertEqual(lines[1], T4_COUNTS_REASON)
        return result.stdout

    def test_f15_52_control_full_item_row_canonical_counts_stand(self):
        table = base_case()
        table["DECISION-QUEUE.md"] = queue_file([QUEUE_ROW_8])
        root = build_tree(table)
        report = self._assert_counts_stand(root)
        d1 = row_block(report, "D-1")
        assert_verdict(self, d1, "present", "D-1")
        self.assertEqual(
            d1.splitlines()[0],
            "D-1 | present | Pointer: DECISION-QUEUE.md | median "
            "8 hours; longest 8 hours; Item Q-1: raised 2026-11-01 "
            "09:00, ruled 2026-11-01 17:00, latency 8 hours | "
            "denominator decision items in the governing feeder")

    def test_f15_52_control_full_item_row_duplicate_counts_stand(self):
        table = base_case()
        table["DECISION-QUEUE.md"] = ""
        table["sub/DECISION-QUEUE.md"] = queue_file([QUEUE_ROW_8])
        self._assert_counts_stand(build_tree(table))


if __name__ == "__main__":
    unittest.main()
