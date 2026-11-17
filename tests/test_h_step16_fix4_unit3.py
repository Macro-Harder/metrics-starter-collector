"""Step 16 fix pass 4 unit 3 tests: the T family unit.

Pinning tests for register items R16-4-04 (High, B4-02) and
R16-4-08 (Medium, B4-06) of Step 16 round 4. The governing
rule of the pass: a piece not read in full, for whatever
reason, is not read. Where the feeder a T row rests on
stands not read in full, the row stands present but not
derivable naming the piece and its bound, and no absence
is claimed over it; missing stands only where no feeder
record stands in the tree at all.

Two defect forms stand pinned, each exactly as spin 1137
built it at Attack 3. The T-4 form: the path ledger
carrying its three transitions and the line "Step 1 BANKED
for 5 hours", padded to 1,200,097 bytes over the file
limit and unread, standing missing with the no feeder
record code. The T-7 form: the Step 2 step record carrying
the "Loop step" marker and two closing outcome records
with their work lines, padded over the file limit and
unread, standing missing with the same code. Held controls
stand pinned beside them, byte for byte: the read control
of each defect form (the same ledger read in full, T-4
present at Step 1 wait 5 hours; the same loop record read
in full, T-7 present but not derivable on the round
mapping); the T-1 and T-2 not read forms in the unread
ledger report shape, the family model inside the same
report; the T-7 checked form of spin 1136, the all gates
unread construction, whose missing grounds rest on read
step records; the decision table forms of fix pass 1
Unit 2 as they stand on the D-1 row and on the T-4 row
(the notice skip and the two table counting); the ledger
family rows B-1 to B-4 in the unread ledger report shape;
and a genuinely absent feeder form for each row, missing
in its standing governed form.

Trees are written through the Unit 1 module helpers of fix
pass 1, because the constructions turn on exact byte
counts. The product is invoked through run_tool, which
runs the module entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, decision_table,
    metrics_record, row_block, run_tool, step_record)
from tests.test_h_step16_fix3_unit1 import _clean_files
from tests.test_h_step16_unit1 import _padded, _write_tree
from tests.test_h_step16_unit2 import (
    DATE_ONLY_ROW, FULL_ROW, NOTICE_ROW, TABLE_DATE_ROW,
    _base_files as _unit2_base_files, _metrics, _table)

BANKED_LEDGER = (
    "# Path ledger\n\nSteps stated: 1, 2, 3.\n\n## Transitions\n\n"
    "Step 1 IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 17:00.\n"
    "Step 2 IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 17:00.\n"
    "Step 3 IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 17:00.\n"
    "Step 1 BANKED for 5 hours.\n")

LOOP_RECORD_EXTRA = (
    "Loop step. Round 1 closing outcome record: Round 1 closed, "
    "work inside Round 1 stands in this record. Round 2 closing "
    "outcome record: Round 2 closed, work inside Round 2 stands "
    "in this record.")

READ_T4 = (
    "T-4 Wait on a decision | Verdict: present | Value: Step 1 "
    "wait 5 hours | Row coverage: denominator step universe 3 "
    "steps | Reconciled against: the metric carries no total to "
    "reconcile against | Pointer: the path ledger BANKED entries "
    "and the decision table row for each item counted "
    "(PATH-LEDGER.md)\n"
    "Statement line: degraded form: the row is shown without its "
    "queue cross check, from the BANKED interval durations "
    "standing in the feeder records")

NOT_READ_T1 = (
    "T-1 Step elapsed time | Verdict: present but not derivable "
    "| Reason: What the record shows: a path ledger piece is "
    "present but not read in full in the capture, so no "
    "transition log can be read to form an interval What "
    "follows: over-limit-piece the piece is marked not read in "
    "full in the inventory and no figure is read from it, so no "
    "interval figure stands (not producible) | Pointer: the "
    "path ledger transition entries (PATH-LEDGER.md)")

NOT_READ_T2 = (
    "T-2 Step active time | Verdict: present but not derivable "
    "| Reason: What the record shows: the path ledger piece is "
    "present but not read in full in the capture What follows: "
    "over-limit-piece no duration is read from a piece that is "
    "not read in full, so no figure stands (not producible) | "
    "Pointer: the path ledger transition entries (PATH-LEDGER.md)")

READ_T7 = (
    "T-7 Loop rounds | Verdict: present but not derivable | "
    "Reason: What the record shows: broken link, the round "
    "mapping link between the records of a loop step and its "
    "rounds (wrong form); form required, rounds mapped by an "
    "outcome record for the step, with both parts of the "
    "mapping test standing, the mapping conditions and the "
    "pairing evidence; form held, Step 2 rounds unpaired: "
    "Round 1, Round 2 stand as outcome records with no pairing "
    "record stating the work disposed of, a mapping test part "
    "two failure failing the single round What follows: no "
    "code fits the round mapping the row requires does not "
    "stand for the step named, so no round figure stands | "
    "Pointer: the loop round table and the verdict records for "
    "each loop step (steps/step-01-gate-record.md)")

MISSING_T4 = (
    "T-4 Wait on a decision | Verdict: missing | Reason: What "
    "the record shows: no path ledger piece in the capture "
    "holds a banked state from which a wait can form What "
    "follows: no-feeder-record no feeder record for the metric "
    "exists in the tree, so the row is missing (missing "
    "record) | Pointer: PATH-LEDGER.md")

MISSING_T7 = (
    "T-7 Loop rounds | Verdict: missing | Reason: What the "
    "record shows: the step universe holds no loop step for "
    "the metric to count, and no loop round table stands in "
    "the metrics record What follows: no-feeder-record no "
    "feeder record for the metric exists in the tree, so the "
    "row is missing (missing record) | Pointer: the loop round "
    "table and the verdict records for each loop step "
    "(steps/step-01-gate-record.md)")

NOTICE_D1 = (
    "D-1 Decision latency | Verdict: present but not derivable "
    "| Statement: Foundation statement: the decision table "
    "inside the root is the feeder this row rests on, under "
    "the exception for a tree with no queue file, and no queue "
    "file stands in the tree | Reason: What the record shows: "
    "broken link, the decision item rows of the decision table "
    "inside the root (missing field); form required, decision "
    "items carrying raised and ruled timestamps that can form "
    "a duration; form held, the decision table stands and "
    "holds no item at all What follows: missing-field the "
    "feeder stands and holds no item, so the row is not "
    "derivable and not missing | Pointer: the decision table "
    "inside the root, the allowed feeder "
    "(wiki/wiki/synthesis/build-metrics-record.md)\n"
    "Statement line: Foundation statement: the decision table "
    "inside the root is the feeder this row rests on, under "
    "the exception for a tree with no queue file, and no queue "
    "file stands in the tree")

TWO_TABLES_D1 = (
    "D-1 Decision latency | Verdict: present | Value: median "
    "28 hours over 1 items (Second item); longest 28 hours; "
    "items not counted: First item stands open with no ruled "
    "timestamp | Row coverage: denominator decision items in "
    "the governing record | Reconciled against: the metric "
    "carries no total to reconcile against | Statement: "
    "Foundation statement: the decision table inside the root "
    "is the feeder this row rests on, under the exception for "
    "a tree with no queue file, and no queue file stands in "
    "the tree; the metrics record carries two decision "
    "tables, and the items of every table stand together as "
    "the feeder items | Pointer: "
    "wiki/wiki/synthesis/build-metrics-record.md\n"
    "Statement line: Foundation statement: the decision table "
    "inside the root is the feeder this row rests on, under "
    "the exception for a tree with no queue file, and no queue "
    "file stands in the tree; the metrics record carries two "
    "decision tables, and the items of every table stand "
    "together as the feeder items")

TWO_TABLES_NAMED_D1 = TWO_TABLES_D1.replace(
    "First item stands open", "Table item stands open")

TABLE_T4 = (
    "T-4 Wait on a decision | Verdict: present | Value: Step 1 "
    "wait 2 hours | Row coverage: denominator step universe 3 "
    "steps | Reconciled against: the metric carries no total to "
    "reconcile against | Pointer: the path ledger BANKED "
    "entries and the decision table row for each item counted "
    "(PATH-LEDGER.md)\n"
    "Statement line: degraded form: the row is shown without "
    "its queue cross check, the decision table in the metrics "
    "record standing as the cross check in place of the queue "
    "file")

READ_B2 = (
    "B-2 Total cost against budget | Verdict: present | Value: "
    "money spent 60 against a money budget of 100, 60 percent; "
    "token spent 6000 against a token budget of 10000, 60 "
    "percent | Row coverage: denominator step universe 3 steps "
    "| Reconciled against: the metric carries no total to "
    "reconcile against | Pointer: registers/cost-ledger.md\n"
    "Statement line: build state naming: the build stands in "
    "progress, and no recognised piece states a halt in its own "
    "words")


def _t4_unread_files():
    files = _clean_files()
    files["PATH-LEDGER.md"] = _padded(BANKED_LEDGER, 1200097)
    return files


def _t7_unread_files():
    files = _clean_files()
    files["steps/step-02-record.md"] = _padded(
        step_record(2, extra=LOOP_RECORD_EXTRA), 1200097)
    return files


class TestStep16Fix4Unit3(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    # ------------------------------------------------------
    # Defect forms
    # ------------------------------------------------------

    def test_r16_4_04_ledger_unread_over_file_limit(self):
        """B4-02: T-4 missing over an unread path ledger."""
        report = self._run(_t4_unread_files())
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present but not derivable", "T-4")
        self.assertIn("PATH-LEDGER.md", t4)
        self.assertIn("file limit", t4)
        self.assertNotIn("no path ledger piece in the capture "
                         "holds a banked state", t4)
        self.assertNotIn("no feeder record for the metric exists",
                         t4)
        self.assertNotIn("no-feeder-record", t4)
        self.assertNotIn("Step 1 wait 5 hours", t4)

    def test_r16_4_08_loop_step_record_unread_over_file_limit(self):
        """B4-06: T-7 missing over an unread loop step record."""
        report = self._run(_t7_unread_files())
        t7 = row_block(report, "T-7")
        assert_verdict(self, t7, "present but not derivable", "T-7")
        self.assertIn("steps/step-02-record.md", t7)
        self.assertIn("file limit", t7)
        self.assertNotIn("holds no loop step", t7)
        self.assertNotIn("no feeder record for the metric exists",
                         t7)
        self.assertNotIn("no-feeder-record", t7)

    # ------------------------------------------------------
    # Read controls of the defect forms
    # ------------------------------------------------------

    def test_r16_4_04_read_control_byte_for_byte(self):
        """Read control: the same ledger read in full."""
        files = _clean_files()
        files["PATH-LEDGER.md"] = BANKED_LEDGER
        report = self._run(files)
        self.assertEqual(row_block(report, "T-4"), READ_T4)

    def test_r16_4_08_read_control_byte_for_byte(self):
        """Read control: the same loop record read in full."""
        files = _clean_files()
        files["steps/step-02-record.md"] = step_record(
            2, extra=LOOP_RECORD_EXTRA)
        report = self._run(files)
        self.assertEqual(row_block(report, "T-7"), READ_T7)

    # ------------------------------------------------------
    # Held controls: the family model in the same report
    # ------------------------------------------------------

    def test_r16_4_held_t1_not_read_byte_for_byte(self):
        """Held control: T-1 not read form on the unread ledger."""
        report = self._run(_t4_unread_files())
        self.assertEqual(row_block(report, "T-1"), NOT_READ_T1)

    def test_r16_4_held_t2_not_read_byte_for_byte(self):
        """Held control: T-2 not read form on the unread ledger."""
        report = self._run(_t4_unread_files())
        self.assertEqual(row_block(report, "T-2"), NOT_READ_T2)

    def test_r16_4_held_ledger_family_rows_on_unread_ledger(self):
        """Held control: B-1 to B-4 in their governed forms."""
        report = self._run(_t4_unread_files())
        for code in ("B-1", "B-3", "B-4"):
            block = row_block(report, code)
            assert_verdict(self, block, "present but not derivable",
                           code)
            self.assertIn("the T-1 row stands present but not "
                          "derivable", block)
        self.assertEqual(row_block(report, "B-2"), READ_B2)

    # ------------------------------------------------------
    # Held controls: the decision table forms
    # ------------------------------------------------------

    def test_r16_4_held_d1_notice_skip_byte_for_byte(self):
        """Held control: the notice skip of fix pass 1 Unit 2."""
        files = _unit2_base_files(_metrics(_table([NOTICE_ROW])))
        report = self._run(files)
        self.assertEqual(row_block(report, "D-1"), NOTICE_D1)

    def test_r16_4_held_d1_two_tables_count_byte_for_byte(self):
        """Held control: the second table item counts."""
        text = _table([DATE_ONLY_ROW]) + "\n" + _table(
            [FULL_ROW], heading="## Decision table (continued)")
        files = _unit2_base_files(_metrics(text))
        report = self._run(files)
        self.assertEqual(row_block(report, "D-1"), TWO_TABLES_D1)

    def test_r16_4_held_d1_two_tables_named_byte_for_byte(self):
        """Held control: the second table named beside a present row."""
        text = _table([FULL_ROW]) + "\n" + _table(
            [TABLE_DATE_ROW], heading="## Decision table (continued)")
        files = _unit2_base_files(_metrics(text))
        report = self._run(files)
        self.assertEqual(row_block(report, "D-1"), TWO_TABLES_NAMED_D1)

    def test_r16_4_held_t4_decision_table_byte_for_byte(self):
        """Held control: T-4 counted through the decision table."""
        files = _clean_files()
        files["PATH-LEDGER.md"] = BANKED_LEDGER.replace(
            "Step 1 BANKED for 5 hours.",
            "Step 1 BANKED duration 2 hours on Q-1.")
        files["wiki/wiki/synthesis/build-metrics-record.md"] = (
            metrics_record(
                body="Step table stands complete for the fixture "
                     "steps.",
                decision_table=decision_table(
                    ["| Q-1 | 1 | 2026-11-01 09:00 | "
                     "2026-11-01 10:00 | 2026-11-01 13:00 |"])))
        report = self._run(files)
        self.assertEqual(row_block(report, "T-4"), TABLE_T4)

    # ------------------------------------------------------
    # Held controls: checked and absent feeder forms
    # ------------------------------------------------------

    def test_r16_4_held_t7_all_gates_unread_byte_for_byte(self):
        """Held control: spin 1136 checked form, gates unread."""
        files = _clean_files()
        for n in (1, 2, 3):
            path = "steps/step-%02d-gate-record.md" % n
            files[path] = _padded(files[path], 1200097)
        report = self._run(files)
        self.assertEqual(row_block(report, "T-7"), MISSING_T7)

    def test_r16_4_held_t4_absent_feeder_byte_for_byte(self):
        """Held control: no path ledger stands anywhere."""
        files = _clean_files()
        del files["PATH-LEDGER.md"]
        report = self._run(files)
        self.assertEqual(row_block(report, "T-4"), MISSING_T4)

    def test_r16_4_held_t7_absent_feeder_byte_for_byte(self):
        """Held control: no step or gate record stands anywhere."""
        files = _clean_files()
        for path in [p for p in files
                     if "gate" in p or ("step" in p and "record" in p)]:
            del files[path]
        report = self._run(files)
        self.assertEqual(row_block(report, "T-7"), MISSING_T7)


if __name__ == "__main__":
    import unittest
    unittest.main()
