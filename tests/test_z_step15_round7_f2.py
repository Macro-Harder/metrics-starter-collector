"""Step 15 fix round 7 tests: F-2 contested base pieces and step scoped closures.

Each case pins one fix round 7 finding in derivation_core.py:
F15-46, the F15-14 conflict guard reading piece texts only, so a
disagreement merged base piece standing behind a substantive
governing piece was invisible to it and the step counted on the
governing piece alone; and F15-47, closure extraction reading a
closure statement anywhere in a piece, so a governing piece whose
only closure named a different step counted that foreign closure
for its own step. Control cases pin the behaviour that must not
move: the sound pair guard in both branches, a disagreement piece
governing at a base identity, a contested piece at a non base
identity behind a sound base pair, a closure naming the piece own
step, a closure naming no step at all, and the twin of the foreign
construction with the foreign closure removed.
Every case asserts the full printed figures field and the verdict
of the F-2 row, not substrings of them.
"""
import unittest

from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, gate_record,
                                     gate_ruling, row_block, run_tool)

NOT_DERIVABLE_FIGURES = ("no rate figure; plain approvals 0; "
                         "qualified approvals 0; steps ruled on 0")
PLAIN_ONE_FIGURES = ("first-time approval rate 100 percent; "
                     "plain approvals 1; qualified approvals 0; "
                     "steps ruled on 1")
NOT_APPROVED_FIGURES = ("first-time approval rate 0 percent; "
                        "plain approvals 0; qualified approvals 0; "
                        "steps ruled on 1; Step 2 ruled and not "
                        "approved")

FOREIGN_RECORDED_AS_RECORD = (
    "# Step 2 gate record\n\n"
    "This record notes the Step 3 ruling, recorded as CLOSED-PASS.\n")
BARE_NOTE_RECORD = ("# Step 2 gate record\n\n"
                    "This record notes the Step 3 ruling.\n")
FOREIGN_CLOSES_RULING = (
    "# Step 2 gate ruling\n\n"
    "This ruling closes CLOSED-PASS for Step 3.\n")
FOREIGN_FIELD_RECORD = (
    "# Step 2 gate record\n\n"
    "Closure state: CLOSED-PASS for Step 3.\n")
FOREIGN_FAIL_RULING = (
    "# Step 2 gate ruling\n\n"
    "This ruling notes the Step 3 ruling, recorded as CLOSED-FAIL.\n")
OWN_STEP_RECORDED_AS_RECORD = (
    "# Step 2 gate record\n\n"
    "This record notes the Step 2 ruling, recorded as CLOSED-PASS.\n")
FOREIGN_THEN_OWN_RECORD = (
    "# Step 2 gate record\n\n"
    "This record notes the Step 3 ruling, recorded as CLOSED-PASS.\n"
    "This record was recorded as CLOSED-FAIL.\n")


class TestStep15Round7F2(FixtureTestCase):

    def _assert_f2_row(self, root, verdict, figures):
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, verdict, "F-2")
        first_line = block.splitlines()[0]
        fields = [part.strip() for part in first_line.split("|")]
        self.assertEqual(fields[3], figures)
        return block

    def _contested_ruling_table(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-ruling.md"] = gate_ruling(
            2, "CLOSED-PASS")
        table["steps/sub/step-02-gate-ruling.md"] = gate_ruling(
            2, "CLOSED-FAIL")
        return table

    # ------------------------------------------------------------ F15-46

    def test_f15_46_contested_ruling_behind_record_plain_branch_not_derivable(self):
        root = build_tree(self._contested_ruling_table())
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_46_contested_ruling_behind_record_regate_branch_not_derivable(self):
        table = self._contested_ruling_table()
        table["steps/step-02-regate-record.md"] = gate_record(
            2, "CLOSED-QUALIFIED")
        root = build_tree(table)
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_46_contested_record_governing_not_derivable(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = gate_record(
            2, "CLOSED-PASS")
        table["steps/sub/step-02-gate-record.md"] = gate_record(
            2, "CLOSED-FAIL")
        table["steps/step-02-gate-ruling.md"] = gate_ruling(
            2, "CLOSED-PASS")
        root = build_tree(table)
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_46_control_sound_fail_ruling_not_derivable(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-ruling.md"] = gate_ruling(
            2, "CLOSED-FAIL")
        root = build_tree(table)
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_46_control_sound_fail_ruling_with_regate_not_derivable(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-ruling.md"] = gate_ruling(
            2, "CLOSED-FAIL")
        table["steps/step-02-regate-record.md"] = gate_record(
            2, "CLOSED-QUALIFIED")
        root = build_tree(table)
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_46_control_agreeing_record_and_ruling_counts_plain(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-ruling.md"] = gate_ruling(
            2, "CLOSED-PASS")
        root = build_tree(table)
        self._assert_f2_row(root, "present", PLAIN_ONE_FIGURES)

    def test_f15_46_control_contested_adjudication_behind_base_pair_counts_plain(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-ruling.md"] = gate_ruling(
            2, "CLOSED-PASS")
        table["steps/step-02-gate-adjudication.md"] = gate_record(
            2, "CLOSED-PASS")
        table["steps/sub/step-02-gate-adjudication.md"] = gate_record(
            2, "CLOSED-FAIL")
        root = build_tree(table)
        self._assert_f2_row(root, "present", PLAIN_ONE_FIGURES)

    # ------------------------------------------------------------ F15-47

    def test_f15_47_foreign_recorded_as_governing_record_not_derivable(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = \
            FOREIGN_RECORDED_AS_RECORD
        table["steps/step-02-gate-adjudication.md"] = gate_record(
            2, "CLOSED-FAIL")
        root = build_tree(table)
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_47_foreign_closes_only_closure_ruling_not_derivable(self):
        table = base_case(steps=(2,))
        del table["steps/step-02-gate-record.md"]
        table["steps/step-02-gate-ruling.md"] = FOREIGN_CLOSES_RULING
        root = build_tree(table)
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_47_foreign_recorded_as_regate_branch_not_derivable(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = \
            FOREIGN_RECORDED_AS_RECORD
        table["steps/step-02-gate-adjudication.md"] = gate_record(
            2, "CLOSED-FAIL")
        table["steps/step-02-regate-record.md"] = gate_record(
            2, "CLOSED-QUALIFIED")
        root = build_tree(table)
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_47_foreign_field_form_governing_record_not_derivable(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = FOREIGN_FIELD_RECORD
        table["steps/step-02-gate-adjudication.md"] = gate_record(
            2, "CLOSED-FAIL")
        root = build_tree(table)
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_47_foreign_closure_in_base_ruling_counts_nowhere(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-ruling.md"] = FOREIGN_FAIL_RULING
        root = build_tree(table)
        self._assert_f2_row(root, "present", PLAIN_ONE_FIGURES)

    def test_f15_47_foreign_then_own_closure_in_one_piece_counts_own(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = \
            FOREIGN_THEN_OWN_RECORD
        root = build_tree(table)
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_47_control_record_without_foreign_closure_not_derivable(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = BARE_NOTE_RECORD
        table["steps/step-02-gate-adjudication.md"] = gate_record(
            2, "CLOSED-FAIL")
        root = build_tree(table)
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_47_control_own_step_named_closure_counts(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = \
            OWN_STEP_RECORDED_AS_RECORD
        root = build_tree(table)
        self._assert_f2_row(root, "present", PLAIN_ONE_FIGURES)

    def test_f15_47_control_no_step_named_closure_counts(self):
        table = base_case(steps=(2,))
        del table["steps/step-02-gate-record.md"]
        table["steps/step-02-gate-ruling.md"] = gate_ruling(
            2, "CLOSED-PASS")
        root = build_tree(table)
        self._assert_f2_row(root, "present", PLAIN_ONE_FIGURES)


if __name__ == "__main__":
    unittest.main()
