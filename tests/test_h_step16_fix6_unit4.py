"""Step 16 fix pass 6 unit 4 tests: the T family.

Pinning tests for register items R16-6-05 (Medium, B6-05)
and R16-6-10 (Low, C6-05 and B6-08 merged) of Step 16
round 6. The governing rule of the pass, in its extended
form: a piece not read in full, for whatever reason, is
not read.

R16-6-05: counted T-7 rounds for a loop step are silently
changed by an unread gate ruling carrying a closing
outcome record for that step, with no bound naming the
ruling, its limit, or its state. Construction: Step 2
counted at 2 rounds on its read step and gate records,
Step 3 standing at 2 rounds counted on its read records,
beside the Step 3 gate ruling carrying the Round 3
closing outcome record in its file bytes and padded over
the file limit; the truncated form takes the same present
row; against the read control standing Step 3 at 3 rounds
counted. Locus: derivation_core.py, _derive_t7, the loop
steps branch unread collection, which consults the step
record class only, while _t7_round_evidence takes outcome
records from every piece class, gate pieces among them.
The cure these tests pin: the T-7 bound collection
consults every piece class its evidence reading counts
from, gate records and gate rulings beside step records,
so where outcome evidence for a loop step stands in a
piece not read in full, a present row carries a bound
naming that piece and its bound or state, in the counted
form and in the mapping form alike.

R16-6-10: the unnamed durations branch of T-4 takes its
degraded statement over an unread governing queue byte
identical to the queue absent control; no piece, limit,
or standing is named. Construction: the path ledger read
in full carrying the banked line naming no item, beside
the decision queue file carrying a ruled item and padded
over the file limit, against the read control standing
at the same value with no statement line. Locus:
derivation_core.py, _derive_t4, the unnamed durations
branch. The cure these tests pin: where the governing
queue stands not read in full, the T-4 unnamed durations
statement names the queue piece and its bound or state,
as the named item branch beside it now does, whether the
row stands present on the ledger durations or withheld.

Held controls stand pinned beside the defect forms: the
cured step record routes of T-7 in both charged forms,
counted and mapping, from fix pass 5 Unit 5; the cured
named item branch of T-4 from the same unit; the ledger
routes of both rows in their governed forms, T-1 and T-2
byte for byte on the unread ledger report; the queue
absent and queue read forms of the unnamed durations
branch, byte for byte; and the withheld unnamed form
with no queue standing and with the queue read, whose
standing words must stand exactly as they stand.

Trees are written through the Unit 1 module helpers of
fix pass 1, because the constructions turn on exact byte
counts. The product is invoked through run_tool, which
runs the module entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, decision_table,
    gate_record, gate_ruling, metrics_record, queue_file,
    row_block, run_tool, step_record)
from tests.test_h_step16_fix3_unit1 import _clean_files
from tests.test_h_step16_fix4_unit3 import (
    BANKED_LEDGER, LOOP_RECORD_EXTRA, NOT_READ_T1,
    NOT_READ_T2, READ_T4, READ_T7, _t4_unread_files,
    _t7_unread_files)
from tests.test_h_step16_fix5_unit5 import (
    ABSENT_QUEUE_T4, COUNTED_T7, READ_QUEUE_T4, _t4_files)
from tests.test_h_step16_unit1 import _padded, _write_tree

METRICS_PATH = "wiki/wiki/synthesis/build-metrics-record.md"
RULING_3 = "steps/step-03-gate-ruling.md"
GATE_3 = "steps/step-03-gate-record.md"
STEP3_RECORD = "steps/step-03-record.md"
QUEUE = "DECISION-QUEUE.md"

COUNTED_STEP2_RECORD = (
    "Loop step. Round 1 work stands in this record. "
    "Round 2 work stands in this record.")
COUNTED_GATE2 = (
    "Round 1 closing outcome record. "
    "Round 2 closing outcome record.")
WORK_STEP3 = (
    "Loop step. Round 1 work stands in this record. "
    "Round 2 work stands in this record. "
    "Round 3 work stands in this record.")
GATE3_TWO = (
    "Round 1 closing outcome record. "
    "Round 2 closing outcome record.")
RULING3_ROUND3 = "Round 3 closing outcome record."
LOOP_STEP3 = (
    "Loop step. Round 1 closing outcome record: Round 1 "
    "closed, work inside Round 1 stands. Round 2 closing "
    "outcome record: Round 2 closed, work inside Round 2 "
    "stands.")

Q_ROW = ("| Q-1 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | "
         "2026-11-02 13:00 |")
NO_DURATION_LEDGER = BANKED_LEDGER.replace(
    "Step 1 BANKED for 5 hours.", "Step 1 BANKED.")


def _t7_gate_files(ruling):
    files = _clean_files()
    files["steps/step-02-record.md"] = step_record(
        2, extra=COUNTED_STEP2_RECORD)
    files["steps/step-02-gate-record.md"] = gate_record(
        2, extra=COUNTED_GATE2)
    files["steps/step-03-record.md"] = step_record(
        3, extra=WORK_STEP3)
    files[GATE_3] = gate_record(3, extra=GATE3_TWO)
    if ruling is not None:
        files[RULING_3] = ruling
    return files


def _t7_gate_record_files(gate3):
    files = _t7_gate_files(None)
    files[RULING_3] = gate_ruling(3, extra=GATE3_TWO)
    files[GATE_3] = gate3
    return files


def _t7_mapping_gate_files(ruling):
    files = _clean_files()
    files["steps/step-02-record.md"] = step_record(
        2, extra=LOOP_RECORD_EXTRA)
    files["steps/step-03-record.md"] = step_record(
        3, extra=WORK_STEP3)
    files[GATE_3] = gate_record(3, extra=GATE3_TWO)
    files[RULING_3] = ruling
    return files


def _t4_unnamed_files(queue, ledger=BANKED_LEDGER,
                      table_row=None):
    files = _clean_files()
    files["PATH-LEDGER.md"] = ledger
    if queue is not None:
        files[QUEUE] = queue
    if table_row is not None:
        files[METRICS_PATH] = metrics_record(
            body="Step table stands complete for the "
                 "fixture steps.",
            decision_table=decision_table([table_row]))
    return files


class TestStep16Fix6Unit4(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    def _bound(self, block):
        self.assertIn("Bound:", block)
        return block[block.find("Bound:"):]

    # ------------------------------------------------------
    # Defect forms, R16-6-05, row T-7 counted form
    # ------------------------------------------------------

    def test_r16_6_05_t7_counted_gate_ruling_over_limit(self):
        """B6-05: Step 3 counted 2 beside its unread ruling."""
        files = _t7_gate_files(_padded(
            gate_ruling(3, extra=RULING3_ROUND3), 1200097))
        report = self._run(files)
        t7 = row_block(report, "T-7")
        assert_verdict(self, t7, "present", "T-7")
        self.assertIn("Step 2: 2 rounds counted", t7)
        self.assertIn("Step 3: 2 rounds counted", t7)
        bound = self._bound(t7)
        self.assertIn(RULING_3, bound)
        self.assertIn("file limit", bound)

    def test_r16_6_05_t7_counted_gate_ruling_truncated(self):
        """B6-05 truncated form: the same ruling closed by a marker."""
        files = _t7_gate_files(
            gate_ruling(3, extra=RULING3_ROUND3) + "TRUNCATED\n")
        report = self._run(files)
        t7 = row_block(report, "T-7")
        assert_verdict(self, t7, "present", "T-7")
        self.assertIn("Step 3: 2 rounds counted", t7)
        bound = self._bound(t7)
        self.assertIn(RULING_3, bound)
        self.assertIn("truncat", bound.lower())

    def test_r16_6_05_t7_counted_gate_record_over_limit(self):
        """B6-05 gate record form: outcome evidence in a gate record."""
        files = _t7_gate_record_files(_padded(
            gate_record(3, extra=RULING3_ROUND3), 1200097))
        report = self._run(files)
        t7 = row_block(report, "T-7")
        assert_verdict(self, t7, "present", "T-7")
        self.assertIn("Step 3: 2 rounds counted", t7)
        bound = self._bound(t7)
        self.assertIn(GATE_3, bound)
        self.assertIn("file limit", bound)

    # ------------------------------------------------------
    # Defect forms, R16-6-05, row T-7 mapping form
    # ------------------------------------------------------

    def test_r16_6_05_t7_mapping_gate_ruling_truncated(self):
        """B6-05 mapping form: the ruling named beside a failure."""
        files = _t7_mapping_gate_files(
            gate_ruling(3, extra=RULING3_ROUND3) + "TRUNCATED\n")
        report = self._run(files)
        t7 = row_block(report, "T-7")
        assert_verdict(self, t7, "present but not derivable", "T-7")
        self.assertIn("Step 2 rounds unpaired", t7)
        self.assertIn(RULING_3, t7)
        self.assertIn("truncat", t7.lower())
        self.assertNotEqual(t7, READ_T7)

    # ------------------------------------------------------
    # Defect forms, R16-6-10, row T-4 unnamed durations
    # ------------------------------------------------------

    def test_r16_6_10_t4_unnamed_queue_over_limit(self):
        """C6-05: the degraded statement over an unread queue."""
        files = _t4_unnamed_files(
            _padded(queue_file([Q_ROW]), 1200097))
        report = self._run(files)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present", "T-4")
        self.assertIn("Step 1 wait 5 hours", t4)
        self.assertIn(QUEUE, t4)
        self.assertIn("file limit", t4)

    def test_r16_6_10_t4_unnamed_queue_truncated(self):
        """C6-05 damaged form: the queue closed by a marker."""
        files = _t4_unnamed_files(
            queue_file([Q_ROW]) + "TRUNCATED\n")
        report = self._run(files)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present", "T-4")
        self.assertIn("Step 1 wait 5 hours", t4)
        self.assertIn(QUEUE, t4)
        self.assertIn("truncat", t4.lower())

    def test_r16_6_10_t4_unnamed_b6_08_table_named_queue(self):
        """B6-08: the same ledger beside a table naming the item."""
        files = _t4_unnamed_files(
            _padded(queue_file([Q_ROW]), 1200097),
            table_row=Q_ROW)
        report = self._run(files)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present", "T-4")
        self.assertIn("Step 1 wait 5 hours", t4)
        self.assertIn(QUEUE, t4)
        self.assertIn("file limit", t4)

    def test_r16_6_10_t4_unnamed_withheld_queue_over_limit(self):
        """R16-6-10 withheld form: no duration stands on the ledger."""
        files = _t4_unnamed_files(
            _padded(queue_file([Q_ROW]), 1200097),
            ledger=NO_DURATION_LEDGER)
        report = self._run(files)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present but not derivable", "T-4")
        self.assertIn(QUEUE, t4)
        self.assertIn("file limit", t4)
        self.assertNotIn(
            "a queue file stands in the tree for the cross "
            "check", t4)

    # ------------------------------------------------------
    # Held controls, T-7 read and cured step record forms
    # ------------------------------------------------------

    def test_r16_6_held_t7_gate_ruling_read_control(self):
        """Held control: the B6-05 ruling read stands Step 3 at 3."""
        files = _t7_gate_files(gate_ruling(3, extra=RULING3_ROUND3))
        report = self._run(files)
        t7 = row_block(report, "T-7")
        assert_verdict(self, t7, "present", "T-7")
        self.assertIn("Step 3: 3 rounds counted", t7)
        self.assertNotIn("Bound:", t7)
        self.assertNotIn("not read in full", t7)

    def test_r16_6_held_t7_counted_read_control_byte_for_byte(self):
        """Held control: the fix pass 5 counted read control."""
        files = _clean_files()
        files["steps/step-02-record.md"] = step_record(
            2, extra=COUNTED_STEP2_RECORD)
        files["steps/step-02-gate-record.md"] = gate_record(
            2, extra=COUNTED_GATE2)
        files[STEP3_RECORD] = step_record(3)
        report = self._run(files)
        self.assertEqual(row_block(report, "T-7"), COUNTED_T7)

    def test_r16_6_held_t7_counted_step_record_over_limit(self):
        """Held R16-5-06: the cured counted step record route."""
        files = _clean_files()
        files["steps/step-02-record.md"] = step_record(
            2, extra=COUNTED_STEP2_RECORD)
        files["steps/step-02-gate-record.md"] = gate_record(
            2, extra=COUNTED_GATE2)
        files[STEP3_RECORD] = _padded(
            step_record(3, extra=LOOP_STEP3), 1200097)
        report = self._run(files)
        t7 = row_block(report, "T-7")
        assert_verdict(self, t7, "present", "T-7")
        bound = self._bound(t7)
        self.assertIn(STEP3_RECORD, bound)
        self.assertIn("file limit", bound)

    def test_r16_6_held_t7_counted_step_record_truncated(self):
        """Held R16-5-06 damaged form: the same route, truncated."""
        files = _clean_files()
        files["steps/step-02-record.md"] = step_record(
            2, extra=COUNTED_STEP2_RECORD)
        files["steps/step-02-gate-record.md"] = gate_record(
            2, extra=COUNTED_GATE2)
        files[STEP3_RECORD] = step_record(
            3, extra=LOOP_STEP3) + "TRUNCATED\n"
        report = self._run(files)
        t7 = row_block(report, "T-7")
        assert_verdict(self, t7, "present", "T-7")
        bound = self._bound(t7)
        self.assertIn(STEP3_RECORD, bound)
        self.assertIn("truncat", bound.lower())

    def test_r16_6_held_t7_mapping_read_control_byte_for_byte(self):
        """Held control: the fix pass 5 mapping read control."""
        files = _clean_files()
        files["steps/step-02-record.md"] = step_record(
            2, extra=LOOP_RECORD_EXTRA)
        files[STEP3_RECORD] = step_record(3)
        report = self._run(files)
        self.assertEqual(row_block(report, "T-7"), READ_T7)

    def test_r16_6_held_t7_mapping_step_record_truncated(self):
        """Held R16-5-14: the cured mapping step record route."""
        files = _clean_files()
        files["steps/step-02-record.md"] = step_record(
            2, extra=LOOP_RECORD_EXTRA)
        files[STEP3_RECORD] = step_record(
            3, extra=LOOP_STEP3) + "TRUNCATED\n"
        report = self._run(files)
        t7 = row_block(report, "T-7")
        assert_verdict(self, t7, "present but not derivable", "T-7")
        self.assertIn("Step 2 rounds unpaired", t7)
        self.assertIn(STEP3_RECORD, t7)
        self.assertIn("truncat", t7.lower())

    def test_r16_6_held_t7_missing_branch_cured(self):
        """Held R16-4-08: the missing branch cure of fix pass 4."""
        report = self._run(_t7_unread_files())
        t7 = row_block(report, "T-7")
        assert_verdict(self, t7, "present but not derivable", "T-7")
        self.assertIn("steps/step-02-record.md", t7)
        self.assertIn("file limit", t7)
        self.assertNotIn("no-feeder-record", t7)

    # ------------------------------------------------------
    # Held controls, T-4 unnamed read and absent forms
    # ------------------------------------------------------

    def test_r16_6_held_t4_unnamed_queue_absent_byte_for_byte(self):
        """Held control: no queue file stands in the tree at all."""
        files = _t4_unnamed_files(None)
        report = self._run(files)
        self.assertEqual(row_block(report, "T-4"), READ_T4)

    def test_r16_6_held_t4_unnamed_queue_read_byte_for_byte(self):
        """Held control: the governing queue read in full."""
        files = _t4_unnamed_files(queue_file([Q_ROW]))
        report = self._run(files)
        self.assertEqual(row_block(report, "T-4"), READ_QUEUE_T4)

    def test_r16_6_held_t4_unnamed_withheld_queue_absent(self):
        """Held control: the withheld form with no queue standing."""
        files = _t4_unnamed_files(None, ledger=NO_DURATION_LEDGER)
        report = self._run(files)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present but not derivable", "T-4")
        self.assertIn(
            "no queue file stands in the tree for the cross "
            "check", t4)
        self.assertNotIn(QUEUE, t4)

    def test_r16_6_held_t4_unnamed_withheld_queue_read(self):
        """Held control: the withheld form with the queue read."""
        files = _t4_unnamed_files(
            queue_file([Q_ROW]), ledger=NO_DURATION_LEDGER)
        report = self._run(files)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present but not derivable", "T-4")
        self.assertIn(
            "a queue file stands in the tree for the cross "
            "check", t4)
        self.assertNotIn("not read in full", t4)

    # ------------------------------------------------------
    # Held controls, T-4 named branch and ledger routes
    # ------------------------------------------------------

    def test_r16_6_held_t4_named_queue_over_limit(self):
        """Held R16-5-13: the cured named item branch naming."""
        files = _t4_files(_padded(queue_file([Q_ROW]), 1200097),
                          Q_ROW)
        report = self._run(files)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present", "T-4")
        self.assertIn("Step 1 wait 5 hours", t4)
        self.assertIn(QUEUE, t4)
        self.assertIn("file limit", t4)

    def test_r16_6_held_t4_named_queue_absent_byte_for_byte(self):
        """Held control: the named branch with no queue standing."""
        files = _t4_files(None, Q_ROW)
        report = self._run(files)
        self.assertEqual(row_block(report, "T-4"), ABSENT_QUEUE_T4)

    def test_r16_6_held_t4_named_queue_read_byte_for_byte(self):
        """Held control: the named branch with the queue read."""
        files = _t4_files(queue_file([Q_ROW]), Q_ROW)
        report = self._run(files)
        self.assertEqual(row_block(report, "T-4"), READ_QUEUE_T4)

    def test_r16_6_held_t4_ledger_unread_and_t1_t2_held(self):
        """Held R16-4-04: T-4, T-1 and T-2 on the unread ledger."""
        report = self._run(_t4_unread_files())
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present but not derivable", "T-4")
        self.assertIn("PATH-LEDGER.md", t4)
        self.assertIn("file limit", t4)
        self.assertEqual(row_block(report, "T-1"), NOT_READ_T1)
        self.assertEqual(row_block(report, "T-2"), NOT_READ_T2)


if __name__ == "__main__":
    import unittest
    unittest.main()
