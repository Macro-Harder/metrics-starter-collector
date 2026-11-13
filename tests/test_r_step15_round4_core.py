"""Step 15 fix round 4 tests: derivation core cluster.

Each case pins one fix round 4 finding in derivation_core.py:
F15-28, a regate piece counted as the first ruling where the only
ruling beside it stands in a numbered round or re-audit named
ruling, because the ranked order demoted those names to the regate
rank; and F15-29, negated interval duration mentions in further
shapes still standing as durations for T-2, on both the interval
duration path and the BANKED alternative. Control cases pin the
behaviour that must not move: the unnumbered re-audit form, the
M-1 recycled step counting, the F15-14 conflict construction, the
F15-23 forms, the F15-16, F15-21 and F15-25 duration controls, and
the genuinely standing duration forms.
"""
import unittest

from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, gate_record,
                                     gate_ruling, metrics_record,
                                     path_ledger, row_block, run_tool)

DATE_ONLY_LINE = "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.\n"
FULL_INTERVALS = (
    "Step 1 IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 17:00.\n"
    "Step 2 IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 17:00.\n"
    "Step 3 IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 17:00.")


class TestStep15Round4Core(FixtureTestCase):

    # ------------------------------------------------------------ F15-28

    def _numbered_ruling_tree(self, ruling_name, ruling_closure,
                              regate_closure):
        table = base_case(steps=(2,))
        del table["steps/step-02-gate-record.md"]
        table["steps/" + ruling_name] = gate_ruling(2, ruling_closure)
        if regate_closure is not None:
            table["steps/step-02-regate-record.md"] = gate_record(
                2, regate_closure)
        return build_tree(table)

    def _assert_f2_not_approved(self, root):
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")
        self.assertIn("first-time approval rate 0 percent", block)
        self.assertIn("plain approvals 0", block)
        self.assertIn("qualified approvals 0", block)
        self.assertIn("steps ruled on 1", block)
        self.assertIn("Step 2 ruled and not approved", block)

    def test_f15_28_reaudit1_fail_ruling_with_regate_counts_not_approved(self):
        self._assert_f2_not_approved(self._numbered_ruling_tree(
            "step-02-gate-ruling-reaudit-1.md", "CLOSED-FAIL",
            "CLOSED-QUALIFIED"))

    def test_f15_28_round1_fail_ruling_with_regate_counts_not_approved(self):
        self._assert_f2_not_approved(self._numbered_ruling_tree(
            "step-02-gate-ruling-round-1.md", "CLOSED-FAIL",
            "CLOSED-QUALIFIED"))

    def test_f15_28_round2_fail_ruling_with_regate_counts_not_approved(self):
        self._assert_f2_not_approved(self._numbered_ruling_tree(
            "step-02-gate-ruling-round-2.md", "CLOSED-FAIL",
            "CLOSED-QUALIFIED"))

    def test_f15_28_reaudit1_pass_ruling_with_regate_fail_counts_plain(self):
        root = self._numbered_ruling_tree(
            "step-02-gate-ruling-reaudit-1.md", "CLOSED-PASS",
            "CLOSED-FAIL")
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")
        self.assertIn("first-time approval rate 100 percent", block)
        self.assertIn("plain approvals 1", block)
        self.assertIn("qualified approvals 0", block)
        self.assertIn("steps ruled on 1", block)
        self.assertNotIn("not approved", block)

    def test_f15_28_mixed_steps_numbered_fail_beside_clean_pass(self):
        table = base_case(steps=(1, 2))
        del table["steps/step-02-gate-record.md"]
        table["steps/step-02-gate-ruling-reaudit-1.md"] = gate_ruling(
            2, "CLOSED-FAIL")
        table["steps/step-02-regate-record.md"] = gate_record(
            2, "CLOSED-QUALIFIED")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")
        self.assertIn("first-time approval rate 50 percent", block)
        self.assertIn("plain approvals 1", block)
        self.assertIn("qualified approvals 0", block)
        self.assertIn("steps ruled on 2", block)
        self.assertIn("Step 2 ruled and not approved", block)

    def test_f15_28_control_numbered_ruling_without_regate_counts_fail(self):
        self._assert_f2_not_approved(self._numbered_ruling_tree(
            "step-02-gate-ruling-reaudit-1.md", "CLOSED-FAIL", None))

    def test_f15_28_control_unnumbered_reaudit_fail_with_regate(self):
        self._assert_f2_not_approved(self._numbered_ruling_tree(
            "step-02-gate-ruling-reaudit.md", "CLOSED-FAIL",
            "CLOSED-QUALIFIED"))

    def test_f15_28_control_recycled_step_counted_once_by_first_ruling(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = gate_record(
            2, "CLOSED-FAIL")
        table["steps/step-02-regate-record.md"] = gate_record(
            2, "CLOSED-QUALIFIED", extra="Recycled instance ruling.")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")
        self.assertIn("first-time approval rate 0 percent", block)
        self.assertIn("plain approvals 0", block)
        self.assertIn("qualified approvals 0", block)
        self.assertIn("steps ruled on 1", block)
        self.assertIn("first instance closed CLOSED-FAIL", block)

    def test_f15_28_control_regate_conflicting_base_closures_not_derivable(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = gate_record(
            2, "CLOSED-PASS")
        table["steps/step-02-gate-ruling.md"] = gate_ruling(
            2, "CLOSED-FAIL")
        table["steps/step-02-regate-record.md"] = gate_record(
            2, "CLOSED-QUALIFIED")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present but not derivable", "F-2")
        self.assertNotIn("100 percent", block)
        self.assertIn("plain approvals 0", block)
        self.assertIn("steps ruled on 0", block)

    def test_f15_28_control_adjudication_first_fail_with_regate(self):
        table = base_case(steps=(2,))
        del table["steps/step-02-gate-record.md"]
        table["steps/step-02-gate-adjudication.md"] = gate_record(
            2, "CLOSED-FAIL")
        table["steps/step-02-regate-record.md"] = gate_record(
            2, "CLOSED-QUALIFIED")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")
        self.assertIn("first-time approval rate 0 percent", block)
        self.assertIn("qualified approvals 0", block)
        self.assertIn("steps ruled on 1", block)
        self.assertIn("Step 2 ruled and not approved", block)

    def test_f15_28_control_regate_round_ruling_fail_beside_record_pass(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = gate_record(
            2, "CLOSED-PASS")
        table["steps/step-02-gate-ruling-round-1.md"] = gate_ruling(
            2, "CLOSED-FAIL")
        table["steps/step-02-regate-record.md"] = gate_record(
            2, "CLOSED-QUALIFIED")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")
        self.assertIn("first-time approval rate 100 percent", block)
        self.assertIn("plain approvals 1", block)
        self.assertIn("qualified approvals 0", block)
        self.assertIn("steps ruled on 1", block)
        self.assertNotIn("ran as two instances", block)

    def test_f15_28_control_regate_alone_counts_as_first_ruling(self):
        table = base_case(steps=(2,))
        del table["steps/step-02-gate-record.md"]
        table["steps/step-02-regate-record.md"] = gate_record(
            2, "CLOSED-QUALIFIED")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")
        self.assertIn("first-time approval rate 100 percent", block)
        self.assertIn("plain approvals 0", block)
        self.assertIn("qualified approvals 1", block)
        self.assertIn("steps ruled on 1", block)

    # ------------------------------------------------------------ F15-29

    def _date_only_t2_block(self, note_text):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            DATE_ONLY_LINE + note_text, steps="1, 2, 3")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        return row_block(result.stdout, "T-2")

    def _assert_date_only_true_ground(self, note_text):
        block = self._date_only_t2_block(note_text)
        assert_verdict(self, block, "missing", "T-2")
        self.assertIn("date-only-form", block)
        self.assertIn("no BANKED, SUSPENDED or halt interval "
                      "duration stands", block)
        self.assertNotIn("an interval duration stands in the "
                         "transition log, but no active figure",
                         block)

    def test_f15_29_after_auxiliary_negations_date_only_true_ground(self):
        for note in (
                "Note: the interval duration was not recorded for "
                "this step.",
                "Note: the interval duration has not been recorded "
                "for this step.",
                "Note: the interval duration was never recorded for "
                "this step.",
                "Note: an interval duration does not stand in this "
                "log."):
            with self.subTest(note=note):
                self._assert_date_only_true_ground(note)

    def test_f15_29_after_comma_intervening_contraction_date_only(self):
        for note in (
                "Note: interval duration, not recorded for this "
                "step.",
                "Note: the interval duration for this step was not "
                "kept.",
                "Note: the interval duration isn't recorded for "
                "this step."):
            with self.subTest(note=note):
                self._assert_date_only_true_ground(note)

    def test_f15_29_after_negations_no_timestamp_true_ground(self):
        for note in (
                "Note: the interval duration was not recorded for "
                "this step.",
                "Note: interval duration, not recorded for this "
                "step.",
                "Note: the interval duration isn't recorded for "
                "this step."):
            with self.subTest(note=note):
                table = base_case()
                table["PATH-LEDGER.md"] = path_ledger(
                    "Step 1 stands with no transitions recorded.\n"
                    + note, steps="1, 2, 3")
                root = build_tree(table)
                result = run_tool(root)
                self.assertEqual(result.returncode, 0,
                                 result.stderr)
                block = row_block(result.stdout, "T-2")
                assert_verdict(self, block, "missing", "T-2")
                self.assertIn("no-feeder-record", block)
                self.assertIn("no interval duration stands in the "
                              "transition log to carry an active "
                              "figure", block)
                self.assertNotIn(
                    "an interval duration stands in the transition "
                    "log, but no active figure", block)

    def test_f15_29_neighbouring_clause_denials_date_only(self):
        for note in (
                "An interval duration is discussed in this note.\n"
                "No such duration is recorded for any step.",
                "No duration is recorded for this step.\n"
                "Interval duration: see the note above.",
                "No wait was banked. The interval duration is a "
                "heading only in this log."):
            with self.subTest(note=note):
                self._assert_date_only_true_ground(note)

    def test_f15_29_quoted_and_retracted_mentions_date_only(self):
        for note in (
                'The draft states "an interval duration stands", '
                "but that claim was withdrawn and no duration was "
                "recorded.",
                "According to the earlier note, an interval "
                "duration was recorded, although that note was "
                "wrong."):
            with self.subTest(note=note):
                self._assert_date_only_true_ground(note)

    def test_f15_29_other_denial_shapes_date_only(self):
        for note in (
                "Note: an interval duration cannot be derived for "
                "this step.",
                "Note: an interval duration is absent from this "
                "log.",
                "Note: the log stands without an interval "
                "duration.",
                "Note: the log fails to record an interval "
                "duration."):
            with self.subTest(note=note):
                self._assert_date_only_true_ground(note)

    def test_f15_29_negated_banked_line_with_number_date_only(self):
        for note in (
                "Note: no BANKED interval duration 5 hours was "
                "recorded.",
                "Note: a BANKED interval duration 5 hours was not "
                "recorded for this step."):
            with self.subTest(note=note):
                self._assert_date_only_true_ground(note)

    def test_f15_29_refusal_negated_mention_t2_missing_no_feeder(self):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            FULL_INTERVALS + "\nNote: the interval duration was "
            "not recorded for this step.", steps="1, 2, 3")
        table["wiki/wiki/synthesis/build-metrics-record.md"] = \
            metrics_record(body="Step table stands.",
                           header_version="unknown-version-999")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "T-2")
        assert_verdict(self, block, "missing", "T-2")
        self.assertIn("no-feeder-record", block)
        self.assertIn("no interval duration stands in the "
                      "transition log from which an active figure "
                      "for this row could form", block)
        self.assertNotIn("unknown-definitions-version", block)

    def test_f15_29_control_genuine_banked_duration_still_stands(self):
        block = self._date_only_t2_block(
            "Step 1 BANKED interval duration 5 hours.")
        assert_verdict(self, block, "missing", "T-2")
        self.assertIn("no-feeder-record", block)
        self.assertIn("an interval duration stands in the "
                      "transition log", block)

    def test_f15_29_control_banked_number_without_interval_words_stands(self):
        block = self._date_only_t2_block("Step 1 BANKED 5 hours.")
        assert_verdict(self, block, "missing", "T-2")
        self.assertIn("no-feeder-record", block)
        self.assertNotIn("date-only-form", block)

    def test_f15_29_control_standing_beside_negated_mention_still_stands(self):
        block = self._date_only_t2_block(
            "Step 1 BANKED interval duration 5 hours.\n"
            "Note: no interval duration is recorded for Step 2.")
        assert_verdict(self, block, "missing", "T-2")
        self.assertIn("no-feeder-record", block)
        self.assertIn("an interval duration stands in the "
                      "transition log", block)

    def test_f15_29_control_before_negation_still_true_ground(self):
        self._assert_date_only_true_ground(
            "Note: no interval duration is recorded for this step.")

    def test_f15_29_control_refusal_genuine_duration_unknown_version(self):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            FULL_INTERVALS + "\nStep 1 BANKED interval duration "
            "5 hours.", steps="1, 2, 3")
        table["wiki/wiki/synthesis/build-metrics-record.md"] = \
            metrics_record(body="Step table stands.",
                           header_version="unknown-version-999")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "T-2")
        assert_verdict(self, block, "present but not derivable",
                       "T-2")
        self.assertIn("unknown-definitions-version", block)
        self.assertIn("unknown-version-999", block)


if __name__ == "__main__":
    unittest.main()
