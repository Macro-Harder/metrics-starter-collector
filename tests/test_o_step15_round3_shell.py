"""Step 15 fix round 3 tests: shell no content duplicate cluster.

Each charged case pins fix register item F15-22, on the constructions
in design/audit/step-15-confirmation2-breaker.md (CB2-1): a duplicate
at the same identity that yields no readable content and stands
outside the walk damaged map (a directory, a link to a directory, a
malformed file, an over limit file) still merged with the sound piece
at that identity, discarded the sound text whole, and was labelled
duplicate content disagreement, a cause that cannot exist where one
side has no readable content. The sound piece must read, count and
feed derivations exactly as on the intact tree, and the no content
entry must stand as its own piece with its true state. Control cases
pin the behaviour that must not move: two genuine, differing,
readable duplicates still merge as duplicate content disagreement,
and two identical readable duplicates still merge into one sound
piece.
"""
import os
import unittest
from pathlib import Path

from metrics_starter_collector.derivation_core import (
    CLS_GATE_RECORD, CLS_STEP_RECORD)
from tests.fixture_builder import (FixtureTestCase, base_case, build_tree,
                                     coverage_statement, piece_entry_for,
                                     row_block, run_tool, step_record)


def capture(root):
    from metrics_starter_collector.shell_reader import capture_read
    return capture_read(root)


def pieces_for(captured, record_class, step):
    return [p for p in captured.pieces
            if p.record_class == record_class and p.step == step]


class TestStep15Round3Shell(FixtureTestCase):

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

    def _check_sound_survives(self, root, record_class, step,
                              sound_path, broken_path, quality, words,
                              broken_size=None):
        result = self._check_rows_match_intact(root)
        self.assertNotIn("duplicate", result.stdout.lower())
        captured = capture(root)
        pieces = pieces_for(captured, record_class, step)
        sound = [p for p in pieces if p.text is not None]
        broken = [p for p in pieces if p.text is None]
        self.assertEqual(len(pieces), 2, pieces)
        self.assertEqual(len(sound), 1, pieces)
        self.assertEqual(len(broken), 1, pieces)
        self.assertEqual(sound[0].paths, (sound_path,))
        self.assertEqual(broken[0].paths, (broken_path,))
        self.assertEqual(broken[0].quality_state, quality)
        self.assertIn(words, broken[0].not_read_reason)
        self.assertNotIn("duplicate", broken[0].not_read_reason)
        if broken_size is not None:
            self.assertEqual(broken[0].size, broken_size)
        coverage = coverage_statement(result.stdout)
        self.assertIn(broken_path, coverage)
        self.assertIn(words, coverage)
        entry = piece_entry_for(result.stdout, broken_path)
        self.assertTrue(entry)
        self.assertIn(quality, entry.lower())

    # ------------------------------------------------------------ F15-22

    def test_f15_22_directory_duplicate_sound_record_reads(self):
        root = build_tree(base_case())
        sub = root / "steps" / "sub"
        sub.mkdir(parents=True)
        (sub / "step-02-record.md").mkdir()
        self._check_sound_survives(
            root, CLS_STEP_RECORD, 2,
            "steps/step-02-record.md", "steps/sub/step-02-record.md",
            "unreadable", "Is a directory", broken_size=0)

    def test_f15_22_link_to_directory_duplicate_sound_record_reads(self):
        root = build_tree(base_case())
        sub = root / "steps" / "sub"
        sub.mkdir(parents=True)
        os.symlink(str(root / "steps"), str(sub / "step-02-record.md"))
        self._check_sound_survives(
            root, CLS_STEP_RECORD, 2,
            "steps/step-02-record.md", "steps/sub/step-02-record.md",
            "unreadable", "Is a directory", broken_size=0)

    def test_f15_22_directory_at_canonical_sound_duplicate_reads(self):
        root = build_tree(base_case())
        canonical = root / "steps" / "step-02-record.md"
        sound_text = canonical.read_text(encoding="utf-8")
        canonical.unlink()
        canonical.mkdir()
        sub = root / "steps" / "sub"
        sub.mkdir(parents=True)
        (sub / "step-02-record.md").write_text(sound_text,
                                               encoding="utf-8")
        self._check_sound_survives(
            root, CLS_STEP_RECORD, 2,
            "steps/sub/step-02-record.md", "steps/step-02-record.md",
            "unreadable", "Is a directory", broken_size=0)

    def test_f15_22_directory_duplicate_gate_record_f2_stands(self):
        root = build_tree(base_case())
        sub = root / "steps" / "sub"
        sub.mkdir(parents=True)
        (sub / "step-02-gate-record.md").mkdir()
        self._check_sound_survives(
            root, CLS_GATE_RECORD, 2,
            "steps/step-02-gate-record.md",
            "steps/sub/step-02-gate-record.md",
            "unreadable", "Is a directory", broken_size=0)
        result = run_tool(root)
        self.assertIn("plain approvals 3", row_block(result.stdout, "F-2"))
        self.assertIn("steps ruled on 3", row_block(result.stdout, "F-2"))

    def test_f15_22_malformed_duplicate_sound_record_reads(self):
        table = base_case()
        table["steps/sub/step-02-record.md"] = \
            b"\xff\xfe\x00 not utf8 \x80\x81"
        root = build_tree(table)
        self._check_sound_survives(
            root, CLS_STEP_RECORD, 2,
            "steps/step-02-record.md", "steps/sub/step-02-record.md",
            "malformed", "malformed")
        result = run_tool(root)
        self.assertIn("malformed", result.stdout.lower())

    def test_f15_22_over_limit_duplicate_sound_record_reads(self):
        table = base_case()
        table["steps/sub/step-02-record.md"] = b"x" * 1050018
        root = build_tree(table)
        self._check_sound_survives(
            root, CLS_STEP_RECORD, 2,
            "steps/step-02-record.md", "steps/sub/step-02-record.md",
            "over limit", "over limit", broken_size=1050018)
        result = run_tool(root)
        coverage = coverage_statement(result.stdout)
        self.assertIn("steps/sub/step-02-record.md", coverage)
        self.assertIn("1050018 bytes", coverage)

    # ------------------------------------------------------------ controls

    def test_f15_22_control_differing_readable_duplicates_still_merge(self):
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
        self.assertEqual(
            pieces[0].paths,
            ("copy/step-01-record.md", "steps/step-01-record.md"))
        self.assertIn("duplicate content disagreement",
                      pieces[0].not_read_reason)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("duplicate content disagreement", result.stdout)

    def test_f15_22_control_identical_readable_duplicates_still_merge(self):
        table = base_case()
        table["steps/sub/step-02-record.md"] = step_record(2)
        root = build_tree(table)
        result = self._check_rows_match_intact(root)
        self.assertNotIn("duplicate", result.stdout.lower())
        captured = capture(root)
        pieces = pieces_for(captured, CLS_STEP_RECORD, 2)
        self.assertEqual(len(pieces), 1, pieces)
        self.assertIsNotNone(pieces[0].text)
        self.assertEqual(
            pieces[0].paths,
            ("steps/step-02-record.md", "steps/sub/step-02-record.md"))


if __name__ == "__main__":
    unittest.main()
