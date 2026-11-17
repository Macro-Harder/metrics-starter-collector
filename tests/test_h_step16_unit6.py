"""Step 16 fix unit 6 tests: the run cost counts.

Pinning tests for register item R16-21 (Low) of Step 16 round 1,
finding U-06 of the use it stage (spin 1103), confirmed by spin
1106. The run cost line labels recognised piece counts as files
visited and entries visited, counts the walk itself never
reports, so the line misstates what was visited. On run (b) the
report states 980 files visited and 993 entries visited over a
tree holding 2,581 files as a user counts it, with no line
stating that the counts cover recognised pieces only or that any
folder is skipped; most of the gap is the 1,381 files under
design/.git, which the walk enumeration visits and the counts
omit. The governing passages are brief Section 5, the single
read component, the walk records files visited, files opened,
bytes read and entries visited as it goes, and the run cost line
data shape at D4R-27 and Section 5, carrying those four counts
in those words.

The cure these tests pin: the walk enumeration count and the
count of enumerated files the visited counts do not cover reach
the run cost composition, and where that second count stands
above zero the run cost line states both counts, in the form
Walk enumerated files: N and Files not counted: M, between the
Entries visited part and the Limit part, so the line reconciles
with the tree as a user counts it: files visited plus files not
counted stands equal to the files the walk enumerated, which
stand equal to the files standing in the tree. On a tree with
no enumerated file left uncounted, the line stands byte for
byte as it stands today, with no new part.

The exclusion kinds the walk performs today, enumerated from
_walk_entries and capture_read, and how this unit treats each:
an unrecognised file, the .git subtree files and plain notes
among them, is enumerated and stands in the files not counted
count; a second path to a file already counted, an alias link
or a link whose target an earlier link already reached, is
enumerated and stands in that count, its file counted once; a
file past the whole walk bound that no pattern recognises is
never entered and stands in that count, while a recognised
piece past the bound stands as a not visited piece and stays
counted in files visited, so it stands in neither count as
excluded; a link out of the tree at a recognised name stands as
a damaged piece and stays counted in files visited, so it is no
exclusion, while the same link at an unrecognised name is
enumerated and stands in the files not counted count; a
directory is enumerated as an entry and descended, never a
file, so it stands in no file count; a non regular entry is
enumerated and stands in no file count; and a subtree the walk
cannot list, or a linked directory it does not descend into, is
never enumerated at all, so no count can state its files, and
the walk note and coverage statement carry that failure in the
open, as they stand today. The last three kinds stand outside
the files reconciliation this item governs and are named here
and in the unit report, with the directory and non regular
entry kinds pinned by the last test of this module.
"""
import os

from tests.fixture_builder import (
    FixtureTestCase, capture_derive_render, gate_record,
    metrics_record, run_tool, step_record, tracked_tempdir)

METRICS_PATH = "wiki/wiki/synthesis/build-metrics-record.md"


def _base_files():
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
    files[METRICS_PATH] = metrics_record(
        body="Step table stands complete for the fixture steps.")
    return files


def _write_tree(files, holder_name="tree"):
    """Write one tree under a tracked temporary directory."""
    holder = tracked_tempdir("msc_step16_unit6_")
    root = holder / holder_name
    for rel in sorted(files):
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(files[rel], encoding="utf-8")
    return holder, root


def _line(report, prefix):
    """Return the one report line opening with the given prefix."""
    found = [ln for ln in report.splitlines()
             if ln.startswith(prefix)]
    return found[0] if len(found) == 1 else None


def _counted_bytes(root, files):
    """Bytes read on a full reading: the size of every base file."""
    return sum((root / rel).stat().st_size for rel in files)


def _files_in_tree(root):
    """The files standing in the tree, as a user counts them."""
    return sum(1 for path in root.rglob("*")
               if path.is_file() and not path.is_symlink())


class TestStep16Unit6(FixtureTestCase):

    def _run(self, files):
        holder, root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return root, result.stdout

    def test_r16_21_git_subtree_files_not_counted_stated(self):
        """R16-21 defect form: the .git files stand stated as not counted."""
        files = _base_files()
        files[".git/HEAD"] = "ref: refs/heads/main\n"
        files[".git/config"] = "[core]\nrepositoryformatversion = 0\n"
        files[".git/refs/heads/main"] = "0" * 40 + "\n"
        files[".git/objects/ab/cdef0123"] = "packed object bytes\n"
        root, report = self._run(files)
        self.assertEqual(_files_in_tree(root), 13)
        run_cost = _line(report, "Run cost: ")
        self.assertEqual(
            run_cost,
            "Run cost: Files visited: 9 | Files opened: 9 | Bytes "
            "read: %d | Entries visited: 9 | Walk enumerated "
            "files: 13 | Files not counted: 4 | Limit: no limit "
            "crossed | Reading: full"
            % _counted_bytes(root, _base_files()))
        visited = 9
        enumerated = 13
        not_counted = 4
        self.assertEqual(visited + not_counted, enumerated)
        self.assertEqual(enumerated, _files_in_tree(root))

    def test_r16_21_plain_unrecognised_files_not_counted_stated(self):
        """R16-21: plain unrecognised files stand stated as not counted."""
        files = _base_files()
        files["notes/plain-note.txt"] = "a plain note, no record\n"
        files["bulk/filler.txt"] = "bulk\n"
        root, report = self._run(files)
        self.assertEqual(_files_in_tree(root), 11)
        run_cost = _line(report, "Run cost: ")
        self.assertEqual(
            run_cost,
            "Run cost: Files visited: 9 | Files opened: 9 | Bytes "
            "read: %d | Entries visited: 9 | Walk enumerated "
            "files: 11 | Files not counted: 2 | Limit: no limit "
            "crossed | Reading: full"
            % _counted_bytes(root, _base_files()))

    def test_r16_21_control_no_excluded_files_line_unchanged(self):
        """Control: no file left uncounted, the line stands as today."""
        files = _base_files()
        root, report = self._run(files)
        self.assertEqual(_files_in_tree(root), 9)
        run_cost = _line(report, "Run cost: ")
        self.assertEqual(
            run_cost,
            "Run cost: Files visited: 9 | Files opened: 9 | Bytes "
            "read: %d | Entries visited: 9 | Limit: no limit "
            "crossed | Reading: full"
            % _counted_bytes(root, files))
        self.assertNotIn("not counted", report)
        self.assertNotIn("Walk enumerated", report)

    def test_r16_21_alias_path_to_counted_file_not_counted_stated(self):
        """R16-21: a second path to a counted file is stated once over."""
        files = _base_files()
        holder, root = _write_tree(files)
        os.symlink(str(root / "steps" / "step-01-record.md"),
                   str(root / "zz-alias.md"))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        run_cost = _line(result.stdout, "Run cost: ")
        self.assertEqual(
            run_cost,
            "Run cost: Files visited: 9 | Files opened: 9 | Bytes "
            "read: %d | Entries visited: 9 | Walk enumerated "
            "files: 10 | Files not counted: 1 | Limit: no limit "
            "crossed | Reading: full"
            % _counted_bytes(root, files))

    def test_r16_21_link_outside_tree_recognised_piece_counted(self):
        """Kind control: an outside link at a record name stays counted."""
        files = _base_files()
        holder, root = _write_tree(files)
        outside = holder / "outside-step.md"
        outside.write_text(step_record(9), encoding="utf-8")
        os.symlink(str(outside),
                   str(root / "steps" / "step-09-record.md"))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        run_cost = _line(result.stdout, "Run cost: ")
        self.assertIsNotNone(run_cost)
        self.assertIn("Files visited: 10", run_cost)
        self.assertIn("Entries visited: 10", run_cost)
        self.assertNotIn("Files not counted", run_cost)
        self.assertNotIn("Walk enumerated", run_cost)

    def test_r16_21_walk_bound_unrecognised_files_not_counted_stated(self):
        """R16-21: files past the walk bound stand stated as not counted."""
        holder = tracked_tempdir("msc_step16_unit6_")
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

    def test_r16_21_non_regular_entry_and_directory_no_file_count(self):
        """Kind control: a pipe and a directory stand in no file count."""
        files = _base_files()
        holder, root = _write_tree(files)
        os.mkfifo(str(root / "pipe-entry"))
        (root / "empty-dir").mkdir()
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        self.assertEqual(_files_in_tree(root), 9)
        run_cost = _line(result.stdout, "Run cost: ")
        self.assertEqual(
            run_cost,
            "Run cost: Files visited: 9 | Files opened: 9 | Bytes "
            "read: %d | Entries visited: 9 | Limit: no limit "
            "crossed | Reading: full"
            % _counted_bytes(root, files))
        self.assertNotIn("Files not counted", run_cost)


if __name__ == "__main__":
    import unittest
    unittest.main()
