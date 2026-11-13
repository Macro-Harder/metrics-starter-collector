"""Step 15 fix round 11 tests: figure scale, grouped mixes, point tails.

Each charged case pins one fix register item in the figure
reading machinery of derivation_core.py. F15-90 (CB10-8):
the figure scale stopped at thousand, so "one million" and
"one billion" read as no figure at all, a denial naming
one million therefore took out a standing figure of another
value by the no figure route, and "one million and five"
read as its tail alone. The scale is a ladder: each scale
word multiplies the group before it by a thousand over the
rung below, its multiplier is the sub scale compound below
it, and its tail is the compound of the rungs below it, so
the ladder reads at million, billion and the rung above
them alike. F15-91 (CB10-9): the mixed digit rule required
literal digits ending in 00, so the comma grouped spelling
of the same round form, "1,000 and five", read as its tail
alone, in both directions. A comma grouped round digit
form takes its word tail as the plain round form does.
F15-92 (CB10-10): point tails took single digit words
only, so a tail naming a two digit value ("five point
fifteen", "point twenty five") fell out of the point form
whole and the value itself read as the figure. A point
tail item may name a two digit value, in one word or in a
tens and unit pair, and its digits stand in the tail as
that value's digits. The settled figure forms of rounds 6
to 10 hold as controls. Assertions pin the direct reading
through _clause_subject and the denial scoping in both
directions: a denial of the same figure takes the standing
figure out, and a denial of a different figure leaves it
standing, the parser result as a whole and the printed
T-4 row.
"""
import unittest

from metrics_starter_collector.derivation_core import (
    _clause_subject, _t4_banked_durations)
from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, path_ledger,
                                     row_block, run_tool)

DATE_ONLY_LINE = "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.\n"
T4_MISSING_SHOWS = ("no banked state and no decision item count "
                    "stands in the feeder records for this metric")


def capture(root):
    from metrics_starter_collector.shell_reader import capture_read
    return capture_read(root)


class TestStep15Round11Figures(FixtureTestCase):

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

    def _denial_note(self, standing, words):
        return ("Step 1 BANKED interval duration " + standing +
                " hours stands, and no interval duration " + words +
                " hours was recorded for Step 1.")

    def _assert_reading(self, words, value):
        step, figure = _clause_subject(
            "no interval duration " + words + " hours was recorded")
        self.assertIsNone(step)
        self.assertEqual(figure, value)

    # ---------------------------------------------------------- F15-90

    def test_f15_90_direct_million_forms(self):
        for words, value in (("one million", 1000000.0),
                             ("two million", 2000000.0),
                             ("one million and five", 1000005.0),
                             ("one million five hundred thousand",
                              1500000.0),
                             ("two hundred and fifty million",
                              250000000.0),
                             ("one hundred million", 100000000.0)):
            with self.subTest(words=words):
                self._assert_reading(words, value)

    def test_f15_90_direct_billion_and_trillion_ladder(self):
        for words, value in (("one billion", 1000000000.0),
                             ("two billion", 2000000000.0),
                             ("one billion and five", 1000000005.0),
                             ("one billion five hundred million",
                              1500000000.0),
                             ("fifteen hundred million", 1500000000.0),
                             ("one trillion", 1000000000000.0),
                             ("two trillion and five", 2000000000005.0)):
            with self.subTest(words=words):
                self._assert_reading(words, value)

    def test_f15_90_direct_hyphenated_scale_forms(self):
        for words, value in (("one-million", 1000000.0),
                             ("one-million-and-five", 1000005.0),
                             ("two-billion", 2000000000.0)):
            with self.subTest(words=words):
                self._assert_reading(words, value)

    def test_f15_90_same_figure_denial_taken_out(self):
        for standing, words in (("1000000", "one million"),
                                ("1000000000", "one billion"),
                                ("1000005", "one million and five")):
            with self.subTest(words=words):
                self._assert_taken_out(self._denial_note(standing, words))
        self._assert_taken_out(
            "No interval duration one million hours was recorded for "
            "Step 1, Step 1 BANKED interval duration 1000000 hours "
            "stands.")

    def test_f15_90_different_figure_denial_stands(self):
        for standing, words in (("5", "one million"),
                                ("5", "one billion"),
                                ("5", "one million and five"),
                                ("1000000", "one billion")):
            with self.subTest(words=words):
                self._assert_stands(
                    self._denial_note(standing, words),
                    [(1, float(standing), True)],
                    "Step 1 banked wait " + standing + " hours")

    def test_f15_90_different_figure_denial_before_stands(self):
        self._assert_stands(
            "No interval duration one million hours was recorded for "
            "Step 1, Step 1 BANKED interval duration 5 hours stands.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_90_control_settled_scale_forms_hold(self):
        for words, value in (("thirteen hundred", 1300.0),
                             ("fifteen hundred thousand", 1500000.0),
                             ("400 and nine", 409.0),
                             ("10,000", 10000.0),
                             ("one hundred thousand", 100000.0),
                             ("eleven hundred thousand", 1100000.0)):
            with self.subTest(words=words):
                self._assert_reading(words, value)
        self._assert_taken_out(
            self._denial_note("1300", "thirteen hundred"))
        self._assert_taken_out(
            self._denial_note("1500000", "fifteen hundred thousand"))

    # ---------------------------------------------------------- F15-91

    def test_f15_91_direct_grouped_mixed_forms(self):
        for words, value in (("1,000 and five", 1005.0),
                             ("1,000 and twenty five", 1025.0),
                             ("10,000 and five", 10005.0),
                             ("2,500 and five", 2505.0),
                             ("1,000,000 and five", 1000005.0),
                             ("100 and five", 105.0)):
            with self.subTest(words=words):
                self._assert_reading(words, value)

    def test_f15_91_same_figure_denial_taken_out(self):
        for standing, words in (("1005", "1,000 and five"),
                                ("10005", "10,000 and five")):
            with self.subTest(words=words):
                self._assert_taken_out(self._denial_note(standing, words))

    def test_f15_91_different_figure_denial_stands(self):
        for standing, words in (("5", "1,000 and five"),
                                ("1000", "1,000 and five"),
                                ("1005", "10,000 and five")):
            with self.subTest(words=words):
                self._assert_stands(
                    self._denial_note(standing, words),
                    [(1, float(standing), True)],
                    "Step 1 banked wait " + standing + " hours")

    # ---------------------------------------------------------- F15-92

    def test_f15_92_direct_point_two_digit_tails(self):
        for words, value in (("five point fifteen", 5.15),
                             ("five point twenty five", 5.25),
                             ("point fifteen", 0.15),
                             ("point twenty five", 0.25),
                             ("five point oh fifteen", 5.015),
                             ("five point ten", 5.1),
                             ("point eleven", 0.11),
                             ("five point sixteen", 5.16)):
            with self.subTest(words=words):
                self._assert_reading(words, value)

    def test_f15_92_same_figure_denial_taken_out(self):
        for standing, words in (("5.15", "five point fifteen"),
                                ("5.25", "five point twenty five"),
                                ("0.15", "point fifteen"),
                                ("0.25", "point twenty five")):
            with self.subTest(words=words):
                self._assert_taken_out(self._denial_note(standing, words))

    def test_f15_92_different_figure_denial_stands(self):
        for standing, words in (("15", "five point fifteen"),
                                ("25", "five point twenty five"),
                                ("5", "point fifteen"),
                                ("5.15", "five point twenty five")):
            with self.subTest(words=words):
                self._assert_stands(
                    self._denial_note(standing, words),
                    [(1, float(standing), True)],
                    "Step 1 banked wait " + standing + " hours")

    def test_f15_92_control_settled_point_forms_hold(self):
        for words, value in (("five point five", 5.5),
                             ("five point five five", 5.55),
                             ("point seven five", 0.75),
                             ("five point oh five", 5.05),
                             ("point five", 0.5),
                             ("six point oh nine", 6.09)):
            with self.subTest(words=words):
                self._assert_reading(words, value)
        self._assert_taken_out(self._denial_note("5.5", "five point five"))
        self._assert_taken_out(
            self._denial_note("0.75", "point seven five"))


if __name__ == "__main__":
    unittest.main()
