"""Step 15 fix round 8 tests: true sentence boundaries, F21 seat.

Each charged case pins one fix register item in the boundary
machinery of derivation_core.py. F15-55 (CB7-1, CB7-2): the
fragment test in _recorded_closure cut the fragment at a dotted
stop inside an abbreviation (Dr., Capt., e.g.), a decimal
(version 1.2), a person's initials (J. P.), or a semicolon inside
the closure sentence, so a foreign Step 3 closure counted as a
Step 2 plain approval; and question and exclamation marks were
not fragment stops, so a foreign step across one of them, or in
an earlier closure statement of the same sentence, poisoned an
own no step closure. F15-56 (CB7-11, CB7-9, CB7-10): the fragment
and sentence machinery the duration helpers share took the same
raw stops, so a decimal point truncated the clause fragments (a
5.5 hour denial failed to scope and an attribution part after a
decimal was never searched), a person's initials truncated the
retracting sentence in the retraction finder, and an abbreviation
at the end of the mention's own sentence merged it with the
retracting sentence. Control cases pin the behaviour that must
not move: the comma twin stays foreign, a dotted stop with the
step name after it stays foreign, a closure first form followed
by a separate Step 3 statement still counts, a single closure
statement naming two steps stays discarded, the F20 true end
controls (an abbreviation at the passage end still ends the
retracting sentence), and the decimal and version forms that
already retracted.
"""
import unittest

from metrics_starter_collector.derivation_core import _t4_banked_durations
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


def capture(root):
    from metrics_starter_collector.shell_reader import capture_read
    return capture_read(root)


def record(text):
    return "# Step 2 gate record\n\n" + text + "\n"


class TestStep15Round8Boundary(FixtureTestCase):

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

    def _f2_root(self, record_text, adjudication=False):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = record(record_text)
        if adjudication:
            table["steps/step-02-gate-adjudication.md"] = gate_record(
                2, "CLOSED-FAIL")
        return build_tree(table)

    # ------------------------------------------------------------ F15-55

    def test_f15_55_abbreviation_dr_foreign_not_derivable(self):
        root = self._f2_root(
            "This record notes the Step 3 ruling by Dr. Lane, "
            "recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_55_abbreviation_capt_foreign_not_derivable(self):
        root = self._f2_root(
            "This record notes the Step 3 ruling by Capt. Lane, "
            "recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_55_abbreviation_eg_foreign_not_derivable(self):
        root = self._f2_root(
            "This record notes the Step 3 ruling, e.g. its outcome, "
            "recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_55_decimal_version_foreign_not_derivable(self):
        root = self._f2_root(
            "This record notes the Step 3 ruling in version 1.2 "
            "notes, recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_55_initials_foreign_not_derivable(self):
        root = self._f2_root(
            "This record notes the Step 3 ruling by J. P. Lane, "
            "recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_55_semicolon_inside_sentence_foreign_not_derivable(self):
        root = self._f2_root(
            "The Step 3 ruling stands; recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_55_dotted_foreign_with_fail_adjudication_not_derivable(self):
        root = self._f2_root(
            "This record notes the Step 3 ruling by Dr. Lane, "
            "recorded as CLOSED-PASS.", adjudication=True)
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_55_question_boundary_own_fail_counts(self):
        root = self._f2_root(
            "Was the Step 3 ruling recorded as CLOSED-PASS? "
            "This record was recorded as CLOSED-FAIL.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_55_exclamation_boundary_own_fail_counts(self):
        root = self._f2_root(
            "The Step 3 ruling recorded as CLOSED-PASS! "
            "This record was recorded as CLOSED-FAIL.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_55_field_form_after_question_own_fail_counts(self):
        root = self._f2_root(
            "Was the Step 3 ruling recorded as CLOSED-PASS? "
            "Closure state: CLOSED-FAIL.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_55_own_fail_before_exclamation_counts(self):
        root = self._f2_root(
            "This record was recorded as CLOSED-FAIL! "
            "The Step 3 ruling recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_55_shared_sentence_foreign_first_own_fail_counts(self):
        root = self._f2_root(
            "This record notes the Step 3 ruling recorded as "
            "CLOSED-PASS and this record recorded as CLOSED-FAIL.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_55_shared_sentence_own_first_own_fail_counts(self):
        root = self._f2_root(
            "This record recorded as CLOSED-FAIL and the Step 3 "
            "ruling recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_55_control_comma_twin_stays_foreign(self):
        root = self._f2_root(
            "The Step 3 ruling stands, recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_55_control_step_after_dotted_stop_stays_foreign(self):
        root = self._f2_root(
            "Dr. Lane notes the Step 3 ruling, recorded as "
            "CLOSED-PASS.")
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_55_control_closure_first_semicolon_counts_own(self):
        root = self._f2_root(
            "This record recorded as CLOSED-PASS; the Step 3 "
            "ruling was separate.")
        self._assert_f2_row(root, "present", PLAIN_ONE_FIGURES)

    def test_f15_55_control_closure_first_full_stop_counts_own(self):
        root = self._f2_root(
            "This record recorded as CLOSED-PASS. The Step 3 "
            "ruling was separate.")
        self._assert_f2_row(root, "present", PLAIN_ONE_FIGURES)

    def test_f15_55_control_two_steps_one_statement_stays_discarded(self):
        root = self._f2_root(
            "This record notes the Step 2 and Step 3 ruling, "
            "recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_55_control_own_step_after_abbreviation_counts(self):
        root = self._f2_root(
            "This record notes the Step 2 ruling by Dr. Lane, "
            "recorded as CLOSED-PASS.")
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

    def _assert_banked_stands(self, note_text, expected=None):
        root, report = self._report(note_text)
        self.assertEqual(_t4_banked_durations(capture(root)),
                         expected if expected is not None
                         else [(1, 5.0, True)])
        t2 = row_block(report, "T-2")
        assert_verdict(self, t2, "missing", "T-2")
        self.assertIn("an interval duration stands in the "
                      "transition log", t2)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present", "T-4")
        return root, report

    def _assert_taken_out(self, note_text):
        root, report = self._report(note_text)
        self.assertEqual(_t4_banked_durations(capture(root)), [])
        t2 = row_block(report, "T-2")
        assert_verdict(self, t2, "missing", "T-2")
        self.assertIn("date-only-form", t2)
        self.assertIn("no BANKED, SUSPENDED or halt interval "
                      "duration stands", t2)
        self.assertNotIn("an interval duration stands in the "
                         "transition log, but no active figure", t2)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "missing", "T-4")
        self.assertIn(T4_MISSING_SHOWS, t4)
        self.assertNotIn("banked wait", report)
        return root, report

    # ------------------------------------------------------------ F15-56

    def test_f15_56_decimal_denial_scopes_elsewhere_stands(self):
        root, report = self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands, and "
            "no interval duration 5.5 hours was recorded for "
            "Step 1.")
        t4 = row_block(report, "T-4")
        self.assertIn("Step 1 banked wait 5 hours", t4)

    def test_f15_56_decimal_attribution_part_after_decimal_searched(self):
        root, report = self._assert_banked_stands(
            "Step 1 heading: BANKED interval duration 5 hours "
            "stands, the 5.5 hour review noted, recorded for "
            "Step 2.", expected=[(2, 5.0, True)])
        t4 = row_block(report, "T-4")
        self.assertIn("Step 2 banked wait 5 hours", t4)
        self.assertNotIn("Step 1 banked wait", t4)

    def test_f15_56_initials_in_retracting_sentence_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands. "
                "That claim, J. P. Lane noted, was withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands. "
                "That claim, J. Lane noted, was withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands. "
                "That claim, Lane J. P. noted, was withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands. "
                "That claim, J. P. Lane noted, was wrong."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_56_initials_unvalued_retraction_taken_out(self):
        self._assert_taken_out(
            'The draft states "an interval duration stands". '
            "That claim, A. B. Lane noted, was retracted.")

    def test_f15_56_abbreviation_at_mention_sentence_end_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands "
                "for the U.S. That claim was withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "for the U.K. That claim was withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "at 5 p.m. That claim was withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "noted by Dr. That claim was withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_56_control_abbreviation_at_passage_end_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands. "
                "That claim was withdrawn by Dr.",
                "Step 1 BANKED interval duration 5 hours stands. "
                "That claim was withdrawn in the U.S."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_56_control_title_before_name_retraction_taken_out(self):
        self._assert_taken_out(
            "Step 1 BANKED interval duration 5 hours stands. "
            "That claim, Dr. Lane noted, was withdrawn.")

    def test_f15_56_control_decimal_claim_retraction_taken_out(self):
        self._assert_taken_out(
            "Step 1 BANKED interval duration 5 hours stands. "
            "That claim of 5.5 hours was withdrawn.")

    def test_f15_56_control_version_in_retracting_sentence_taken_out(self):
        self._assert_taken_out(
            "Step 1 BANKED interval duration 5 hours stands. "
            "That claim, in version 1.2 notes, was withdrawn.")

    def test_f15_56_control_genuine_banked_duration_stands(self):
        root, report = self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands.")
        t4 = row_block(report, "T-4")
        self.assertIn("Step 1 banked wait 5 hours", t4)


if __name__ == "__main__":
    unittest.main()
