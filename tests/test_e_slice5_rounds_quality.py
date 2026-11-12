"""Slice 5 tests: rounds and quality family T-7, Q-1, Q-3, Q-4."""
import unittest

from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     assert_reads_capture_only, base_case,
                                     build_tree, gate_record, metrics_record,
                                     row_block, run_tool, statement_segment,
                                     step_record)

TRUNCATED = ("# Audit paper\n\nFindings so far: Critical 1, High 2.\n"
             "This paper ends mid sentence with no closing total and no\n")


def audit_table(extra_files):
    table = base_case()
    table.update(extra_files)
    return table


def assert_ca10_before_count(test, block, count_text):
    lowered = block.lower()
    pop_at = lowered.find("population")
    excl_at = lowered.find("excluded")
    count_at = block.find(count_text)
    test.assertTrue(0 <= pop_at < excl_at, block[:500])
    test.assertTrue(0 <= excl_at < count_at,
                    "exclusion list does not stand before the count")


class TestSlice5RoundsQuality(FixtureTestCase):

    def test_f05_truncated_paper_no_correcting_record(self):
        root = build_tree(audit_table({"audit/step-01-red.md": TRUNCATED}))
        result = run_tool(root)
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present but not derivable", "Q-1")
        self.assertIn("truncated-no-correcting-record", block)
        self.assertIn("incomplete", result.stdout.lower())

    def test_f06_truncated_paper_with_correcting_record(self):
        root = build_tree(audit_table({
            "audit/step-01-red.md": TRUNCATED,
            "audit/step-01-correction.md": (
                "# Correction\n\nThe truncated paper audit/step-01-red.md "
                "corrected total: Critical 1, High 2, Medium 0, Low 0, "
                "post triage breakdown.\n")}))
        result = run_tool(root)
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present", "Q-1")
        self.assertIn("step-01-correction.md", block)
        self.assertIn("Critical 1", block)
        self.assertIn("High 2", block)

    def test_f06b_repaired_truncation_present_with_repair_cited(self):
        repaired = (TRUNCATED +
                    "\n## Completion section\n\nThis piece was found "
                    "truncated. This file, audit/step-01-red.md, supplies "
                    "the missing content in place: post triage breakdown "
                    "Critical 1, High 2, Medium 0, Low 0.\n")
        root = build_tree(audit_table({"audit/step-01-red.md": repaired}))
        result = run_tool(root)
        self.assertIn("repair", result.stdout.lower())
        self.assertNotIn("unrepaired truncation", result.stdout.lower())
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present", "Q-1")

    def test_f07_placeholder_zero_against_measured_zero(self):
        root = build_tree(audit_table({
            "registers/defect-register.md": (
                "# Defect register\n\nEscaped defects printed as 0 with "
                "no measurement basis stated.\n")}))
        result = run_tool(root)
        block = row_block(result.stdout, "Q-3")
        assert_verdict(self, block, "present but not derivable", "Q-3")
        self.assertIn("no-measurement-basis", block)
        root2 = build_tree(audit_table({
            "registers/defect-register.md": (
                "# Defect register\n\nEscaped defects: 0. Measurement "
                "basis: every register entry was triaged in full on "
                "2026-11-02 and no entry escaped.\n")}))
        result2 = run_tool(root2)
        block2 = row_block(result2.stdout, "Q-3")
        assert_verdict(self, block2, "present", "Q-3")
        self.assertIn("measurement basis", block2.lower())

    def test_f07b_zero_with_correcting_record_basis(self):
        root = build_tree(audit_table({
            "registers/defect-register.md": (
                "# Defect register\n\nEscaped defects: 0.\n"),
            "registers/correction.md": (
                "# Correction\n\nThe zero for escaped defects in the "
                "defect register is corrected: its measurement basis is "
                "a full triage of every register entry, none escaped.\n")}))
        result = run_tool(root)
        block = row_block(result.stdout, "Q-3")
        assert_verdict(self, block, "present", "Q-3")
        self.assertIn("correction.md", block)

    def test_q3_printed_zero_never_stated_as_measured_zero(self):
        root = build_tree(audit_table({
            "wiki/wiki/synthesis/build-metrics-record.md": metrics_record(
                body="Escapes attributed (Q-3): 0, none known.")}))
        result = run_tool(root)
        block = row_block(result.stdout, "Q-3")
        assert_verdict(self, block, "present but not derivable", "Q-3")
        self.assertIn("no-measurement-basis", block)

    def test_q3_contested_origin_step_carried_under_d18(self):
        root = build_tree(audit_table({
            "registers/defect-register.md": (
                "# Defect register\n\nEntry D-9: defect disposition, "
                "origin step Step 2.\n"),
            "wiki/wiki/synthesis/build-metrics-record.md": metrics_record(
                body="Metrics record states the step universe as 1 step.")}))
        result = run_tool(root)
        block = row_block(result.stdout, "Q-3")
        segment = statement_segment(block)
        self.assertIn("record disagrees", segment)
        self.assertIn("Step 2", segment)
        self.assertIn("build-metrics-record.md", segment)

    def test_f12_empty_tables_with_stale_text_t7_limb(self):
        root = build_tree(audit_table({
            "wiki/wiki/synthesis/build-metrics-record.md": metrics_record(
                body="Loop round table: no rows. Text states no loop "
                     "step has run yet. Audit round table: no rows.")}))
        result = run_tool(root)
        block = row_block(result.stdout, "T-7")
        assert_verdict(self, block, "present but not derivable", "T-7")
        self.assertNotIn("0 rounds", block)
        q1 = row_block(result.stdout, "Q-1")
        assert_verdict(self, q1, "missing", "Q-1")
        self.assertIn("no-feeder-record", q1)
        self.assertNotIn("0 rounds", q1)

    def test_f14_mixed_severity_scales(self):
        root = build_tree(audit_table({
            "audit/step-01-red.md": (
                "# Round 1\n\nPost triage breakdown on Scale A: "
                "Critical 1.\n"),
            "audit/step-02-red.md": (
                "# Round 2\n\nPost triage breakdown on Scale B: "
                "Critical 5.\n")}))
        result = run_tool(root)
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present but not derivable", "Q-1")
        self.assertIn("governing-scale-conflict", block)

    def test_g05_irreconcilable_counts_both_named(self):
        root = build_tree(audit_table({
            "steps/step-01-record.md": step_record(
                1, extra="Loop step. Pass count in this record: 3 passes."),
            "steps/step-01-gate-record.md": gate_record(
                1, extra="Verdict record count for this step: 1 verdict "
                         "record stands.")}))
        result = run_tool(root)
        block = row_block(result.stdout, "T-7")
        assert_verdict(self, block, "present but not derivable", "T-7")
        self.assertIn("record-disagrees", block)
        import re
        self.assertRegex(block, r"(?<!\d)(?<!\d\.)3 passes\b|"
                                r"pass count[^\d]*3(?!\d)(?!\.\d)")
        self.assertRegex(block, r"verdict[^\d]*1(?!\d)(?!\.\d)")

    def test_g06_pre_triage_breakdown_refused(self):
        root = build_tree(audit_table({
            "audit/step-01-red.md": (
                "# Round 1 paper\n\nPre triage counts: Critical 4, "
                "High 4. No post triage breakdown stands.\n")}))
        result = run_tool(root)
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present but not derivable", "Q-1")
        self.assertIn("no-post-triage-breakdown", block)

    def test_g07_commissioned_scale_limited_and_attack_totals_refused(self):
        root = build_tree(audit_table({
            "steps/step-01-gate-adjudication.md": (
                "# Adjudication\n\nA commissioned severity scale governs "
                "Round 1 only. Round 1 post triage breakdown: "
                "Critical 1, High 0, Medium 0, Low 0.\n"),
            "audit/step-02-red.md": (
                "# Round 2\n\nAttack totals: Critical 9, High 9. "
                "These grade attacks, not triaged findings.\n")}))
        result = run_tool(root)
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present but not derivable", "Q-1")
        self.assertIn("Round 2", block)
        self.assertIn("Critical 1", block)
        self.assertNotIn("Critical 9", block)
        self.assertNotIn("High 9", block)

    def test_g08_first_trace_by_record_order_with_form_precedence(self):
        root = build_tree(audit_table({
            "steps/step-01-trace.md": (
                "# First trace\n\nElements: 10. LANDED 8, PARTIAL 2.\n"),
            "steps/step-01-gate-record.md": gate_record(
                1, extra="Later re-audit trace: 10 of 10 LANDED.")}))
        result = run_tool(root)
        block = row_block(result.stdout, "Q-4")
        assert_verdict(self, block, "present", "Q-4")
        self.assertIn("step-01-trace.md", block)
        self.assertRegex(block, r"(?<!\d)(?<!\d\.)8(?!\d)(?!\.\d)")

    def test_wv6_conflicting_governing_adjudications(self):
        root = build_tree(audit_table({
            "steps/step-01-gate-adjudication.md": (
                "# Adjudication A\n\nScale X governs Rounds 1 and 2.\n"),
            "steps/step-02-gate-adjudication.md": (
                "# Adjudication B\n\nScale Y governs Rounds 1 and 2.\n"),
            "audit/step-03-red.md": (
                "# Round 3\n\nPost triage breakdown: Critical 0, "
                "High 1, Medium 0, Low 0.\n")}))
        result = run_tool(root)
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present but not derivable", "Q-1")
        self.assertIn("governing-scale-conflict", block)
        self.assertIn("Round 1", block)

    def test_wv6_resolved_conflict_variant_not_blocked(self):
        root = build_tree(audit_table({
            "steps/step-01-gate-adjudication.md": (
                "# Adjudication A\n\nScale X governs Round 1.\n"),
            "steps/step-02-gate-adjudication.md": (
                "# Adjudication B\n\nScale Y governs Round 1. This later "
                "governing statement resolves the conflict: Scale X "
                "governs Round 1.\n"),
            "audit/step-01-red.md": (
                "# Round 1\n\nPost triage breakdown: Critical 1, "
                "High 0, Medium 0, Low 0.\n")}))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "Q-1")
        self.assertTrue(block)
        self.assertNotIn("governing-scale-conflict", block)

    def test_ca10_q1_population_and_exclusion_list_before_count(self):
        root = build_tree(audit_table({
            "audit/step-01-red.md": (
                "# Round 1\n\nPost triage breakdown: Critical 1.\n"),
            "audit/step-02-red.md": (
                "# Round 2\n\nPre triage counts only: Critical 3.\n")}))
        result = run_tool(root)
        block = row_block(result.stdout, "Q-1")
        assert_ca10_before_count(self, block, "Critical 1")
        excl_at = block.lower().find("excluded")
        excl_segment = block[excl_at:]
        self.assertIn("Round 2", excl_segment)
        self.assertIn("no post triage breakdown", excl_segment.lower())

    def test_ca10_t7_population_and_exclusion_list(self):
        table = base_case()
        table["steps/step-01-record.md"] = step_record(
            1, extra="Loop step. Rounds run in a loop for this step.")
        table["steps/step-02-record.md"] = step_record(
            2, extra="Loop step. A board ruling held inside this record "
                     "states 2 rounds for this step.")
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "T-7")
        assert_ca10_before_count(self, block, "2 rounds")
        lowered = block.lower()
        pop_at = lowered.find("population")
        excl_at = lowered.find("excluded")
        self.assertTrue(0 <= pop_at < excl_at, block[:500])
        pop_segment = block[pop_at:excl_at]
        self.assertIn("Step 1", pop_segment)
        self.assertIn("Step 2", pop_segment)
        excl_segment = block[excl_at:]
        self.assertIn("board ruling", excl_segment.lower())
        self.assertTrue("Step 2" in excl_segment or
                        "step-02-record" in excl_segment, excl_segment[:300])

    def test_q1_bounded_form_prints_qualifying_round_counts_only(self):
        root = build_tree(audit_table({
            "audit/step-01-red.md": (
                "# Round 1\n\nPost triage breakdown: Critical 2, "
                "High 1, Medium 0, Low 0.\n"),
            "audit/step-02-red.md": (
                "# Round 2\n\nPre triage counts only: Critical 7.\n")}))
        result = run_tool(root)
        block = row_block(result.stdout, "Q-1")
        self.assertIn("bounded", block.lower())
        self.assertIn("Round 1", block)
        self.assertIn("Critical 2", block)
        self.assertNotIn("Critical 7", block)

    def test_g09_q4_present_with_coverage_remainder_forms(self):
        root = build_tree(audit_table({
            "steps/step-01-trace.md": (
                "# Trace\n\nElements: 10. LANDED 10.\n"),
            "steps/step-02-record.md": step_record(
                2, extra="No fold in trace as such: analogue only step."),
            "steps/step-03-trace.md": (
                "# Trace\n\nElements: 0. LANDED 0.\n")}))
        result = run_tool(root)
        block = row_block(result.stdout, "Q-4")
        assert_verdict(self, block, "present", "Q-4")
        self.assertIn("Step 2", block)
        self.assertIn("analogue", block.lower())
        self.assertIn("Step 3", block)
        self.assertIn("zero total", block.lower())

    def test_q4_partial_coverage_without_defined_form_is_not_present(self):
        root = build_tree(audit_table({
            "steps/step-01-trace.md": "# Trace fragment\n\nNo totals stand.\n"}))
        result = run_tool(root)
        block = row_block(result.stdout, "Q-4")
        assert_verdict(self, block, "present but not derivable", "Q-4")
        self.assertIn("missing-field", block)

    def test_q4_step_stating_no_trace_applies_is_excluded(self):
        root = build_tree(audit_table({
            "steps/step-01-trace.md": (
                "# Trace\n\nElements: 4. LANDED 4.\n"),
            "steps/step-02-record.md": step_record(
                2, extra="No trace applies to this step.")}))
        result = run_tool(root)
        block = row_block(result.stdout, "Q-4")
        assert_verdict(self, block, "present", "Q-4")
        self.assertIn("Step 2", block)
        self.assertIn("not applicable", block.lower())

    def test_q4_row_cross_check_marking_in_statement_line(self):
        root = build_tree(audit_table({
            "steps/step-01-trace.md": (
                "# Trace\n\nElements: 10. LANDED 8.\n"),
            "wiki/wiki/synthesis/build-metrics-record.md": metrics_record(
                body="Metrics record states Q-4 for Step 1 as 10 of 10.")}))
        result = run_tool(root)
        block = row_block(result.stdout, "Q-4")
        segment = statement_segment(block)
        self.assertIn("record disagrees", segment)
        self.assertIn("build-metrics-record.md", segment)
        self.assertIn("8 of 10", segment)
        self.assertIn("10 of 10", segment)

    def test_f18_unknown_version_slice5_rows(self):
        root = build_tree(audit_table({
            "steps/step-01-trace.md": (
                "# Trace\n\nElements: 10. LANDED 8.\n"),
            "audit/step-01-red.md": (
                "# Round 1\n\nPost triage breakdown: Critical 1.\n"),
            "wiki/wiki/synthesis/build-metrics-record.md": metrics_record(
                body="Step table stands.",
                header_version="unknown-version-999")}))
        result = run_tool(root)
        for code in ("T-7", "Q-1", "Q-4"):
            block = row_block(result.stdout, code)
            assert_verdict(self, block, "present but not derivable", code)
            self.assertIn("unknown-definitions-version", block, code)
            self.assertIn("unknown-version-999", block, code)
        assert_verdict(self, row_block(result.stdout, "Q-3"), "missing", "Q-3")

    def test_rounds_family_reads_capture_only(self):
        root = build_tree(base_case())
        assert_reads_capture_only(self, root, count_reads=True)


if __name__ == "__main__":
    unittest.main()
