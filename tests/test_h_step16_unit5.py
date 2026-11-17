"""Step 16 fix unit 5 tests: delivery atomicity.

Pinning tests for register item R16-07 (Medium) of Step 16 round 1,
finding S-01 of the correctness paper (spin 1106). Report delivery
is not atomic: deliver_report in shell_reader.py opens the
destination in place with os.O_TRUNC and writes the finished text
to that handle, so a write failure after the open destroys a prior
file at the destination and leaves an empty file in its place, at
an exit outside the contract set. The governing form stands in the
deliver_report docstring itself: a delivery failure leaves no
partial file and leaves a prior file at the destination as it
stood.

The defect case is forced at the file object level, not by the
ulimit form spin 1106 used on the bench: the test replaces os.write
for the duration of one deliver_report call, so the write fails
after the destination has been opened, which is the exact point
the defect lives at. The ulimit form is not portable into a suite
test: it depends on the shell that launches the test process and
on signal handling in the test runner, while the file object form
forces the same failure, at the same locus, on every machine the
suite runs on, and asserts the same governed outcome: the prior
report stands byte for byte intact and no partial or empty file
stands in its place.

The held refusal controls stand beside the defect case: spin 1106
item 7 cases A, B and C, and spin 1107 Attack 6, the full delivery
refusal sweep. Every one of those destinations fails at or before
the open, each at exit 2 in the governed error form, and every one
must keep failing the same way after the cure. A successful
delivery control stands last: a normal --report delivery writes
the full report, byte identical to the stdout form of the same
run, at exit 0.
"""
import hashlib
import os
import stat
from unittest import mock

from metrics_starter_collector.shell_reader import (
    UsageError, deliver_report)
from tests.fixture_builder import (
    FixtureTestCase, build_case, clean_files, run_tool,
    tracked_tempdir)

PRIOR = b"PRIOR CONTENT\n"


def _tree(holder):
    return build_case(
        {"name": "u5-tree", "features": (), "files": clean_files()},
        holder)


def _outside(holder):
    outside = holder / "outside"
    outside.mkdir(parents=True, exist_ok=True)
    return outside


class TestStep16Unit5(FixtureTestCase):

    # The defect case, R16-07, forced at the file object level.

    def test_r16_07_write_failure_after_open_prior_intact(self):
        """S-01 defect form: a failed write leaves the prior file."""
        holder = tracked_tempdir("msc_step16_unit5_")
        root = _tree(holder)
        dest_dir = _outside(holder)
        dest = dest_dir / "report.txt"
        dest.write_bytes(PRIOR)
        with mock.patch(
                "os.write",
                side_effect=OSError(28, "No space left on device")):
            with self.assertRaises(UsageError):
                deliver_report("finished report text\n", str(root),
                               str(dest))
        self.assertEqual(dest.read_bytes(), PRIOR)
        self.assertEqual(sorted(os.listdir(str(dest_dir))),
                         ["report.txt"])

    def test_r16_07_write_failure_after_open_no_prior_no_partial(self):
        """S-01 defect form, no prior file: no partial file stands."""
        holder = tracked_tempdir("msc_step16_unit5_")
        root = _tree(holder)
        dest_dir = _outside(holder)
        dest = dest_dir / "report.txt"
        with mock.patch(
                "os.write",
                side_effect=OSError(28, "No space left on device")):
            with self.assertRaises(UsageError):
                deliver_report("finished report text\n", str(root),
                               str(dest))
        self.assertFalse(dest.exists())
        self.assertEqual(sorted(os.listdir(str(dest_dir))), [])

    def test_r16_07_short_write_after_open_prior_intact(self):
        """S-01 defect form, short write: the prior file stands."""
        holder = tracked_tempdir("msc_step16_unit5_")
        root = _tree(holder)
        dest_dir = _outside(holder)
        dest = dest_dir / "report.txt"
        dest.write_bytes(PRIOR)

        def short_write(handle, data):
            return len(data) - 1

        with mock.patch("os.write", side_effect=short_write):
            with self.assertRaises(UsageError):
                deliver_report("finished report text\n", str(root),
                               str(dest))
        self.assertEqual(dest.read_bytes(), PRIOR)
        self.assertEqual(sorted(os.listdir(str(dest_dir))),
                         ["report.txt"])

    # Held refusal controls, spin 1106 item 7, cases A, B and C.

    def test_r16_held_case_a_destination_in_read_only_directory(self):
        """Item 7 case A: new file in a read only directory, exit 2."""
        holder = tracked_tempdir("msc_step16_unit5_")
        root = _tree(holder)
        ro_dir = _outside(holder) / "ro"
        ro_dir.mkdir()
        (ro_dir / "prior.txt").write_bytes(PRIOR)
        os.chmod(str(ro_dir), 0o555)
        try:
            dest = ro_dir / "new-report.txt"
            result = run_tool(root, ("--report", str(dest)))
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertTrue(result.stderr.startswith(
                "error: deliver the report: destination %s: "
                % (dest,)), result.stderr[:300])
            self.assertFalse(dest.exists())
            self.assertEqual(sorted(os.listdir(str(ro_dir))),
                             ["prior.txt"])
        finally:
            os.chmod(str(ro_dir), 0o755)

    def test_r16_held_case_b_prior_read_only_file_left_as_it_stood(self):
        """Item 7 case B: a prior read only file stands, exit 2."""
        holder = tracked_tempdir("msc_step16_unit5_")
        root = _tree(holder)
        ro_dir = _outside(holder) / "ro"
        ro_dir.mkdir()
        dest = ro_dir / "report.txt"
        dest.write_bytes(b"PRIOR CONTENT")
        os.chmod(str(dest), 0o444)
        os.chmod(str(ro_dir), 0o555)
        try:
            result = run_tool(root, ("--report", str(dest)))
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertTrue(result.stderr.startswith(
                "error: deliver the report: destination %s: "
                % (dest,)), result.stderr[:300])
            self.assertEqual(dest.read_bytes(), b"PRIOR CONTENT")
        finally:
            os.chmod(str(ro_dir), 0o755)
            os.chmod(str(dest), 0o644)

    def test_r16_held_case_c_parent_directory_does_not_stand(self):
        """Item 7 case C: a missing parent directory, exit 2."""
        holder = tracked_tempdir("msc_step16_unit5_")
        root = _tree(holder)
        dest = _outside(holder) / "no-such-dir" / "report.txt"
        result = run_tool(root, ("--report", str(dest)))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn(
            "the parent directory does not stand", result.stderr)
        self.assertFalse(dest.parent.exists())
        self.assertFalse(dest.exists())

    # Held refusal controls, spin 1107 Attack 6, the refusal sweep.

    def test_r16_held_attack6_destination_under_proc(self):
        """Attack 6: a destination under /proc, exit 2, no file."""
        holder = tracked_tempdir("msc_step16_unit5_")
        root = _tree(holder)
        dest = "/proc/msc-unit5-report.txt"
        result = run_tool(root, ("--report", dest))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("deliver the report: destination %s: "
                      % (dest,), result.stderr)
        self.assertFalse(os.path.exists(dest))

    def test_r16_held_attack6_destination_under_sys_kernel(self):
        """Attack 6: a destination under /sys/kernel, exit 2."""
        holder = tracked_tempdir("msc_step16_unit5_")
        root = _tree(holder)
        dest = "/sys/kernel/msc-unit5-report.txt"
        result = run_tool(root, ("--report", dest))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("deliver the report: destination %s: "
                      % (dest,), result.stderr)
        self.assertFalse(os.path.exists(dest))

    def test_r16_held_attack6_destination_inside_tree_plain(self):
        """Attack 6: a destination inside the tree, exit 2."""
        holder = tracked_tempdir("msc_step16_unit5_")
        root = _tree(holder)
        dest = root / "report.txt"
        result = run_tool(root, ("--report", str(dest)))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("lies inside the tree read", result.stderr)
        self.assertFalse(dest.exists())

    def test_r16_held_attack6_link_outside_pointing_inside(self):
        """Attack 6: a link outside pointing inside, exit 2."""
        holder = tracked_tempdir("msc_step16_unit5_")
        root = _tree(holder)
        target = root / "inside-target.txt"
        link = _outside(holder) / "link-in.txt"
        os.symlink(str(target), str(link))
        result = run_tool(root, ("--report", str(link)))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertFalse(target.exists())

    def test_r16_held_attack6_destination_is_a_feeder_file(self):
        """Attack 6: the tree own PATH-LEDGER.md, exit 2, unchanged."""
        holder = tracked_tempdir("msc_step16_unit5_")
        root = _tree(holder)
        feeder = root / "PATH-LEDGER.md"
        before = hashlib.sha256(feeder.read_bytes()).hexdigest()
        result = run_tool(root, ("--report", str(feeder)))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        after = hashlib.sha256(feeder.read_bytes()).hexdigest()
        self.assertEqual(after, before)

    def test_r16_held_attack6_parent_segments_resolving_inside(self):
        """Attack 6: parent segments resolving inside, exit 2."""
        holder = tracked_tempdir("msc_step16_unit5_")
        root = _tree(holder)
        sibling = _outside(holder)
        dest = str(sibling / ".." / root.name / "report.txt")
        result = run_tool(root, ("--report", dest))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertFalse((root / "report.txt").exists())

    def test_r16_held_attack6_destination_is_the_root_itself(self):
        """Attack 6: the root itself as destination, exit 2."""
        holder = tracked_tempdir("msc_step16_unit5_")
        root = _tree(holder)
        result = run_tool(root, ("--report", str(root)))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("deliver the report", result.stderr)

    def test_r16_held_attack6_link_inside_pointing_outside(self):
        """Attack 6: a link inside pointing outside, exit 2."""
        holder = tracked_tempdir("msc_step16_unit5_")
        root = _tree(holder)
        target = _outside(holder) / "outside-target.txt"
        link = root / "link-out.txt"
        os.symlink(str(target), str(link))
        result = run_tool(root, ("--report", str(link)))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertFalse(target.exists())

    def test_r16_held_attack6_parent_link_to_the_tree(self):
        """Attack 6: a destination through a parent link, exit 2."""
        holder = tracked_tempdir("msc_step16_unit5_")
        root = _tree(holder)
        parent_link = _outside(holder) / "tree-link"
        os.symlink(str(root), str(parent_link))
        dest = parent_link / "report.txt"
        result = run_tool(root, ("--report", str(dest)))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertFalse((root / "report.txt").exists())

    def test_r16_held_attack6_named_pipe_destination(self):
        """Attack 6: a named pipe outside the tree, exit 2, no block."""
        holder = tracked_tempdir("msc_step16_unit5_")
        root = _tree(holder)
        dest = _outside(holder) / "report-pipe"
        os.mkfifo(str(dest))
        result = run_tool(root, ("--report", str(dest)))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("does not stand as a regular file",
                      result.stderr)
        self.assertTrue(stat.S_ISFIFO(os.stat(str(dest)).st_mode))

    # The successful delivery control.

    def test_r16_control_successful_delivery_matches_stdout(self):
        """Control: a normal delivery, exit 0, bytes as on stdout."""
        holder = tracked_tempdir("msc_step16_unit5_")
        root = _tree(holder)
        dest = _outside(holder) / "report.txt"
        plain = run_tool(root)
        self.assertEqual(plain.returncode, 0, plain.stderr[:300])
        delivered = run_tool(root, ("--report", str(dest)))
        self.assertEqual(delivered.returncode, 0,
                         delivered.stderr[:300])
        self.assertEqual(delivered.stdout, "")
        self.assertEqual(dest.read_bytes(),
                         plain.stdout.encode("utf-8"))


if __name__ == "__main__":
    import unittest
    unittest.main()
