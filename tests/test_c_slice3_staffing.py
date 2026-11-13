"""Slice 3 tests: step universe, gates, staffing family E-1, E-2, F-2."""
import re
import unittest

from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     assert_reads_capture_only, base_case,
                                     build_tree, coverage_statement,
                                     gate_record, gate_ruling, metrics_record,
                                     path_ledger, row_block, run_tool,
                                     statement_segment, step_record)


def staffing_table(closure="CLOSED-PASS"):
    table = base_case()
    for n in (1, 2, 3):
        table["steps/step-%02d-gate-record.md" % n] = gate_record(n, closure)
    return table


def wv4_table():
    table = base_case(steps=(1, 2, 3))
    table["wiki/wiki/synthesis/build-metrics-record.md"] = metrics_record(
        body="Metrics record states the step universe as 2 steps.")
    table["PATH-LEDGER.md"] = path_ledger(
        "Step 1 IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 17:00.\n"
        "Step 2 IN PROGRESS 2026-11-02 09:00, closed 2026-11-02 17:00.\n"
        "Step 3 IN PROGRESS 2026-11-03 09:00, closed 2026-11-03 17:00.",
        steps="1, 2, 3")
    return table


def assert_wv4_disputed_form(test, result):
    cov = coverage_statement(result.stdout)
    test.assertTrue(cov, "header coverage statement stands")
    test.assertIn("build-metrics-record.md", cov)
    test.assertTrue("PATH-LEDGER.md" in cov or "step record" in cov.lower(),
                    cov[:400])
    test.assertRegex(cov, r"(?<!\d)2 steps\b")
    test.assertRegex(cov, r"(?<!\d)3 steps\b")
    test.assertIn("disagrees", cov.lower())
    block = row_block(result.stdout, "E-1")
    segment = statement_segment(block)
    test.assertIn("record disagrees", segment)
    test.assertIn("Step 3", block)
    test.assertRegex(block, r"(denominator[^\d]*3(?!\d)(?!\.\d)|"
                            r"of 3 steps\b|(?<!\d)3 steps\b)")


class TestSlice3Staffing(FixtureTestCase):

    def test_f04_both_gate_names_read(self):
        table = staffing_table()
        table["steps/step-01-gate-ruling.md"] = gate_ruling(1, "CLOSED-PASS")
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")

    def test_f04_step_with_neither_gate_name(self):
        table = staffing_table()
        del table["steps/step-03-gate-record.md"]
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")
        self.assertIn("Step 3", block)

    def test_f03_metrics_record_stops_early_coverage_naming(self):
        table = staffing_table()
        table["wiki/wiki/synthesis/build-metrics-record.md"] = metrics_record(
            body="Step table stops at Step 1. Steps 2 and 3 not stated.")
        root = build_tree(table)
        result = run_tool(root)
        self.assertIn("coverage", result.stdout.lower())
        self.assertTrue("Step 2" in result.stdout or "Step 3" in result.stdout)

    def test_g01_exact_closure_state_matching_two_subcounts(self):
        table = base_case(steps=(1, 2, 3, 4))
        table["steps/step-01-gate-record.md"] = gate_record(1, "CLOSED-PASS")
        table["steps/step-02-gate-record.md"] = gate_record(2, "CLOSED-QUALIFIED")
        table["steps/step-03-gate-record.md"] = gate_record(3, "CLOSED-FAIL")
        table["steps/step-04-gate-record.md"] = gate_record(4, "CLOSED-PASS-EXTRA")
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present but not derivable", "F-2")
        self.assertRegex(block, r"plain[^\d]*1(?!\d)(?!\.\d)")
        self.assertRegex(block, r"qualified[^\d]*1(?!\d)(?!\.\d)")
        self.assertRegex(block, r"(denominator[^\d]*3(?!\d)(?!\.\d)|"
                                r"of 3(?!\d)(?!\.\d)|(?<!\d)3 steps ruled\b)")

    def test_g02_adjudication_as_first_ruling_source(self):
        table = base_case(steps=(1,))
        del table["steps/step-01-gate-record.md"]
        table["steps/step-01-gate-adjudication.md"] = gate_record(
            1, "CLOSED-PASS", extra="Adjudication states the first gate outcome.")
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")
        self.assertIn("adjudication", block.lower())

    def test_g02_step_record_gate_histories_never_read(self):
        table = base_case(steps=(1,))
        del table["steps/step-01-gate-record.md"]
        table["steps/step-01-record.md"] = step_record(
            1, extra="Gate history inside this record claims CLOSED-PASS.")
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present but not derivable", "F-2")

    def test_g03_additions_over_base_with_ca9_three_figures(self):
        table = base_case(steps=(1,))
        table["steps/step-01-record.md"] = step_record(
            1, base=2, total_spins=7,
            extra="Detail total spins: 7. Stated total spins: 6.")
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "E-2")
        assert_verdict(self, block, "present", "E-2")
        self.assertIn("additions over base", block.lower())
        self.assertIn("total spins", block.lower())
        self.assertRegex(block, r"detail[^\d]*7(?!\d)(?!\.\d)")
        self.assertRegex(block, r"stated[^\d]*6(?!\d)(?!\.\d)")
        self.assertRegex(block, r"variance[^\d]*1(?!\d)(?!\.\d)")

    def test_g03_step_with_no_base_named_for_additions_only(self):
        table = base_case(steps=(1, 2))
        table["steps/step-02-record.md"] = (
            "# Step 2 record\n\nNo base stated. Total spins: 5.\n")
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "E-2")
        assert_verdict(self, block, "present", "E-2")
        self.assertIn("Step 2", block)
        self.assertIn("missing-field", block)

    def test_g04_keeper_gate_in_qualified_subcount_no_t7_effect(self):
        table = base_case(steps=(22,))
        table["steps/step-22-record.md"] = step_record(22)
        table["steps/step-22-gate-record.md"] = gate_record(
            22, "CLOSED-QUALIFIED",
            extra="Release gate record held by the Release-gate Keeper. Outcome: Go.")
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "F-2")
        self.assertRegex(block, r"qualified[^\d]*1(?!\d)(?!\.\d)")
        self.assertRegex(block, r"(denominator[^\d]*1(?!\d)(?!\.\d)|"
                                r"of 1(?!\d)(?!\.\d))")
        t7 = row_block(result.stdout, "T-7")
        assert_verdict(self, t7, "missing", "T-7")

    def test_g04_recycled_step_counted_once(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = gate_record(2, "CLOSED-FAIL")
        table["steps/step-02-regate-record.md"] = gate_record(
            2, "CLOSED-QUALIFIED", extra="Recycled instance ruling.")
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")
        self.assertIn("first-time approval rate 0 percent", block)
        self.assertIn("not approved", block.lower())
        self.assertRegex(block, r"plain[^\d]*0(?!\d)(?!\.\d)")
        self.assertRegex(block, r"qualified[^\d]*0(?!\d)(?!\.\d)")
        self.assertRegex(block, r"(denominator[^\d]*1(?!\d)(?!\.\d)|"
                                r"of 1(?!\d)(?!\.\d)|(?<!\d)1 step ruled\b)")

    def test_g09_e1_present_with_coverage_remainder_named(self):
        table = base_case(steps=(1, 2, 3, 4))
        table["steps/step-04-record.md"] = (
            "# Step 4 record\n\nRoster stands. No base stated for this step.\n")
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "E-1")
        assert_verdict(self, block, "present", "E-1")
        self.assertIn("Step 4", block)
        self.assertRegex(block, r"(denominator[^\d]*4(?!\d)(?!\.\d)|"
                                r"of 4 steps\b|(?<!\d)4 steps\b)")

    def test_e1_partial_coverage_without_defined_form_is_not_present(self):
        table = base_case(steps=(1, 2))
        table["steps/step-01-record.md"] = "# Step 1 record\n\nRoster fragment only.\n"
        table["steps/step-02-record.md"] = "# Step 2 record\n\nRoster fragment only.\n"
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "E-1")
        assert_verdict(self, block, "present but not derivable", "E-1")
        self.assertIn("missing-field", block)

    def test_wv4_disputed_count_header_and_denominators(self):
        root = build_tree(wv4_table())
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        assert_wv4_disputed_form(self, result)

    def test_e1_row_cross_check_marking_in_statement_line(self):
        table = base_case(steps=(1,))
        table["steps/step-01-record.md"] = step_record(1, team=3)
        table["wiki/wiki/synthesis/build-metrics-record.md"] = metrics_record(
            body="Metrics record states E-1 for Step 1 as 9 of 2.")
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "E-1")
        segment = statement_segment(block)
        self.assertIn("record disagrees", segment)
        self.assertIn("build-metrics-record.md", segment)
        self.assertIn("3 of 2", segment)
        self.assertIn("9 of 2", segment)

    def test_f18_unknown_version_slice3_rows(self):
        table = base_case()
        for n in (1, 2, 3):
            del table["steps/step-%02d-gate-record.md" % n]
        table["wiki/wiki/synthesis/build-metrics-record.md"] = metrics_record(
            body="Step table stands.", header_version="unknown-version-999")
        root = build_tree(table)
        result = run_tool(root)
        for code in ("E-1", "E-2"):
            block = row_block(result.stdout, code)
            assert_verdict(self, block, "present but not derivable", code)
            self.assertIn("unknown-definitions-version", block, code)
            self.assertIn("unknown-version-999", block, code)
        assert_verdict(self, row_block(result.stdout, "F-2"), "missing", "F-2")

    def test_step_universe_reads_capture_only(self):
        root = build_tree(staffing_table())
        assert_reads_capture_only(self, root)


if __name__ == "__main__":
    unittest.main()
