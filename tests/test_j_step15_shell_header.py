"""Step 15 fix round tests: shell passages and header totals.

Each case pins one Step 15 round 1 finding or settlement in the shell
and header cluster: the M-2 force state, A-1 to A-4 on the header
totals, and B-1 to B-5 on the silent shell passages. The trees are
built through the one fixture builder, with links and special files
placed on disk after the build where a case table cannot name them.
"""
import os
import re
import unittest
from pathlib import Path

from tests.fixture_builder import (STARTER_ORDER, FixtureTestCase,
                                     assert_verdict, base_case, build_tree,
                                     data_quality_entry_for,
                                     data_quality_section, gate_record,
                                     gate_ruling, header_region, manifest,
                                     metrics_record, piece_entry_for,
                                     row_block, row_order, run_tool,
                                     step_record)

FORM_A_CHANGE4_NOT_IN_FORCE = (
    "## Record-change statement\n\n"
    "1. Timestamped state transitions in the path record: IN FORCE.\n"
    "2. Decision queue timestamps and origin: IN FORCE.\n"
    "3. Origin step on findings: IN FORCE.\n"
    "4. Agent-turn and per-agent engagement telemetry: NOT IN FORCE.\n"
    "5. Explicit loop round markers: IN FORCE.\n")

FORM_A_ALL_IN_FORCE = (
    "## Record-change statement\n\n"
    "1. Timestamped state transitions in the path record: IN FORCE.\n"
    "2. Decision queue timestamps and origin: IN FORCE.\n"
    "3. Origin step on findings: IN FORCE.\n"
    "4. Agent-turn and per-agent engagement telemetry: IN FORCE.\n"
    "5. Explicit loop round markers: IN FORCE.\n")

GATE_CLASS_NAMES = ("gate record", "gate ruling", "regate record",
                    "gate adjudication")


def class_counts(report, name):
    """Return (expected, found, not found, not yet recordable) or None."""
    head = header_region(report)
    exp = re.search(r"Class %s: expected (\d+), found (\d+)"
                    % re.escape(name), head)
    nf = re.search(r"Class %s: not found (\d+)" % re.escape(name), head)
    nyr = re.search(r"Class %s: not yet recordable (\d+)"
                    % re.escape(name), head)
    if not (exp and nf and nyr):
        return None
    return (int(exp.group(1)), int(exp.group(2)), int(nf.group(1)),
            int(nyr.group(1)))


def capture(root):
    from metrics_starter_collector.shell_reader import capture_read
    return capture_read(root)


def force_states(captured):
    return getattr(captured, "record_change_force", None)


class TestStep15ShellHeader(FixtureTestCase):

    # ------------------------------------------------------------ M-2

    def test_m2_form_a_change4_not_in_force_recorded_counts_stay_zero(self):
        table = base_case()
        table["wiki/wiki/synthesis/build-metrics-record.md"] = \
            metrics_record(body=FORM_A_CHANGE4_NOT_IN_FORCE)
        table["registers/cost-ledger.md"] = \
            "# Cost ledger\n\nTokens: 10. Money: 0.\n"
        root = build_tree(table)
        captured = capture(root)
        self.assertEqual(force_states(captured),
                         {1: "IN FORCE", 2: "IN FORCE", 3: "IN FORCE",
                          4: "NOT IN FORCE", 5: "IN FORCE"})
        for entry in captured.inventory_totals.values():
            self.assertEqual(entry["not_yet_recordable"], 0)
        self.assertEqual(
            captured.inventory_totals["cost ledger"]["not_found"], 0)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        head = header_region(result.stdout)
        nyr = [ln for ln in head.splitlines()
               if "not yet recordable" in ln.lower()]
        self.assertTrue(nyr, head[:600])
        for ln in nyr:
            self.assertTrue(ln.rstrip().endswith(" 0"), ln)
        self.assertEqual(class_counts(result.stdout, "cost ledger"),
                         (1, 1, 0, 0))

    def test_m2_form_a_all_in_force_recorded_counts_stay_zero(self):
        table = base_case()
        table["wiki/wiki/synthesis/build-metrics-record.md"] = \
            metrics_record(body=FORM_A_ALL_IN_FORCE)
        root = build_tree(table)
        captured = capture(root)
        self.assertEqual(force_states(captured),
                         {1: "IN FORCE", 2: "IN FORCE", 3: "IN FORCE",
                          4: "IN FORCE", 5: "IN FORCE"})
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        head = header_region(result.stdout)
        nyr = [ln for ln in head.splitlines()
               if "not yet recordable" in ln.lower()]
        self.assertTrue(nyr, head[:600])
        for ln in nyr:
            self.assertTrue(ln.rstrip().endswith(" 0"), ln)

    def test_m2_form_b_only_statement_creates_no_force_state(self):
        table = base_case()
        table["wiki/wiki/synthesis/build-metrics-record.md"] = \
            metrics_record(
                body="The board restatement states that change 4 is "
                     "NOT IN FORCE for this build, in prose form.\n")
        root = build_tree(table)
        captured = capture(root)
        self.assertEqual(force_states(captured), {})
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        head = header_region(result.stdout)
        nyr = [ln for ln in head.splitlines()
               if "not yet recordable" in ln.lower()]
        self.assertTrue(nyr, head[:600])
        for ln in nyr:
            self.assertTrue(ln.rstrip().endswith(" 0"), ln)

    # ------------------------------------------------------------ A-1

    def test_a1_gate_aliases_share_one_first_gate_expectation(self):
        table = base_case(steps=(1, 2, 3))
        del table["steps/step-02-gate-record.md"]
        table["steps/step-02-gate-ruling.md"] = gate_ruling(2)
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        total_not_found = 0
        for name in GATE_CLASS_NAMES:
            counts = class_counts(result.stdout, name)
            self.assertIsNotNone(counts, name)
            total_not_found += counts[2]
        self.assertEqual(total_not_found, 0)
        self.assertEqual(class_counts(result.stdout, "gate record"),
                         (2, 2, 0, 0))
        self.assertEqual(class_counts(result.stdout, "gate ruling"),
                         (1, 1, 0, 0))

    def test_a1_step_without_any_gate_piece_counts_one_not_found(self):
        table = base_case(steps=(1, 2, 3))
        del table["steps/step-02-gate-record.md"]
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        carriers = []
        total_not_found = 0
        for name in GATE_CLASS_NAMES:
            counts = class_counts(result.stdout, name)
            self.assertIsNotNone(counts, name)
            total_not_found += counts[2]
            if counts[2]:
                carriers.append(name)
        self.assertEqual(total_not_found, 1)
        self.assertEqual(carriers, ["gate record"])
        self.assertEqual(class_counts(result.stdout, "gate record"),
                         (3, 2, 1, 0))

    # ------------------------------------------------------------ A-2

    def test_a2_class_with_no_found_piece_prints_its_header_lines(self):
        table = base_case()
        del table["wiki/wiki/synthesis/build-metrics-record.md"]
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(class_counts(result.stdout, "metrics record"),
                         (1, 0, 1, 0))

    # ------------------------------------------------------------ A-3

    def test_a3_per_round_expected_from_rounds_evidenced(self):
        table = base_case(steps=(1,))
        table["steps/step-01-record.md"] = step_record(
            1, extra="Pass count in this record: 4 passes.")
        table["papers/step1-red.md"] = "# Audit paper\n\nRound paper.\n"
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(class_counts(result.stdout, "audit paper"),
                         (4, 1, 3, 0))

    # ------------------------------------------------------------ A-4

    def test_a4_class_states_print_before_coverage_statement(self):
        root = build_tree(base_case())
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        lines = result.stdout.splitlines()
        class_at = next((i for i, ln in enumerate(lines)
                         if ln.startswith("Class ")), -1)
        coverage_at = next((i for i, ln in enumerate(lines)
                            if ln.startswith("Coverage statement:")), -1)
        self.assertTrue(0 <= class_at < coverage_at,
                        "class states do not stand before the coverage "
                        "statement")

    # ------------------------------------------------------------ B-1

    def test_b1_self_symlink_loop_marked_and_report_issues(self):
        root = build_tree(base_case())
        target = root / "steps" / "step-02-record.md"
        target.unlink()
        os.symlink(str(target), str(target))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(row_order(result.stdout), STARTER_ORDER)
        entry = piece_entry_for(result.stdout, "step-02-record.md")
        self.assertTrue(entry)
        self.assertIn("unreadable", entry.lower())
        self.assertTrue(
            data_quality_entry_for(result.stdout, "step-02-record.md"))

    def test_b1_mutual_symlink_loop_marked_and_report_issues(self):
        root = build_tree(base_case())
        os.symlink(str(root / "steps" / "step-05-record.md"),
                   str(root / "steps" / "step-04-record.md"))
        os.symlink(str(root / "steps" / "step-04-record.md"),
                   str(root / "steps" / "step-05-record.md"))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(row_order(result.stdout), STARTER_ORDER)
        for name in ("step-04-record.md", "step-05-record.md"):
            entry = piece_entry_for(result.stdout, name)
            self.assertTrue(entry, name)
            self.assertIn("unreadable", entry.lower(), name)

    # ------------------------------------------------------------ B-2

    def test_b2_dangling_step_record_surfaced_and_rows_honest(self):
        root = build_tree(base_case())
        target = root / "steps" / "step-02-record.md"
        target.unlink()
        os.symlink(str(root / "steps" / "no-such-target.md"),
                   str(target))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = piece_entry_for(result.stdout, "step-02-record.md")
        self.assertTrue(entry)
        self.assertIn("unreadable", entry.lower())
        self.assertTrue(
            data_quality_entry_for(result.stdout, "step-02-record.md"))
        self.assertEqual(class_counts(result.stdout, "step record"),
                         (3, 3, 0, 0))
        e1 = row_block(result.stdout, "E-1")
        self.assertIn("not read in full", e1)
        self.assertNotIn("no base stated", e1)
        e2 = row_block(result.stdout, "E-2")
        self.assertIn("not read in full", e2)
        self.assertNotIn("missing-field for the absent stated base", e2)

    def test_b2_dangling_gate_record_f2_not_printed_as_full_rate(self):
        table = base_case()
        table["steps/step-02-gate-record.md"] = \
            gate_record(2, "CLOSED-FAIL")
        root = build_tree(table)
        gate = root / "steps" / "step-02-gate-record.md"
        gate.unlink()
        os.symlink("gone.md", str(gate))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = piece_entry_for(result.stdout, "step-02-gate-record.md")
        self.assertTrue(entry)
        self.assertIn("unreadable", entry.lower())
        self.assertTrue(data_quality_entry_for(
            result.stdout, "step-02-gate-record.md"))
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present but not derivable", "F-2")
        self.assertNotIn("100 percent", block)
        self.assertNotIn("no gate record or gate ruling stands for "
                         "that step", block)

    # ------------------------------------------------------------ B-3

    def test_b3_fifo_at_record_name_surfaced(self):
        root = build_tree(base_case())
        os.mkfifo(str(root / "steps" / "step-06-record.md"))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = piece_entry_for(result.stdout, "step-06-record.md")
        self.assertTrue(entry)
        self.assertIn("unreadable", entry.lower())
        self.assertTrue(
            data_quality_entry_for(result.stdout, "step-06-record.md"))

    # ------------------------------------------------------------ B-4

    def test_b4_failed_stat_marks_size_unknown(self):
        root = build_tree(base_case())
        gate = root / "steps" / "step-02-gate-record.md"
        gate.unlink()
        os.symlink(str(root / "steps" / "missing-target.md"), str(gate))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        section = data_quality_section(result.stdout)
        self.assertIn("step-02-gate-record.md", section)
        self.assertIn("size unknown", section)

    # ------------------------------------------------------------ B-5

    def test_b5_destination_link_inside_tree_pointing_outside_refused(self):
        root = build_tree(base_case())
        outside = Path(root).parent / "escape-target-report.md"
        self.assertFalse(outside.exists())
        os.symlink(str(outside), str(root / "escape-link.md"))
        before = manifest(root)
        result = run_tool(root, extra=("--report",
                                       str(root / "escape-link.md")))
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertFalse(outside.exists())
        self.assertTrue((root / "escape-link.md").is_symlink())
        self.assertEqual(manifest(root), before)


if __name__ == "__main__":
    unittest.main()
