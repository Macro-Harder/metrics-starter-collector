"""Step 16 fix pass 7 unit 1 tests: the F-2 unit.

Pinning tests for register items R16-7-01 (High, B7-01) and
R16-7-02 (Medium, B7-02) of Step 16 round 7. The governing
rule of the pass, in its extended form: a piece not read in
full, for whatever reason, is not read.

R16-7-01: gate records for Steps 1 and 2 read in full
carrying Go, beside a Step 3 gate record read in full
carrying a closure state alone and a Step 3 gate ruling
carrying Hold in its file bytes and closed by a TRUNCATED
marker. F-2 stood present at 2 of 2 approved, byte identical
to the control in which no Step 3 ruling stands in the tree
at all, its coverage asserting that no first ruling outcome
is recorded for the step, against the read control standing
present at 2 of 3 approved with Step 3 counted on its Hold
outcome. The Go form of the same construction took the same
present row at 2 of 2 against its read control at 3 of 3.
Locus: derivation_core.py, _derive_f2, the closure alone
branches, the plain, qualified and not approved closure
positions, which consult no unread position; the later
source branch of fix pass 6 fires only where an outcome
stands from a read source. The cure these tests pin: where
a counted source of a closure alone instance stands not
read in full, no rate stands over the instance, the row
taking the not derivable form naming that source piece and
its bound or state.

R16-7-02: gate records for Steps 1, 2 and 3 read in full
carrying Go, beside a Step 2 gate ruling carrying Hold in
its file bytes and failing completeness signal one in its
own text, so the capture holds it in the truncated state
with no text and its capture reason names the failed
signal. F-2 stood present at 3 of 3 approved, byte identical
in its row to the marker truncated form. The read control,
with the sequence made sound, stands present but not
derivable on the stated disagreement stating Go and Hold.
Locus: derivation_core.py, _derive_f2, the later source
branch filter, which tests the capture quality state alone
and consults no capture reason. The cure these tests pin:
the later source exclusion stands narrowed to the marker
truncated state, the state the held neighbour actually
stands in, so the signal failed state blocks as every other
not read state does.

Held controls stand pinned beside the defect forms: the
cured positions of fix pass 6 Unit 1, the file limit and
malformed later source forms, the first source cure in
every state it stands cured, and the disagreement naming
of R16-6-02; the repaired subform of the truncated state
standing read on its held text; and the marker truncated
later source in the outcome carrying position, pinned here
exactly as it stands, as the DESIGN QUESTION remainder of
R16-6-01 recorded in the round 7 register, not as a cure:
a marker truncated ruling carrying Hold and the same ruling
carrying No Go stand byte identical at 3 of 3 approved, and
no test in this module presents that position as cured.

Trees are written through the Unit 1 module helpers of fix
pass 1, because the constructions turn on exact byte counts.
The product is invoked through run_tool, which runs the
module entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, gate_record, gate_ruling,
    row_block, run_tool)
from tests.test_h_step16_fix3_unit1 import _clean_files
from tests.test_h_step16_fix4_unit5 import GO_READ_F2
from tests.test_h_step16_unit1 import _padded, _write_tree

GO_EXTRA = "First ruling outcome: Go."
HOLD_EXTRA = "First ruling outcome: Hold."
NO_GO_EXTRA = "First ruling outcome: No Go."
RECORD_2 = "steps/step-02-gate-record.md"
RULING_2 = "steps/step-02-gate-ruling.md"
RULING_2_ROUND_2 = "steps/step-02-gate-ruling-round-2.md"
RECORD_3 = "steps/step-03-gate-record.md"
RULING_3 = "steps/step-03-gate-ruling.md"
MALFORMED_RULING = b"\xff\xfe\xfd gate ruling, not valid text\n"
SIGNAL_HOLD = ("Finding 1 stands.\nFinding 3 stands.\n"
               "First ruling outcome: Hold.")
SIGNAL_NO_GO = ("Finding 1 stands.\nFinding 3 stands.\n"
                "First ruling outcome: No Go.")
SOUND_HOLD = ("Finding 1 stands.\nFinding 2 stands.\n"
              "Finding 3 stands.\nFirst ruling outcome: Hold.")
REPAIR_TAIL = (
    "\n## Completion section\n\nThis piece was found truncated. "
    "This file supplies the missing content in place.\n")


def _go_files():
    files = _clean_files()
    for n in (1, 2, 3):
        files["steps/step-%02d-gate-record.md" % n] = gate_record(
            n, extra=GO_EXTRA)
    return files


def _closure_alone_files(ruling_3, closure="CLOSED-PASS"):
    files = _clean_files()
    files["steps/step-01-gate-record.md"] = gate_record(
        1, extra=GO_EXTRA)
    files["steps/step-02-gate-record.md"] = gate_record(
        2, extra=GO_EXTRA)
    files[RECORD_3] = gate_record(3, closure=closure)
    if ruling_3 is not None:
        files[RULING_3] = ruling_3
    return files


def _signal_files(extra):
    files = _go_files()
    files[RULING_2] = gate_ruling(2, extra=extra)
    return files


class TestStep16Fix7Unit1(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    def _assert_blocked(self, report, piece_path, bound_word):
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present but not derivable", "F-2")
        self.assertIn(piece_path, f2)
        self.assertIn(bound_word, f2)
        self.assertNotIn("first-time approval rate:", f2)
        return f2

    # ------------------------------------------------------
    # Defect forms, R16-7-01, closure alone position
    # ------------------------------------------------------

    def test_r16_7_01_closure_plain_truncated_ruling_hold(self):
        """B7-01 exact form: plain closure, truncated Hold ruling."""
        files = _closure_alone_files(
            gate_ruling(3, extra=HOLD_EXTRA) + "TRUNCATED\n")
        report = self._run(files)
        f2 = self._assert_blocked(report, RULING_3, "truncated")
        self.assertNotIn("2 of 2 approved", f2)
        self.assertNotIn("no first ruling outcome recorded "
                         "for the step", f2)

    def test_r16_7_01_closure_plain_truncated_ruling_go(self):
        """B7-01 Go form: plain closure, truncated Go ruling."""
        files = _closure_alone_files(
            gate_ruling(3, extra=GO_EXTRA) + "TRUNCATED\n")
        report = self._run(files)
        f2 = self._assert_blocked(report, RULING_3, "truncated")
        self.assertNotIn("2 of 2 approved", f2)

    def test_r16_7_01_closure_qualified_truncated_ruling_hold(self):
        """B7-01 qualified branch: qualified closure alone."""
        files = _closure_alone_files(
            gate_ruling(3, closure="CLOSED-QUALIFIED",
                        extra=HOLD_EXTRA) + "TRUNCATED\n",
            closure="CLOSED-QUALIFIED")
        report = self._run(files)
        self._assert_blocked(report, RULING_3, "truncated")

    def test_r16_7_01_closure_not_approved_truncated_ruling_hold(self):
        """B7-01 not approved branch: CLOSED-FAIL closure alone."""
        files = _closure_alone_files(
            gate_ruling(3, closure="CLOSED-FAIL",
                        extra=HOLD_EXTRA) + "TRUNCATED\n",
            closure="CLOSED-FAIL")
        report = self._run(files)
        self._assert_blocked(report, RULING_3, "truncated")

    # ------------------------------------------------------
    # Defect forms, R16-7-02, signal failed later source
    # ------------------------------------------------------

    def test_r16_7_02_signal_failed_ruling_hold(self):
        """B7-02 exact form: signal failed ruling carrying Hold."""
        report = self._run(_signal_files(SIGNAL_HOLD))
        f2 = self._assert_blocked(report, RULING_2, "truncated")
        self.assertIn("signal-one", f2)
        self.assertNotIn("3 of 3 approved", f2)

    def test_r16_7_02_signal_failed_ruling_no_go(self):
        """B7-02 width form: signal failed ruling carrying No Go."""
        report = self._run(_signal_files(SIGNAL_NO_GO))
        f2 = self._assert_blocked(report, RULING_2, "truncated")
        self.assertIn("signal-one", f2)
        self.assertNotIn("3 of 3 approved", f2)

    # ------------------------------------------------------
    # Read and no ruling controls of the defect constructions
    # ------------------------------------------------------

    def test_r16_7_01_no_ruling_control_present_2_of_2(self):
        """B7-01 no ruling control: no Step 3 ruling in the tree."""
        report = self._run(_closure_alone_files(None))
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present", "F-2")
        self.assertIn("2 of 2 approved", f2)
        self.assertIn("no first ruling outcome recorded "
                      "for the step", f2)

    def test_r16_7_01_read_control_ruling_hold_2_of_3(self):
        """B7-01 read control: the ruling read in full, Hold."""
        files = _closure_alone_files(gate_ruling(3, extra=HOLD_EXTRA))
        report = self._run(files)
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present", "F-2")
        self.assertIn("2 of 3 approved", f2)

    def test_r16_7_01_read_control_ruling_go_3_of_3(self):
        """B7-01 Go read control: the ruling read in full, Go."""
        files = _closure_alone_files(gate_ruling(3, extra=GO_EXTRA))
        report = self._run(files)
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present", "F-2")
        self.assertIn("3 of 3 approved", f2)

    def test_r16_7_02_sound_sequence_read_control_disagreement(self):
        """B7-02 read control: sound sequence, record Go, ruling Hold."""
        report = self._run(_signal_files(SOUND_HOLD))
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present but not derivable", "F-2")
        self.assertIn("disagree", f2)
        self.assertIn("Hold", f2)
        self.assertIn("Go", f2)
        self.assertNotIn("first-time approval rate:", f2)

    # ------------------------------------------------------
    # The remainder position, pinned as the remainder it is
    # ------------------------------------------------------

    def test_r16_7_remainder_marker_truncated_hold_outcome_position(self):
        """Remainder: marker truncated Hold ruling, outcome position.

        The marker truncated later source in the outcome
        carrying position stands as the DESIGN QUESTION
        remainder of R16-6-01 in the round 7 register. It is
        pinned here exactly as it stands at the entering head,
        present at 3 of 3 approved, and not as a cure.
        """
        files = _go_files()
        files[RULING_2] = gate_ruling(
            2, extra=HOLD_EXTRA) + "TRUNCATED\n"
        report = self._run(files)
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present", "F-2")
        self.assertIn("3 of 3 approved", f2)

    def test_r16_7_remainder_marker_truncated_no_go_byte_identical(self):
        """Remainder neighbour: the truncated No Go ruling alike.

        The held neighbour of the remainder: a marker truncated
        ruling carrying No Go in its file bytes stands byte for
        byte as the marker truncated Hold form stands, the two
        indistinguishable on the capture as it stands.
        """
        files = _go_files()
        files[RULING_2] = gate_ruling(
            2, extra=HOLD_EXTRA) + "TRUNCATED\n"
        hold_report = self._run(files)
        files[RULING_2] = gate_ruling(
            2, extra=NO_GO_EXTRA) + "TRUNCATED\n"
        report = self._run(files)
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present", "F-2")
        self.assertIn("3 of 3 approved", f2)
        self.assertEqual(f2, row_block(hold_report, "F-2"))

    # ------------------------------------------------------
    # Held controls, the cured forms of fix pass 6 Unit 1
    # ------------------------------------------------------

    def test_r16_7_held_later_source_over_limit_hold(self):
        """Held control: later source over the file limit blocks."""
        files = _go_files()
        files[RULING_2] = _padded(
            gate_ruling(2, extra=HOLD_EXTRA), 1200097)
        report = self._run(files)
        self._assert_blocked(report, RULING_2, "file limit")

    def test_r16_7_held_later_source_malformed_hold(self):
        """Held control: later source malformed blocks."""
        files = _go_files()
        files[RULING_2] = MALFORMED_RULING
        report = self._run(files)
        f2 = self._assert_blocked(report, RULING_2, "not read in full")
        self.assertIn("malformed", f2.lower())

    def test_r16_7_held_first_source_over_limit(self):
        """Held control: the first source cure of fix pass 5."""
        files = _go_files()
        files[RECORD_2] = _padded(
            gate_record(2, extra=HOLD_EXTRA), 1200097)
        files[RULING_2] = gate_ruling(2, extra=GO_EXTRA)
        report = self._run(files)
        self._assert_blocked(report, RECORD_2, "file limit")

    def test_r16_7_held_disagreement_names_unread_record(self):
        """Held control: the R16-6-02 disagreement naming stands."""
        files = _go_files()
        files[RECORD_2] = _padded(
            gate_record(2, extra=HOLD_EXTRA), 1200097)
        files[RULING_2] = gate_ruling(2, extra=GO_EXTRA)
        files[RULING_2_ROUND_2] = gate_ruling(2, extra=HOLD_EXTRA)
        report = self._run(files)
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present but not derivable", "F-2")
        self.assertIn("disagree", f2)
        self.assertIn(RECORD_2, f2)
        self.assertIn("file limit", f2)
        self.assertNotIn("first-time approval rate:", f2)

    def test_r16_7_held_ruling_no_go_read_beside_record_go(self):
        """Held neighbour: ruling No Go read beside record Go."""
        files = _go_files()
        files[RULING_2] = gate_ruling(2, extra=NO_GO_EXTRA)
        report = self._run(files)
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present", "F-2")
        self.assertIn("3 of 3 approved", f2)

    def test_r16_7_held_all_read_go_byte_for_byte(self):
        """Held control: all gates read with outcomes, 3 of 3."""
        report = self._run(_go_files())
        self.assertEqual(row_block(report, "F-2"), GO_READ_F2)

    # ------------------------------------------------------
    # Held controls, the repaired subform standing read
    # ------------------------------------------------------

    def test_r16_7_held_repaired_ruling_disagreement(self):
        """Held control: a repaired ruling stands read on its text.

        The ruling fails signal one and carries an in place
        Completion section, so the capture holds its completed
        text and the derivation reads it: beside a read Go
        record it takes the disagreement position.
        """
        files = _go_files()
        files[RULING_2] = gate_ruling(
            2, extra=SIGNAL_HOLD) + REPAIR_TAIL
        report = self._run(files)
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present but not derivable", "F-2")
        self.assertIn("disagree", f2)
        self.assertIn("Hold", f2)
        self.assertIn("Go", f2)
        self.assertNotIn("first-time approval rate:", f2)

    def test_r16_7_held_repaired_ruling_beside_closure_alone(self):
        """Held control: a repaired Go ruling beside closure alone.

        The repaired ruling stands read on its held text, so
        beside a closure alone record it stands byte for byte
        as its plain read control stands, present at 3 of 3.
        """
        files = _closure_alone_files(
            gate_ruling(3, extra=SIGNAL_HOLD.replace(
                "First ruling outcome: Hold.",
                "First ruling outcome: Go.")) + REPAIR_TAIL)
        report = self._run(files)
        read_files = _closure_alone_files(
            gate_ruling(3, extra=GO_EXTRA))
        read_report = self._run(read_files)
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present", "F-2")
        self.assertIn("3 of 3 approved", f2)
        self.assertEqual(f2, row_block(read_report, "F-2"))


if __name__ == "__main__":
    import unittest
    unittest.main()
