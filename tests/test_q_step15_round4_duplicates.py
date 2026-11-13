"""Step 15 fix round 4 tests: duplicate selection and empty duplicate.

Each charged case pins fix register items F15-26 and F15-27, on the
constructions in design/audit/step-15-confirmation3-breaker.md
(CB3-1 and CB3-3). F15-26: the capture partition of F15-22 holds, but
the derivations that select a single piece from an identity group
took the first piece in path order, so where the canonical piece at
an identity has no content and a sound duplicate stands in a
subdirectory, the ledger rows T-1, T-2 and T-4 and the gate counting
in F-2 fed from the piece with no content and the sound duplicate
fed nothing, while the same trees with the duplicate at a path that
sorts first printed fully present. The selection must feed from a
readable piece where one stands in the identity group, as the step
record and metrics record selections already do. F15-27: a zero byte
or single newline duplicate still merged with the sound piece as a
duplicate content disagreement and erased it, because the partition
keyed on the read text being None and an empty file reads as an
empty text. The empty duplicate must stand as its own piece in the
no content family with its true state, and disagreement merging must
require two substantive differing texts. Control cases pin the
behaviour that must not move: where no readable piece stands in a
group the standing not derivable forms hold, identical duplicates,
empty or not, still merge into one piece, differing substantive
duplicates still merge as duplicate content disagreement, and a
lone empty canonical keeps its standing treatment.
"""
import os
import unittest

from metrics_starter_collector.derivation_core import (
    CLS_GATE_RECORD, CLS_PATH_LEDGER, CLS_STEP_RECORD)
from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree,
                                     piece_entry_for, row_block,
                                     run_tool, step_record)


def capture(root):
    from metrics_starter_collector.shell_reader import capture_read
    return capture_read(root)


def pieces_for(captured, record_class, step=None):
    return [p for p in captured.pieces
            if p.record_class == record_class
            and (step is None or p.step == step)]


class TestStep15Round4Duplicates(FixtureTestCase):

    def _intact_rows(self):
        intact = build_tree(base_case())
        result = run_tool(intact)
        self.assertEqual(result.returncode, 0, result.stderr)
        return (row_block(result.stdout, "E-1"),
                row_block(result.stdout, "E-2"),
                row_block(result.stdout, "F-2"))

    def _check_rows_match_intact(self, root):
        e1, e2, f2 = self._intact_rows()
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(row_block(result.stdout, "E-1"), e1)
        self.assertEqual(row_block(result.stdout, "E-2"), e2)
        self.assertEqual(row_block(result.stdout, "F-2"), f2)
        return result

    def _check_empty_duplicate(self, root, record_class, step,
                               sound_path, empty_path, empty_size,
                               empty_text):
        result = self._check_rows_match_intact(root)
        self.assertNotIn("duplicate", result.stdout.lower())
        captured = capture(root)
        pieces = pieces_for(captured, record_class, step)
        self.assertEqual(len(pieces), 2, pieces)
        sound = [p for p in pieces if p.paths == (sound_path,)]
        empty = [p for p in pieces if p.paths == (empty_path,)]
        self.assertEqual(len(sound), 1, pieces)
        self.assertEqual(len(empty), 1, pieces)
        self.assertIsNotNone(sound[0].text)
        self.assertTrue(sound[0].text.strip())
        self.assertEqual(empty[0].text, empty_text)
        self.assertEqual(empty[0].size, empty_size)
        self.assertIsNone(empty[0].quality_state)
        self.assertIsNone(empty[0].not_read_reason)
        entry = piece_entry_for(result.stdout, empty_path)
        self.assertTrue(entry)
        self.assertIn("read in full", entry)
        self.assertIn("%d bytes" % empty_size, entry)
        return result

    # ------------------------------------------------------------ F15-26

    def test_f15_26_directory_canonical_ledger_sound_duplicate_feeds(self):
        root = build_tree(base_case())
        ledger = root / "PATH-LEDGER.md"
        sound_text = ledger.read_text(encoding="utf-8")
        sound_text += "\nStep 1 BANKED interval duration 5 hours.\n"
        ledger.unlink()
        ledger.mkdir()
        sub = root / "sub"
        sub.mkdir()
        (sub / "PATH-LEDGER.md").write_text(sound_text,
                                            encoding="utf-8")
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        t1 = row_block(result.stdout, "T-1")
        assert_verdict(self, t1, "present", "T-1")
        self.assertIn("Pointer: sub/PATH-LEDGER.md", t1)
        self.assertIn("Step 1 elapsed 8 hours; Step 2 elapsed 8 hours; "
                      "Step 3 elapsed 8 hours", t1)
        self.assertNotIn("no transition log can be read", t1)
        t2 = row_block(result.stdout, "T-2")
        assert_verdict(self, t2, "present", "T-2")
        self.assertIn("Pointer: sub/PATH-LEDGER.md", t2)
        self.assertIn("Step 1 active 8 hours", t2)
        t4 = row_block(result.stdout, "T-4")
        assert_verdict(self, t4, "present", "T-4")
        self.assertIn("Pointer: sub/PATH-LEDGER.md", t4)
        self.assertIn("Step 1 banked wait 5 hours", t4)
        captured = capture(root)
        pieces = pieces_for(captured, CLS_PATH_LEDGER)
        self.assertEqual(len(pieces), 2, pieces)
        sound = [p for p in pieces if p.text is not None]
        broken = [p for p in pieces if p.text is None]
        self.assertEqual(len(sound), 1, pieces)
        self.assertEqual(sound[0].paths, ("sub/PATH-LEDGER.md",))
        self.assertEqual(len(broken), 1, pieces)
        self.assertEqual(broken[0].paths, ("PATH-LEDGER.md",))
        self.assertEqual(broken[0].quality_state, "unreadable")

    def test_f15_26_fifo_canonical_ledger_sound_duplicate_feeds(self):
        root = build_tree(base_case())
        ledger = root / "PATH-LEDGER.md"
        sound_text = ledger.read_text(encoding="utf-8")
        ledger.unlink()
        os.mkfifo(str(ledger))
        sub = root / "sub"
        sub.mkdir()
        (sub / "PATH-LEDGER.md").write_text(sound_text,
                                            encoding="utf-8")
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        t1 = row_block(result.stdout, "T-1")
        assert_verdict(self, t1, "present", "T-1")
        self.assertIn("Step 3 elapsed 8 hours", t1)
        t2 = row_block(result.stdout, "T-2")
        assert_verdict(self, t2, "present", "T-2")
        self.assertIn("Step 3 active 8 hours", t2)
        t4 = row_block(result.stdout, "T-4")
        assert_verdict(self, t4, "missing", "T-4")
        self.assertNotIn("not read in full", t4)

    def test_f15_26_malformed_canonical_ledger_sound_duplicate_feeds(self):
        table = base_case()
        sound_text = table["PATH-LEDGER.md"]
        table["PATH-LEDGER.md"] = b"\xff\xfe\x00 not utf8 \x80\x81"
        table["sub/PATH-LEDGER.md"] = sound_text
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        t1 = row_block(result.stdout, "T-1")
        assert_verdict(self, t1, "present", "T-1")
        self.assertIn("Pointer: sub/PATH-LEDGER.md", t1)
        self.assertIn("Step 2 elapsed 8 hours", t1)
        t2 = row_block(result.stdout, "T-2")
        assert_verdict(self, t2, "present", "T-2")
        self.assertIn("Step 2 active 8 hours", t2)

    def test_f15_26_directory_canonical_gate_sound_duplicate_feeds_f2(self):
        root = build_tree(base_case())
        gate = root / "steps" / "step-02-gate-record.md"
        sound_text = gate.read_text(encoding="utf-8")
        gate.unlink()
        gate.mkdir()
        sub = root / "steps" / "sub"
        sub.mkdir(parents=True)
        (sub / "step-02-gate-record.md").write_text(sound_text,
                                                    encoding="utf-8")
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        f2 = row_block(result.stdout, "F-2")
        assert_verdict(self, f2, "present", "F-2")
        self.assertIn("first-time approval rate 100 percent", f2)
        self.assertIn("plain approvals 3", f2)
        self.assertIn("steps ruled on 3", f2)
        self.assertNotIn("carry no first ruling outcome", f2)
        captured = capture(root)
        pieces = pieces_for(captured, CLS_GATE_RECORD, 2)
        self.assertEqual(len(pieces), 2, pieces)
        sound = [p for p in pieces if p.text is not None]
        broken = [p for p in pieces if p.text is None]
        self.assertEqual(len(sound), 1, pieces)
        self.assertEqual(sound[0].paths,
                         ("steps/sub/step-02-gate-record.md",))
        self.assertEqual(len(broken), 1, pieces)
        self.assertEqual(broken[0].paths,
                         ("steps/step-02-gate-record.md",))
        self.assertEqual(broken[0].quality_state, "unreadable")

    def test_f15_26_malformed_canonical_gate_sound_duplicate_feeds_f2(self):
        table = base_case()
        table["steps/sub/step-02-gate-record.md"] = \
            table["steps/step-02-gate-record.md"]
        table["steps/step-02-gate-record.md"] = \
            b"\xff\xfe\x00 not utf8 \x80\x81"
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        f2 = row_block(result.stdout, "F-2")
        assert_verdict(self, f2, "present", "F-2")
        self.assertIn("plain approvals 3", f2)
        self.assertIn("steps ruled on 3", f2)
        self.assertNotIn("carry no first ruling outcome", f2)
        captured = capture(root)
        pieces = pieces_for(captured, CLS_GATE_RECORD, 2)
        broken = [p for p in pieces if p.text is None]
        self.assertEqual(len(broken), 1, pieces)
        self.assertEqual(broken[0].quality_state, "malformed")

    def test_f15_26_control_directory_canonical_gate_aaa_duplicate_feeds(self):
        root = build_tree(base_case())
        gate = root / "steps" / "step-02-gate-record.md"
        sound_text = gate.read_text(encoding="utf-8")
        gate.unlink()
        gate.mkdir()
        aaa = root / "steps" / "aaa"
        aaa.mkdir(parents=True)
        (aaa / "step-02-gate-record.md").write_text(sound_text,
                                                    encoding="utf-8")
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        f2 = row_block(result.stdout, "F-2")
        assert_verdict(self, f2, "present", "F-2")
        self.assertIn("plain approvals 3", f2)
        self.assertIn("steps ruled on 3", f2)

    def test_f15_26_control_no_readable_ledger_piece_forms_hold(self):
        root = build_tree(base_case())
        ledger = root / "PATH-LEDGER.md"
        ledger.unlink()
        ledger.mkdir()
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        for code in ("T-1", "T-2", "T-4"):
            block = row_block(result.stdout, code)
            assert_verdict(self, block, "present but not derivable",
                           code)
            self.assertIn("present but not read in full", block)

    def test_f15_26_control_no_readable_gate_piece_forms_hold(self):
        root = build_tree(base_case())
        gate = root / "steps" / "step-02-gate-record.md"
        gate.unlink()
        gate.mkdir()
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        f2 = row_block(result.stdout, "F-2")
        assert_verdict(self, f2, "present but not derivable", "F-2")
        self.assertIn("plain approvals 2", f2)
        self.assertIn("steps ruled on 2", f2)

    # ------------------------------------------------------------ F15-27

    def test_f15_27_zero_byte_duplicate_step_record_sound_reads(self):
        table = base_case()
        table["steps/sub/step-02-record.md"] = b""
        root = build_tree(table)
        self._check_empty_duplicate(
            root, CLS_STEP_RECORD, 2,
            "steps/step-02-record.md", "steps/sub/step-02-record.md",
            0, "")

    def test_f15_27_newline_duplicate_step_record_sound_reads(self):
        table = base_case()
        table["steps/sub/step-02-record.md"] = b"\n"
        root = build_tree(table)
        self._check_empty_duplicate(
            root, CLS_STEP_RECORD, 2,
            "steps/step-02-record.md", "steps/sub/step-02-record.md",
            1, "\n")

    def test_f15_27_zero_byte_duplicate_gate_record_f2_stands(self):
        table = base_case()
        table["steps/sub/step-02-gate-record.md"] = b""
        root = build_tree(table)
        self._check_empty_duplicate(
            root, CLS_GATE_RECORD, 2,
            "steps/step-02-gate-record.md",
            "steps/sub/step-02-gate-record.md", 0, "")

    def test_f15_27_newline_duplicate_gate_record_f2_stands(self):
        table = base_case()
        table["steps/sub/step-02-gate-record.md"] = b"\n"
        root = build_tree(table)
        self._check_empty_duplicate(
            root, CLS_GATE_RECORD, 2,
            "steps/step-02-gate-record.md",
            "steps/sub/step-02-gate-record.md", 1, "\n")

    def test_f15_27_zero_byte_at_canonical_sound_duplicate_reads(self):
        table = base_case()
        table["steps/sub/step-02-record.md"] = \
            table["steps/step-02-record.md"]
        table["steps/step-02-record.md"] = b""
        root = build_tree(table)
        self._check_empty_duplicate(
            root, CLS_STEP_RECORD, 2,
            "steps/sub/step-02-record.md", "steps/step-02-record.md",
            0, "")

    def test_f15_27_empty_canonical_ledger_sound_duplicate_feeds(self):
        table = base_case()
        sound_text = table["PATH-LEDGER.md"]
        table["PATH-LEDGER.md"] = b""
        table["sub/PATH-LEDGER.md"] = sound_text
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("duplicate", result.stdout.lower())
        t1 = row_block(result.stdout, "T-1")
        assert_verdict(self, t1, "present", "T-1")
        self.assertIn("Pointer: sub/PATH-LEDGER.md", t1)
        self.assertIn("Step 2 elapsed 8 hours", t1)
        t2 = row_block(result.stdout, "T-2")
        assert_verdict(self, t2, "present", "T-2")
        self.assertIn("Step 2 active 8 hours", t2)
        captured = capture(root)
        pieces = pieces_for(captured, CLS_PATH_LEDGER)
        self.assertEqual(len(pieces), 2, pieces)
        empty = [p for p in pieces if p.paths == ("PATH-LEDGER.md",)]
        self.assertEqual(len(empty), 1, pieces)
        self.assertEqual(empty[0].text, "")
        self.assertEqual(empty[0].size, 0)

    def test_f15_27_newline_canonical_gate_sound_duplicate_feeds_f2(self):
        table = base_case()
        table["steps/sub/step-02-gate-record.md"] = \
            table["steps/step-02-gate-record.md"]
        table["steps/step-02-gate-record.md"] = b"\n"
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("duplicate", result.stdout.lower())
        f2 = row_block(result.stdout, "F-2")
        assert_verdict(self, f2, "present", "F-2")
        self.assertIn("plain approvals 3", f2)
        self.assertIn("steps ruled on 3", f2)
        captured = capture(root)
        pieces = pieces_for(captured, CLS_GATE_RECORD, 2)
        self.assertEqual(len(pieces), 2, pieces)
        empty = [p for p in pieces
                 if p.paths == ("steps/step-02-gate-record.md",)]
        self.assertEqual(len(empty), 1, pieces)
        self.assertEqual(empty[0].text, "\n")
        self.assertEqual(empty[0].size, 1)

    def test_f15_27_control_identical_empty_duplicates_still_merge(self):
        table = base_case()
        table["steps/step-02-record.md"] = b""
        table["steps/sub/step-02-record.md"] = b""
        root = build_tree(table)
        captured = capture(root)
        pieces = pieces_for(captured, CLS_STEP_RECORD, 2)
        self.assertEqual(len(pieces), 1, pieces)
        self.assertEqual(pieces[0].text, "")
        self.assertEqual(
            pieces[0].paths,
            ("steps/step-02-record.md", "steps/sub/step-02-record.md"))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("duplicate", result.stdout.lower())
        e1 = row_block(result.stdout, "E-1")
        self.assertIn("remainder Step 2 named, no base stated", e1)

    def test_f15_27_control_lone_empty_step_record_standing_treatment(self):
        table = base_case()
        table["steps/step-02-record.md"] = b""
        root = build_tree(table)
        captured = capture(root)
        pieces = pieces_for(captured, CLS_STEP_RECORD, 2)
        self.assertEqual(len(pieces), 1, pieces)
        self.assertEqual(pieces[0].text, "")
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        e1 = row_block(result.stdout, "E-1")
        self.assertIn("remainder Step 2 named, no base stated", e1)
        self.assertNotIn("feeder record present but not read in full",
                         e1)

    def test_f15_27_control_lone_empty_ledger_standing_treatment(self):
        table = base_case()
        table["PATH-LEDGER.md"] = b""
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        for code in ("T-1", "T-2", "T-4"):
            assert_verdict(self, row_block(result.stdout, code),
                           "missing", code)

    def test_f15_27_control_differing_substantive_duplicates_still_merge(self):
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
