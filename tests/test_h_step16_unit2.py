"""Step 16 fix unit 2 tests: the decision table family.

Pinning tests for register items R16-03 (Medium) and R16-04 (Low)
of Step 16 round 1. R16-03: a decision table whose only data row
is its own empty notice, carrying no item name, no origin and no
raised field, must stand in the governed no item form, present
but not derivable with the reason naming that the table stands
and holds no item at all; the notice must not be counted as one
decision item standing open. The truly empty table, header and
separator and no item rows, stands in that same form and must
stay held. R16-04: a second decision table inside one metrics
record must not be silently ignored; its items count beside the
first table items, and where no item of either table forms a
latency the row names both tables and every item. The breaker
Attack 4 held forms stand as controls and must stay held: case b,
items carrying dates only in both forms; case c, a complete table
outside the root and a complete table in an unrecognised file
inside the root, neither feeding D-1; case d first form, a queue
file inside the root governing over a date only decision table.

Trees are written directly by this module, in the form the unit 1
pinning module uses. The product is invoked through run_tool,
which runs the module entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, gate_record, queue_file,
    row_block, run_tool, step_record, tracked_tempdir)

METRICS_PATH = "wiki/wiki/synthesis/build-metrics-record.md"
NOTICE = ("No decision queue items belonging to this build are "
          "recorded yet.")
NOTICE_ROW = "| %s |  |  |  |  |" % NOTICE
DATE_ONLY_ROW = "| First item | 1 | 2026-11-01 |  |  |"
FULL_ROW = ("| Second item | 1 | 2026-11-01 09:00 | "
            "2026-11-01 10:00 | 2026-11-02 13:00 |")
QUEUE_ROW = ("| Queue item | 1 | 2026-11-01 09:00 | "
             "2026-11-01 10:00 | 2026-11-02 13:00 |")
TABLE_DATE_ROW = "| Table item | 1 | 2026-11-01 |  |  |"


def _table(rows, heading="## Decision table"):
    """One decision table text: heading, header, separator, rows."""
    lines = [heading, "",
             "| Item | Origin step | Raised | Presented | Ruled |",
             "| --- | --- | --- | --- | --- |"]
    lines.extend(rows)
    return "\n".join(lines) + "\n"


def _metrics(table_text):
    """The metrics record text carrying the given table text."""
    return ("# Build metrics record\n\nBuild: metrics fixture "
            "build.\n\nStep table stands complete for the fixture "
            "steps.\n\n" + table_text)


def _base_files(metrics_text):
    """The small complete tree files, steps 1 to 3, as plain data."""
    files = {}
    transitions = []
    for n in (1, 2, 3):
        files["steps/step-%02d-record.md" % n] = step_record(n)
        files["steps/step-%02d-gate-record.md" % n] = gate_record(n)
        transitions.append(
            "Step %d IN PROGRESS 2026-11-01 09:00, closed "
            "2026-11-01 17:00." % n)
    files["PATH-LEDGER.md"] = (
        "# Path ledger\n\nSteps stated: 1, 2, 3.\n\n"
        "## Transitions\n\n%s\n" % "\n".join(transitions))
    files["TIER-RECORD.md"] = "# Tier record\n\nTier: Low. Base: 2.\n"
    files[METRICS_PATH] = metrics_text
    return files


def _write_tree(files):
    """Write one tree under a tracked temporary directory."""
    root = tracked_tempdir("msc_step16_unit2_") / "tree"
    for rel in sorted(files):
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(files[rel], encoding="utf-8")
    return root


class TestStep16Unit2(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout, root

    def test_r16_03_notice_as_table_data_row(self):
        """R16-03: the empty notice as a data row counts as no item."""
        files = _base_files(_metrics(_table([NOTICE_ROW])))
        report, _root = self._run(files)
        block = row_block(report, "D-1")
        assert_verdict(self, block, "present but not derivable",
                       "D-1")
        self.assertIn("holds no item at all", block)
        self.assertNotIn("holds one items", block)
        self.assertNotIn("stands open with no ruled timestamp",
                         block)
        self.assertNotIn(NOTICE, block)

    def test_r16_03_truly_empty_table_held(self):
        """Held control: header and separator, no item rows at all."""
        files = _base_files(_metrics(_table([])))
        report, _root = self._run(files)
        block = row_block(report, "D-1")
        assert_verdict(self, block, "present but not derivable",
                       "D-1")
        self.assertIn("holds no item at all", block)

    def test_r16_held_attack4_case_b_open_items(self):
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

    def test_r16_held_attack4_case_b_date_only_items(self):
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

    def test_r16_held_attack4_case_c_table_outside_root(self):
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

    def test_r16_held_attack4_case_c_table_unrecognised_file(self):
        """Held control, Attack 4 case c second form: stray file."""
        files = _base_files(_metrics(""))
        files["notes/decision-table-copy.md"] = _table([FULL_ROW])
        report, _root = self._run(files)
        block = row_block(report, "D-1")
        assert_verdict(self, block, "missing", "D-1")
        self.assertIn("no decision table stands in the capture",
                      block)
        self.assertNotIn("28 hours", block)

    def test_r16_held_attack4_case_d_queue_governs(self):
        """Held control, Attack 4 case d first form: queue governs."""
        files = _base_files(_metrics(_table([TABLE_DATE_ROW])))
        files["DECISION-QUEUE.md"] = queue_file([QUEUE_ROW])
        report, _root = self._run(files)
        block = row_block(report, "D-1")
        assert_verdict(self, block, "present", "D-1")
        self.assertIn("median 28 hours", block)
        self.assertIn("DECISION-QUEUE.md", block)
        self.assertIn("Queue item", block)

    def test_r16_04_second_table_item_counts(self):
        """R16-04: the second table latency item forms the figure."""
        text = _table([DATE_ONLY_ROW]) + "\n" + _table(
            [FULL_ROW], heading="## Decision table (continued)")
        files = _base_files(_metrics(text))
        report, _root = self._run(files)
        block = row_block(report, "D-1")
        assert_verdict(self, block, "present", "D-1")
        self.assertIn("median 28 hours", block)
        self.assertIn("Second item", block)
        self.assertIn("two decision tables", block)

    def test_r16_04_second_table_named_beside_present_row(self):
        """R16-04: the second table named on a present row as well."""
        text = _table([FULL_ROW]) + "\n" + _table(
            [TABLE_DATE_ROW], heading="## Decision table (continued)")
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
