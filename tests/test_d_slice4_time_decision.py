"""Slice 4 tests: time family, D-1 feeder cells, B-1, B-3, B-4, F-16 to F-19."""
import re
import unittest

from tests.fixture_builder import (FixtureTestCase, STARTER_ORDER,
                                     assert_verdict, assert_reads_capture_only,
                                     base_case, build_tree, coverage_statement,
                                     data_quality_entry_for, decision_table,
                                     metrics_record, path_ledger, queue_file,
                                     row_block, row_order, run_tool,
                                     statement_segment, step_record)

RULED_ROW = ("| Q-1 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | "
             "2026-11-01 13:00 |")
RULED_ROW_LATE = ("| Q-1 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | "
                  "2026-11-01 19:00 |")
RULED_ROW_2 = ("| Q-2 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | "
               "2026-11-01 11:00 |")
OPEN_ROW = "| Q-3 | 2 | 2026-11-02 09:00 | 2026-11-02 10:00 |  |"
DATE_ONLY_ROW = "| Q-4 | 2 | 2026-11-02 | 2026-11-02 | 2026-11-03 |"


def d1_table(queue=None, table_rows=None, split=False, unusable_queue=False):
    table = base_case()
    if queue is not None:
        table["DECISION-QUEUE.md"] = queue
    if unusable_queue:
        table["DECISION-QUEUE.md"] = b"\xff\xfe unusable queue \x80"
    if table_rows is not None:
        if split:
            del table["wiki/wiki/synthesis/build-metrics-record.md"]
            table["wiki/wiki/synthesis/build-metrics-record-part-1.md"] = (
                "# Page 1\n\nPage order: 1.\n\n" +
                decision_table(table_rows))
        else:
            table["wiki/wiki/synthesis/build-metrics-record.md"] = (
                metrics_record(decision_table=decision_table(table_rows)))
    return table


def assert_foundation(test, block, fragment):
    test.assertIn("foundation", block.lower())
    test.assertIn(fragment, block)


def assert_median(test, block, hours):
    match = re.search(r"median[^\d]*(\d+(?:\.\d+)?)", block)
    test.assertIsNotNone(match, "median figure stands in the D-1 row")
    test.assertEqual(float(match.group(1)), float(hours))


class TestSlice4TimeDecision(FixtureTestCase):

    def test_f02_date_only_timestamps_t1_and_t2_missing(self):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.")
        root = build_tree(table)
        result = run_tool(root)
        for code in ("T-1", "T-2"):
            block = row_block(result.stdout, code)
            assert_verdict(self, block, "missing", code)
            self.assertIn("date-only-form", block, code)

    def test_mixed_series_partial_span(self):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 17:00.\n"
            "Step 2 IN PROGRESS 2026-11-02, closed 2026-11-03.\n"
            "Step 3 stands with no transitions.")
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "T-1")
        assert_verdict(self, block, "present but not derivable", "T-1")
        self.assertIn("partial-span", block)
        self.assertIn("Step 1", block)
        self.assertIn("Step 2", block)
        self.assertIn("Step 3", block)

    def test_d1_ruled_open_and_date_only_items(self):
        table = d1_table(queue=queue_file([RULED_ROW, RULED_ROW_2,
                                           OPEN_ROW, DATE_ONLY_ROW]))
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        assert_median(self, block, 3)
        self.assertIn("open", block.lower())
        self.assertIn("Q-3", block)
        self.assertIn("Q-4", block)
        self.assertTrue("date only" in block.lower() or
                        "date-only" in block.lower() or
                        "excluded" in block.lower(), block[:400])

    def test_d1_even_count_median_rule(self):
        table = d1_table(queue=queue_file([RULED_ROW, RULED_ROW_2]))
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        self.assertIn("median", block.lower())
        assert_median(self, block, 3)

    def test_d1_no_ruled_item_is_not_derivable(self):
        table = d1_table(queue=queue_file([OPEN_ROW]))
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present but not derivable", "D-1")
        self.assertIn("open", block.lower())

    def test_d1_cell_queue_named_complete_single_page(self):
        table = d1_table(queue=queue_file([RULED_ROW]),
                         table_rows=[RULED_ROW_LATE])
        root = build_tree(table)
        block = row_block(run_tool(root).stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        assert_foundation(self, block, "DECISION-QUEUE.md")
        assert_median(self, block, 4)

    def test_d1_cell_queue_named_complete_split(self):
        table = d1_table(queue=queue_file([RULED_ROW]),
                         table_rows=[RULED_ROW_LATE], split=True)
        root = build_tree(table)
        block = row_block(run_tool(root).stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        assert_foundation(self, block, "DECISION-QUEUE.md")
        assert_median(self, block, 4)

    def test_d1_cell_queue_named_no_decision_table(self):
        table = d1_table(queue=queue_file([RULED_ROW]))
        root = build_tree(table)
        block = row_block(run_tool(root).stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        assert_foundation(self, block, "DECISION-QUEUE.md")

    def test_d1_cell_no_queue_complete_single_page(self):
        table = d1_table(table_rows=[RULED_ROW])
        root = build_tree(table)
        block = row_block(run_tool(root).stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        assert_foundation(self, block, "decision table")

    def test_d1_cell_no_queue_complete_split(self):
        table = d1_table(table_rows=[RULED_ROW], split=True)
        root = build_tree(table)
        block = row_block(run_tool(root).stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        assert_foundation(self, block, "decision table")

    def test_d1_cell_no_queue_no_decision_table_missing(self):
        table = d1_table()
        root = build_tree(table)
        block = row_block(run_tool(root).stdout, "D-1")
        assert_verdict(self, block, "missing", "D-1")
        assert_foundation(self, block, "no feeder")

    def test_d1_cell_unusable_queue_complete_single_page(self):
        table = d1_table(table_rows=[RULED_ROW], unusable_queue=True)
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        assert_foundation(self, block, "decision table")
        entry = data_quality_entry_for(result.stdout, "DECISION-QUEUE.md")
        self.assertTrue(entry, "queue file named in the data quality section")
        self.assertIn("not read in full", entry.lower())

    def test_d1_cell_unusable_queue_complete_split(self):
        table = d1_table(table_rows=[RULED_ROW], split=True,
                         unusable_queue=True)
        root = build_tree(table)
        result = run_tool(root)
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        assert_foundation(self, block, "decision table")
        entry = data_quality_entry_for(result.stdout, "DECISION-QUEUE.md")
        self.assertTrue(entry, "queue file named in the data quality section")
        self.assertIn("not read in full", entry.lower())

    def test_d1_cell_unusable_queue_no_complete_table(self):
        table = d1_table(unusable_queue=True)
        root = build_tree(table)
        block = row_block(run_tool(root).stdout, "D-1")
        assert_verdict(self, block, "present but not derivable", "D-1")
        assert_foundation(self, block, "DECISION-QUEUE.md")

    def test_d1_row_rendered_in_full_with_cross_check_marking(self):
        table = d1_table(queue=queue_file([RULED_ROW]),
                         table_rows=[RULED_ROW_LATE])
        root = build_tree(table)
        block = row_block(run_tool(root).stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        assert_foundation(self, block, "DECISION-QUEUE.md")
        segment = statement_segment(block)
        self.assertIn("record disagrees", segment)
        self.assertIn("decision table", segment.lower())
        self.assertIn("13:00", segment)
        self.assertIn("19:00", segment)
        assert_median(self, block, 4)

    def test_t4_present_row_cross_check_marking_in_statement_line(self):
        table = base_case()
        table["wiki/wiki/synthesis/build-metrics-record.md"] = metrics_record(
            body="Metrics record states T-4 wait as 99 hours.",
            decision_table=decision_table([RULED_ROW]))
        table["PATH-LEDGER.md"] = path_ledger(
            "Step 1 BANKED duration 2 hours on Q-1.")
        root = build_tree(table)
        block = row_block(run_tool(root).stdout, "T-4")
        segment = statement_segment(block)
        self.assertIn("record disagrees", segment)
        self.assertIn("build-metrics-record.md", segment)
        self.assertIn("2 hours", segment)
        self.assertIn("99 hours", segment)

    def test_t4_degraded_row_shown_without_queue_cross_check(self):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            "Step 1 BANKED interval duration 2 hours. "
            "Step 2 BANKED interval duration 3 hours.")
        root = build_tree(table)
        block = row_block(run_tool(root).stdout, "T-4")
        assert_verdict(self, block, "present", "T-4")
        self.assertIn("without its queue cross check", block)
        self.assertIn("without its queue cross check",
                      statement_segment(block))

    def test_a7_9_b1_cross_piece_basis_mismatch_no_code_fits(self):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01 09:00 UTC, first timestamp "
            "stands with its basis stated as UTC.")
        table["steps/step-03-gate-record.md"] = (
            "# Step 3 gate record\n\nClosing ruling at 2026-11-03 17:00 "
            "with no time basis stated.\nClosure state: CLOSED-PASS.\n")
        root = build_tree(table)
        block = row_block(run_tool(root).stdout, "B-1")
        assert_verdict(self, block, "present but not derivable", "B-1")
        self.assertIn("no code fits", block.lower())
        self.assertIn("UTC", block)
        self.assertTrue("no time basis" in block.lower() or
                        "no basis" in block.lower(), block[:500])

    def test_b3_ranking_tie_lists_every_tied_step(self):
        table = base_case(steps=(1, 2, 3, 4))
        table["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 19:00. "
            "Active 10 hours.\n"
            "Step 2 IN PROGRESS 2026-11-02 09:00, closed 2026-11-02 19:00. "
            "Active 10 hours.\n"
            "Step 3 IN PROGRESS 2026-11-03 09:00, closed 2026-11-03 19:00. "
            "Active 10 hours.\n"
            "Step 4 IN PROGRESS 2026-11-04 09:00, closed 2026-11-04 19:00. "
            "Active 10 hours.", steps="1, 2, 3, 4")
        root = build_tree(table)
        block = row_block(run_tool(root).stdout, "B-3")
        self.assertIn("tied", block.lower())
        for name in ("Step 1", "Step 2", "Step 3", "Step 4"):
            self.assertIn(name, block)
        self.assertRegex(block, r"eligible[^\d]*4(?!\d)(?!\.\d)")

    def test_b3_fewer_than_three_eligible_steps(self):
        table = base_case(steps=(1, 2))
        root = build_tree(table)
        block = row_block(run_tool(root).stdout, "B-3")
        assert_verdict(self, block, "present", "B-3")
        self.assertIn("Step 1", block)
        self.assertIn("Step 2", block)
        self.assertRegex(block, r"eligible[^\d]*2(?!\d)(?!\.\d)")

    def test_b4_ranking_tie_lists_every_tied_step(self):
        table = base_case(steps=(1, 2, 3, 4))
        table["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 19:00. "
            "Active 10 hours.\n"
            "Step 2 IN PROGRESS 2026-11-02 09:00, closed 2026-11-02 19:00. "
            "Active 10 hours.\n"
            "Step 3 IN PROGRESS 2026-11-03 09:00, closed 2026-11-03 19:00. "
            "Active 10 hours.\n"
            "Step 4 IN PROGRESS 2026-11-04 09:00, closed 2026-11-04 19:00. "
            "Active 10 hours.", steps="1, 2, 3, 4")
        root = build_tree(table)
        block = row_block(run_tool(root).stdout, "B-4")
        self.assertIn("tied", block.lower())
        for name in ("Step 1", "Step 2", "Step 3", "Step 4"):
            self.assertIn(name, block)
        self.assertRegex(block, r"eligible[^\d]*4(?!\d)(?!\.\d)")

    def test_b4_fewer_than_three_eligible_steps(self):
        table = base_case(steps=(1, 2))
        root = build_tree(table)
        block = row_block(run_tool(root).stdout, "B-4")
        assert_verdict(self, block, "present", "B-4")
        self.assertIn("Step 1", block)
        self.assertIn("Step 2", block)
        self.assertRegex(block, r"eligible[^\d]*2(?!\d)(?!\.\d)")

    def test_f16_in_progress_tree_open_state_wording(self):
        table = base_case()
        del table["steps/step-03-gate-record.md"]
        root = build_tree(table)
        result = run_tool(root)
        cov = coverage_statement(result.stdout)
        self.assertIn("in progress", cov.lower())
        self.assertIn("closing ruling", cov.lower())
        self.assertRegex(cov.lower(), r"missing piece|not read|absent")
        self.assertIn("step-03", cov.lower())
        self.assertIn("captured read", result.stdout.lower())
        self.assertNotIn("halted", result.stdout.lower())
        present_named = False
        for code in ("B-1", "B-3", "B-4"):
            block = row_block(result.stdout, code)
            self.assertIn("in progress", statement_segment(block).lower(),
                          code)
            from tests.fixture_builder import row_verdict
            if row_verdict(block) == "present" and \
                    "in progress" in statement_segment(block).lower():
                present_named = True
        self.assertTrue(present_named,
                        "one present B row carries the open state naming")

    def test_f17_halted_tree_halt_named_and_full_rows(self):
        table = base_case()
        table["steps/step-02-record.md"] = step_record(
            2, extra="This build stands halted. The work is halted by order.")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        cov = coverage_statement(result.stdout)
        self.assertIn("halted", cov.lower())
        self.assertEqual(row_order(result.stdout), STARTER_ORDER)
        present_named = False
        for code in ("B-1", "B-3", "B-4"):
            block = row_block(result.stdout, code)
            self.assertTrue(block, code)
            self.assertIn("halted", statement_segment(block).lower(), code)
            from tests.fixture_builder import row_verdict
            if row_verdict(block) == "present" and \
                    "halted" in statement_segment(block).lower():
                present_named = True
        self.assertTrue(present_named,
                        "one present B row carries the halt naming")

    def test_f19_unrecognised_halt_wording_read_as_in_progress(self):
        table = base_case()
        table["notes/random-note.md"] = "Everything halted everywhere.\n"
        root = build_tree(table)
        result = run_tool(root)
        self.assertNotIn("halted", result.stdout.lower())
        self.assertIn("in progress", result.stdout.lower())

    def test_f19_non_naming_halt_wording_in_recognised_piece(self):
        table = base_case()
        table["steps/step-02-record.md"] = step_record(
            2, extra="Everything halted everywhere.")
        root = build_tree(table)
        result = run_tool(root)
        self.assertNotIn("halted", result.stdout.lower())
        self.assertIn("in progress", result.stdout.lower())
        cov = coverage_statement(result.stdout)
        self.assertIn("in progress", cov.lower())

    def test_f18_unknown_version_slice4_rows(self):
        table = d1_table(queue=queue_file([RULED_ROW]))
        table["wiki/wiki/synthesis/build-metrics-record.md"] = metrics_record(
            body="Step table stands.", header_version="unknown-version-999",
            decision_table=decision_table([RULED_ROW]))
        root = build_tree(table)
        result = run_tool(root)
        for code in ("T-1", "T-4", "D-1"):
            block = row_block(result.stdout, code)
            assert_verdict(self, block, "present but not derivable", code)
            self.assertIn("unknown-definitions-version", block, code)
            self.assertIn("unknown-version-999", block, code)
        assert_verdict(self, row_block(result.stdout, "T-2"), "missing", "T-2")
        for code in ("B-1", "B-3", "B-4"):
            block = row_block(result.stdout, code)
            assert_verdict(self, block, "missing", code)
        self.assertIn("T-2", row_block(result.stdout, "B-1"))

    def test_time_family_reads_capture_only(self):
        root = build_tree(base_case())
        assert_reads_capture_only(self, root, count_reads=True)


if __name__ == "__main__":
    unittest.main()
