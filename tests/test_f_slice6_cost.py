"""Slice 6 tests: cost family E-3, E-4, B-2 and the cross check guard."""
import re
import unittest

from tests.feeder_mapping import D1_FEEDER_CONDITION, FEEDER_MAP, METRICS_RECORD
from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     assert_reads_capture_only, base_case,
                                     build_tree, metrics_record, row_block,
                                     run_tool, statement_segment, step_record)

LEDGER_FULL = ("# Cost ledger\n\nStep 1: money 10, tokens 1000.\n"
               "Step 2: money 20, tokens 2000.\n"
               "Step 3: money 30, tokens 3000.\n"
               "Budget: money 100, tokens 10000.\n")
LEDGER_PARTIAL = ("# Cost ledger\n\nStep 1: money 10, tokens 1000.\n"
                  "No entries for Steps 2 and 3.\n"
                  "Budget: money 100, tokens 10000.\n")
LEDGER_MONEY_ONLY = ("# Cost ledger\n\nStep 1: money 10.\n"
                     "Step 2: money 20.\n"
                     "Step 3: money 30.\n"
                     "Budget: money 100.\n")


class TestSlice6Cost(FixtureTestCase):

    def test_f13_unreconciled_figure(self):
        table = base_case()
        table["registers/cost-ledger.md"] = (
            "# Cost ledger\n\nStep 1: money 10. Step 2: money 20. "
            "Build total stated: money 99.\n")
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "E-4")
        assert_verdict(self, block, "present but not derivable", "E-4")
        self.assertIn("unreconciled-figure", block)
        self.assertRegex(block, r"(?<!\d)(?<!\d\.)99(?!\d)(?!\.\d)")
        self.assertRegex(block, r"(?<!\d)(?<!\d\.)30(?!\d)(?!\.\d)")

    def test_wv9_partial_metering_e3(self):
        table = base_case()
        table["registers/cost-ledger.md"] = LEDGER_PARTIAL
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "E-3")
        assert_verdict(self, block, "present but not derivable", "E-3")
        self.assertIn("Step 1", block)
        self.assertNotIn("Step 2: 0", block)

    def test_wv9_partial_metering_b2_and_zero_budget_limb(self):
        table = base_case()
        table["registers/cost-ledger.md"] = (
            "# Cost ledger\n\nStep 1: money 0, tokens 1000.\n"
            "Budget: money 0, tokens 10000.\n")
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "B-2")
        assert_verdict(self, block, "present but not derivable", "B-2")
        self.assertIn("undefined", block.lower())
        self.assertNotIn("0 percent", block.lower())
        self.assertNotIn("100 percent", block.lower())

    def test_e3_present_on_complete_cost_ledger_span(self):
        table = base_case()
        table["registers/cost-ledger.md"] = LEDGER_FULL
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "E-3")
        assert_verdict(self, block, "present", "E-3")
        self.assertRegex(block, r"(?<!\d)(?<!\d\.)1000(?!\d)(?!\.\d)")

    def test_e4_complete_per_step_money_series_present(self):
        table = base_case()
        table["registers/cost-ledger.md"] = LEDGER_FULL
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "E-4")
        assert_verdict(self, block, "present", "E-4")
        self.assertIn("Step 1", block)

    def test_e4_partial_series_present_but_not_derivable(self):
        table = base_case()
        table["registers/cost-ledger.md"] = LEDGER_PARTIAL
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "E-4")
        assert_verdict(self, block, "present but not derivable", "E-4")

    def test_ac12_non_d1_figure_in_metrics_record_never_present(self):
        table = base_case()
        table["wiki/wiki/synthesis/build-metrics-record.md"] = metrics_record(
            body="Metrics record states E-3 tokens for Step 1 as 4242. "
                 "No cost ledger stands in this tree.")
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "E-3")
        assert_verdict(self, block, "missing", "E-3")
        self.assertNotIn("4242", block)

    def test_ac12_feeder_mapping_d1_is_only_metrics_record_feeder(self):
        with_metrics = [code for code, feeders in FEEDER_MAP.items()
                        if METRICS_RECORD in feeders]
        self.assertEqual(with_metrics, ["D-1"])
        self.assertEqual(len(FEEDER_MAP), 17)
        self.assertIn("only where no DECISION-QUEUE.md", D1_FEEDER_CONDITION)
        self.assertIn("D-09", D1_FEEDER_CONDITION)
        self.assertIn("WV-12", D1_FEEDER_CONDITION)
        table = base_case()
        table["wiki/wiki/synthesis/build-metrics-record.md"] = metrics_record(
            body="Metrics record states E-4 money for Step 1 as 77 and "
                 "Q-4 share as 100 percent.")
        root = build_tree(table)
        result = run_tool(root)
        e4 = row_block(result.stdout, "E-4")
        assert_verdict(self, e4, "present but not derivable", "E-4")
        self.assertNotIn("77", e4)
        q4 = row_block(result.stdout, "Q-4")
        assert_verdict(self, q4, "missing", "Q-4")

    def test_no_untraced_figure_for_cost_rows(self):
        table = base_case()
        table["notes/untraced-figures.md"] = (
            "# Working notes, not a feeder record\n\n"
            "E-3 tokens noted as 4242. E-4 money noted as 5353. "
            "B-2 total noted as 6464.\n")
        table["steps/step-01-gate-record.md"] = (
            "# Step 1 gate record\n\nClosure state: CLOSED-PASS.\n"
            "Money noted in passing as 5353.\n")
        root = build_tree(table)
        result = run_tool(root)
        planted = {"E-3": "4242", "E-4": "5353", "B-2": "6464"}
        verdicts = {"E-3": "missing", "E-4": "present but not derivable",
                    "B-2": "present but not derivable"}
        for code in ("E-3", "E-4", "B-2"):
            block = row_block(result.stdout, code)
            assert_verdict(self, block, verdicts[code], code)
            self.assertNotIn(planted[code], block, code)

    def test_b2_row_cross_check_marking_in_statement_line(self):
        table = base_case()
        table["registers/cost-ledger.md"] = LEDGER_FULL
        table["wiki/wiki/synthesis/build-metrics-record.md"] = metrics_record(
            body="Metrics record states B-2 money spent as 999.")
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "B-2")
        segment = statement_segment(block)
        self.assertIn("record disagrees", segment)
        self.assertIn("build-metrics-record.md", segment)
        self.assertRegex(segment, r"(?<!\d)(?<!\d\.)60(?!\d)(?!\.\d)")
        self.assertRegex(segment, r"(?<!\d)(?<!\d\.)999(?!\d)(?!\.\d)")

    def test_b2_not_derivable_row_cross_check_marking_second_case(self):
        table = base_case()
        table["registers/cost-ledger.md"] = LEDGER_PARTIAL
        table["wiki/wiki/synthesis/build-metrics-record.md"] = metrics_record(
            body="Metrics record states B-2 token total as 8888.")
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "B-2")
        assert_verdict(self, block, "present but not derivable", "B-2")
        segment = statement_segment(block)
        self.assertIn("record disagrees", segment)
        self.assertIn("build-metrics-record.md", segment)
        self.assertRegex(segment, r"(?<!\d)(?<!\d\.)1000(?!\d)(?!\.\d)")
        self.assertRegex(segment, r"(?<!\d)(?<!\d\.)8888(?!\d)(?!\.\d)")

    def test_f16_b2_open_state_row_reason(self):
        table = base_case()
        del table["steps/step-03-gate-record.md"]
        table["registers/cost-ledger.md"] = LEDGER_PARTIAL
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "B-2")
        self.assertIn("in progress", block.lower())

    def test_f17_b2_halt_row_reason(self):
        table = base_case()
        table["steps/step-02-record.md"] = step_record(
            2, extra="This build stands halted. The work is halted by order.")
        table["registers/cost-ledger.md"] = LEDGER_PARTIAL
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "B-2")
        self.assertIn("halted", block.lower())

    def test_f18_unknown_version_slice6_rows(self):
        table = base_case()
        table["registers/cost-ledger.md"] = LEDGER_MONEY_ONLY
        table["wiki/wiki/synthesis/build-metrics-record.md"] = metrics_record(
            body="Step table stands.", header_version="unknown-version-999")
        root = build_tree(table)
        result = run_tool(root)
        for code in ("E-4", "B-2"):
            block = row_block(result.stdout, code)
            assert_verdict(self, block, "present but not derivable", code)
            self.assertIn("unknown-definitions-version", block, code)
            self.assertIn("unknown-version-999", block, code)
        assert_verdict(self, row_block(result.stdout, "E-3"), "missing", "E-3")

    def test_cost_family_and_cross_check_read_capture_only(self):
        table = base_case()
        table["registers/cost-ledger.md"] = LEDGER_FULL
        root = build_tree(table)
        assert_reads_capture_only(self, root, count_reads=True)


if __name__ == "__main__":
    unittest.main()
