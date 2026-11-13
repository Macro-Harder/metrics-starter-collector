"""Step 15 fix round 11 tests: attribution segment bounds, the bare
recorded for test, and standalone falsity scope.

Each charged case pins one fix register item in the attribution
machinery of derivation_core.py. F15-93 (C10-2 with CB10-11): the
segment bounds took only and, but, or and while of the closure
reading's join set, and no dash, so yet, nor, so, as, whereas,
although, though, since and because joins and an em dash all left
a genuine recorded for scoped by a preceding denial or falsity.
The segment bounds are charged to take the join set the closure
fragment reading takes, plus the dash bound CB10-11 names.
F15-94 (CB10-12): the bare recorded for test was an exact match,
so inert tails (by Lane, yesterday, in the log) and leads (then,
also) defeated the adjacent falsity completion and the denied
step attributed. F15-95 (C10-3): a standalone falsity part with
the listed word wrong on a carrier subject (the claim was wrong,
recorded for Step 2) was read by the listed word test as a denial
of the duration itself and erased the standing figure whole, the
genuine Step 1 part included, where the is false twin prints the
stepless figure standing. Assertions pin the parser result as a
whole and the full printed figures, as the round 10 attribution
module does.
"""
import unittest

from metrics_starter_collector.derivation_core import _t4_banked_durations
from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, path_ledger,
                                     row_block, run_tool)

DATE_ONLY_LINE = "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.\n"
T4_STATEMENT = (
    "Statement line: the row is shown without its queue cross check, "
    "from the BANKED interval durations standing in the feeder "
    "records, with only the decision table cross check absent.")


def capture(root):
    from metrics_starter_collector.shell_reader import capture_read
    return capture_read(root)


class TestStep15Round11Attribution(FixtureTestCase):

    # ------------------------------------------------------------ shared

    def _report(self, note_text):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            DATE_ONLY_LINE + note_text, steps="1, 2, 3")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        return root, result.stdout

    def _assert_banked(self, note, parsed, figures):
        root, report = self._report(note)
        self.assertEqual(_t4_banked_durations(capture(root)), parsed)
        block = row_block(report, "T-4")
        assert_verdict(self, block, "present", "T-4")
        lines = block.splitlines()
        self.assertEqual(
            lines[0],
            "T-4 | present | Pointer: PATH-LEDGER.md | " + figures +
            " | denominator decision items and banked states in the tree")
        self.assertEqual(lines[1], T4_STATEMENT)
        return root, report

    def _assert_stepless(self, note):
        return self._assert_banked(
            note, [(None, 5.0, True)], "banked wait 5 hours")

    # ---------------------------------------------------------- F15-93

    def test_f15_93_denial_round10_conjunctions_genuine_governs(self):
        for conjunction in ("yet", "nor", "so", "as", "whereas",
                            "although", "though"):
            note = ("BANKED interval duration 5 hours stands, no "
                    "interval duration was recorded for Step 2 " +
                    conjunction + " the figure recorded for Step 1.")
            with self.subTest(note=note):
                self._assert_banked(
                    note, [(1, 5.0, True)],
                    "Step 1 banked wait 5 hours")

    def test_f15_93_denial_since_because_genuine_governs(self):
        for conjunction in ("since", "because"):
            note = ("BANKED interval duration 5 hours stands, no "
                    "interval duration was recorded for Step 2 " +
                    conjunction + " the figure recorded for Step 1.")
            with self.subTest(note=note):
                self._assert_banked(
                    note, [(1, 5.0, True)],
                    "Step 1 banked wait 5 hours")

    def test_f15_93_falsity_yet_genuine_governs(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands, the claim "
            "recorded for Step 2 is false yet the figure recorded "
            "for Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_93_em_dash_join_genuine_governs(self):
        for note in (
                "BANKED interval duration 5 hours stands, no interval "
                "duration was recorded for Step 2 \u2014 the figure "
                "recorded for Step 1.",
                "BANKED interval duration 5 hours stands, the claim "
                "recorded for Step 2 is false \u2014 the figure "
                "recorded for Step 1."):
            with self.subTest(note=note):
                self._assert_banked(
                    note, [(1, 5.0, True)],
                    "Step 1 banked wait 5 hours")

    def test_f15_93_fallback_yet_skips_scoped_step(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands, the figure "
            "recorded for Step 2 is invalid yet Step 3 was noted.",
            [(3, 5.0, True)], "Step 3 banked wait 5 hours")

    def test_f15_93_controls_and_but_or_while_still_govern(self):
        for conjunction in ("and", "but", "or", "while"):
            note = ("BANKED interval duration 5 hours stands, no "
                    "interval duration was recorded for Step 2 " +
                    conjunction + " the figure recorded for Step 1.")
            with self.subTest(note=note):
                self._assert_banked(
                    note, [(1, 5.0, True)],
                    "Step 1 banked wait 5 hours")

    # ---------------------------------------------------------- F15-94

    def test_f15_94_inert_tails_complete_bare_recorded_for(self):
        for tail in ("by Lane", "yesterday", "in the log"):
            note = ("BANKED interval duration 5 hours stands, the "
                    "recording is in error, recorded for Step 2 " +
                    tail + ".")
            with self.subTest(note=note):
                root, report = self._assert_stepless(note)
                self.assertNotIn("Step 2 banked wait", report)

    def test_f15_94_inert_leads_complete_bare_recorded_for(self):
        for note in (
                "BANKED interval duration 5 hours stands, the "
                "recording is in error, then recorded for Step 2.",
                "BANKED interval duration 5 hours stands, the claim "
                "is false, also recorded for Step 2."):
            with self.subTest(note=note):
                root, report = self._assert_stepless(note)
                self.assertNotIn("Step 2 banked wait", report)

    def test_f15_94_inert_tail_then_genuine_governs(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands, the recording "
            "is in error, recorded for Step 2 by Lane, recorded "
            "for Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_94_control_subject_carrying_part_not_completed(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands, the recording "
            "is in error, the figure recorded for Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")
        self._assert_banked(
            "BANKED interval duration 5 hours stands, the claim "
            "recorded for Step 2 is false, recorded for Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    # ---------------------------------------------------------- F15-95

    def test_f15_95_standalone_wrong_carrier_figure_stands_stepless(self):
        for subject in ("the claim was wrong", "the record was wrong",
                        "that note was wrong"):
            note = ("BANKED interval duration 5 hours stands, " +
                    subject + ", recorded for Step 2.")
            with self.subTest(note=note):
                root, report = self._assert_stepless(note)
                self.assertNotIn("Step 2 banked wait", report)

    def test_f15_95_standalone_wrong_then_genuine_governs(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands, the claim was "
            "wrong, recorded for Step 2, recorded for Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_95_control_is_false_twin_stepless(self):
        root, report = self._assert_stepless(
            "BANKED interval duration 5 hours stands, the claim is "
            "false, recorded for Step 2.")
        self.assertNotIn("Step 2 banked wait", report)

    def test_f15_95_control_duration_denial_still_takes_out(self):
        root, report = self._report(
            "BANKED interval duration 5 hours stands, the duration "
            "was withdrawn.")
        self.assertEqual(_t4_banked_durations(capture(root)), [])
        self.assertNotIn("banked wait", report)

    def test_f15_95_control_claim_wrong_before_unvalued_takes_out(self):
        root, report = self._report(
            "Note: the claim was wrong, an interval duration is "
            "noted for this step.")
        self.assertEqual(_t4_banked_durations(capture(root)), [])
        t2 = row_block(report, "T-2")
        assert_verdict(self, t2, "missing", "T-2")
        self.assertIn("date-only-form", t2)
        self.assertIn("no BANKED, SUSPENDED or halt interval "
                      "duration stands", t2)
        self.assertNotIn("banked wait", report)


if __name__ == "__main__":
    unittest.main()
