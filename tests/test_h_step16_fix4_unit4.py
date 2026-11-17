"""Step 16 fix pass 4 unit 4 tests: the D-1 unit.

Pinning tests for register item R16-4-09 (Medium, B4-07) of
Step 16 round 4. The governing rule of the pass: a piece not
read in full, for whatever reason, is not read. Where a
queue file in the named form stands in the tree and not
read in full, D-1 stands present but not derivable naming
the queue piece and its bound, and no foundation statement
asserts that no queue file in the named form stands; the
decision table fallback governs only where no queue file
in the named form stands at all.

The defect form stands pinned exactly as spin 1137 built
it at Attack 3: a decision queue file in the named form
carrying one ruled item, raised 2026-11-01 09:00 and ruled
2026-11-02 13:00, a 28 hour latency, padded to 1,200,097
bytes over the file limit and unread; the metrics record
decision table carrying one different ruled item, Item
two, raised 2026-11-01 09:00 and ruled 2026-11-01 19:00, a
10 hour latency. D-1 stood present at median 10 hours
formed from the table, under a foundation statement
stating that no queue file in the named form stands in
the tree. The companion form, the same unread queue
beside an empty decision table, stood present but not
derivable carrying the same foundation statement.

Held controls stand pinned beside them, byte for byte:
the read control of the defect form (the same queue read
in full beside the same table, D-1 present at median 28
hours with the queue named as the governing feeder); the
Attack 4 queue control (a queue file beside a date only
decision table, D-1 present at median 28 hours); the
governed fallback form (no queue file anywhere in the
tree, D-1 present at median 10 hours from the table, the
foundation statement standing as today); the truly empty
table; the decision table forms of fix pass 1 Unit 2 on
the D-1 row (the notice skip, and the two table counting
with the table count named); the notice seam forms of
fix pass 2 Unit 2 (the notice with one filled cell
skipped in both its forms, a real item beside the notice
words counted, and notice words beside real fields
counted); and the date only table form, no latency
formed.

Trees are written through the Unit 2 module helpers of
fix pass 1, because the constructions turn on exact byte
counts. The product is invoked through run_tool, which
runs the module entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, d1_case, queue_file,
    row_block, run_tool)
from tests.test_d_slice4_time_decision import (
    RULED_ROW as SLICE4_RULED_ROW, run_case as run_slice4_case)
from tests.test_h_step16_fix2_unit2 import (
    NOTICE_ORIGIN_ROW, NOTICE_RAISED_ROW, REAL_FIELDS_NOTICE_ROW,
    REAL_ITEM_NOTICE_ROW)
from tests.test_h_step16_unit1 import _padded, _write_tree
from tests.test_h_step16_unit2 import (
    DATE_ONLY_ROW, FULL_ROW, NOTICE_ROW, QUEUE_ROW, TABLE_DATE_ROW,
    _base_files, _metrics, _table)

QUEUE_28_ROW = ("| Item one | 1 | 2026-11-01 09:00 | "
                "2026-11-01 10:00 | 2026-11-02 13:00 |")
TABLE_10_ROW = ("| Item two | 1 | 2026-11-01 09:00 | "
                "2026-11-01 10:00 | 2026-11-01 19:00 |")

READ_QUEUE_D1 = (
    "D-1 Decision latency | Verdict: present | Value: median "
    "28 hours over 1 items (Item one); longest 28 hours | Row "
    "coverage: denominator decision items in the governing "
    "record | Reconciled against: the metric carries no total "
    "to reconcile against | Statement: Foundation statement: "
    "the feeder this row rests on is DECISION-QUEUE.md, the "
    "queue file inside the root, governing over the metrics "
    "record decision table under WV-12, with the decision "
    "table standing as the cross check where one stands | "
    "Pointer: DECISION-QUEUE.md\n"
    "Statement line: Foundation statement: the feeder this row "
    "rests on is DECISION-QUEUE.md, the queue file inside the "
    "root, governing over the metrics record decision table "
    "under WV-12, with the decision table standing as the "
    "cross check where one stands")

READ_QUEUE_DATE_TABLE_D1 = READ_QUEUE_D1.replace(
    "(Item one)", "(Queue item)")

FALLBACK_D1 = (
    "D-1 Decision latency | Verdict: present | Value: median "
    "10 hours over 1 items (Item two); longest 10 hours | Row "
    "coverage: denominator decision items in the governing "
    "record | Reconciled against: the metric carries no total "
    "to reconcile against | Statement: Foundation statement: "
    "the decision table inside the root is the feeder this "
    "row rests on, under the exception for a tree with no "
    "queue file, and no queue file stands in the tree | "
    "Pointer: wiki/wiki/synthesis/build-metrics-record.md\n"
    "Statement line: Foundation statement: the decision table "
    "inside the root is the feeder this row rests on, under "
    "the exception for a tree with no queue file, and no "
    "queue file stands in the tree")

EMPTY_TABLE_D1 = (
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

REAL_ITEM_NOTICE_D1 = (
    "D-1 Decision latency | Verdict: present but not derivable "
    "| Statement: Foundation statement: the decision table "
    "inside the root is the feeder this row rests on, under "
    "the exception for a tree with no queue file, and no queue "
    "file stands in the tree | Reason: What the record shows: "
    "broken link, the presented and ruled timestamp fields on "
    "the decision table items (missing field); form required, "
    "raised and ruled timestamps that can form a duration on "
    "an item, with the median and the longest formed over the "
    "items that produce a latency; form held, the decision "
    "table holds one items, Real item, no decision queue items "
    "belonging to this build are recorded yet, each with "
    "origin step 1 and raised stated as a date only, "
    "2026-11-01, with presented and ruled blank; Real item, no "
    "decision queue items belonging to this build are recorded "
    "yet stands open with no ruled timestamp What follows: "
    "missing-field the raised and ruled fields the row "
    "requires do not both stand in full form on any item, so "
    "no median figure stands | Pointer: the decision table "
    "inside the root, the allowed feeder "
    "(wiki/wiki/synthesis/build-metrics-record.md)\n"
    "Statement line: Foundation statement: the decision table "
    "inside the root is the feeder this row rests on, under "
    "the exception for a tree with no queue file, and no queue "
    "file stands in the tree")

REAL_FIELDS_NOTICE_D1 = (
    "D-1 Decision latency | Verdict: present | Value: median "
    "28 hours over 1 items (No decision queue items belonging "
    "to this build are recorded yet. for the audit round); "
    "longest 28 hours | Row coverage: denominator decision "
    "items in the governing record | Reconciled against: the "
    "metric carries no total to reconcile against | "
    "Statement: Foundation statement: the decision table "
    "inside the root is the feeder this row rests on, under "
    "the exception for a tree with no queue file, and no queue "
    "file stands in the tree | Pointer: "
    "wiki/wiki/synthesis/build-metrics-record.md\n"
    "Statement line: Foundation statement: the decision table "
    "inside the root is the feeder this row rests on, under "
    "the exception for a tree with no queue file, and no queue "
    "file stands in the tree")

DATE_ONLY_D1 = (
    "D-1 Decision latency | Verdict: present but not derivable "
    "| Statement: Foundation statement: the decision table "
    "inside the root is the feeder this row rests on, under "
    "the exception for a tree with no queue file, and no queue "
    "file stands in the tree | Reason: What the record shows: "
    "broken link, the presented and ruled timestamp fields on "
    "the decision table items (missing field); form required, "
    "raised and ruled timestamps that can form a duration on "
    "an item, with the median and the longest formed over the "
    "items that produce a latency; form held, the decision "
    "table holds two items, Item one and Item two, each with "
    "origin step 1; Item one carries date only timestamps and "
    "forms no duration; Item two carries date only timestamps "
    "and forms no duration What follows: missing-field the "
    "raised and ruled fields the row requires do not both "
    "stand in full form on any item, so no median figure "
    "stands | Pointer: the decision table inside the root, "
    "the allowed feeder "
    "(wiki/wiki/synthesis/build-metrics-record.md)\n"
    "Statement line: Foundation statement: the decision table "
    "inside the root is the feeder this row rests on, under "
    "the exception for a tree with no queue file, and no queue "
    "file stands in the tree")


def _unread_queue_files(table_rows):
    files = _base_files(_metrics(_table(table_rows)))
    files["DECISION-QUEUE.md"] = _padded(
        queue_file([QUEUE_28_ROW]), 1200097)
    return files


class TestStep16Fix4Unit4(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    def _assert_unread_queue_cured(self, report):
        d1 = row_block(report, "D-1")
        assert_verdict(self, d1, "present but not derivable", "D-1")
        self.assertIn("DECISION-QUEUE.md", d1)
        self.assertIn("file limit", d1)
        self.assertNotIn("median 10 hours", d1)
        self.assertNotIn("median 28 hours", d1)
        self.assertNotIn(
            "no queue file in the named form stands", d1)
        self.assertNotIn("no queue file stands in the tree", d1)
        self.assertNotIn("no-feeder-record", d1)
        return d1

    # ------------------------------------------------------
    # Defect forms
    # ------------------------------------------------------

    def test_r16_4_09_unread_queue_beside_table_figure(self):
        """B4-07: D-1 table figure over an unread governing queue."""
        report = self._run(_unread_queue_files([TABLE_10_ROW]))
        self._assert_unread_queue_cured(report)

    def test_r16_4_09_unread_queue_beside_empty_table(self):
        """B4-07 companion: the same queue beside an empty table."""
        report = self._run(_unread_queue_files([]))
        self._assert_unread_queue_cured(report)

    # ------------------------------------------------------
    # Read controls of the defect form
    # ------------------------------------------------------

    def test_r16_4_09_read_control_byte_for_byte(self):
        """Read control: the same queue read in full governs."""
        files = _base_files(_metrics(_table([TABLE_10_ROW])))
        files["DECISION-QUEUE.md"] = queue_file([QUEUE_28_ROW])
        report = self._run(files)
        self.assertEqual(row_block(report, "D-1"), READ_QUEUE_D1)

    def test_r16_4_held_queue_beside_date_table_byte_for_byte(self):
        """Held control: Attack 4 queue beside a date only table."""
        files = _base_files(_metrics(_table([TABLE_DATE_ROW])))
        files["DECISION-QUEUE.md"] = queue_file([QUEUE_ROW])
        report = self._run(files)
        self.assertEqual(row_block(report, "D-1"),
                         READ_QUEUE_DATE_TABLE_D1)

    # ------------------------------------------------------
    # Held controls: the governed fallback and empty forms
    # ------------------------------------------------------

    def test_r16_4_held_fallback_no_queue_byte_for_byte(self):
        """Held control: no queue anywhere, the table governs."""
        files = _base_files(_metrics(_table([TABLE_10_ROW])))
        report = self._run(files)
        self.assertEqual(row_block(report, "D-1"), FALLBACK_D1)

    def test_r16_4_held_truly_empty_table_byte_for_byte(self):
        """Held control: header and separator, no item rows."""
        files = _base_files(_metrics(_table([])))
        report = self._run(files)
        self.assertEqual(row_block(report, "D-1"), EMPTY_TABLE_D1)

    def test_r16_4_held_date_only_table_byte_for_byte(self):
        """Held control: date only items form no latency."""
        rows = ["| Item one | 1 | 2026-11-01 | 2026-11-02 | "
                "2026-11-03 |",
                "| Item two | 1 | 2026-11-02 | 2026-11-03 | "
                "2026-11-04 |"]
        files = _base_files(_metrics(_table(rows)))
        report = self._run(files)
        self.assertEqual(row_block(report, "D-1"), DATE_ONLY_D1)

    # ------------------------------------------------------
    # Held controls: fix pass 1 Unit 2 decision table forms
    # ------------------------------------------------------

    def test_r16_4_held_notice_skip_byte_for_byte(self):
        """Held control: the notice skip of fix pass 1 Unit 2."""
        files = _base_files(_metrics(_table([NOTICE_ROW])))
        report = self._run(files)
        self.assertEqual(row_block(report, "D-1"), EMPTY_TABLE_D1)

    def test_r16_4_held_two_tables_count_byte_for_byte(self):
        """Held control: the second table item counts."""
        text = _table([DATE_ONLY_ROW]) + "\n" + _table(
            [FULL_ROW], heading="## Decision table (continued)")
        files = _base_files(_metrics(text))
        report = self._run(files)
        self.assertEqual(row_block(report, "D-1"), TWO_TABLES_D1)

    def test_r16_4_held_two_tables_named_byte_for_byte(self):
        """Held control: the second table named beside a present row."""
        text = _table([FULL_ROW]) + "\n" + _table(
            [TABLE_DATE_ROW], heading="## Decision table (continued)")
        files = _base_files(_metrics(text))
        report = self._run(files)
        self.assertEqual(row_block(report, "D-1"),
                         TWO_TABLES_NAMED_D1)

    # ------------------------------------------------------
    # Held controls: fix pass 2 Unit 2 notice seam forms
    # ------------------------------------------------------

    def test_r16_4_held_notice_origin_cell_byte_for_byte(self):
        """Held control: notice with origin stated stands skipped."""
        files = _base_files(_metrics(_table([NOTICE_ORIGIN_ROW])))
        report = self._run(files)
        self.assertEqual(row_block(report, "D-1"), EMPTY_TABLE_D1)

    def test_r16_4_held_notice_raised_cell_byte_for_byte(self):
        """Held control: notice with raised stated stands skipped."""
        files = _base_files(_metrics(_table([NOTICE_RAISED_ROW])))
        report = self._run(files)
        self.assertEqual(row_block(report, "D-1"), EMPTY_TABLE_D1)

    def test_r16_4_held_real_item_notice_byte_for_byte(self):
        """Held control: a genuine item beside notice words counts."""
        files = _base_files(_metrics(
            _table([REAL_ITEM_NOTICE_ROW])))
        report = self._run(files)
        self.assertEqual(row_block(report, "D-1"),
                         REAL_ITEM_NOTICE_D1)

    def test_r16_4_held_unusable_queue_table_governs(self):
        """Held control: Slice 4 cells 7 and 8, unusable queue.

        A queue standing unusable in the malformed form, not
        over a limit, stands outside this cure: the complete
        decision table governs and D-1 stands present, in the
        standing Slice 4 cell form.
        """
        result, _built = run_slice4_case(d1_case(
            "d1-unit4-unusable-held", table_rows=[SLICE4_RULED_ROW],
            unusable_queue=True))
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        self.assertIn("median 4 hours", block)
        self.assertIn("decision table", block)

    def test_r16_4_held_real_fields_notice_byte_for_byte(self):
        """Held control: notice words beside real fields count."""
        files = _base_files(_metrics(
            _table([REAL_FIELDS_NOTICE_ROW])))
        report = self._run(files)
        self.assertEqual(row_block(report, "D-1"),
                         REAL_FIELDS_NOTICE_D1)


if __name__ == "__main__":
    import unittest
    unittest.main()
