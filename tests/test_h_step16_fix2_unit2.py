"""Step 16 fix pass 2 unit 2 tests: the notice one cell seam.

Pinning tests for register item R16-2-02 of Step 16 round 2
(spin 1123, finding B2-02, Low), a seam in the R16-03 cure of
fix pass 1 unit 2. That cure skips a decision table data row
that is the table own empty notice only where its origin cell
and its raised cell both stand empty. A notice row carrying
one filled cell, an origin step stated or a raised date
stated, is counted as one decision item standing open, in a
single table and in either table of a two table record, while
the same notice with both cells empty is correctly skipped.
The verdict, present but not derivable, is right in effect;
the reason is false, reporting a notice that no items are
recorded as one item awaiting a ruling.

The cure these tests pin, in the register words: a data row
that is the empty notice in its words stands skipped as a
decision item whether its origin cell, its raised cell, or
both stand empty, and a row carrying item substance in any
cell stands counted as it stands counted now.

Held controls stand pinned beside the defect forms: the
charged form of R16-03, the both empty notice skipped; the
truly empty table of the brief, header and separator and no
item rows; a real item row carrying the notice words beside a
genuine item name, and a row carrying the notice words beside
genuine item content with its real fields stated, each of
which still counts; and every held form of the fix pass 1
unit 2 module, the breaker Attack 4 case b, case c and case d
forms and the two R16-04 two table forms, in the same words
that module pins them.

Trees are written through the unit 2 module helpers. The
product is invoked through run_tool, which runs the module
entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, queue_file, row_block,
    run_tool)
from tests.test_h_step16_unit2 import (
    DATE_ONLY_ROW, FULL_ROW, NOTICE, QUEUE_ROW, TABLE_DATE_ROW,
    _base_files, _metrics, _table, _write_tree)

NOTICE_ORIGIN_ROW = "| %s | 3 |  |  |  |" % NOTICE
NOTICE_RAISED_ROW = "| %s |  | 2026-11-01 |  |  |" % NOTICE
NOTICE_BOTH_EMPTY_ROW = "| %s |  |  |  |  |" % NOTICE
REAL_ITEM_NOTICE_ROW = (
    "| Real item, no decision queue items belonging to this "
    "build are recorded yet | 1 | 2026-11-01 |  |  |")
REAL_FIELDS_NOTICE_ROW = (
    "| %s for the audit round | 1 | 2026-11-01 09:00 | "
    "2026-11-01 10:00 | 2026-11-02 13:00 |" % NOTICE)
SECOND_HEADING = "## Decision table (continued)"


def _two_tables(first_rows, second_rows):
    """One record text carrying two decision tables, in order."""
    return _table(first_rows) + "\n" + _table(
        second_rows, heading=SECOND_HEADING)


class TestStep16Fix2Unit2(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout, root

    def _assert_no_item(self, report):
        block = row_block(report, "D-1")
        assert_verdict(self, block, "present but not derivable",
                       "D-1")
        self.assertIn("holds no item at all", block)
        self.assertNotIn("holds one items", block)
        self.assertNotIn("stands open with no ruled timestamp",
                         block)
        self.assertNotIn(NOTICE, block)
        return block

    def test_r16_2_02_origin_only_single_table(self):
        """Defect form: notice with origin stated, single table."""
        files = _base_files(_metrics(_table([NOTICE_ORIGIN_ROW])))
        report, _root = self._run(files)
        self._assert_no_item(report)

    def test_r16_2_02_raised_only_single_table(self):
        """Defect form: notice with raised stated, single table."""
        files = _base_files(_metrics(_table([NOTICE_RAISED_ROW])))
        report, _root = self._run(files)
        self._assert_no_item(report)

    def test_r16_2_02_origin_only_first_of_two_tables(self):
        """Defect form: origin notice first, empty notice second."""
        text = _two_tables([NOTICE_ORIGIN_ROW],
                           [NOTICE_BOTH_EMPTY_ROW])
        files = _base_files(_metrics(text))
        report, _root = self._run(files)
        self._assert_no_item(report)

    def test_r16_2_02_origin_only_second_of_two_tables(self):
        """Defect form: empty notice first, origin notice second."""
        text = _two_tables([NOTICE_BOTH_EMPTY_ROW],
                           [NOTICE_ORIGIN_ROW])
        files = _base_files(_metrics(text))
        report, _root = self._run(files)
        self._assert_no_item(report)

    def test_r16_2_02_raised_only_first_of_two_tables(self):
        """Defect form: raised notice first, empty notice second."""
        text = _two_tables([NOTICE_RAISED_ROW],
                           [NOTICE_BOTH_EMPTY_ROW])
        files = _base_files(_metrics(text))
        report, _root = self._run(files)
        self._assert_no_item(report)

    def test_r16_2_02_raised_only_second_of_two_tables(self):
        """Defect form: empty notice first, raised notice second."""
        text = _two_tables([NOTICE_BOTH_EMPTY_ROW],
                           [NOTICE_RAISED_ROW])
        files = _base_files(_metrics(text))
        report, _root = self._run(files)
        self._assert_no_item(report)

    def test_r16_2_held_both_empty_notice_skipped(self):
        """Held control: the R16-03 charged form, both cells empty."""
        files = _base_files(_metrics(
            _table([NOTICE_BOTH_EMPTY_ROW])))
        report, _root = self._run(files)
        self._assert_no_item(report)

    def test_r16_2_held_truly_empty_table(self):
        """Held control: header and separator, no item rows at all."""
        files = _base_files(_metrics(_table([])))
        report, _root = self._run(files)
        block = row_block(report, "D-1")
        assert_verdict(self, block, "present but not derivable",
                       "D-1")
        self.assertIn("holds no item at all", block)

    def test_r16_2_held_real_item_beside_notice_words(self):
        """Held control: a genuine item name beside notice words."""
        files = _base_files(_metrics(
            _table([REAL_ITEM_NOTICE_ROW])))
        report, _root = self._run(files)
        block = row_block(report, "D-1")
        assert_verdict(self, block, "present but not derivable",
                       "D-1")
        self.assertIn("holds one items", block)
        self.assertIn("Real item", block)
        self.assertIn("stands open with no ruled timestamp", block)

    def test_r16_2_held_notice_words_with_real_fields(self):
        """Held control: notice words beside genuine item content."""
        files = _base_files(_metrics(
            _table([REAL_FIELDS_NOTICE_ROW])))
        report, _root = self._run(files)
        block = row_block(report, "D-1")
        assert_verdict(self, block, "present", "D-1")
        self.assertIn("median 28 hours", block)
        self.assertIn("for the audit round", block)

    def test_r16_2_held_attack4_case_b_open_items(self):
        """Held control, Attack 4 case b first form: raised dates."""
        rows = ["| Item one | 1 | 2026-11-01 |  |  |",
                "| Item two | 1 | 2026-11-02 |  |  |"]
        files = _base_files(_metrics(_table(rows)))
        report, _root = self._run(files)
        block = row_block(report, "D-1")
        assert_verdict(self, block, "present but not derivable",
                       "D-1")
        self.assertIn("holds two items", block)
        self.assertIn("Item one", block)
        self.assertIn("Item two", block)

    def test_r16_2_held_attack4_case_b_date_only_items(self):
        """Held control, Attack 4 case b second form: all dates."""
        rows = ["| Item one | 1 | 2026-11-01 | 2026-11-02 | "
                "2026-11-03 |",
                "| Item two | 1 | 2026-11-02 | 2026-11-03 | "
                "2026-11-04 |"]
        files = _base_files(_metrics(_table(rows)))
        report, _root = self._run(files)
        block = row_block(report, "D-1")
        assert_verdict(self, block, "present but not derivable",
                       "D-1")
        self.assertIn("carries date only timestamps", block)

    def test_r16_2_held_attack4_case_c_table_outside_root(self):
        """Held control, Attack 4 case c first form: outside table."""
        files = _base_files(_metrics(""))
        root = _write_tree(files)
        outside = root.parent / "outside-decision-table.md"
        outside.write_text(_table([FULL_ROW]), encoding="utf-8")
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "missing", "D-1")
        self.assertIn("no decision table stands in the capture",
                      block)
        self.assertNotIn("28 hours", block)

    def test_r16_2_held_attack4_case_c_table_unrecognised_file(self):
        """Held control, Attack 4 case c second form: stray file."""
        files = _base_files(_metrics(""))
        files["notes/decision-table-copy.md"] = _table([FULL_ROW])
        report, _root = self._run(files)
        block = row_block(report, "D-1")
        assert_verdict(self, block, "missing", "D-1")
        self.assertIn("no decision table stands in the capture",
                      block)
        self.assertNotIn("28 hours", block)

    def test_r16_2_held_attack4_case_d_queue_governs(self):
        """Held control, Attack 4 case d first form: queue governs."""
        files = _base_files(_metrics(_table([TABLE_DATE_ROW])))
        files["DECISION-QUEUE.md"] = queue_file([QUEUE_ROW])
        report, _root = self._run(files)
        block = row_block(report, "D-1")
        assert_verdict(self, block, "present", "D-1")
        self.assertIn("median 28 hours", block)
        self.assertIn("DECISION-QUEUE.md", block)
        self.assertIn("Queue item", block)

    def test_r16_2_held_r16_04_second_table_item_counts(self):
        """Held control, R16-04: the second table item counts."""
        text = _two_tables([DATE_ONLY_ROW], [FULL_ROW])
        files = _base_files(_metrics(text))
        report, _root = self._run(files)
        block = row_block(report, "D-1")
        assert_verdict(self, block, "present", "D-1")
        self.assertIn("median 28 hours", block)
        self.assertIn("Second item", block)
        self.assertIn("two decision tables", block)

    def test_r16_2_held_r16_04_second_table_named_beside_present(self):
        """Held control, R16-04: second table named on present row."""
        text = _two_tables([FULL_ROW], [TABLE_DATE_ROW])
        files = _base_files(_metrics(text))
        report, _root = self._run(files)
        block = row_block(report, "D-1")
        assert_verdict(self, block, "present", "D-1")
        self.assertIn("median 28 hours", block)
        self.assertIn("two decision tables", block)
        self.assertIn("Table item", block)


if __name__ == "__main__":
    import unittest
    unittest.main()
