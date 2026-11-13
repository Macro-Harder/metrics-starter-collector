"""Step 15 fix round 9 tests: closure fragment joins, F25 seat.

Each charged case pins F15-64 (CB8-3, Low) in the closure
fragment test of derivation_core.py. The fragment in
_closure_names_foreign_step was bounded after a match only by
" and " and a semicolon, so a second closure statement joined
to the first by a comma, or, but, while, a colon or a dash in
the same sentence poisoned the first statement's own closure
with its foreign step; and a step named after an earlier
closure token in the same sentence (the field form naming its
step after its token) leaked into the next closure statement's
fragment, so that statement's own closure was discarded as
foreign. Control cases pin the behaviour that must not move:
the comma inside a single closure sentence stays inside its
fragment (the F15-47 form), a single statement naming two
steps stays discarded, the " and " and semicolon bounds hold
as before, and the closure pattern precedence (the field form
scanned first) holds.
"""
import unittest

from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, row_block,
                                     run_tool)

NOT_DERIVABLE_FIGURES = ("no rate figure; plain approvals 0; "
                         "qualified approvals 0; steps ruled on 0")
PLAIN_ONE_FIGURES = ("first-time approval rate 100 percent; "
                     "plain approvals 1; qualified approvals 0; "
                     "steps ruled on 1")
NOT_APPROVED_FIGURES = ("first-time approval rate 0 percent; "
                        "plain approvals 0; qualified approvals 0; "
                        "steps ruled on 1; Step 2 ruled and not "
                        "approved")


def record(text):
    return "# Step 2 gate record\n\n" + text + "\n"


class TestStep15Round9Closure(FixtureTestCase):

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

    # ------------------------------------------- after a match (i)

    def test_f15_64_after_comma_foreign_does_not_poison_own_fail(self):
        root = self._f2_root(
            "This record recorded as CLOSED-FAIL, the Step 3 "
            "ruling recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_64_after_or_but_while_foreign_does_not_poison(self):
        for join in ("or", "but", "while"):
            with self.subTest(join=join):
                root = self._f2_root(
                    "This record recorded as CLOSED-FAIL " + join
                    + " the Step 3 ruling recorded as CLOSED-PASS.")
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    def test_f15_64_after_colon_dash_foreign_does_not_poison(self):
        for join in (":", " -"):
            with self.subTest(join=join):
                root = self._f2_root(
                    "This record recorded as CLOSED-FAIL" + join
                    + " the Step 3 ruling recorded as CLOSED-PASS.")
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    # --------------------------- step after an earlier token (ii)

    def test_f15_64_step_after_earlier_token_comma_does_not_leak(self):
        root = self._f2_root(
            "Closure state: CLOSED-PASS for Step 3, this record "
            "recorded as CLOSED-FAIL.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_64_step_after_earlier_token_named_own_step_reads_fail(self):
        root = self._f2_root(
            "Closure state: CLOSED-PASS for Step 3, the Step 2 "
            "ruling recorded as CLOSED-FAIL.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_64_step_after_earlier_token_other_joins_do_not_leak(self):
        frames = (
            "Closure state: CLOSED-PASS for Step 3 and this record "
            "recorded as CLOSED-FAIL.",
            "Closure state: CLOSED-PASS for Step 3 or this record "
            "recorded as CLOSED-FAIL.",
            "Closure state: CLOSED-PASS for Step 3 but this record "
            "recorded as CLOSED-FAIL.",
            "Closure state: CLOSED-PASS for Step 3 while this "
            "record recorded as CLOSED-FAIL.",
            "Closure state: CLOSED-PASS for Step 3: this record "
            "recorded as CLOSED-FAIL.",
            "Closure state: CLOSED-PASS for Step 3 - this record "
            "recorded as CLOSED-FAIL.",
            "Closure state: CLOSED-PASS for Step 3; this record "
            "recorded as CLOSED-FAIL.",
        )
        for frame in frames:
            with self.subTest(frame=frame):
                root = self._f2_root(frame)
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    def test_f15_64_step_after_earlier_token_field_form_next_counts(self):
        root = self._f2_root(
            "Closure state: CLOSED-PASS for Step 3, Closure "
            "state: CLOSED-FAIL.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    # ------------------------------------------------------ controls

    def test_f15_64_control_comma_inside_single_statement_stays_foreign(self):
        root = self._f2_root(
            "The Step 3 ruling stands, recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_64_control_two_steps_one_statement_stays_discarded(self):
        root = self._f2_root(
            "This record notes the Step 2 and Step 3 ruling, "
            "recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_64_control_comma_inside_single_own_statement_counts(self):
        root = self._f2_root(
            "This record notes the Step 2 ruling, recorded as "
            "CLOSED-PASS.")
        self._assert_f2_row(root, "present", PLAIN_ONE_FIGURES)

    def test_f15_64_control_after_and_semicolon_own_fail_counts(self):
        for frame in (
                "This record recorded as CLOSED-FAIL and the "
                "Step 3 ruling recorded as CLOSED-PASS.",
                "This record recorded as CLOSED-FAIL; the Step 3 "
                "ruling recorded as CLOSED-PASS."):
            with self.subTest(frame=frame):
                root = self._f2_root(frame)
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    def test_f15_64_control_pattern_precedence_field_form_first(self):
        root = self._f2_root(
            "This record recorded as CLOSED-PASS. Closure "
            "state: CLOSED-FAIL.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)


if __name__ == "__main__":
    unittest.main()
