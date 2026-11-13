"""Step 15 fix round 10 tests: figure compounds and mixed forms.

Each charged case pins one fix register item in the figure
reading machinery of derivation_core.py. F15-78 (CB9-9):
figure compounds stopped at the charged scale tails, so
"eleven hundred" and the hundred thousand forms read as no
figure at all, and hyphenated hundred compounds read as
their tail alone; a denial naming the true figure therefore
took out a different standing figure by the no figure route
and failed against its own. Figure compounds read in full:
a small form may stand before hundred, a hundred form may
stand before thousand, and the hundred and thousand joins
take a hyphen as they take a space. F15-79 (CB9-10): the
figure pattern took digits alone or words alone, so comma
grouped digits read as their last group, mixed digit and
word forms read as their tail alone, a point tail carrying
oh read as its last unit word, and a leading point form
read as its unit word alone, a standing 0.5 surviving its
own denial. Mixed forms read in full: comma grouped digits,
a digit round form with a word tail, a word scale form with
a digit tail, point tails carrying oh and zero as the zero
digit, and a point form with no integer part read as its
fraction. The settled figure forms of rounds 6 to 9 hold as
controls. Assertions pin the direct reading through
_clause_subject and the denial scoping in both directions:
a denial of the same figure takes the standing figure out,
and a denial of a different figure leaves it standing, the
parser result as a whole and the printed T-4 row.
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


class TestStep15Round10Figures(FixtureTestCase):

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

    # ---------------------------------------------------------- F15-78

    def test_f15_78_direct_hundred_with_teen_multiplier(self):
        for words, value in (("eleven hundred", 1100.0),
                             ("twelve hundred", 1200.0),
                             ("eleven-hundred", 1100.0),
                             ("twenty five hundred", 2500.0)):
            with self.subTest(words=words):
                self._assert_reading(words, value)

    def test_f15_78_direct_hundred_thousand_forms(self):
        for words, value in (("one hundred thousand", 100000.0),
                             ("five hundred thousand", 500000.0),
                             ("two hundred thousand", 200000.0),
                             ("one hundred and five thousand", 105000.0),
                             ("one-hundred-thousand", 100000.0)):
            with self.subTest(words=words):
                self._assert_reading(words, value)

    def test_f15_78_direct_hyphenated_hundred_compounds(self):
        for words, value in (("one-hundred-and-five", 105.0),
                             ("two-hundred-and-fifty", 250.0),
                             ("two-hundred-and-thirty-five", 235.0),
                             ("five-hundred-and-twenty-five", 525.0),
                             ("one-hundred", 100.0)):
            with self.subTest(words=words):
                self._assert_reading(words, value)

    def test_f15_78_same_figure_denial_taken_out(self):
        for standing, words in (
                ("1100", "eleven hundred"),
                ("100000", "one hundred thousand"),
                ("500000", "five hundred thousand"),
                ("105", "one-hundred-and-five"),
                ("250", "two-hundred-and-fifty")):
            with self.subTest(words=words):
                self._assert_taken_out(self._denial_note(standing, words))

    def test_f15_78_different_figure_denial_stands(self):
        for standing, words in (
                ("11", "eleven hundred"),
                ("5", "one hundred thousand"),
                ("5", "one-hundred-and-five"),
                ("50", "two-hundred-and-fifty"),
                ("100", "five hundred thousand")):
            with self.subTest(words=words):
                self._assert_stands(
                    self._denial_note(standing, words),
                    [(1, float(standing), True)],
                    "Step 1 banked wait " + standing + " hours")

    def test_f15_78_control_settled_compounds_hold(self):
        for words, value in (
                ("one thousand two hundred and thirty five", 1235.0),
                ("twenty one thousand", 21000.0),
                ("one hundred and five", 105.0),
                ("two hundred and fifty", 250.0),
                ("one thousand five hundred", 1500.0)):
            with self.subTest(words=words):
                self._assert_reading(words, value)
        self._assert_taken_out(
            self._denial_note("1235",
                              "one thousand two hundred and thirty five"))
        self._assert_taken_out(
            self._denial_note("21000", "twenty one thousand"))

    # ---------------------------------------------------------- F15-79

    def test_f15_79_direct_comma_grouped_digits(self):
        for words, value in (("1,000", 1000.0),
                             ("2,500", 2500.0),
                             ("1,000,000", 1000000.0),
                             ("12,345", 12345.0)):
            with self.subTest(words=words):
                self._assert_reading(words, value)

    def test_f15_79_direct_mixed_digit_and_word_forms(self):
        for words, value in (("100 and five", 105.0),
                             ("one hundred and 5", 105.0),
                             ("200 and twenty five", 225.0),
                             ("one hundred and 25", 125.0),
                             ("one thousand and 5", 1005.0),
                             ("5 hundred and five", 505.0)):
            with self.subTest(words=words):
                self._assert_reading(words, value)

    def test_f15_79_direct_point_edge_forms(self):
        for words, value in (("five point oh five", 5.05),
                             ("five point zero five", 5.05),
                             ("point five", 0.5),
                             ("point oh five", 0.05),
                             ("5 point five", 5.5),
                             (".5", 0.5)):
            with self.subTest(words=words):
                self._assert_reading(words, value)

    def test_f15_79_comma_grouped_same_figure_taken_out(self):
        self._assert_taken_out(self._denial_note("1000", "1,000"))
        self._assert_taken_out(self._denial_note("2500", "2,500"))

    def test_f15_79_comma_grouped_different_figure_stands(self):
        self._assert_stands(
            self._denial_note("5", "1,000"),
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")
        self._assert_stands(
            self._denial_note("250", "2,500"),
            [(1, 250.0, True)], "Step 1 banked wait 250 hours")

    def test_f15_79_comma_grouped_denial_before_stands(self):
        self._assert_stands(
            "No interval duration 1,000 hours was recorded for "
            "Step 1, Step 1 BANKED interval duration 5 hours stands.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_79_mixed_same_figure_taken_out(self):
        for standing, words in (("105", "100 and five"),
                                ("105", "one hundred and 5")):
            with self.subTest(words=words):
                self._assert_taken_out(self._denial_note(standing, words))

    def test_f15_79_mixed_different_figure_stands(self):
        for words in ("100 and five", "one hundred and 5"):
            with self.subTest(words=words):
                self._assert_stands(
                    self._denial_note("5", words),
                    [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_79_point_edge_same_figure_taken_out(self):
        self._assert_taken_out(
            self._denial_note("5.05", "five point oh five"))
        self._assert_taken_out(self._denial_note("0.5", "point five"))

    def test_f15_79_point_edge_different_figure_stands(self):
        for standing, words in (("5", "five point oh five"),
                                ("5", "point five"),
                                ("0.5", "five point oh five")):
            with self.subTest(words=words):
                self._assert_stands(
                    self._denial_note(standing, words),
                    [(1, float(standing), True)],
                    "Step 1 banked wait " + standing + " hours")

    def test_f15_79_control_settled_figure_forms_hold(self):
        for words, value in (("five point five", 5.5),
                             ("five point five five", 5.55),
                             ("forty two", 42.0),
                             ("100", 100.0),
                             ("twenty five point five", 25.5)):
            with self.subTest(words=words):
                self._assert_reading(words, value)
        self._assert_taken_out(self._denial_note("5.5", "five point five"))
        self._assert_stands(
            self._denial_note("5", "100"),
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")


if __name__ == "__main__":
    unittest.main()
