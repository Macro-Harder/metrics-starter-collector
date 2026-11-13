"""Step 15 fix round 5 tests: verdict record counting and empty copies.

Each charged case pins one fix register item from fix round 5, on
the constructions in design/audit/step-15-confirmation4-breaker.md.
F15-31 (CB4-2): the F15-22 and F15-27 partition stands a damaged or
empty duplicate as its own piece, and two consumers counted pieces
as verdict records: the T-7 verdict count in the core and the
shell evidenced rounds that set the header rounds expectation. A
directory at the canonical gate record path with the sound record
at a sub path, and a zero byte duplicate beside the sound record,
each printed 2 rounds counted for one verdict record, the zero
byte form raised the header audit paper expectation from 3 to 4,
and with a stated pass count of 1 the row flipped to present but
not derivable on a disagreement that existed only in the counting.
The cure counts records, not partitioned copies: copies at one
identity count once in both consumers. The header found counts are
honest piece counts and do not move. F15-35 (CB4-6): two empty
entries at one identity with different empty forms, zero bytes and
a single newline, merged into one piece with no text and the
duplicate content disagreement reason, reported as not read in
full, although neither carries content that could disagree, and on
a ledger identity the second empty copy moved T-1 and T-2 from
their lone empty missing form to present but not derivable on that
false ground, while the inventory listed the newline path at
0 bytes because the merged piece carried the first path size.
The cure: empty entries never merge as a content disagreement.
Control cases pin the behaviour that must not move: identical
empty duplicates still merge as one piece, an empty entry beside a
substantive sibling still stands alone, differing substantive
duplicates still merge as a disagreement, a lone empty canonical
keeps its standing treatment, and two gate records at distinct
identities for one step still count as two verdict records.
"""
import re
import unittest

from metrics_starter_collector.derivation_core import (
    CLS_GATE_RECORD, CLS_PATH_LEDGER, CLS_STEP_RECORD)
from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree,
                                     data_quality_entry_for, gate_ruling,
                                     header_region, piece_entry_for,
                                     row_block, run_tool, step_record)


def capture(root):
    from metrics_starter_collector.shell_reader import capture_read
    return capture_read(root)


def pieces_for(captured, record_class, step=None):
    return [p for p in captured.pieces
            if p.record_class == record_class
            and (step is None or p.step == step)]


def class_counts(report, name):
    """Return (expected, found, not found, not yet recordable)."""
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


def loop_table(pass_count=None):
    """A three step tree where Step 2 names itself a loop step."""
    table = base_case(steps=(1, 2, 3))
    extra = "This step is a loop step."
    if pass_count is not None:
        extra += " Pass count in this record: %d passes." % pass_count
    table["steps/step-02-record.md"] = step_record(2, extra=extra)
    return table


class TestStep15Round5Counting(FixtureTestCase):

    # ------------------------------------------------------------ F15-31

    def test_f15_31_control_intact_loop_step_counts_one_round(self):
        root = build_tree(loop_table())
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        t7 = row_block(result.stdout, "T-7")
        assert_verdict(self, t7, "present", "T-7")
        self.assertIn("Step 2: 1 rounds counted", t7)
        self.assertEqual(class_counts(result.stdout, "audit paper"),
                         (3, 0, 3, 0))

    def test_f15_31_directory_gate_duplicate_counts_one_record(self):
        root = build_tree(loop_table())
        gate = root / "steps" / "step-02-gate-record.md"
        sound_text = gate.read_text(encoding="utf-8")
        gate.unlink()
        gate.mkdir()
        sub = root / "steps" / "sub"
        sub.mkdir(parents=True)
        (sub / "step-02-gate-record.md").write_text(sound_text,
                                                    encoding="utf-8")
        captured = capture(root)
        pieces = pieces_for(captured, CLS_GATE_RECORD, 2)
        self.assertEqual(len(pieces), 2, pieces)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        t7 = row_block(result.stdout, "T-7")
        assert_verdict(self, t7, "present", "T-7")
        self.assertIn("Step 2: 1 rounds counted", t7)
        self.assertNotIn("Step 2: 2 rounds counted", t7)
        self.assertEqual(class_counts(result.stdout, "audit paper"),
                         (3, 0, 3, 0))

    def test_f15_31_zero_byte_gate_duplicate_counts_one_record(self):
        table = loop_table()
        table["steps/sub/step-02-gate-record.md"] = b""
        root = build_tree(table)
        captured = capture(root)
        pieces = pieces_for(captured, CLS_GATE_RECORD, 2)
        self.assertEqual(len(pieces), 2, pieces)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        t7 = row_block(result.stdout, "T-7")
        assert_verdict(self, t7, "present", "T-7")
        self.assertIn("Step 2: 1 rounds counted", t7)
        self.assertNotIn("Step 2: 2 rounds counted", t7)
        self.assertEqual(class_counts(result.stdout, "audit paper"),
                         (3, 0, 3, 0))

    def test_f15_31_zero_byte_gate_duplicate_pass_count_reconciles(self):
        table = loop_table(pass_count=1)
        table["steps/sub/step-02-gate-record.md"] = b""
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        t7 = row_block(result.stdout, "T-7")
        assert_verdict(self, t7, "present", "T-7")
        self.assertIn("Step 2: 1 rounds counted", t7)
        self.assertNotIn("cannot be reconciled", t7)
        self.assertNotIn("verdict record count is 2", t7)

    def test_f15_31_control_distinct_gate_records_count_twice(self):
        table = loop_table()
        table["steps/step-02-gate-ruling.md"] = gate_ruling(2)
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        t7 = row_block(result.stdout, "T-7")
        assert_verdict(self, t7, "present", "T-7")
        self.assertIn("Step 2: 2 rounds counted", t7)
        self.assertEqual(class_counts(result.stdout, "audit paper"),
                         (4, 0, 4, 0))

    # ------------------------------------------------------------ F15-35

    def test_f15_35_two_empty_step_record_forms_no_disagreement(self):
        table = base_case()
        table["steps/step-02-record.md"] = b""
        table["steps/sub/step-02-record.md"] = b"\n"
        root = build_tree(table)
        captured = capture(root)
        pieces = pieces_for(captured, CLS_STEP_RECORD, 2)
        self.assertEqual(len(pieces), 2, pieces)
        by_path = {p.paths[0]: p for p in pieces}
        self.assertEqual(set(by_path),
                         {"steps/step-02-record.md",
                          "steps/sub/step-02-record.md"})
        zero = by_path["steps/step-02-record.md"]
        self.assertEqual(zero.paths, ("steps/step-02-record.md",))
        self.assertEqual(zero.text, "")
        self.assertEqual(zero.size, 0)
        self.assertIsNone(zero.quality_state)
        self.assertIsNone(zero.not_read_reason)
        newline = by_path["steps/sub/step-02-record.md"]
        self.assertEqual(newline.paths,
                         ("steps/sub/step-02-record.md",))
        self.assertEqual(newline.text, "\n")
        self.assertEqual(newline.size, 1)
        self.assertIsNone(newline.quality_state)
        self.assertIsNone(newline.not_read_reason)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("duplicate", result.stdout.lower())
        entry = piece_entry_for(result.stdout, "steps/step-02-record.md")
        self.assertTrue(entry)
        self.assertIn("0 bytes", entry)
        self.assertIn("read in full", entry)
        entry = piece_entry_for(result.stdout,
                                "steps/sub/step-02-record.md")
        self.assertTrue(entry)
        self.assertIn("1 bytes", entry)
        self.assertIn("read in full", entry)
        self.assertFalse(data_quality_entry_for(
            result.stdout, "step-02-record.md"))
        e1 = row_block(result.stdout, "E-1")
        self.assertIn("remainder Step 2 named, no base stated", e1)
        self.assertNotIn("not read in full", e1)

    def test_f15_35_two_empty_ledger_forms_rows_missing(self):
        table = base_case()
        table["PATH-LEDGER.md"] = b""
        table["sub/PATH-LEDGER.md"] = b"\n"
        root = build_tree(table)
        captured = capture(root)
        pieces = pieces_for(captured, CLS_PATH_LEDGER)
        self.assertEqual(len(pieces), 2, pieces)
        for piece in pieces:
            self.assertIsNotNone(piece.text)
            self.assertFalse(piece.text.strip())
            self.assertIsNone(piece.quality_state)
            self.assertIsNone(piece.not_read_reason)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("duplicate", result.stdout.lower())
        for code in ("T-1", "T-2", "T-4"):
            block = row_block(result.stdout, code)
            assert_verdict(self, block, "missing", code)
            self.assertNotIn("present but not read in full", block)
        entry = piece_entry_for(result.stdout, "sub/PATH-LEDGER.md")
        self.assertTrue(entry)
        self.assertIn("1 bytes", entry)
        self.assertIn("read in full", entry)

    def test_f15_35_control_identical_zero_duplicates_still_merge(self):
        table = base_case()
        table["steps/step-02-record.md"] = b""
        table["steps/sub/step-02-record.md"] = b""
        root = build_tree(table)
        captured = capture(root)
        pieces = pieces_for(captured, CLS_STEP_RECORD, 2)
        self.assertEqual(len(pieces), 1, pieces)
        self.assertEqual(pieces[0].text, "")
        self.assertEqual(pieces[0].size, 0)
        self.assertEqual(
            pieces[0].paths,
            ("steps/step-02-record.md", "steps/sub/step-02-record.md"))
        self.assertIsNone(pieces[0].not_read_reason)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("duplicate", result.stdout.lower())
        e1 = row_block(result.stdout, "E-1")
        self.assertIn("remainder Step 2 named, no base stated", e1)

    def test_f15_35_control_identical_newline_duplicates_still_merge(self):
        table = base_case()
        table["steps/step-02-record.md"] = b"\n"
        table["steps/sub/step-02-record.md"] = b"\n"
        root = build_tree(table)
        captured = capture(root)
        pieces = pieces_for(captured, CLS_STEP_RECORD, 2)
        self.assertEqual(len(pieces), 1, pieces)
        self.assertEqual(pieces[0].text, "\n")
        self.assertEqual(pieces[0].size, 1)
        self.assertEqual(
            pieces[0].paths,
            ("steps/step-02-record.md", "steps/sub/step-02-record.md"))
        self.assertIsNone(pieces[0].not_read_reason)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("duplicate", result.stdout.lower())

    def test_f15_35_control_empty_beside_substantive_stands_alone(self):
        table = base_case()
        table["steps/sub/step-02-record.md"] = b""
        root = build_tree(table)
        captured = capture(root)
        pieces = pieces_for(captured, CLS_STEP_RECORD, 2)
        self.assertEqual(len(pieces), 2, pieces)
        sound = [p for p in pieces
                 if p.paths == ("steps/step-02-record.md",)]
        empty = [p for p in pieces
                 if p.paths == ("steps/sub/step-02-record.md",)]
        self.assertEqual(len(sound), 1, pieces)
        self.assertTrue(sound[0].text.strip())
        self.assertEqual(len(empty), 1, pieces)
        self.assertEqual(empty[0].text, "")
        self.assertIsNone(empty[0].not_read_reason)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("duplicate", result.stdout.lower())
        e1 = row_block(result.stdout, "E-1")
        self.assertIn("Step 2 staffed 3 of base 2", e1)

    def test_f15_35_control_differing_substantive_duplicates_merge(self):
        table = base_case()
        table["steps/step-01-record.md"] = step_record(
            1, base=2, team=3,
            extra="Original content marker ORIGONLY stands here.")
        table["copy/step-01-record.md"] = step_record(
            1, base=2, team=99,
            extra="Duplicate content marker DUPONLY99 stands here.")
        root = build_tree(table)
        captured = capture(root)
        pieces = pieces_for(captured, CLS_STEP_RECORD, 1)
        self.assertEqual(len(pieces), 1, pieces)
        self.assertIsNone(pieces[0].text)
        self.assertIn("duplicate content disagreement",
                      pieces[0].not_read_reason)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("duplicate content disagreement", result.stdout)


if __name__ == "__main__":
    unittest.main()
