"""Slice 6 tests: cost family E-3, E-4, B-2 and the cross check.

Every case states the EC points and the WV22 fields it asserts in its
first line, in the citation forms the test design record states.
Fixture trees are built through the fixture builder case table form,
with build_case or build_cases into a tracked temporary directory,
and the product is invoked through run_tool, which runs the module
entry route as a subprocess from the repo root with the root argument
first. The B-2 token side and the B-2 money side stand stated and
asserted separately, at WV22 B-2 F1 to F3 and F4 to F6, with the
combination asserted only at F7.
"""
import re
import unittest

from tests.fixture_builder import (
    FixtureTestCase, assert_reads_capture_only, assert_verdict,
    build_case, build_cases, decision_table, metrics_record, queue_file,
    row_block, row_verdict, run_tool, statement_segment, step_record,
    tracked_tempdir)

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
LEDGER_PATH = "registers/cost-ledger.md"
METRICS_PATH = "wiki/wiki/synthesis/build-metrics-record.md"


def base_files(steps=(1, 2, 3)):
    """Return the files dict of a small complete tree, as plain data."""
    files = {}
    transitions = []
    for n in steps:
        files["steps/step-%02d-record.md" % n] = step_record(n)
        files["steps/step-%02d-gate-record.md" % n] = (
            "# Step %d gate record\n\nClosure state: CLOSED-PASS.\n" % n)
        transitions.append(
            "Step %d IN PROGRESS 2026-11-01 09:00, closed "
            "2026-11-01 17:00." % n)
    files["PATH-LEDGER.md"] = (
        "# Path ledger\n\nSteps stated: %s.\n\n## Transitions\n\n%s\n"
        % (", ".join(str(s) for s in steps), "\n".join(transitions)))
    files["TIER-RECORD.md"] = "# Tier record\n\nTier: Low. Base: 2.\n"
    files[METRICS_PATH] = metrics_record(
        body="Step table stands complete for the fixture steps.")
    return files


def make_case(name, files, features=()):
    """Return one case table in the fixture builder case table form."""
    return {"name": name, "features": tuple(features),
            "files": dict(files)}


def run_case(case):
    """Build one case under a tracked temporary root and run the tool."""
    root = tracked_tempdir("msc_slice6_")
    built = build_case(case, root)
    return run_tool(built), built


def ledger_case(name, ledger, features=("token-figures-in-ledger",
                                        "cost-ledger-inside-root",
                                        "per-step-money-figures")):
    files = base_files()
    files[LEDGER_PATH] = ledger
    return make_case(name, files, features)


def has_number(block, number):
    return re.search(r"(?<!\d)(?<!\d\.)%s(?!\d)(?!\.\d)" % number,
                     block) is not None


class TestSlice6Cost(FixtureTestCase):

    def test_f13_unreconciled_figure(self):
        """EC-31, EC-18; WV22 E-4 F1."""
        files = base_files()
        files[LEDGER_PATH] = (
            "# Cost ledger\n\nStep 1: money 10. Step 2: money 20. "
            "Build total stated: money 99.\n")
        result, _ = run_case(make_case(
            "f13-unreconciled", files,
            ("per-step-money-figures", "unreconciled-figure",
             "cost-ledger-inside-root")))
        block = row_block(result.stdout, "E-4")
        assert_verdict(self, block, "present but not derivable", "E-4")
        self.assertIn("unreconciled-figure", block)
        self.assertTrue(has_number(block, "99"))
        self.assertTrue(has_number(block, "30"))

    def test_wv9_partial_metering_e3(self):
        """EC-30, EC-18; WV22 E-3 F1."""
        result, _ = run_case(ledger_case("wv9-partial-e3", LEDGER_PARTIAL))
        block = row_block(result.stdout, "E-3")
        assert_verdict(self, block, "present but not derivable", "E-3")
        self.assertIn("Step 1", block)
        self.assertNotIn("Step 2: 0", block)

    def test_wv9_partial_metering_b2(self):
        """EC-38, EC-18; WV22 B-2 F1, WV22 B-2 F4."""
        result, _ = run_case(ledger_case("wv9-partial-b2", LEDGER_PARTIAL))
        block = row_block(result.stdout, "B-2")
        assert_verdict(self, block, "present but not derivable", "B-2")
        self.assertTrue(has_number(block, "1000"))

    def test_wv9_zero_budget_token_side_percentage_undefined(self):
        """EC-38; WV22 B-2 F2, WV22 B-2 F3, token side only."""
        files = base_files()
        files[LEDGER_PATH] = (
            "# Cost ledger\n\nStep 1: tokens 1000.\n"
            "Budget: tokens 0.\n")
        result, _ = run_case(make_case(
            "b2-zero-token-budget", files,
            ("token-figures-in-ledger", "cost-ledger-inside-root")))
        block = row_block(result.stdout, "B-2")
        assert_verdict(self, block, "present but not derivable", "B-2")
        self.assertIn("undefined", block.lower())
        self.assertNotIn("percent", block.lower().replace(
            "percentage is undefined", ""))

    def test_wv9_zero_budget_money_side_percentage_undefined(self):
        """EC-38; WV22 B-2 F5, WV22 B-2 F6, money side only."""
        files = base_files()
        files[LEDGER_PATH] = (
            "# Cost ledger\n\nStep 1: money 10.\n"
            "Budget: money 0.\n")
        result, _ = run_case(make_case(
            "b2-zero-money-budget", files,
            ("per-step-money-figures", "cost-ledger-inside-root")))
        block = row_block(result.stdout, "B-2")
        assert_verdict(self, block, "present but not derivable", "B-2")
        self.assertIn("undefined", block.lower())
        self.assertNotIn("0 percent", block.lower())
        self.assertNotIn("100 percent", block.lower())

    def test_b2_absent_budget_both_sides_undefined_never_zero(self):
        """EC-38; WV22 B-2 F3, WV22 B-2 F6."""
        result, _ = run_case(ledger_case("b2-no-ledger", LEDGER_PARTIAL))
        no_ledger_files = base_files()
        result2, _ = run_case(make_case("b2-absent", no_ledger_files))
        block = row_block(result2.stdout, "B-2")
        assert_verdict(self, block, "present but not derivable", "B-2")
        self.assertIn("undefined", block.lower())
        self.assertNotIn("0 percent", block.lower())
        self.assertTrue(result.stdout)

    def test_e3_present_on_complete_cost_ledger_span(self):
        """EC-30, EC-18; WV22 E-3 F1."""
        result, _ = run_case(ledger_case("e3-complete", LEDGER_FULL))
        block = row_block(result.stdout, "E-3")
        assert_verdict(self, block, "present", "E-3")
        self.assertTrue(has_number(block, "1000"))

    def test_e3_token_figure_in_step_record_counts_for_nothing(self):
        """EC-30; WV22 E-3 F1."""
        files = base_files()
        files["steps/step-01-record.md"] = step_record(
            1, extra="Tokens for step 1 stated here as 4242.")
        result, _ = run_case(make_case("e3-step-record-only", files))
        block = row_block(result.stdout, "E-3")
        assert_verdict(self, block, "missing", "E-3")
        self.assertNotIn("4242", block)

    def test_e3_proxy_label_counts_for_nothing(self):
        """EC-30, EC-18; WV22 E-3 F1."""
        files = base_files()
        files["steps/step-01-record.md"] = step_record(
            1, extra="Token position on a labelled proxy basis: 4242 "
                     "documented units.")
        result, _ = run_case(make_case(
            "e3-proxy-only", files, ("proxy-label",)))
        block = row_block(result.stdout, "E-3")
        assert_verdict(self, block, "missing", "E-3")
        self.assertNotIn("4242", block)

    def test_e4_complete_per_step_money_series_present(self):
        """EC-31, EC-18; WV22 E-4 F1."""
        result, _ = run_case(ledger_case("e4-complete", LEDGER_FULL))
        block = row_block(result.stdout, "E-4")
        assert_verdict(self, block, "present", "E-4")
        self.assertIn("Step 1", block)

    def test_e4_partial_series_present_but_not_derivable(self):
        """EC-31; WV22 E-4 F1."""
        result, _ = run_case(ledger_case("e4-partial", LEDGER_PARTIAL))
        block = row_block(result.stdout, "E-4")
        assert_verdict(self, block, "present but not derivable", "E-4")

    def test_e4_figure_credited_to_other_step_counts_for_described(self):
        """EC-31; WV22 E-4 F1."""
        files = base_files()
        files[LEDGER_PATH] = (
            "# Cost ledger\n\nEntry stored on the step 1 line, "
            "describing step 2: money 20.\nStep 1: money 10.\n"
            "Step 3: money 30.\nBudget: money 100.\n")
        result, _ = run_case(make_case(
            "e4-credited", files,
            ("per-step-money-figures", "cost-ledger-inside-root",
             "figure-credited-to-other-step")))
        block = row_block(result.stdout, "E-4")
        assert_verdict(self, block, "present", "E-4")
        self.assertIn("Step 2", block)
        self.assertTrue(has_number(block, "20"))

    def test_e4_per_step_figure_in_step_record_counts(self):
        """EC-31; WV22 E-4 F2."""
        files = base_files()
        for n, amount in ((1, 10), (2, 20), (3, 30)):
            files["steps/step-%02d-record.md" % n] = step_record(
                n, extra="Money spent for this step itself: %d." % amount)
        result, _ = run_case(make_case(
            "e4-step-records", files, ("per-step-money-figures",)))
        block = row_block(result.stdout, "E-4")
        assert_verdict(self, block, "present", "E-4")
        self.assertIn("Step 1", block)

    def test_e4_whole_build_statement_never_a_per_step_figure(self):
        """EC-31; WV22 E-4 F2."""
        files = base_files()
        files["steps/step-01-record.md"] = step_record(
            1, extra="Budget position: money 0 external spend for the "
                     "whole build.")
        result, _ = run_case(make_case(
            "e4-whole-build-only", files,
            ("whole-build-money-statement",)))
        block = row_block(result.stdout, "E-4")
        assert_verdict(self, block, "present but not derivable", "E-4")

    def test_ac12_non_d1_figure_in_metrics_record_never_present(self):
        """EC-30; WV22 E-3 F1."""
        files = base_files()
        files[METRICS_PATH] = metrics_record(
            body="Metrics record states E-3 tokens for Step 1 as 4242. "
                 "No cost ledger stands in this tree.")
        result, _ = run_case(make_case("ac12-e3", files))
        block = row_block(result.stdout, "E-3")
        assert_verdict(self, block, "missing", "E-3")
        self.assertNotIn("4242", block)

    def test_ac12_feeder_mapping_d1_is_only_metrics_record_feeder(self):
        """EC-31; WV22 E-4 F1, WV22 E-4 F2."""
        files = base_files()
        files[METRICS_PATH] = metrics_record(
            body="Metrics record states E-4 money for Step 1 as 77 and "
                 "Q-4 share as 100 percent.")
        result, _ = run_case(make_case("ac12-mapping", files))
        e4 = row_block(result.stdout, "E-4")
        assert_verdict(self, e4, "present but not derivable", "E-4")
        self.assertNotIn("77", e4)
        q4 = row_block(result.stdout, "Q-4")
        assert_verdict(self, q4, "missing", "Q-4")

    def test_no_untraced_figure_for_cost_rows(self):
        """EC-18, EC-30, EC-31, EC-38; WV22 E-3 F1, WV22 E-4 F1."""
        files = base_files()
        files["notes/untraced-figures.md"] = (
            "# Working notes, not a feeder record\n\n"
            "E-3 tokens noted as 4242. E-4 money noted as 5353. "
            "B-2 total noted as 6464.\n")
        files["steps/step-01-gate-record.md"] = (
            "# Step 1 gate record\n\nClosure state: CLOSED-PASS.\n"
            "Money noted in passing as 5353.\n")
        result, _ = run_case(make_case("no-untraced", files))
        planted = {"E-3": "4242", "E-4": "5353", "B-2": "6464"}
        verdicts = {"E-3": "missing",
                    "E-4": "present but not derivable",
                    "B-2": "present but not derivable"}
        for code in ("E-3", "E-4", "B-2"):
            block = row_block(result.stdout, code)
            assert_verdict(self, block, verdicts[code], code)
            self.assertNotIn(planted[code], block, code)

    def test_b2_row_cross_check_marking_in_statement_line(self):
        """EC-38, EC-04; WV22 B-2 F7."""
        files = base_files()
        files[LEDGER_PATH] = LEDGER_FULL
        files[METRICS_PATH] = metrics_record(
            body="Metrics record states B-2 money spent as 999.")
        result, _ = run_case(make_case(
            "b2-cross-present", files,
            ("token-figures-in-ledger", "cost-ledger-inside-root",
             "per-step-money-figures")))
        block = row_block(result.stdout, "B-2")
        segment = statement_segment(block)
        self.assertIn("record disagrees", segment)
        self.assertIn("build-metrics-record.md", segment)
        self.assertTrue(has_number(segment, "60"))
        self.assertTrue(has_number(segment, "999"))

    def test_b2_not_derivable_row_cross_check_marking_second_case(self):
        """EC-38, EC-04; WV22 B-2 F7."""
        files = base_files()
        files[LEDGER_PATH] = LEDGER_PARTIAL
        files[METRICS_PATH] = metrics_record(
            body="Metrics record states B-2 token total as 8888.")
        result, _ = run_case(make_case(
            "b2-cross-not-derivable", files,
            ("token-figures-in-ledger", "cost-ledger-inside-root",
             "per-step-money-figures")))
        block = row_block(result.stdout, "B-2")
        assert_verdict(self, block, "present but not derivable", "B-2")
        segment = statement_segment(block)
        self.assertIn("record disagrees", segment)
        self.assertIn("build-metrics-record.md", segment)
        self.assertTrue(has_number(segment, "1000"))
        self.assertTrue(has_number(segment, "8888"))

    def test_f16_b2_open_state_row_reason(self):
        """EC-38, EC-02; WV22 B-2 F7."""
        files = base_files()
        del files["steps/step-03-gate-record.md"]
        files[LEDGER_PATH] = LEDGER_PARTIAL
        result, _ = run_case(make_case(
            "f16-b2-open", files,
            ("token-figures-in-ledger", "cost-ledger-inside-root",
             "open-build")))
        block = row_block(result.stdout, "B-2")
        self.assertIn("in progress", block.lower())

    def test_f17_b2_halt_row_reason(self):
        """EC-38, EC-02; WV22 B-2 F7."""
        files = base_files()
        files["steps/step-02-record.md"] = step_record(
            2, extra="This build stands halted. The work is halted "
                     "by order.")
        files[LEDGER_PATH] = LEDGER_PARTIAL
        result, _ = run_case(make_case(
            "f17-b2-halt", files,
            ("token-figures-in-ledger", "cost-ledger-inside-root",
             "halt-statement-recognised")))
        block = row_block(result.stdout, "B-2")
        self.assertIn("halted", block.lower())

    def test_f18_unknown_version_slice6_rows(self):
        """EC-03; WV22 E-3 F1, WV22 E-4 F1, WV22 B-2 F1."""
        files = base_files()
        files[LEDGER_PATH] = LEDGER_MONEY_ONLY
        files[METRICS_PATH] = metrics_record(
            body="Step table stands.", header_version="unknown-version-999")
        result, _ = run_case(make_case(
            "f18-slice6", files,
            ("per-step-money-figures", "cost-ledger-inside-root",
             "unknown-definitions-version")))
        for code in ("E-4", "B-2"):
            block = row_block(result.stdout, code)
            assert_verdict(self, block, "present but not derivable", code)
            self.assertIn("unknown-definitions-version", block, code)
            self.assertIn("unknown-version-999", block, code)
        assert_verdict(self, row_block(result.stdout, "E-3"),
                       "missing", "E-3")

    def test_b2_token_side_spent_and_budget_from_ledger_only(self):
        """EC-38; WV22 B-2 F1, WV22 B-2 F2, token side only."""
        result, _ = run_case(ledger_case("b2-token-side", LEDGER_FULL))
        block = row_block(result.stdout, "B-2")
        assert_verdict(self, block, "present", "B-2")
        self.assertTrue(has_number(block, "6000"))
        self.assertTrue(has_number(block, "10000"))

    def test_b2_money_side_spent_and_budget_from_ledger_only(self):
        """EC-38; WV22 B-2 F4, WV22 B-2 F5, money side only."""
        result, _ = run_case(ledger_case("b2-money-side", LEDGER_FULL))
        block = row_block(result.stdout, "B-2")
        assert_verdict(self, block, "present", "B-2")
        self.assertTrue(has_number(block, "60"))
        self.assertTrue(has_number(block, "100"))

    def test_b2_combination_percentages_from_both_sides(self):
        """EC-38; WV22 B-2 F3, WV22 B-2 F6, WV22 B-2 F7."""
        result, _ = run_case(ledger_case("b2-combined", LEDGER_FULL))
        block = row_block(result.stdout, "B-2")
        assert_verdict(self, block, "present", "B-2")
        self.assertTrue(has_number(block, "60"))

    def test_b2_step_record_figures_count_for_nothing_on_either_side(self):
        """EC-38; WV22 B-2 F1, WV22 B-2 F2, WV22 B-2 F4, WV22 B-2 F5."""
        files = base_files()
        files["steps/step-01-record.md"] = step_record(
            1, extra="Spent stated here as money 10 and tokens 1000. "
                     "Budget stated here as money 100 and tokens 10000.")
        result, _ = run_case(make_case("b2-step-record-only", files))
        block = row_block(result.stdout, "B-2")
        assert_verdict(self, block, "present but not derivable", "B-2")
        self.assertNotIn("1000", block)
        self.assertNotIn("10000", block)

    def test_b2_proxy_reported_as_proxy_only(self):
        """EC-38, EC-45; WV22 B-2 F7."""
        files = base_files()
        files[LEDGER_PATH] = LEDGER_FULL
        files["steps/step-01-record.md"] = step_record(
            1, extra="Agent count ceiling of 10 documented units on a "
                     "labelled proxy basis.")
        result, _ = run_case(make_case(
            "b2-proxy", files,
            ("token-figures-in-ledger", "cost-ledger-inside-root",
             "per-step-money-figures", "proxy-label")))
        self.assertIn("proxy", result.stdout.lower())
        block = row_block(result.stdout, "B-2")
        assert_verdict(self, block, "present", "B-2")
        self.assertTrue(has_number(block, "6000"))

    def test_b2_money_spent_with_absent_budget_percentage_undefined(self):
        """EC-38; WV22 B-2 F4, WV22 B-2 F5, WV22 B-2 F6, money side."""
        files = base_files()
        files[LEDGER_PATH] = (
            "# Cost ledger\n\nStep 1: money 10.\nStep 2: money 20.\n"
            "Step 3: money 30.\nNo budget figure stands.\n")
        result, _ = run_case(make_case(
            "b2-money-no-budget", files,
            ("per-step-money-figures", "cost-ledger-inside-root")))
        block = row_block(result.stdout, "B-2")
        assert_verdict(self, block, "present but not derivable", "B-2")
        self.assertIn("undefined", block.lower())
        self.assertNotIn("percent", block.lower().replace(
            "percentage is undefined", ""))

    def test_b2_token_side_absent_in_money_only_ledger_not_zero(self):
        """EC-38, EC-30; WV22 B-2 F1, WV22 B-2 F2, WV22 B-2 F3."""
        result, _ = run_case(ledger_case(
            "b2-money-only", LEDGER_MONEY_ONLY,
            ("per-step-money-figures", "cost-ledger-inside-root")))
        assert_verdict(self, row_block(result.stdout, "E-3"),
                       "missing", "E-3")
        block = row_block(result.stdout, "B-2")
        assert_verdict(self, block, "present but not derivable", "B-2")
        self.assertNotIn("0 percent", block.lower())

    def test_wv21_ledger_habit_equivalent_cost_rows(self):
        """EC-04, EC-07, EC-18, EC-31, EC-38."""
        shape_a_files = base_files()
        for n, amount in ((1, 10), (2, 20), (3, 30)):
            shape_a_files["steps/step-%02d-record.md" % n] = step_record(
                n, extra="Money spent for this step itself: %d." % amount)
        shape_b_files = base_files()
        shape_b_files[LEDGER_PATH] = LEDGER_MONEY_ONLY
        root = tracked_tempdir("msc_slice6_wv21_ledger_")
        built = build_cases([
            make_case("shape-a-step-records", shape_a_files,
                      ("per-step-money-figures",)),
            make_case("shape-b-ledger", shape_b_files,
                      ("per-step-money-figures",
                       "cost-ledger-inside-root"))], root)
        out_a = run_tool(built["shape-a-step-records"]).stdout
        out_b = run_tool(built["shape-b-ledger"]).stdout
        for code in ("E-4", "B-2"):
            self.assertEqual(row_verdict(row_block(out_a, code)),
                             row_verdict(row_block(out_b, code)),
                             "row %s verdict differs between shapes, "
                             "shape difference: cost ledger inside the "
                             "root in shape B" % code)

    def test_wv21_queue_habit_equivalent_content_same_rows(self):
        """EC-04, EC-08, EC-17, EC-36."""
        table_rows = ["| Q-1 | 1 | 2026-11-01 09:00 | "
                      "2026-11-01 10:00 | 2026-11-01 13:00 |"]
        shape_a_files = base_files()
        shape_a_files[METRICS_PATH] = metrics_record(
            body="Step table stands.",
            decision_table=decision_table(table_rows))
        shape_b_files = base_files()
        shape_b_files[METRICS_PATH] = metrics_record(
            body="Step table stands.",
            decision_table=decision_table(table_rows))
        shape_b_files["DECISION-QUEUE.md"] = queue_file(table_rows)
        root = tracked_tempdir("msc_slice6_wv21_queue_")
        built = build_cases([
            make_case("shape-a-table", shape_a_files,
                      ("decision-table-inside-root",
                       "decision-items-full-timestamps")),
            make_case("shape-b-queue", shape_b_files,
                      ("decision-table-inside-root",
                       "queue-file-inside-root", "queue-governs-over-table",
                       "decision-items-full-timestamps"))], root)
        out_a = run_tool(built["shape-a-table"]).stdout
        out_b = run_tool(built["shape-b-queue"]).stdout
        block_a = row_block(out_a, "D-1")
        block_b = row_block(out_b, "D-1")
        assert_verdict(self, block_a, "present", "D-1")
        assert_verdict(self, block_b, "present", "D-1")

    def test_cost_family_and_cross_check_read_capture_only(self):
        """EC-04; WV22 B-2 F7. Named reread test for Slice 6, plan S5."""
        files = base_files()
        files[LEDGER_PATH] = LEDGER_FULL
        root = tracked_tempdir("msc_slice6_reread_")
        built = build_case(make_case(
            "reread-cost", files,
            ("token-figures-in-ledger", "cost-ledger-inside-root",
             "per-step-money-figures")), root)
        assert_reads_capture_only(self, built, count_reads=True)


if __name__ == "__main__":
    unittest.main()
