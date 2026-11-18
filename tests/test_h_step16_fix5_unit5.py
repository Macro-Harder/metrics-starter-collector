"""Step 16 fix pass 5 unit 5 tests: the T family.

Pinning tests for register items R16-5-06 (Medium, C5-06),
R16-5-14 (Low, B5-10) and R16-5-13 (Low, C5-12) of Step 16
round 5. The governing rule of the pass, in its extended
form: a piece not read in full, for whatever reason, is
not read.

R16-5-06: a present T-7 row states its counted rounds for
one loop step and omits a second loop step standing in an
unread step record, with no bound naming the piece, the
limit, or the omitted step. Locus: _derive_t7, whose not
read branch stands only in the no loop steps position.
R16-5-14: the same branch position, in the mapping form:
a present but not derivable T-7 row in its round mapping
form omits a damaged loop step record in silence.
R16-5-13: T-4 takes its queue cross check from the
fallback decision table over an unread governing queue,
in a statement that nowhere names the queue piece, its
limit, or the fact that a queue file stands in the tree
unread. Locus: _derive_t4, the named item branch.

The cure these tests pin: where any step record of the
evidenced universe stands not read in full, a present
T-7 row carries a bound naming the piece and the bound
or the state, in the counted form and in the mapping
form alike; and where the governing queue stands not
read in full, the T-4 cross check statement names the
queue piece and the bound or the state, whether the
cross check falls to the table or stands withheld.

Held controls stand pinned beside the defect forms: the
cured missing branches of T-7 and T-4 from fix pass 4
Unit 3, byte for byte where that unit pinned them; T-1
and T-2 in their governed forms on the same unread
ledger report; the read controls of every defect form;
the queue absent T-4 form, byte for byte, whose statement
must stand exactly as it stands today because no queue
piece stands in that tree at all; and the damaged and
malformed ledger routes of T-4 standing held in round 5.

Trees are written through the Unit 1 module helpers of
fix pass 1, because the constructions turn on exact byte
counts. The product is invoked through run_tool, which
runs the module entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, decision_table,
    gate_record, metrics_record, queue_file, row_block,
    run_tool, step_record)
from tests.test_h_step16_fix3_unit1 import _clean_files
from tests.test_h_step16_fix4_unit3 import (
    BANKED_LEDGER, LOOP_RECORD_EXTRA, MISSING_T7,
    NOT_READ_T1, NOT_READ_T2, READ_T4, READ_T7,
    _t4_unread_files, _t7_unread_files)
from tests.test_h_step16_unit1 import _padded, _write_tree

METRICS_PATH = "wiki/wiki/synthesis/build-metrics-record.md"
STEP3_RECORD = "steps/step-03-record.md"
MALFORMED_SUFFIX = b"\xff\xfe\xfd\n"

COUNTED_STEP2_RECORD = (
    "Loop step. Round 1 work stands in this record. "
    "Round 2 work stands in this record.")
COUNTED_GATE2 = (
    "Round 1 closing outcome record. "
    "Round 2 closing outcome record.")
LOOP_STEP3 = (
    "Loop step. Round 1 closing outcome record: Round 1 "
    "closed, work inside Round 1 stands. Round 2 closing "
    "outcome record: Round 2 closed, work inside Round 2 "
    "stands.")

COUNTED_T7 = (
    "T-7 Loop rounds | Verdict: present | Value: Step 2: 2 "
    "rounds counted; counted from verdict records, the "
    "rounds standing marked as counted, counted not marked "
    "from any table entry, a table entry alone counting "
    "nothing and outcome records alone counting once as "
    "counted | Row coverage: denominator step universe 3 "
    "steps; steps counted: Step 2 | Reconciled against: "
    "the metric carries no total to reconcile against | "
    "Pointer: the loop round table and the verdict records "
    "for each loop step (steps/step-01-gate-record.md)")

Q_ROW = ("| Q-1 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | "
         "2026-11-02 13:00 |")
OTHER_ROW = ("| Q-9 | 1 | 2026-11-01 09:00 | "
             "2026-11-01 10:00 | 2026-11-02 13:00 |")
LEDGER_Q1 = BANKED_LEDGER.replace(
    "Step 1 BANKED for 5 hours.",
    "Step 1 BANKED for 5 hours, item Q-1.")

ABSENT_QUEUE_T4 = (
    "T-4 Wait on a decision | Verdict: present | Value: "
    "Step 1 wait 5 hours | Row coverage: denominator step "
    "universe 3 steps | Reconciled against: the metric "
    "carries no total to reconcile against | Pointer: the "
    "path ledger BANKED entries and the decision table row "
    "for each item counted (PATH-LEDGER.md)\n"
    "Statement line: degraded form: the row is shown "
    "without its queue cross check, the decision table in "
    "the metrics record standing as the cross check in "
    "place of the queue file")

READ_QUEUE_T4 = (
    "T-4 Wait on a decision | Verdict: present | Value: "
    "Step 1 wait 5 hours | Row coverage: denominator step "
    "universe 3 steps | Reconciled against: the metric "
    "carries no total to reconcile against | Pointer: the "
    "path ledger BANKED entries and the decision table row "
    "for each item counted (PATH-LEDGER.md)")


def _t7_counted_files(step3):
    files = _clean_files()
    files["steps/step-02-record.md"] = step_record(
        2, extra=COUNTED_STEP2_RECORD)
    files["steps/step-02-gate-record.md"] = gate_record(
        2, extra=COUNTED_GATE2)
    files[STEP3_RECORD] = step3
    return files


def _t7_mapping_files(step3):
    files = _clean_files()
    files["steps/step-02-record.md"] = step_record(
        2, extra=LOOP_RECORD_EXTRA)
    files[STEP3_RECORD] = step3
    return files


def _t4_files(queue, table_row):
    files = _clean_files()
    files["PATH-LEDGER.md"] = LEDGER_Q1
    if queue is not None:
        files["DECISION-QUEUE.md"] = queue
    files[METRICS_PATH] = metrics_record(
        body="Step table stands complete for the fixture "
             "steps.",
        decision_table=decision_table([table_row]))
    return files


class TestStep16Fix5Unit5(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    def _bound(self, block):
        self.assertIn("Bound:", block)
        return block[block.find("Bound:"):]

    # ------------------------------------------------------
    # Defect forms, R16-5-06, row T-7 counted form
    # ------------------------------------------------------

    def test_r16_5_06_t7_counted_step3_over_limit(self):
        """C5-06: Step 2 counted, the Step 3 loop record unread."""
        files = _t7_counted_files(
            _padded(step_record(3, extra=LOOP_STEP3), 1200097))
        report = self._run(files)
        t7 = row_block(report, "T-7")
        assert_verdict(self, t7, "present", "T-7")
        self.assertIn("Step 2: 2 rounds counted", t7)
        bound = self._bound(t7)
        self.assertIn(STEP3_RECORD, bound)
        self.assertIn("file limit", bound)
        self.assertNotEqual(t7, COUNTED_T7)

    def test_r16_5_06_t7_counted_step3_truncated(self):
        """R16-5-06 damaged form: the Step 3 loop record truncated."""
        files = _t7_counted_files(
            step_record(3, extra=LOOP_STEP3) + "TRUNCATED\n")
        report = self._run(files)
        t7 = row_block(report, "T-7")
        assert_verdict(self, t7, "present", "T-7")
        self.assertIn("Step 2: 2 rounds counted", t7)
        bound = self._bound(t7)
        self.assertIn(STEP3_RECORD, bound)
        self.assertIn("truncat", bound.lower())
        self.assertNotEqual(t7, COUNTED_T7)

    # ------------------------------------------------------
    # Defect forms, R16-5-14, row T-7 mapping form
    # ------------------------------------------------------

    def test_r16_5_14_t7_mapping_step3_truncated(self):
        """B5-10: the mapping form omits a damaged loop record."""
        files = _t7_mapping_files(
            step_record(3, extra=LOOP_STEP3) + "TRUNCATED\n")
        report = self._run(files)
        t7 = row_block(report, "T-7")
        assert_verdict(self, t7, "present but not derivable", "T-7")
        self.assertIn("Step 2 rounds unpaired", t7)
        self.assertIn(STEP3_RECORD, t7)
        self.assertIn("truncat", t7.lower())
        self.assertNotEqual(t7, READ_T7)

    def test_r16_5_14_t7_mapping_step3_over_limit(self):
        """R16-5-14 over limit form: the same branch position."""
        files = _t7_mapping_files(
            _padded(step_record(3, extra=LOOP_STEP3), 1200097))
        report = self._run(files)
        t7 = row_block(report, "T-7")
        assert_verdict(self, t7, "present but not derivable", "T-7")
        self.assertIn("Step 2 rounds unpaired", t7)
        self.assertIn(STEP3_RECORD, t7)
        self.assertIn("file limit", t7)
        self.assertNotEqual(t7, READ_T7)

    # ------------------------------------------------------
    # Defect forms, R16-5-13, row T-4 cross check
    # ------------------------------------------------------

    def test_r16_5_13_t4_queue_over_limit_table_cross_check(self):
        """C5-12: the table cross check over an unread queue."""
        files = _t4_files(_padded(queue_file([Q_ROW]), 1200097),
                          Q_ROW)
        report = self._run(files)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present", "T-4")
        self.assertIn("Step 1 wait 5 hours", t4)
        self.assertIn("DECISION-QUEUE.md", t4)
        self.assertIn("file limit", t4)
        self.assertNotEqual(t4, ABSENT_QUEUE_T4)

    def test_r16_5_13_t4_queue_truncated_table_cross_check(self):
        """R16-5-13 damaged form: the queue closed by a marker."""
        files = _t4_files(queue_file([Q_ROW]) + "TRUNCATED\n",
                          Q_ROW)
        report = self._run(files)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present", "T-4")
        self.assertIn("Step 1 wait 5 hours", t4)
        self.assertIn("DECISION-QUEUE.md", t4)
        self.assertIn("truncat", t4.lower())
        self.assertNotEqual(t4, ABSENT_QUEUE_T4)

    def test_r16_5_13_t4_queue_malformed_table_cross_check(self):
        """R16-5-13 malformed form: the queue not valid text."""
        queue = queue_file([Q_ROW]).encode("utf-8") \
            + MALFORMED_SUFFIX
        files = _t4_files(queue, Q_ROW)
        report = self._run(files)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present", "T-4")
        self.assertIn("Step 1 wait 5 hours", t4)
        self.assertIn("DECISION-QUEUE.md", t4)
        self.assertIn("not read in full", t4)
        self.assertNotEqual(t4, ABSENT_QUEUE_T4)

    def test_r16_5_13_t4_queue_over_limit_cross_check_withheld(self):
        """R16-5-13 withheld form: no table item names Q-1."""
        files = _t4_files(_padded(queue_file([Q_ROW]), 1200097),
                          OTHER_ROW)
        report = self._run(files)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present but not derivable", "T-4")
        self.assertIn("DECISION-QUEUE.md", t4)
        self.assertIn("file limit", t4)
        self.assertNotIn(
            "no queue file and no decision table inside the "
            "root names that item", t4)

    # ------------------------------------------------------
    # Held controls, the T-7 read and cured forms
    # ------------------------------------------------------

    def test_r16_5_held_t7_counted_read_control_byte_for_byte(self):
        """Held control: Step 3 read, carrying no loop marker."""
        files = _t7_counted_files(step_record(3))
        report = self._run(files)
        self.assertEqual(row_block(report, "T-7"), COUNTED_T7)

    def test_r16_5_held_t7_mapping_read_control_byte_for_byte(self):
        """Held control: the B5-10 tree with Step 3 read plain."""
        files = _t7_mapping_files(step_record(3))
        report = self._run(files)
        self.assertEqual(row_block(report, "T-7"), READ_T7)

    def test_r16_5_held_t7_counted_read_loop_step_counted(self):
        """Held control: Step 3 read as a loop step stands named.

        The Step 3 record read in full carrying its loop
        marker and its closing outcome records takes the
        mapping form on its own unpaired rounds, exactly as
        the read tree stands; no bound for an unread piece
        stands, because no piece stands unread.
        """
        files = _t7_counted_files(step_record(3, extra=LOOP_STEP3))
        report = self._run(files)
        t7 = row_block(report, "T-7")
        assert_verdict(self, t7, "present but not derivable", "T-7")
        self.assertIn("Step 3 rounds unpaired", t7)
        self.assertNotIn("Bound:", t7)
        self.assertNotIn("not read in full", t7)

    def test_r16_5_held_t7_missing_branch_cured_byte_held(self):
        """Held R16-4-08: the missing branch cure of fix pass 4."""
        report = self._run(_t7_unread_files())
        t7 = row_block(report, "T-7")
        assert_verdict(self, t7, "present but not derivable", "T-7")
        self.assertIn("steps/step-02-record.md", t7)
        self.assertIn("file limit", t7)
        self.assertNotIn("no-feeder-record", t7)

    def test_r16_5_held_t7_absent_feeder_byte_for_byte(self):
        """Held control: no step or gate record stands anywhere."""
        files = _clean_files()
        for path in [p for p in files
                     if "gate" in p or ("step" in p and "record" in p)]:
            del files[path]
        report = self._run(files)
        self.assertEqual(row_block(report, "T-7"), MISSING_T7)

    # ------------------------------------------------------
    # Held controls, the T-4 read, absent and cured forms
    # ------------------------------------------------------

    def test_r16_5_held_t4_queue_absent_byte_for_byte(self):
        """Held control: no queue file stands in the tree at all."""
        files = _t4_files(None, Q_ROW)
        report = self._run(files)
        self.assertEqual(row_block(report, "T-4"), ABSENT_QUEUE_T4)

    def test_r16_5_held_t4_queue_read_byte_for_byte(self):
        """Held control: the governing queue read, naming Q-1."""
        files = _t4_files(queue_file([Q_ROW]), Q_ROW)
        report = self._run(files)
        self.assertEqual(row_block(report, "T-4"), READ_QUEUE_T4)

    def test_r16_5_held_t4_withheld_queue_absent(self):
        """Held control: the withheld form with no queue standing."""
        files = _t4_files(None, OTHER_ROW)
        report = self._run(files)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present but not derivable", "T-4")
        self.assertIn(
            "no queue file and no decision table inside the "
            "root names that item", t4)
        self.assertNotIn("DECISION-QUEUE.md", t4)

    def test_r16_5_held_t4_read_control_byte_for_byte(self):
        """Held R16-4-04 read control: the ledger read in full."""
        files = _clean_files()
        files["PATH-LEDGER.md"] = BANKED_LEDGER
        report = self._run(files)
        self.assertEqual(row_block(report, "T-4"), READ_T4)

    def test_r16_5_held_t4_ledger_unread_and_t1_t2_held(self):
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
