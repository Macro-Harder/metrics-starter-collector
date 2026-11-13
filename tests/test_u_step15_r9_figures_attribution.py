"""Step 15 fix round 9 tests: figure words in full, falsity scope.

Each charged case pins one fix register item in the figure and
attribution machinery of derivation_core.py. F15-68 (CB8-7 and
C8-3): figure words stopped at the hundred tail, so "one
hundred and five" read as its tail or the hundred alone, "one
thousand" read as no figure at all, and "five point five five"
read as its last word; a denial naming the true figure therefore
took out a different standing figure and failed against its own.
Figure words read in full: hundred forms with and tails and
compound tails, thousand forms and their compounds, and point
forms with multi part tails, with the F15-53 and F15-61 digit,
tens compound, plain hundred and single tail point forms
holding as controls. F15-69 (CB8-8): the attribution denial
scope took only the marker sets, so a recorded for part carrying
a falsity predicate (in error, is false, wrong, incorrect,
mistaken) attributed its step at tier 0, ahead of a genuine
recorded for part, and where a denial and a genuine recorded
for shared one comma part the whole part was denial scoped and
the line first Step token fallback landed on the denied step.
A falsity carrying recorded for part never attributes, on
either side; a genuine recorded for sharing a part with a
denial still governs; and the fallback never lands on a step
named only inside denial scope. The F15-40, F15-48 and F15-57
tier precedence and nearest first controls hold. Assertions pin
the parser result as a whole and the full printed figures.
"""
import unittest

from metrics_starter_collector.derivation_core import _t4_banked_durations
from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, path_ledger,
                                     row_block, run_tool)

DATE_ONLY_LINE = "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.\n"
T4_MISSING_SHOWS = ("no banked state and no decision item count "
                    "stands in the feeder records for this metric")
T4_STATEMENT = (
    "Statement line: the row is shown without its queue cross check, "
    "from the BANKED interval durations standing in the feeder "
    "records, with only the decision table cross check absent.")


def capture(root):
    from metrics_starter_collector.shell_reader import capture_read
    return capture_read(root)


class TestStep15Round9FiguresAttribution(FixtureTestCase):

    # ------------------------------------------------------------ shared

    def _report(self, note_text):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            DATE_ONLY_LINE + note_text, steps="1, 2, 3")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        return root, result.stdout

    def _assert_stands(self, note_text, parsed, wait_text):
        root, report = self._report(note_text)
        self.assertEqual(_t4_banked_durations(capture(root)), parsed)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present", "T-4")
        self.assertIn(wait_text, t4)
        return root, report

    def _assert_taken_out(self, note_text):
        root, report = self._report(note_text)
        self.assertEqual(_t4_banked_durations(capture(root)), [])
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "missing", "T-4")
        self.assertIn(T4_MISSING_SHOWS, t4)
        self.assertNotIn("banked wait", report)
        return root, report

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

    # ---------------------------------------------------------- F15-68

    def test_f15_68_hundred_and_tail_same_figure_taken_out(self):
        for standing, words in (
                ("105", "one hundred and five"),
                ("235", "two hundred and thirty five"),
                ("250", "two hundred and fifty"),
                ("150", "one hundred and fifty")):
            note = ("Step 1 BANKED interval duration " + standing +
                    " hours stands, and no interval duration " + words +
                    " hours was recorded for Step 1.")
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_68_hundred_and_tail_different_figure_stands(self):
        for standing, words, wait in (
                ("5", "one hundred and five",
                 "Step 1 banked wait 5 hours"),
                ("5", "two hundred and fifty",
                 "Step 1 banked wait 5 hours"),
                ("250", "one hundred and fifty",
                 "Step 1 banked wait 250 hours")):
            note = ("Step 1 BANKED interval duration " + standing +
                    " hours stands, and no interval duration " + words +
                    " hours was recorded for Step 1.")
            with self.subTest(note=note):
                self._assert_stands(
                    note, [(1, float(standing), True)], wait)

    def test_f15_68_thousand_same_figure_taken_out(self):
        for standing, words in (("1000", "one thousand"),
                                ("2000", "two thousand")):
            note = ("Step 1 BANKED interval duration " + standing +
                    " hours stands, and no interval duration " + words +
                    " hours was recorded for Step 1.")
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_68_thousand_different_figure_stands(self):
        for words in ("one thousand", "two thousand"):
            note = ("Step 1 BANKED interval duration 5 hours stands, "
                    "and no interval duration " + words +
                    " hours was recorded for Step 1.")
            with self.subTest(note=note):
                self._assert_stands(
                    note, [(1, 5.0, True)],
                    "Step 1 banked wait 5 hours")

    def test_f15_68_thousand_compound_figures_read_whole(self):
        for standing, words in (
                ("1500", "one thousand five hundred"),
                ("1005", "one thousand and five")):
            note = ("Step 1 BANKED interval duration " + standing +
                    " hours stands, and no interval duration " + words +
                    " hours was recorded for Step 1.")
            with self.subTest(note=note):
                self._assert_taken_out(note)
        self._assert_stands(
            "Step 1 BANKED interval duration 5 hours stands, and no "
            "interval duration one thousand and five hours was "
            "recorded for Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_68_point_multi_tail_same_figure_taken_out(self):
        for standing, words in (
                ("5.55", "five point five five"),
                ("5.555", "five point five five five")):
            note = ("Step 1 BANKED interval duration " + standing +
                    " hours stands, and no interval duration " + words +
                    " hours was recorded for Step 1.")
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_68_point_multi_tail_different_figure_stands(self):
        for standing in ("5", "5.5"):
            note = ("Step 1 BANKED interval duration " + standing +
                    " hours stands, and no interval duration five "
                    "point five five hours was recorded for Step 1.")
            with self.subTest(note=note):
                self._assert_stands(
                    note, [(1, float(standing), True)],
                    "Step 1 banked wait " + standing + " hours")

    def test_f15_68_control_existing_figure_forms_hold(self):
        self._assert_stands(
            "Step 1 BANKED interval duration 5 hours stands, and no "
            "interval duration 100 hours was recorded for Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")
        self._assert_stands(
            "Step 1 BANKED interval duration 5 hours stands, and no "
            "interval duration forty two hours was recorded for "
            "Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")
        for standing, words in (
                ("105", "one hundred five"),
                ("235", "two hundred thirty five"),
                ("5.5", "five point five"),
                ("25.5", "twenty five point five")):
            note = ("Step 1 BANKED interval duration " + standing +
                    " hours stands, and no interval duration " + words +
                    " hours was recorded for Step 1.")
            with self.subTest(note=note):
                self._assert_taken_out(note)

    # ---------------------------------------------------------- F15-69

    def test_f15_69_in_error_part_never_attributes(self):
        root, report = self._report(
            "BANKED interval duration 5 hours stands, recorded for "
            "Step 2 in error.")
        self.assertEqual(_t4_banked_durations(capture(root)),
                         [(None, 5.0, True)])
        self.assertNotIn("Step 2 banked wait", report)

    def test_f15_69_falsity_predicates_never_attribute(self):
        for predicate in ("is false", "is incorrect", "is mistaken"):
            note = ("BANKED interval duration 5 hours stands, the "
                    "claim recorded for Step 2 " + predicate + ".")
            with self.subTest(note=note):
                root, report = self._report(note)
                self.assertEqual(
                    _t4_banked_durations(capture(root)),
                    [(None, 5.0, True)])
                self.assertNotIn("Step 2 banked wait", report)

    def test_f15_69_false_claim_nearer_genuine_recorded_for_governs(self):
        self._assert_banked(
            "Step 1 heading: BANKED interval duration 5 hours "
            "stands, the claim recorded for Step 2 is false; "
            "recorded for Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")
        self._assert_banked(
            "Step 1 heading: BANKED interval duration 5 hours "
            "stands, the claim recorded for Step 2 is false, "
            "recorded for Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_69_falsity_on_before_side_genuine_governs(self):
        self._assert_banked(
            "Recorded for Step 1, the claim recorded for Step 2 is "
            "false: BANKED interval duration 5 hours stands.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_69_shared_part_denial_and_genuine_recorded_for(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands, no interval "
            "duration was recorded for Step 2 and the figure "
            "recorded for Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_69_shared_part_falsity_and_genuine_recorded_for(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands, the claim "
            "recorded for Step 2 is false and the figure recorded "
            "for Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_69_fallback_skips_denial_only_step(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands, recorded for "
            "Step 2 in error, Step 3 wait noted.",
            [(3, 5.0, True)], "Step 3 banked wait 5 hours")

    def test_f15_69_controls_recorded_for_precedence_hold(self):
        self._assert_banked(
            "Step 1 heading: BANKED interval duration 5 hours "
            "stands, recorded for Step 2.",
            [(2, 5.0, True)], "Step 2 banked wait 5 hours")
        self._assert_banked(
            "BANKED interval duration 5 hours stands, recorded for "
            "Step 2, recorded for Step 1.",
            [(2, 5.0, True)], "Step 2 banked wait 5 hours")
        self._assert_banked(
            "Step 1 heading: BANKED interval duration 5 hours "
            "stands, no interval duration was recorded for Step 2.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")


if __name__ == "__main__":
    unittest.main()
