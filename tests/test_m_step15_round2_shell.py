"""Step 15 fix round 2 tests: shell and identity cluster.

Each case pins one fix round 2 finding in the shell territory:
F15-13, a damaged piece at a duplicate identity path poisoning the
sound piece at that identity; F15-17, the destination refusal
bypassed through a symlink alias of the root itself; F15-18, a link
at a recognised name to a FIFO inside the tree surfaced with a false
dangling reason; and F15-19, a dangling link at a near match name
vanishing from the near match listing. Control cases pin the
behaviour that must not move: destinations that must stay refused,
legitimate outside destinations that must still be delivered, the
dangling reason where the target truly does not stand, and the
silence for a dangling link at a wholly unrecognised name.
"""
import os
import unittest
from pathlib import Path

from metrics_starter_collector.derivation_core import CLS_STEP_RECORD
from tests.fixture_builder import (FixtureTestCase, base_case, build_tree,
                                     coverage_statement, manifest,
                                     piece_entry_for, row_block, run_tool)


def capture(root):
    from metrics_starter_collector.shell_reader import capture_read
    return capture_read(root)


def step_record_pieces(captured, step):
    return [p for p in captured.pieces
            if p.record_class == CLS_STEP_RECORD and p.step == step]


class TestStep15Round2Shell(FixtureTestCase):

    # ------------------------------------------------------------ F15-13

    def _intact_rows(self):
        intact = build_tree(base_case())
        result = run_tool(intact)
        self.assertEqual(result.returncode, 0, result.stderr)
        return (row_block(result.stdout, "E-1"),
                row_block(result.stdout, "E-2"))

    def _check_sound_survives(self, root, step, damage_words):
        e1_intact, e2_intact = self._intact_rows()
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(row_block(result.stdout, "E-1"), e1_intact)
        self.assertEqual(row_block(result.stdout, "E-2"), e2_intact)
        self.assertIn("Step %d" % step, row_block(result.stdout, "E-1"))
        self.assertNotIn("duplicate", result.stdout.lower())
        captured = capture(root)
        pieces = step_record_pieces(captured, step)
        sound = [p for p in pieces if p.text is not None]
        broken = [p for p in pieces if p.text is None]
        self.assertEqual(len(sound), 1, pieces)
        self.assertEqual(len(broken), 1, pieces)
        self.assertEqual(sound[0].paths,
                         ("steps/step-%02d-record.md" % step,))
        self.assertEqual(broken[0].paths,
                         ("steps/sub/step-%02d-record.md" % step,))
        self.assertIn(damage_words, broken[0].not_read_reason)
        self.assertNotIn("duplicate", broken[0].not_read_reason)
        coverage = coverage_statement(result.stdout)
        self.assertIn("steps/sub/step-%02d-record.md" % step, coverage)
        self.assertIn(damage_words, coverage)

    def test_f15_13_dangling_duplicate_identity_sound_record_reads(self):
        root = build_tree(base_case())
        sub = root / "steps" / "sub"
        sub.mkdir(parents=True)
        os.symlink("gone.md", str(sub / "step-02-record.md"))
        self._check_sound_survives(root, 2, "dangling link")

    def test_f15_13_fifo_duplicate_identity_sound_record_reads(self):
        root = build_tree(base_case())
        sub = root / "steps" / "sub"
        sub.mkdir(parents=True)
        os.mkfifo(str(sub / "step-02-record.md"))
        self._check_sound_survives(root, 2, "not a regular file")

    def test_f15_13_loop_duplicate_identity_sound_record_reads(self):
        root = build_tree(base_case())
        sub = root / "steps" / "sub"
        sub.mkdir(parents=True)
        link = sub / "step-03-record.md"
        os.symlink(str(link), str(link))
        self._check_sound_survives(root, 3, "symlink loop")

    # ------------------------------------------------------------ F15-17

    def test_f15_17_root_alias_escape_link_destination_refused(self):
        root = build_tree(base_case())
        outside = Path(root).parent / "escape-target-report.md"
        self.assertFalse(outside.exists())
        os.symlink(str(outside), str(root / "escape-link.md"))
        alias = Path(root).parent / "root-alias"
        os.symlink(str(root), str(alias))
        before = manifest(root)
        result = run_tool(root, extra=("--report",
                                       str(alias / "escape-link.md")))
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertFalse(outside.exists())
        self.assertEqual(manifest(root), before)

    def test_f15_17_root_alias_new_file_destination_refused(self):
        root = build_tree(base_case())
        alias = Path(root).parent / "root-alias"
        os.symlink(str(root), str(alias))
        before = manifest(root)
        result = run_tool(root, extra=("--report",
                                       str(alias / "new-report.md")))
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertFalse((root / "new-report.md").exists())
        self.assertEqual(manifest(root), before)

    def test_f15_17_outside_alias_destination_delivered(self):
        root = build_tree(base_case())
        outside_dir = Path(root).parent / "outside-dir"
        outside_dir.mkdir()
        alias = Path(root).parent / "outside-alias"
        os.symlink(str(outside_dir), str(alias))
        dest = alias / "delivered-report.md"
        result = run_tool(root, extra=("--report", str(dest)))
        self.assertEqual(result.returncode, 0, result.stderr)
        landed = outside_dir / "delivered-report.md"
        self.assertTrue(landed.is_file())
        self.assertIn("Metrics starter set report",
                      landed.read_text(encoding="utf-8"))

    def test_f15_17_plain_outside_destination_delivered(self):
        root = build_tree(base_case())
        dest = Path(root).parent / "plain-report.md"
        result = run_tool(root, extra=("--report", str(dest)))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(dest.is_file())
        self.assertIn("Metrics starter set report",
                      dest.read_text(encoding="utf-8"))

    # ------------------------------------------------------------ F15-18

    def test_f15_18_link_to_fifo_inside_tree_true_reason(self):
        root = build_tree(base_case())
        fifo = root / "steps" / "real-fifo"
        os.mkfifo(str(fifo))
        os.symlink(str(fifo), str(root / "steps" / "step-07-record.md"))
        captured = capture(root)
        pieces = step_record_pieces(captured, 7)
        self.assertEqual(len(pieces), 1, pieces)
        self.assertIsNone(pieces[0].text)
        self.assertIn("not a regular file", pieces[0].not_read_reason)
        self.assertNotIn("dangling", pieces[0].not_read_reason)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        coverage = coverage_statement(result.stdout)
        self.assertIn("steps/step-07-record.md", coverage)
        self.assertIn("not a regular file", coverage)

    def test_f15_18_control_dangling_link_reason_stands(self):
        root = build_tree(base_case())
        target = root / "steps" / "step-02-record.md"
        target.unlink()
        os.symlink("gone.md", str(target))
        captured = capture(root)
        pieces = step_record_pieces(captured, 2)
        self.assertEqual(len(pieces), 1, pieces)
        self.assertIsNone(pieces[0].text)
        self.assertIn("dangling link", pieces[0].not_read_reason)
        self.assertIn("the link target does not stand",
                      pieces[0].not_read_reason)

    # ------------------------------------------------------------ F15-19

    def test_f15_19_dangling_near_match_inside_target_listed(self):
        root = build_tree(base_case())
        os.symlink("gone.md", str(root / "steps" / "step-02-record.txt"))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = piece_entry_for(result.stdout, "step-02-record.txt")
        self.assertTrue(entry)
        self.assertIn("unrecognised near match", entry)
        self.assertIn("steps/step-02-record.md", entry)

    def test_f15_19_dangling_near_match_outside_target_listed(self):
        root = build_tree(base_case())
        missing = Path(root).parent / "gone-outside.md"
        os.symlink(str(missing),
                   str(root / "steps" / "step-02-record.txt"))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = piece_entry_for(result.stdout, "step-02-record.txt")
        self.assertTrue(entry)
        self.assertIn("unrecognised near match", entry)
        self.assertIn("steps/step-02-record.md", entry)

    def test_f15_19_control_dangling_unrecognised_name_not_listed(self):
        root = build_tree(base_case())
        os.symlink("gone.md", str(root / "random-junk.md"))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("random-junk.md", result.stdout)


if __name__ == "__main__":
    unittest.main()
