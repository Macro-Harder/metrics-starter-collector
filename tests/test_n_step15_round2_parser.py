"""Step 15 fix round 2 tests: force parser name check and L-2 pins.

F15-20 pins that the Form A force parser records no force state for
a numbered list item naming no E-03 record change: an ordinary
agenda list in the metrics record, of the right shape, mints no
force states. F15-21 pins the two constructions the confirmation
correctness seat ruled on for the L-2 divergence between the BANKED
acceptance in the T-2 derivation and the words test in the refusal
helper: the refusal case with its control, and the date only
derivation case.
"""
import unittest

from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree,
                                     metrics_record, path_ledger,
                                     row_block, run_tool)

FULL_INTERVALS = (
    "Step 1 IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 17:00.\n"
    "Step 2 IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 17:00.\n"
    "Step 3 IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 17:00.")


def capture(root):
    from metrics_starter_collector.shell_reader import capture_read
    return capture_read(root)


class TestStep15Round2Parser(FixtureTestCase):

    # ------------------------------------------------------------ F15-20

    def test_f15_20_agenda_list_in_metrics_record_records_no_force_state(self):
        table = base_case()
        table["wiki/wiki/synthesis/build-metrics-record.md"] = \
            metrics_record(body=(
                "## Agenda\n\n"
                "1. Overview of the build: IN FORCE.\n"
                "2. Budget note: IN FORCE.\n"))
        root = build_tree(table)
        captured = capture(root)
        self.assertEqual(
            getattr(captured, "record_change_force", None), {})

    # ------------------------------------------------------------ F15-21

    def test_f15_21_date_only_banked_line_t2_missing_no_feeder_record(self):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.\n"
            "Step 1 BANKED 5 hours.",
            steps="1, 2, 3")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        t1 = row_block(result.stdout, "T-1")
        assert_verdict(self, t1, "missing", "T-1")
        self.assertIn("date-only-form", t1)
        block = row_block(result.stdout, "T-2")
        assert_verdict(self, block, "missing", "T-2")
        self.assertIn("no-feeder-record", block)
        self.assertNotIn("date-only-form", block)

    def test_f15_21_refusal_banked_without_interval_words_t2_missing_no_feeder(self):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            FULL_INTERVALS + "\nStep 1 BANKED 5 hours.",
            steps="1, 2, 3")
        table["wiki/wiki/synthesis/build-metrics-record.md"] = \
            metrics_record(body="Step table stands.",
                           header_version="unknown-version-999")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        t1 = row_block(result.stdout, "T-1")
        assert_verdict(self, t1, "present but not derivable", "T-1")
        block = row_block(result.stdout, "T-2")
        assert_verdict(self, block, "missing", "T-2")
        self.assertIn("no-feeder-record", block)
        self.assertNotIn("unknown-definitions-version", block)

    def test_f15_21_refusal_control_interval_words_t2_not_derivable_unknown_version(self):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            FULL_INTERVALS + "\nStep 1 BANKED interval duration 5 hours.",
            steps="1, 2, 3")
        table["wiki/wiki/synthesis/build-metrics-record.md"] = \
            metrics_record(body="Step table stands.",
                           header_version="unknown-version-999")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        t1 = row_block(result.stdout, "T-1")
        assert_verdict(self, t1, "present but not derivable", "T-1")
        block = row_block(result.stdout, "T-2")
        assert_verdict(self, block, "present but not derivable", "T-2")
        self.assertIn("unknown-definitions-version", block)
        self.assertIn("unknown-version-999", block)


if __name__ == "__main__":
    unittest.main()
