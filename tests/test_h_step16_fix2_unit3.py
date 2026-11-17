"""Step 16 fix pass 2 unit 3 tests: walk bound directory counting.

Pinning tests for register item R16-2-03 (Low) of Step 16 round 2,
finding C2-01 of spin 1122, a new item of the R16-21 genus. On a
walk bound cut tree, directory entries past the bound inside an
already listed recognised directory are formed as not visited
pieces and counted as files visited: spin 1122 built the base
tree of ten files plus 10,050 empty directories under audit/ and
the capture held 66 pieces and a counted pieces total of 66
against 10 files standing in the tree and a walk files total of
10, 56 of the pieces being directories under audit/ past the
bound, each formed as an audit paper piece at 0 bytes in the over
limit state. The run cost line read Files visited: 66 with no
Walk enumerated or Files not counted part, because the Unit 6
reconciliation difference, enumerated files less counted pieces,
stands negative on this form and no reconciliation statement
appears. The reconciliation the R16-21 cure states, counted plus
not counted equals enumerated equals the files in the tree,
therefore fails on this form in the opposite direction from
round 1 run (b): the visited count overstates the files in the
tree by the number of past bound directory entries classed as
pieces.

The cure these tests pin: an entry that does not stand as a file
is not formed as a counted piece past the walk bound and does
not enter the Files visited count, a directory is not a file in
any count the report states, and on a form where counted pieces
would exceed the walk enumerated files the run cost line states
the position rather than standing silent, in the same two parts
the Unit 6 cure states on the positive form, Walk enumerated
files and Files not counted, the second standing negative, so
the figures reconcile in the open on the negative difference
form as on the positive.

Held controls stand pinned beside the defect forms: spin 1122
own control, the same directory form inside the bound, one
directory at audit/some-paper inside every bound, no piece at
all and the run cost line unchanged; the Unit 6 charged forms,
a .git exclusion tree, a plain unrecognised file tree and the
walk bound cut on files, each reconciling exactly as Unit 6
left them, byte for byte in the run cost line; spin 1122 neutral
walk bound construction, 10,050 empty directories under bulk/,
whose counts closed exactly at 10 pieces, 10 counted and 10
walk files; and the walk bound ledger rows of spin 1122 section
6, E-3, B-2 and E-4 present but not derivable naming the whole
walk bound, which no counting cure may disturb, pinned byte for
byte through the fix pass 2 Unit 1 module constants.
"""
import os

from tests.fixture_builder import (
    FixtureTestCase, capture_derive_render, row_block, run_tool,
    tracked_tempdir)
from tests.test_h_step16_fix2_unit1 import (
    LEDGER_B2_WALK, LEDGER_E3_WALK, LEDGER_E4_WALK, LEDGER_FULL,
    LEDGER_PATH, _base_files as _unit1_base_files, _roster_files,
    _write_tree as _unit1_write_tree)
from tests.test_h_step16_unit6 import (
    _base_files, _counted_bytes, _files_in_tree, _line,
    _write_tree)

DIR_COUNT = 10050


def _ten_file_files():
    """The ten file base of spin 1122: the Unit 6 base plus a ledger."""
    files = _base_files()
    files[LEDGER_PATH] = LEDGER_FULL
    return files


def _add_dirs(root, parent, count, prefix="d"):
    """Create count empty directories under root/parent."""
    base = root / parent
    base.mkdir(parents=True, exist_ok=True)
    for index in range(count):
        (base / ("%s%05d" % (prefix, index))).mkdir()


def _piece_lines(report):
    """The piece inventory lines of a report, in report order."""
    return [ln for ln in report.splitlines()
            if ln.startswith("Piece ") and " | " in ln]


class TestStep16Fix2Unit3(FixtureTestCase):

    def _run_ten(self, extra_dirs=None):
        """Run the ten file base, with empty directories added."""
        holder, root = _write_tree(_ten_file_files())
        if extra_dirs is not None:
            parent, count = extra_dirs
            _add_dirs(root, parent, count)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return root, result.stdout

    # The defect forms, spin 1122 section 3

    def test_r16_2_03_dirs_past_bound_not_pieces_not_counted(self):
        """C2-01 defect: past bound directories form no piece at all."""
        root, report = self._run_ten(extra_dirs=("audit", DIR_COUNT))
        self.assertEqual(_files_in_tree(root), 10)
        pieces = _piece_lines(report)
        self.assertEqual(len(pieces), 10)
        self.assertFalse(
            any(ln.startswith("Piece audit/") for ln in pieces),
            "a directory under audit/ stands as a piece")
        run_cost = _line(report, "Run cost: ")
        self.assertIsNotNone(run_cost)
        self.assertIn("Files visited: 10", run_cost)
        self.assertIn("Entries visited: 10", run_cost)
        self.assertIn("Files opened: 2", run_cost)
        self.assertNotIn("Files visited: 66", run_cost)
        self.assertIn("whole walk bound", run_cost)
        self.assertIn("Reading: partial", run_cost)

    def test_r16_2_03_capture_counts_reconcile_on_defect_form(self):
        """C2-01 defect: the capture counts reconcile after the cure."""
        holder, root = _write_tree(_ten_file_files())
        _add_dirs(root, "audit", DIR_COUNT)
        capture_fn, derive_fn, render_fn = capture_derive_render(
            self, root)
        captured = capture_fn(root)
        self.assertEqual(len(captured.pieces), 10)
        self.assertEqual(captured.tree_files, 10)
        self.assertEqual(captured.walk_files_total, 10)
        self.assertFalse(any(
            path.startswith("audit/")
            for piece in captured.pieces for path in piece.paths))
        report = render_fn(derive_fn(captured))
        run_cost = _line(report, "Run cost: ")
        self.assertIsNotNone(run_cost)
        self.assertIn("Files visited: 10", run_cost)
        visited = captured.tree_files
        enumerated = captured.walk_files_total
        self.assertEqual(visited, enumerated)
        self.assertEqual(enumerated, _files_in_tree(root))

    def test_r16_2_03_negative_difference_is_stated(self):
        """C2-01 run cost limb: a negative difference stands stated.

        A directory standing at a recognised file name path inside
        the bound stands as that damaged piece under the standing
        capture exception, so the counted pieces stand at 11
        against 10 enumerated files. The run cost line states the
        position in the Unit 6 parts, with the not counted figure
        standing negative, rather than standing silent.
        """
        holder, root = _write_tree(_ten_file_files())
        (root / "steps" / "step-09-record.md").mkdir(parents=True)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        self.assertEqual(_files_in_tree(root), 10)
        run_cost = _line(result.stdout, "Run cost: ")
        self.assertIsNotNone(run_cost)
        self.assertIn("Files visited: 11", run_cost)
        self.assertIn("Walk enumerated files: 10", run_cost)
        self.assertIn("Files not counted: -1", run_cost)
        self.assertEqual(11 + (-1), 10)

    # Held controls

    def test_r16_2_held_dir_inside_bound_no_piece_line_unchanged(self):
        """Held control: spin 1122 control, the directory inside bound."""
        holder, root = _write_tree(_ten_file_files())
        (root / "audit" / "some-paper").mkdir(parents=True)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        report = result.stdout
        self.assertEqual(len(_piece_lines(report)), 10)
        self.assertFalse(any(
            ln.startswith("Piece audit/") for ln in _piece_lines(report)))
        base_root, base_report = self._run_ten()
        self.assertEqual(_line(report, "Run cost: "),
                         _line(base_report, "Run cost: "))
        self.assertNotIn("Files not counted",
                         _line(report, "Run cost: "))

    def test_r16_2_held_git_form_byte_for_byte(self):
        """Held control: the Unit 6 .git charged form, unchanged."""
        files = _base_files()
        files[".git/HEAD"] = "ref: refs/heads/main\n"
        files[".git/config"] = "[core]\nrepositoryformatversion = 0\n"
        files[".git/refs/heads/main"] = "0" * 40 + "\n"
        files[".git/objects/ab/cdef0123"] = "packed object bytes\n"
        holder, root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        run_cost = _line(result.stdout, "Run cost: ")
        self.assertEqual(
            run_cost,
            "Run cost: Files visited: 9 | Files opened: 9 | Bytes "
            "read: %d | Entries visited: 9 | Walk enumerated "
            "files: 13 | Files not counted: 4 | Limit: no limit "
            "crossed | Reading: full"
            % _counted_bytes(root, _base_files()))

    def test_r16_2_held_plain_unrecognised_byte_for_byte(self):
        """Held control: the Unit 6 plain unrecognised form, unchanged."""
        files = _base_files()
        files["notes/plain-note.txt"] = "a plain note, no record\n"
        files["bulk/filler.txt"] = "bulk\n"
        holder, root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        run_cost = _line(result.stdout, "Run cost: ")
        self.assertEqual(
            run_cost,
            "Run cost: Files visited: 9 | Files opened: 9 | Bytes "
            "read: %d | Entries visited: 9 | Walk enumerated "
            "files: 11 | Files not counted: 2 | Limit: no limit "
            "crossed | Reading: full"
            % _counted_bytes(root, _base_files()))

    def test_r16_2_held_walk_bound_cut_on_files(self):
        """Held control: the Unit 6 walk bound cut on files, unchanged."""
        holder = tracked_tempdir("msc_step16_fix2_unit3_")
        root = holder / "bound-tree"
        root.mkdir(parents=True)
        (root / "PATH-LEDGER.md").write_text(
            "# Path ledger\n\nSteps stated: 1.\n\n"
            "## Transitions\n\n"
            "Step 1 IN PROGRESS 2026-11-01 09:00, closed "
            "2026-11-01 17:00.\n", encoding="utf-8")
        for number in range(10):
            (root / ("z-filler-%02d.txt" % number)).write_bytes(b"")
        capture_fn, derive_fn, render_fn = capture_derive_render(
            self, root)
        import metrics_starter_collector.shell_reader as shell
        standing = shell.WALK_BOUND
        shell.WALK_BOUND = 5
        try:
            captured = capture_fn(root)
            report = render_fn(derive_fn(captured))
        finally:
            shell.WALK_BOUND = standing
        run_cost = _line(report, "Run cost: ")
        self.assertIsNotNone(run_cost)
        self.assertIn("Files visited: 1", run_cost)
        self.assertIn("Walk enumerated files: 11", run_cost)
        self.assertIn("Files not counted: 10", run_cost)
        self.assertIn("whole walk bound", run_cost)
        self.assertIn("Reading: partial", run_cost)

    def test_r16_2_held_neutral_walk_bound_counts_close(self):
        """Held control: spin 1122 neutral walk bound construction."""
        holder, root = _write_tree(_ten_file_files())
        _add_dirs(root, "bulk", DIR_COUNT)
        capture_fn, derive_fn, render_fn = capture_derive_render(
            self, root)
        captured = capture_fn(root)
        self.assertEqual(len(captured.pieces), 10)
        self.assertEqual(captured.tree_files, 10)
        self.assertEqual(captured.walk_files_total, 10)
        self.assertEqual(captured.walk_entries_total, 10066)
        report = render_fn(derive_fn(captured))
        opened_bytes = sum(
            (root / rel).stat().st_size
            for rel in ("PATH-LEDGER.md", "TIER-RECORD.md"))
        run_cost = _line(report, "Run cost: ")
        self.assertEqual(
            run_cost,
            "Run cost: Files visited: 10 | Files opened: 2 | Bytes "
            "read: %d | Entries visited: 10 | Limit: whole walk "
            "bound 10000 entries | Reading: partial" % opened_bytes)

    def test_r16_2_held_walk_bound_ledger_rows_byte_for_byte(self):
        """Held control: the spin 1122 section 6 walk bound ledger rows."""
        files = _unit1_base_files()
        files.update(_roster_files())
        files[LEDGER_PATH] = LEDGER_FULL
        root = _unit1_write_tree(files)
        _add_dirs(root, "audit", DIR_COUNT)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        report = result.stdout
        self.assertEqual(row_block(report, "E-3"), LEDGER_E3_WALK)
        self.assertEqual(row_block(report, "E-4"), LEDGER_E4_WALK)
        self.assertEqual(row_block(report, "B-2"), LEDGER_B2_WALK)


if __name__ == "__main__":
    import unittest
    unittest.main()
