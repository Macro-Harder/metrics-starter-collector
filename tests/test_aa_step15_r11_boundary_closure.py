"""Step 15 fix round 11 tests: boundary and closure family, F32 seat.

Each charged case pins one fix register item from the
confirmation round 10 papers. F15-82 (C10-1 with the Breaker
observation): the closure join set was not closed on its
subordinating side, so since, because, unless, when, if,
until, once, whenever, before and after between two closure
statements poisoned an own closure, and the first six leaked
on the before side; the correctness seat found against the
closed list position, the "for" exclusion standing. F15-83
(CB10-1): the joining abbreviation class held only cf. and
vs., so et al., viz. and a.k.a. still ended a sentence
between the names they join, in both directions. F15-84
(CB10-2): an unspaced hyphen was no closure join on either
side. F15-85 (CB10-3): a closure statement set off by square
brackets was no bound in either direction. Control cases pin
the behaviour that must not move: the widened round 10 joins,
a field form completion naming its own step, a single
statement naming two steps, an own closure beside a joining
abbreviation, the comma bound beside a prepositional phrase,
the spaced hyphen and comma forms, and a single bracketed
foreign statement.
"""
import unittest

from metrics_starter_collector.derivation_core import (
    _dot_ends_sentence, _t4_banked_durations)
from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, path_ledger,
                                     row_block, run_tool)

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


def capture(root):
    from metrics_starter_collector.shell_reader import capture_read
    return capture_read(root)


def record(text):
    return "# Step 2 gate record\n\n" + text + "\n"


def ends_at(text, token):
    pos = text.index(token) + len(token) - 1
    return _dot_ends_sentence(text, pos)


class TestStep15R11BoundaryClosure(FixtureTestCase):

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

    # ------------------------------------------------------------ F15-82

    def test_f15_82_after_subordinating_joins_foreign_not_poison(self):
        for join in ("since", "because", "unless", "when", "if",
                     "until", "once", "whenever", "before", "after"):
            with self.subTest(join=join):
                root = self._f2_root(
                    "This record recorded as CLOSED-FAIL " + join
                    + " the Step 3 ruling recorded as CLOSED-PASS.")
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    def test_f15_82_before_subordinating_joins_do_not_leak(self):
        for join in ("since", "because", "unless", "when", "if",
                     "until"):
            with self.subTest(join=join):
                root = self._f2_root(
                    "Closure state: CLOSED-PASS for Step 3 " + join
                    + " this record recorded as CLOSED-FAIL.")
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    def test_f15_82_positional_joiner_after_unlisted_words(self):
        for join in ("in case", "notwithstanding"):
            with self.subTest(join=join):
                root = self._f2_root(
                    "This record recorded as CLOSED-FAIL " + join
                    + " the Step 3 ruling recorded as CLOSED-PASS.")
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    def test_f15_82_positional_joiner_before_unlisted_words(self):
        for join in ("where", "in case"):
            with self.subTest(join=join):
                root = self._f2_root(
                    "Closure state: CLOSED-PASS for Step 3 " + join
                    + " this record recorded as CLOSED-FAIL.")
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    def test_f15_82_after_completed_list_neighbours(self):
        for join in ("lest", "till", "wherever", "whilst"):
            with self.subTest(join=join):
                root = self._f2_root(
                    "This record recorded as CLOSED-FAIL " + join
                    + " the Step 3 ruling recorded as CLOSED-PASS.")
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    def test_f15_82_before_completed_list_neighbours(self):
        for join in ("lest", "till", "wherever"):
            with self.subTest(join=join):
                root = self._f2_root(
                    "Closure state: CLOSED-PASS for Step 3 " + join
                    + " this record recorded as CLOSED-FAIL.")
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    def test_f15_82_control_joins_and_completions_hold(self):
        root = self._f2_root(
            "This record recorded as CLOSED-FAIL whereas the "
            "Step 3 ruling recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)
        root = self._f2_root("Closure state: CLOSED-PASS for Step 2.")
        self._assert_f2_row(root, "present", PLAIN_ONE_FIGURES)
        root = self._f2_root(
            "This record notes the Step 2 and Step 3 ruling, "
            "recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)
        root = self._f2_root(
            "This record notes a ruling recorded as CLOSED-PASS "
            "by Lane for Step 3, recorded as CLOSED-FAIL.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    # ------------------------------------------------------------ F15-83

    def test_f15_83_joining_abbreviations_closure_foreign(self):
        frames = (
            "This record notes the Step 3 ruling, Lane et al. "
            "Grant, recorded as CLOSED-PASS.",
            "This record notes the Step 3 ruling, Lane et al. "
            "grant, recorded as CLOSED-PASS.",
            "This record notes the Step 3 ruling, Lane viz. "
            "Grant, recorded as CLOSED-PASS.",
            "This record notes the Step 3 ruling, Lane viz. "
            "grant, recorded as CLOSED-PASS.",
            "This record notes the Step 3 ruling, Lane a.k.a. "
            "Grant, recorded as CLOSED-PASS.",
        )
        for frame in frames:
            with self.subTest(frame=frame):
                root = self._f2_root(frame)
                self._assert_f2_row(root, "present but not derivable",
                                    NOT_DERIVABLE_FIGURES)

    def test_f15_83_joining_abbreviations_denial_reaches_duration(self):
        for joiner in ("et al.", "viz.", "a.k.a."):
            with self.subTest(joiner=joiner):
                self._assert_taken_out(
                    "The duration was withdrawn, Lane " + joiner
                    + " Grant noted, Step 1 BANKED interval "
                    "duration 5 hours stands.")

    def test_f15_83_class_rule_direct(self):
        cases = (
            ("given by Lane et al. Grant, recorded", "al.", False),
            ("given by Lane et al. grant, recorded", "al.", False),
            ("given by Lane viz. Grant, recorded", "viz.", False),
            ("given by Lane viz. grant, recorded", "viz.", False),
            ("given by Lane a.k.a. Grant, recorded", "a.k.a.", False),
            ("given by Lane a.k.a. grant, recorded", "a.k.a.", False),
            # Standing forms that must not move.
            ("given by Dr. Lane, recorded", "Dr.", False),
            ("Filed for the U.S. Lane noted", "U.S.", True),
            ("Filed for the U.S. office noted", "U.S.", False),
            ("given by Lane et al.", "al.", True),
        )
        for text, token, expected in cases:
            with self.subTest(text=text, token=token):
                self.assertEqual(ends_at(text, token), expected)

    def test_f15_83_control_own_closure_beside_joining_counts(self):
        root = self._f2_root(
            "This record notes the Step 2 ruling, Lane et al. "
            "Grant, recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present", PLAIN_ONE_FIGURES)
        root = self._f2_root(
            "This record notes the Step 2 ruling, Lane vs. "
            "Grant, recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present", PLAIN_ONE_FIGURES)

    # ------------------------------------------------------------ F15-84

    def test_f15_84_after_unspaced_hyphen_foreign_not_poison(self):
        root = self._f2_root(
            "This record recorded as CLOSED-FAIL-the Step 3 "
            "ruling recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_84_before_unspaced_hyphen_does_not_leak(self):
        root = self._f2_root(
            "Closure state: CLOSED-PASS for Step 3-this record "
            "recorded as CLOSED-FAIL.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_84_unspaced_hyphen_positional_neighbours(self):
        root = self._f2_root(
            "This record recorded as CLOSED-FAIL- the Step 3 "
            "ruling recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)
        root = self._f2_root(
            "Closure state: CLOSED-PASS for Step 3 -this record "
            "recorded as CLOSED-FAIL.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_84_control_spaced_hyphen_and_comma_hold(self):
        root = self._f2_root(
            "This record recorded as CLOSED-FAIL - the Step 3 "
            "ruling recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)
        root = self._f2_root(
            "This record recorded as CLOSED-FAIL, the well-known "
            "Step 3 ruling recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    # ------------------------------------------------------------ F15-85

    def test_f15_85_after_bracketed_foreign_does_not_poison(self):
        root = self._f2_root(
            "This record recorded as CLOSED-FAIL [the Step 3 "
            "ruling recorded as CLOSED-PASS].")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_85_before_bracketed_step_naming_does_not_leak(self):
        root = self._f2_root(
            "Closure state: CLOSED-PASS [for Step 3] this record "
            "recorded as CLOSED-FAIL.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_85_bracket_neighbours(self):
        root = self._f2_root(
            "This record recorded as CLOSED-FAIL [the Step 3 "
            "ruling (see Lane) recorded as CLOSED-PASS].")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)
        root = self._f2_root(
            "Closure state: CLOSED-PASS [for Step 3 noted by "
            "Lane] this record recorded as CLOSED-FAIL.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_85_control_bracketed_forms_hold(self):
        root = self._f2_root(
            "This record was [recorded as CLOSED-PASS].")
        self._assert_f2_row(root, "present", PLAIN_ONE_FIGURES)
        root = self._f2_root(
            "This record notes [the Step 3 ruling recorded as "
            "CLOSED-PASS.]")
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)


if __name__ == "__main__":
    unittest.main()
