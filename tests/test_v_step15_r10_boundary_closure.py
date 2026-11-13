"""Step 15 fix round 10 tests: boundary and closure family, F28 seat.

Each charged case pins one fix register item from the
confirmation round 9 Breaker paper. F15-70 (CB9-1): the next
token test in _dot_ends_sentence returned no end where the
next token was a single letter and no end where it was not a
letter at all, so a sentence opening on the word A or I, or
opening on a figure, merged with the sentence before an other
class abbreviation stop, losing an own closure on the closure
side and letting a foreign denial act on the duration side.
F15-71 (CB9-2): vs. and cf. stood in the ending class although
each stands between the names it joins, so a foreign closure
after one counted as the piece own closure. F15-72 (CB9-3):
the closure join set in _CLOSURE_JOIN_RE was a closed list, so
conjunctions outside it (yet, nor, so, as, whereas) and an
unspaced dash poisoned an own closure on both sides of a
match. F15-73 (CB9-4): no join and no fragment rule treated a
quote or a parenthesis as a statement bound, in either
direction. Control cases pin the behaviour that must not
move: an initialled opener after an other class abbreviation
(A. Lane) still holds its sentence together, a single
statement naming a foreign step stays foreign however it is
set off, and an own closure inside quotes still counts.
"""
import unittest

from metrics_starter_collector.derivation_core import (
    _dot_ends_sentence, _t4_banked_durations)
from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, gate_record,
                                     path_ledger, row_block, run_tool)

NOT_DERIVABLE_FIGURES = ("no rate figure; plain approvals 0; "
                         "qualified approvals 0; steps ruled on 0")
PLAIN_ONE_FIGURES = ("first-time approval rate 100 percent; "
                     "plain approvals 1; qualified approvals 0; "
                     "steps ruled on 1")
NOT_APPROVED_FIGURES = ("first-time approval rate 0 percent; "
                        "plain approvals 0; qualified approvals 0; "
                        "steps ruled on 1; Step 2 ruled and not "
                        "approved")

DATE_ONLY_LINE = "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.\n"
T4_MISSING_SHOWS = ("no banked state and no decision item count "
                    "stands in the feeder records for this metric")

EM_DASH = "\u2014"
EN_DASH = "\u2013"


def capture(root):
    from metrics_starter_collector.shell_reader import capture_read
    return capture_read(root)


def record(text):
    return "# Step 2 gate record\n\n" + text + "\n"


def ends_at(text, token):
    pos = text.index(token) + len(token) - 1
    return _dot_ends_sentence(text, pos)


class TestStep15R10BoundaryClosure(FixtureTestCase):

    # ------------------------------------------------------------ F-2 side

    def _assert_f2_row(self, root, verdict, figures):
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, verdict, "F-2")
        first_line = block.splitlines()[0]
        fields = [part.strip() for part in first_line.split("|")]
        self.assertEqual(fields[3], figures)
        return block

    def _f2_root(self, record_text):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = record(record_text)
        return build_tree(table)

    # ------------------------------------------------------------ F15-70

    def test_f15_70_closure_single_letter_openers_count_own(self):
        frames = (
            "The Step 3 ruling was filed for the U.S. A reviewer "
            "noted this record was recorded as CLOSED-FAIL.",
            # The Breaker paper prints this frame with the
            # words "I recorded this record as", which carries
            # no settled closure form at all, so no boundary
            # cure can make it count; the settled neighbour
            # below pins the same I opener on the F-2 side,
            # and the direct class rule case below pins the
            # boundary on the paper's exact wording.
            "The Step 3 ruling was filed for the U.S. I noted "
            "this record was recorded as CLOSED-FAIL.",
            "The Step 3 ruling was filed at 5 p.m. A reviewer "
            "noted this record was recorded as CLOSED-FAIL.",
        )
        for frame in frames:
            with self.subTest(frame=frame):
                root = self._f2_root(frame)
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    def test_f15_70_closure_digit_opener_counts_own(self):
        frames = (
            "The Step 3 ruling was filed for the U.S. 5 hours "
            "later, this record was recorded as CLOSED-FAIL.",
            "The Step 3 ruling was filed at 5 p.m. 3 days later, "
            "this record was recorded as CLOSED-FAIL.",
        )
        for frame in frames:
            with self.subTest(frame=frame):
                root = self._f2_root(frame)
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    def test_f15_70_duration_single_letter_openers_denial_scopes(self):
        notes = (
            "Step 1 BANKED interval duration 5 hours stands for "
            "the U.S. A reviewer noted no interval duration one "
            "hundred hours was recorded for Step 1.",
            "Step 1 BANKED interval duration 5 hours stands for "
            "the U.S. I noted no interval duration one hundred "
            "hours was recorded for Step 1.",
        )
        for note in notes:
            with self.subTest(note=note):
                root, report = self._report(note)
                self.assertEqual(
                    _t4_banked_durations(capture(root)),
                    [(1, 5.0, True)])
                t4 = row_block(report, "T-4")
                assert_verdict(self, t4, "present", "T-4")
                self.assertIn("Step 1 banked wait 5 hours", t4)

    def test_f15_70_duration_digit_opener_denial_scopes(self):
        root, report = self._report(
            "Step 1 BANKED interval duration 5 hours stands for "
            "the U.S. 5 reviewers noted no interval duration one "
            "hundred hours was recorded for Step 1.")
        self.assertEqual(_t4_banked_durations(capture(root)),
                         [(1, 5.0, True)])
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present", "T-4")
        self.assertIn("Step 1 banked wait 5 hours", t4)

    def test_f15_70_class_rule_direct(self):
        cases = (
            # Single letter sentence openers A and I end a
            # sentence after an other class abbreviation, as a
            # figure opener does, on both charged abbreviations.
            ("Filed for the U.S. A reviewer noted", "U.S.", True),
            ("Filed for the U.S. I recorded this", "U.S.", True),
            ("Filed for the U.S. 5 hours later", "U.S.", True),
            ("Filed at 5 p.m. A reviewer noted", "p.m.", True),
            ("Filed at 5 p.m. 3 days later", "p.m.", True),
            # Standing forms that must not move.
            ("Filed for the U.S. Lane noted", "U.S.", True),
            ("Filed for the U.S. office noted", "U.S.", False),
            ("Filed for the U.S. a reviewer noted", "U.S.", False),
            # A single letter followed by its own stop is an
            # initial, not a sentence opener: the disclosed
            # sacrifice boundary stands on the opener side too.
            ("Filed for the U.S. A. Lane noted", "U.S.", False),
            ("given by Dr. A. Lane, recorded", "Dr.", False),
            ("by J. P. Lane, recorded", "J.", False),
            ("by J. P. Lane, recorded", "P.", False),
            ("withdrawn by Dr.", "Dr.", True),
        )
        for text, token, expected in cases:
            with self.subTest(text=text, token=token):
                self.assertEqual(ends_at(text, token), expected)

    # ------------------------------------------------------------ F15-71

    def test_f15_71_vs_cf_closure_foreign(self):
        frames = (
            "This record notes the Step 3 ruling, Lane vs. "
            "Grant, recorded as CLOSED-PASS.",
            "This record notes the Step 3 ruling, Lane cf. "
            "Grant, recorded as CLOSED-PASS.",
        )
        for frame in frames:
            with self.subTest(frame=frame):
                root = self._f2_root(frame)
                self._assert_f2_row(root, "present but not derivable",
                                    NOT_DERIVABLE_FIGURES)

    def test_f15_71_vs_cf_before_denial_reaches_duration(self):
        for joiner in ("vs.", "cf."):
            with self.subTest(joiner=joiner):
                self._assert_taken_out(
                    "The duration was withdrawn, Lane " + joiner
                    + " Grant noted, Step 1 BANKED interval "
                    "duration 5 hours stands.")

    def test_f15_71_class_rule_direct(self):
        cases = (
            ("given by Lane vs. Grant, recorded", "vs.", False),
            ("given by Lane cf. Grant, recorded", "cf.", False),
            ("given by Lane vs. grant, recorded", "vs.", False),
            # The other class and the title class stand as they
            # stood beside the moved pair.
            ("Filed for the U.S. Lane noted", "U.S.", True),
            ("given by Dr. Lane, recorded", "Dr.", False),
        )
        for text, token, expected in cases:
            with self.subTest(text=text, token=token):
                self.assertEqual(ends_at(text, token), expected)

    def test_f15_71_control_own_closure_beside_vs_counts(self):
        root = self._f2_root(
            "This record notes the Step 2 ruling, Lane vs. "
            "Grant, recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present", PLAIN_ONE_FIGURES)

    # ------------------------------------------------------- duration side

    def _report(self, note_text):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            DATE_ONLY_LINE + note_text, steps="1, 2, 3")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        return root, result.stdout

    def _assert_taken_out(self, note_text):
        root, report = self._report(note_text)
        self.assertEqual(_t4_banked_durations(capture(root)), [])
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "missing", "T-4")
        self.assertIn(T4_MISSING_SHOWS, t4)
        self.assertNotIn("banked wait", report)
        return root, report

    # ------------------------------------------------------------ F15-72

    def test_f15_72_after_joins_foreign_does_not_poison(self):
        for join in ("yet", "nor", "so", "as", "whereas"):
            with self.subTest(join=join):
                root = self._f2_root(
                    "This record recorded as CLOSED-FAIL " + join
                    + " the Step 3 ruling recorded as CLOSED-PASS.")
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    def test_f15_72_after_unspaced_dash_foreign_does_not_poison(self):
        for dash in (EM_DASH, EN_DASH):
            with self.subTest(dash=repr(dash)):
                root = self._f2_root(
                    "This record recorded as CLOSED-FAIL" + dash
                    + "the Step 3 ruling recorded as CLOSED-PASS.")
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    def test_f15_72_before_joins_step_after_token_does_not_leak(self):
        for join in ("yet", "nor", "so", "as", "whereas",
                     "although", "though"):
            with self.subTest(join=join):
                root = self._f2_root(
                    "Closure state: CLOSED-PASS for Step 3 " + join
                    + " this record recorded as CLOSED-FAIL.")
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    def test_f15_72_before_unspaced_dash_does_not_leak(self):
        root = self._f2_root(
            "Closure state: CLOSED-PASS for Step 3" + EM_DASH
            + "the Step 2 ruling recorded as CLOSED-FAIL.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_72_after_further_conjunction_neighbours(self):
        for join in ("although", "though"):
            with self.subTest(join=join):
                root = self._f2_root(
                    "This record recorded as CLOSED-FAIL " + join
                    + " the Step 3 ruling recorded as CLOSED-PASS.")
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    def test_f15_72_control_single_statement_comma_stays_foreign(self):
        root = self._f2_root(
            "The Step 3 ruling stands, recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)
        root = self._f2_root(
            "This record notes the Step 2 and Step 3 ruling, "
            "recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    # ------------------------------------------------------------ F15-73

    def test_f15_73_after_quoted_foreign_does_not_poison(self):
        root = self._f2_root(
            "This record recorded as CLOSED-FAIL \"the Step 3 "
            "ruling recorded as CLOSED-PASS.\"")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_73_after_parenthesised_foreign_does_not_poison(self):
        root = self._f2_root(
            "This record recorded as CLOSED-FAIL (the Step 3 "
            "ruling recorded as CLOSED-PASS).")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_73_before_parenthesised_step_naming_does_not_leak(self):
        frames = (
            "Closure state: CLOSED-PASS (for Step 3) this record "
            "recorded as CLOSED-FAIL.",
            "Closure state: CLOSED-PASS (for Step 3, noted by "
            "Lane) this record recorded as CLOSED-FAIL.",
        )
        for frame in frames:
            with self.subTest(frame=frame):
                root = self._f2_root(frame)
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    def test_f15_73_before_quoted_step_naming_does_not_leak(self):
        root = self._f2_root(
            "Closure state: CLOSED-PASS \"for Step 3\" this "
            "record recorded as CLOSED-FAIL.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_73_control_quoted_foreign_single_statement_foreign(self):
        root = self._f2_root(
            "This record notes \"the Step 3 ruling recorded as "
            "CLOSED-PASS.\"")
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_73_control_own_quoted_closure_counts(self):
        root = self._f2_root(
            "This record was \"recorded as CLOSED-PASS.\"")
        self._assert_f2_row(root, "present", PLAIN_ONE_FIGURES)


if __name__ == "__main__":
    unittest.main()
