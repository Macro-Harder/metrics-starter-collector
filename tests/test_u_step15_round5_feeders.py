"""Step 15 fix round 5 tests: feeder selection and T-4 negation.

Each charged case pins one fix register item in the feeder cluster.
F15-32: the T-4 feeder parser _t4_banked_durations read the ledger
text with its own pattern and no negation handling, so a BANKED line
carrying a number fed T-4 however its own clause denied it, printing
a banked wait figure while T-2 on the same ledger printed the cured
missing form. A BANKED mention denied in its own clause must feed no
banked wait, and T-4 must print its missing form. F15-33: the shell
metrics assembly selected the first metrics piece whose text was not
None, and an empty file carries an empty string as its text, so an
empty canonical metrics record defeated the assembly and a sound
duplicate fed nothing: its decision table was lost, its unknown
definitions version never fired the refusal, and its force states
were never recorded. The assembly must feed from the first metrics
piece carrying substantive text, falling back to the standing
selection where no piece carries any. F15-34: the D-1 queue
selection read only the canonical queue piece, so a sound duplicate
queue fed nothing where the canonical piece was empty or a
directory. The selection must feed from a readable queue piece where
one stands, a sound canonical governing exactly as today, and the
standing forms holding where no queue piece carries a readable
table. Control cases pin the behaviour that must not move.
"""
import unittest

from metrics_starter_collector.derivation_core import _t4_banked_durations
from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, decision_table,
                                     metrics_record, path_ledger,
                                     queue_file, row_block, run_tool)

DATE_ONLY_LINE = "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.\n"
FULL_INTERVALS = (
    "Step 1 IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 17:00.\n"
    "Step 2 IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 17:00.\n"
    "Step 3 IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 17:00.")
CANONICAL_METRICS = "wiki/wiki/synthesis/build-metrics-record.md"
DUPLICATE_METRICS = "zzz/build-metrics-record.md"
QUEUE_ROW_8 = ("| Q-1 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | "
               "2026-11-01 17:00 |")
QUEUE_ROW_4 = ("| Q-2 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | "
               "2026-11-01 13:00 |")
QUEUE_ROW_MED4 = ("| Q-9 | 2 | 2026-11-02 09:00 | 2026-11-02 10:00 | "
                  "2026-11-02 13:00 |")
FORM_A_CHANGE4_NOT_IN_FORCE = (
    "## Record-change statement\n\n"
    "1. Timestamped state transitions in the path record: IN FORCE.\n"
    "2. Decision queue timestamps and origin: IN FORCE.\n"
    "3. Origin step on findings: IN FORCE.\n"
    "4. Agent-turn and per-agent engagement telemetry: NOT IN FORCE.\n"
    "5. Explicit loop round markers: IN FORCE.\n")


def capture(root):
    from metrics_starter_collector.shell_reader import capture_read
    return capture_read(root)


class TestStep15Round5Feeders(FixtureTestCase):

    # ------------------------------------------------------------ F15-32

    def _date_only_report(self, note):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            DATE_ONLY_LINE + note, steps="1, 2, 3")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        return root, result.stdout

    def _assert_t4_missing_on_denial(self, note):
        root, report = self._date_only_report(note)
        t2 = row_block(report, "T-2")
        assert_verdict(self, t2, "missing", "T-2")
        self.assertIn("date-only-form", t2)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "missing", "T-4")
        self.assertIn("no banked state and no decision item count "
                      "stands", t4)
        self.assertNotIn("banked wait 5 hours", report)
        self.assertEqual(_t4_banked_durations(capture(root)), [])

    def test_f15_32_no_banked_interval_duration_t4_missing(self):
        self._assert_t4_missing_on_denial(
            "Note: no BANKED interval duration 5 hours was recorded.")

    def test_f15_32_banked_interval_duration_was_not_recorded_t4_missing(self):
        self._assert_t4_missing_on_denial(
            "Note: a BANKED interval duration 5 hours was not "
            "recorded for this step.")

    def test_f15_32_control_genuine_banked_duration_t4_present(self):
        root, report = self._date_only_report(
            "Step 1 BANKED interval duration 5 hours.")
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present", "T-4")
        self.assertIn("Step 1 banked wait 5 hours", t4)
        self.assertEqual(_t4_banked_durations(capture(root)),
                         [(1, 5.0, True)])

    # ------------------------------------------------------------ F15-33

    def test_f15_33_empty_canonical_metrics_sound_duplicate_d1_present(self):
        table = base_case()
        table[CANONICAL_METRICS] = b""
        table[DUPLICATE_METRICS] = metrics_record(
            decision_table=decision_table([QUEUE_ROW_8, QUEUE_ROW_4]))
        root = build_tree(table)
        captured = capture(root)
        self.assertIn("Decision table", captured.assembled_metrics)
        self.assertEqual(captured.metrics_single_path,
                         DUPLICATE_METRICS)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        self.assertIn("median 6 hours", block)
        self.assertIn("longest 8 hours", block)
        self.assertIn("Pointer: " + DUPLICATE_METRICS, block)

    def test_f15_33_empty_canonical_metrics_unknown_version_refusal(self):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            FULL_INTERVALS + "\nStep 1 BANKED interval duration "
            "5 hours.", steps="1, 2, 3")
        table[CANONICAL_METRICS] = b""
        table[DUPLICATE_METRICS] = metrics_record(
            body="Step table stands.",
            header_version="unknown-version-999")
        root = build_tree(table)
        captured = capture(root)
        self.assertEqual(captured.definitions_version,
                         "unknown-version-999")
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "T-2")
        assert_verdict(self, block, "present but not derivable", "T-2")
        self.assertIn("unknown-definitions-version", block)
        self.assertIn("unknown-version-999", block)

    def test_f15_33_empty_canonical_metrics_force_states_from_duplicate(self):
        table = base_case()
        table[CANONICAL_METRICS] = b""
        table[DUPLICATE_METRICS] = metrics_record(
            body=FORM_A_CHANGE4_NOT_IN_FORCE)
        root = build_tree(table)
        captured = capture(root)
        self.assertEqual(
            getattr(captured, "record_change_force", None),
            {1: "IN FORCE", 2: "IN FORCE", 3: "IN FORCE",
             4: "NOT IN FORCE", 5: "IN FORCE"})

    def test_f15_33_control_directory_canonical_metrics_duplicate_feeds(self):
        table = base_case()
        table[DUPLICATE_METRICS] = metrics_record(
            decision_table=decision_table([QUEUE_ROW_8, QUEUE_ROW_4]))
        root = build_tree(table)
        canonical = root / CANONICAL_METRICS
        canonical.unlink()
        canonical.mkdir(parents=True)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        self.assertIn("median 6 hours", block)

    def test_f15_33_control_sound_canonical_metrics_governs(self):
        table = base_case()
        table[CANONICAL_METRICS] = metrics_record(
            decision_table=decision_table([QUEUE_ROW_MED4]))
        table[DUPLICATE_METRICS] = b""
        root = build_tree(table)
        captured = capture(root)
        self.assertEqual(captured.metrics_single_path,
                         CANONICAL_METRICS)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        self.assertIn("median 4 hours", block)
        self.assertIn("Pointer: " + CANONICAL_METRICS, block)

    def test_f15_33_control_lone_empty_canonical_metrics_standing_form(self):
        table = base_case()
        table[CANONICAL_METRICS] = b""
        root = build_tree(table)
        captured = capture(root)
        self.assertEqual(captured.assembled_metrics, "")
        self.assertEqual(captured.metrics_single_path,
                         CANONICAL_METRICS)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "missing", "D-1")
        self.assertIn("the metrics record holds no decision table",
                      block)

    # ------------------------------------------------------------ F15-34

    def _assert_duplicate_queue_feeds(self, root):
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        self.assertIn("median 6 hours", block)
        self.assertIn("longest 8 hours", block)
        self.assertIn("Pointer: sub/DECISION-QUEUE.md", block)
        self.assertIn("sub/DECISION-QUEUE.md", block)

    def test_f15_34_empty_canonical_queue_sound_duplicate_feeds(self):
        table = base_case()
        table["DECISION-QUEUE.md"] = b""
        table["sub/DECISION-QUEUE.md"] = queue_file(
            [QUEUE_ROW_8, QUEUE_ROW_4])
        self._assert_duplicate_queue_feeds(build_tree(table))

    def test_f15_34_directory_canonical_queue_sound_duplicate_feeds(self):
        table = base_case()
        table["sub/DECISION-QUEUE.md"] = queue_file(
            [QUEUE_ROW_8, QUEUE_ROW_4])
        root = build_tree(table)
        canonical = root / "DECISION-QUEUE.md"
        canonical.mkdir()
        self._assert_duplicate_queue_feeds(root)

    def test_f15_34_duplicate_only_queue_feeds(self):
        table = base_case()
        table["sub/DECISION-QUEUE.md"] = queue_file(
            [QUEUE_ROW_8, QUEUE_ROW_4])
        self._assert_duplicate_queue_feeds(build_tree(table))

    def test_f15_34_control_sound_canonical_queue_governs(self):
        table = base_case()
        table["DECISION-QUEUE.md"] = queue_file([QUEUE_ROW_MED4])
        table["sub/DECISION-QUEUE.md"] = b""
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        self.assertIn("median 4 hours", block)
        self.assertIn("Pointer: DECISION-QUEUE.md", block)

    def test_f15_34_control_no_readable_queue_table_forms_hold(self):
        table = base_case()
        table["DECISION-QUEUE.md"] = b""
        table["sub/DECISION-QUEUE.md"] = (
            "# Decision queue\n\nNo decision table stands here.\n")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present but not derivable", "D-1")
        self.assertIn("holds no decision item table", block)


if __name__ == "__main__":
    unittest.main()
