"""Slice 1 tracer tests: end to end on one path, contracts in minimal form."""
import re
import unittest
from pathlib import Path

from tests.fixture_builder import (FixtureTestCase, STARTER_ORDER,
                                     assert_two_part_form, assert_verdict,
                                     assert_reads_capture_only, base_case,
                                     build_tree, data_quality_entry_for,
                                     data_quality_section, gate_record,
                                     metrics_record, path_ledger, row_block,
                                     row_order, run_tool, run_tool_no_root,
                                     step_record)


class TestSlice1Tracer(FixtureTestCase):

    def test_tracer_end_to_end_full_set_on_clean_tree(self):
        root = build_tree(base_case())
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(row_order(result.stdout), STARTER_ORDER)

    def test_t1_refusal_date_only_form(self):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.\n"
            "Step 2 IN PROGRESS 2026-11-02, closed 2026-11-03.\n"
            "Step 3 IN PROGRESS 2026-11-03, closed 2026-11-04.")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "T-1")
        assert_verdict(self, block, "missing", "T-1")
        self.assertIn("date-only-form", block)
        self.assertIn("PATH-LEDGER.md", block)

    def test_exit_zero_on_completed_report(self):
        root = build_tree(base_case())
        self.assertEqual(run_tool(root).returncode, 0)

    def test_exit_two_on_no_arguments(self):
        result = run_tool_no_root()
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage", (result.stderr + result.stdout).lower())

    def test_exit_two_on_extra_argument(self):
        root = build_tree(base_case())
        result = run_tool(root, extra=("extra-position",))
        self.assertEqual(result.returncode, 2)

    def test_exit_two_on_unknown_option(self):
        root = build_tree(base_case())
        result = run_tool(root, extra=("--bogus",))
        self.assertEqual(result.returncode, 2)

    def test_exit_two_on_help_and_version_forms_barred(self):
        root = build_tree(base_case())
        self.assertEqual(run_tool(root, extra=("--help",)).returncode, 2)
        self.assertEqual(run_tool(root, extra=("--version",)).returncode, 2)

    def test_exit_two_on_report_without_path_and_repeated_report(self):
        root = build_tree(base_case())
        self.assertEqual(run_tool(root, extra=("--report",)).returncode, 2)
        out = Path(root).parent / "r1.md"
        result = run_tool(root, extra=("--report", str(out),
                                       "--report", str(out)))
        self.assertEqual(result.returncode, 2)

    def test_exit_one_on_unreadable_input(self):
        missing = Path(build_tree(base_case())).parent / "no_such_root"
        result = run_tool(missing)
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("No module named", result.stderr)

    def test_exit_one_on_file_as_root(self):
        table = base_case()
        root = build_tree(table)
        result = run_tool(root / "PATH-LEDGER.md")
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("No module named", result.stderr)

    def test_contract1_direct_minimal(self):
        root = build_tree(base_case())
        assert_reads_capture_only(self, root, count_reads=True)
        result = run_tool(build_tree(base_case()))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("latest record timestamp", result.stdout.lower())
        self.assertNotIn("run time:", result.stdout.lower())

    def test_contract2_direct_minimal(self):
        root = build_tree(base_case())
        result = run_tool(root)
        self.assertEqual(row_order(result.stdout), STARTER_ORDER)
        for code in STARTER_ORDER:
            self.assertTrue(row_block(result.stdout, code),
                            "row missing for " + code)

    def test_tracer_reads_capture_only(self):
        root = build_tree(base_case())
        assert_reads_capture_only(self, root)

    def test_two_part_reason_form_label_order_and_code_position(self):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.")
        table["steps/step-02-record.md"] = b"\xff\xfe\x00 bad \x80"
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "T-1")
        assert_two_part_form(self, block, "date-only-form", "T-1 reason line")
        entry = data_quality_entry_for(result.stdout, "step-02-record.md")
        self.assertTrue(entry, "data quality entry for the malformed piece")
        assert_two_part_form(self, entry, "malformed-piece",
                             "data quality entry")

    def test_two_part_reason_form_no_code_fits_case(self):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01 09:00 UTC, first timestamp "
            "stands with its basis stated as UTC.")
        table["steps/step-03-gate-record.md"] = (
            "# Step 3 gate record\n\nClosing ruling at 2026-11-03 17:00 "
            "with no time basis stated.\nClosure state: CLOSED-PASS.\n")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "B-1")
        assert_verdict(self, block, "present but not derivable", "B-1")
        assert_two_part_form(self, block, "no code fits", "B-1 reason line")
        section = data_quality_section(result.stdout)
        self.assertTrue(section, "data quality section stands")
        found = False
        for chunk in re.split(r"\n\s*\n", section):
            if "no code fits" in chunk.lower() and \
                    "what the record shows" in chunk.lower():
                assert_two_part_form(self, chunk, "no code fits",
                                     "data quality entry")
                found = True
        self.assertTrue(found, "one data quality entry carries the no "
                               "code fits wording at its second part start")

    def test_pointer_and_reason_on_all_rows_of_damaged_tree(self):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.")
        root = build_tree(table)
        result = run_tool(root)
        for code in STARTER_ORDER:
            block = row_block(result.stdout, code)
            self.assertTrue(block, code)
            self.assertTrue((".md" in block) or ("present" in block), code)

    def test_split_form_assembly_page_order(self):
        table = base_case()
        del table["wiki/wiki/synthesis/build-metrics-record.md"]
        table["wiki/wiki/synthesis/build-metrics-record-part-z.md"] = (
            "# Metrics record page stated first\n\nPage order: 1.\n\n"
            "## Decision table\n\n"
            "| Item | Origin step | Raised | Presented | Ruled |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| Q-1 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | "
            "2026-11-01 13:00 |\n")
        table["wiki/wiki/synthesis/build-metrics-record-part-a.md"] = (
            "# Metrics record page stated second\n\nPage order: 2.\n\n"
            "| Q-2 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | "
            "2026-11-01 11:00 |\n")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        self.assertRegex(block, r"median[^\d]*3(?!\d)(?!\.\d)")

    def test_split_form_missing_page_tables_absent(self):
        table = base_case()
        del table["wiki/wiki/synthesis/build-metrics-record.md"]
        table["wiki/wiki/synthesis/build-metrics-record-part-1.md"] = (
            "# Metrics record page 1\n\nPage order: 1.\n\n"
            "Decision table stands on page 2, which is absent.\n")
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "missing", "D-1")

    def test_split_form_single_page_precedence(self):
        table = base_case()
        table["wiki/wiki/synthesis/build-metrics-record.md"] = (
            metrics_record(decision_table=(
                "## Decision table\n\n"
                "| Item | Origin step | Raised | Presented | Ruled |\n"
                "| --- | --- | --- | --- | --- |\n"
                "| Q-1 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | "
                "2026-11-01 13:00 |\n")))
        table["wiki/wiki/synthesis/build-metrics-record-part-1.md"] = (
            "# Split copy\n\nSplit copy states the D-1 figure as 4242 "
            "hours.\n")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        self.assertIn("13:00", block)
        self.assertNotIn("4242", block)

    def test_step_universe_includes_step_evidenced_only_by_regate_record(self):
        table = base_case(steps=(1, 2))
        del table["steps/step-02-record.md"]
        del table["steps/step-02-gate-record.md"]
        table["steps/step-02-regate-record.md"] = gate_record(2)
        table["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 17:00.\n"
            "Step 2 IN PROGRESS 2026-11-02 09:00, closed 2026-11-02 17:00.",
            steps="1, 2")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "E-1")
        assert_verdict(self, block, "present", "E-1")
        self.assertIn("Step 2", block)
        self.assertRegex(block, r"(denominator[^\d]*2(?!\d)(?!\.\d)|"
                                r"of 2 steps\b|(?<!\d)2 steps\b)")

    def test_f18_unknown_definitions_version_slice1_rows(self):
        table = base_case()
        table["wiki/wiki/synthesis/build-metrics-record.md"] = metrics_record(
            body="Step table stands.", header_version="unknown-version-999")
        root = build_tree(table)
        result = run_tool(root)
        for code in ("E-1", "E-2", "Q-4"):
            block = row_block(result.stdout, code)
            assert_verdict(self, block, "present but not derivable", code)
            self.assertIn("unknown-definitions-version", block, code)
            self.assertIn("unknown-version-999", block, code)

    def test_header_coverage_and_data_quality_sections_present(self):
        root = build_tree(base_case())
        result = run_tool(root)
        self.assertIn("coverage", result.stdout.lower())
        self.assertIn("piece inventory", result.stdout.lower())
        self.assertIn("data quality", result.stdout.lower())


if __name__ == "__main__":
    unittest.main()
