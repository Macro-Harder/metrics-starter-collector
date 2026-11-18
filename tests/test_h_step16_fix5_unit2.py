"""Step 16 fix pass 5 unit 2 tests: the F-2 unit.

Pinning tests for register item R16-5-02 (High, C5-05) of
Step 16 round 5. The governing rule of the pass, in its
extended form: a piece not read in full, for whatever
reason, is not read. The defect: gate records for Steps 1
and 3 read in full carrying Go, a Step 2 gate ruling read
in full carrying Go, beside the Step 2 gate record carrying
Hold in its file bytes and padded over the file limit,
standing unread. F-2 stood present at 3 of 3 approved, and
no word on the row named the Step 2 gate record, its
limit, or its state. The both read control, the same tree
with the Step 2 gate record read in full, stands present
but not derivable on the stated disagreement between that
gate record and that ruling: the unread state suppresses a
disagreement the row itself treats as blocking, and lets a
rate figure stand that the read tree denies. The gate
record stands first in the source order the gate outcome
reading sorts by path, so the instance figure rests on a
set whose first member was never read. Locus:
derivation_core.py, _derive_f2, whose unread gate branch
fires only where the instance carries no ruling outcome
and no named closure form, so an instance carrying an
outcome from a second counted source never consults the
unread state of its first source.

Three defect forms stand pinned: the C5-05 construction
on the file limit route; the same construction with the
Step 2 gate record damaged by a TRUNCATED marker; and the
same construction with the Step 2 gate record standing as
invalid UTF-8 bytes. Held controls stand pinned beside
them: the both read disagreement control; the same first
source position with the second counted source carrying a
closing state alone and no outcome, which already stands
cured because the first closure state reads from the
first counted source, so the unread branch of fix pass 4
Unit 5 fires on it; the cured no outcome position of fix
pass 4 Unit 5, one unread gate between two read gates
carrying outcomes; the breaker held
neighbours of this round, a gate ruling carrying No Go
read and truncated alike beside a counted gate record
carrying Go, withholding nothing the read piece supplies,
and a gate adjudication truncated beside read gates,
adjudications standing as evidence only and never as
counted sources; the all read Go control byte for byte;
and the exact limit control, the Step 2 gate record at
exactly 1,000,000 bytes read in full beside its ruling.

Trees are written through the Unit 1 module helpers of fix
pass 1, because the constructions turn on exact byte
counts. The product is invoked through run_tool, which
runs the module entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, gate_record, gate_ruling,
    row_block, run_tool)
from tests.test_h_step16_fix3_unit1 import _clean_files
from tests.test_h_step16_fix4_unit5 import GO_READ_F2
from tests.test_h_step16_unit1 import _padded, _write_tree

GO_EXTRA = "First ruling outcome: Go."
HOLD_EXTRA = "First ruling outcome: Hold."
RECORD_2 = "steps/step-02-gate-record.md"
RULING_2 = "steps/step-02-gate-ruling.md"
MALFORMED_RECORD = b"\xff\xfe\xfd gate record, not valid text\n"


def _go_files():
    files = _clean_files()
    for n in (1, 2, 3):
        files["steps/step-%02d-gate-record.md" % n] = gate_record(
            n, extra=GO_EXTRA)
    return files


def _c5_05_files(record_2):
    files = _go_files()
    files[RECORD_2] = record_2
    files[RULING_2] = gate_ruling(2, extra=GO_EXTRA)
    return files


class TestStep16Fix5Unit2(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    def _assert_blocked(self, report, bound_word):
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present but not derivable", "F-2")
        self.assertIn(RECORD_2, f2)
        self.assertIn(bound_word, f2)
        self.assertNotIn("first-time approval rate:", f2)
        self.assertNotIn("3 of 3 approved", f2)
        return f2

    # ------------------------------------------------------
    # Defect forms, R16-5-02
    # ------------------------------------------------------

    def test_r16_5_02_record_over_limit_ruling_go(self):
        """C5-05 exact form: record unread over the file limit."""
        files = _c5_05_files(_padded(
            gate_record(2, extra=HOLD_EXTRA), 1200097))
        report = self._run(files)
        self._assert_blocked(report, "file limit")

    def test_r16_5_02_record_truncated_ruling_go(self):
        """C5-05 damage form: record damaged by truncation."""
        files = _c5_05_files(
            gate_record(2, extra=HOLD_EXTRA) + "TRUNCATED\n")
        report = self._run(files)
        self._assert_blocked(report, "truncated")

    def test_r16_5_02_record_malformed_ruling_go(self):
        """C5-05 damage form: record does not decode."""
        files = _c5_05_files(MALFORMED_RECORD)
        report = self._run(files)
        f2 = self._assert_blocked(report, "not read in full")
        self.assertIn("malformed", f2.lower())

    # ------------------------------------------------------
    # Both read control of the defect construction
    # ------------------------------------------------------

    def test_r16_5_02_both_read_control_disagreement(self):
        """Both read control: record Hold beside ruling Go."""
        files = _c5_05_files(gate_record(2, extra=HOLD_EXTRA))
        report = self._run(files)
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present but not derivable", "F-2")
        self.assertIn("disagree", f2)
        self.assertIn("Hold", f2)
        self.assertIn("Go", f2)
        self.assertNotIn("first-time approval rate:", f2)

    # ------------------------------------------------------
    # Held controls
    # ------------------------------------------------------

    def test_r16_5_held_record_over_limit_ruling_closure_alone(self):
        """Held control: second source carries closure alone.

        The first closure state reads from the first counted
        source, so a closing state standing only in the second
        source counts for nothing, and the unread branch of
        fix pass 4 Unit 5 already fires on this position.
        """
        files = _go_files()
        files[RECORD_2] = _padded(
            gate_record(2, extra=HOLD_EXTRA), 1200097)
        files[RULING_2] = gate_ruling(2)
        report = self._run(files)
        self._assert_blocked(report, "file limit")

    def test_r16_5_held_no_outcome_unread_gate_cured(self):
        """Held control: the fix pass 4 Unit 5 cured position.

        One unread gate record between two read gates carrying
        outcomes, the unread instance carrying no outcome and
        no named closure form from any counted source, stands
        present but not derivable naming the piece and the
        file limit, with no closure state position stated.
        """
        files = _go_files()
        files[RECORD_2] = _padded(
            gate_record(2, extra=GO_EXTRA), 1200097)
        report = self._run(files)
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present but not derivable", "F-2")
        self.assertIn(RECORD_2, f2)
        self.assertIn("file limit", f2)
        self.assertIn("plain closures 2", f2)
        self.assertNotIn("none stated", f2)
        self.assertNotIn("first-time approval rate:", f2)

    def test_r16_5_held_ruling_no_go_read_beside_record_go(self):
        """Held neighbour: ruling No Go read beside record Go."""
        files = _go_files()
        files[RULING_2] = gate_ruling(
            2, extra="First ruling outcome: No Go.")
        report = self._run(files)
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present", "F-2")
        self.assertIn("3 of 3 approved", f2)

    def test_r16_5_held_ruling_no_go_truncated_beside_record_go(self):
        """Held neighbour: the same ruling truncated alike.

        The ruling in this position withholds nothing the read
        piece supplies, so the row stands byte for byte as its
        read form stands.
        """
        files = _go_files()
        files[RULING_2] = gate_ruling(
            2, extra="First ruling outcome: No Go.")
        read_report = self._run(files)
        files[RULING_2] = gate_ruling(
            2, extra="First ruling outcome: No Go.") + "TRUNCATED\n"
        report = self._run(files)
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present", "F-2")
        self.assertIn("3 of 3 approved", f2)
        self.assertEqual(f2, row_block(read_report, "F-2"))

    def test_r16_5_held_adjudication_truncated_beside_read_gates(self):
        """Held neighbour: an adjudication truncated, evidence only."""
        files = _go_files()
        files["steps/step-02-gate-adjudication.md"] = (
            "# Step 2 gate adjudication\n\nEvidence only.\n"
            "TRUNCATED\n")
        report = self._run(files)
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present", "F-2")
        self.assertIn("3 of 3 approved", f2)

    def test_r16_5_held_all_read_go_byte_for_byte(self):
        """Held control: all gates read with outcomes, 3 of 3."""
        report = self._run(_go_files())
        self.assertEqual(row_block(report, "F-2"), GO_READ_F2)

    def test_r16_5_held_record_at_file_limit_with_ruling(self):
        """Held control: the Step 2 record at the limit reads."""
        files = _c5_05_files(_padded(
            gate_record(2, extra=GO_EXTRA), 1000000))
        report = self._run(files)
        self.assertIn(
            "Piece steps/step-02-gate-record.md | gate record "
            "| 1000000 bytes | read in full", report)
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present", "F-2")
        self.assertIn("3 of 3 approved", f2)


if __name__ == "__main__":
    import unittest
    unittest.main()
