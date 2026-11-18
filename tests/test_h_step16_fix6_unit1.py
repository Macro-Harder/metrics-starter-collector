"""Step 16 fix pass 6 unit 1 tests: the F-2 unit.

Pinning tests for register items R16-6-01 (High, a reopening
of R16-5-02) and R16-6-02 (Low) of Step 16 round 6. The
governing rule of the pass, in its extended form: a piece not
read in full, for whatever reason, is not read.

R16-6-01, the mirror of R16-5-02: gate records for Steps 1, 2
and 3 read in full carrying Go, beside the Step 2 gate ruling
carrying Hold in its file bytes and padded over the file
limit, standing unread as a later counted source of the
instance. F-2 stood present at 3 of 3 approved, and no word
on the row named the ruling, its limit, or its state. The
read control, the same tree with the ruling read in full,
stands present but not derivable on the stated disagreement
between the gate record and the ruling: the unread state of
a later counted source suppresses a disagreement the row
itself treats as blocking, and lets a rate figure stand that
the read tree denies. Locus: derivation_core.py, _derive_f2,
the unread_first map and the branch behind it, which consult
only the first counted source of the instance. The cure
extends the blocking test to a later counted source standing
not read in full, in the scope settling recorded in the unit
report: a later counted source in the truncated state stands
in the held neighbour position of fix pass 5, because at the
capture level a truncated later source is held with no text,
exactly as a truncated ruling supplying no outcome word is
held, and the two cannot be told apart from the capture; the
truncated form of the defect therefore stands pinned in this
module in its settled held form, beside the file limit and
malformed forms, which carry no held neighbour and stand
blocked.

R16-6-02: in the disagreement position, the not derivable
reason of F-2 omits an unread first counted source of the
same instance. Construction: the Step 2 gate record carrying
Hold padded over the file limit, beside two read Step 2 gate
rulings carrying Go and Hold. The row stands present but not
derivable on the disagreement between the two read rulings
alone, naming neither the record, its limit, nor its state,
while the read control states the forms of all three
sources. Locus: derivation_core.py, _derive_f2, the loop
order, where the disagreement position is taken before the
unread_first position is consulted. The cure names every
counted source of the instance standing not read in full
beside the disagreement, so no feeder of the instance stands
named nowhere.

Held controls stand pinned beside the defect forms: the
cured first source position of fix pass 5; the both read
disagreement control; the No Go held neighbour in its read
and truncated forms, a ruling supplying no outcome word
beside a read first source flipping nothing; and a gate
adjudication truncated beside read gates, adjudications
standing as evidence only and never as counted sources.

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
RECORD_2 = "steps/step-02-gate-record.md"
RULING_2 = "steps/step-02-gate-ruling.md"
RULING_2_ROUND_2 = "steps/step-02-gate-ruling-round-2.md"
MALFORMED_RULING = b"\xff\xfe\xfd gate ruling, not valid text\n"


def _go_files():
    files = _clean_files()
    for n in (1, 2, 3):
        files["steps/step-%02d-gate-record.md" % n] = gate_record(
            n, extra=GO_EXTRA)
    return files


def _b6_01_files(ruling_2):
    files = _go_files()
    files[RULING_2] = ruling_2
    return files


def _b6_02_files(record_2):
    files = _go_files()
    files[RECORD_2] = record_2
    files[RULING_2] = gate_ruling(2, extra=GO_EXTRA)
    files[RULING_2_ROUND_2] = gate_ruling(2, extra=HOLD_EXTRA)
    return files


class TestStep16Fix6Unit1(FixtureTestCase):

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
        self.assertNotIn("3 of 3 approved", f2)
        return f2

    # ------------------------------------------------------
    # Defect forms, R16-6-01
    # ------------------------------------------------------

    def test_r16_6_01_ruling_over_limit_record_go(self):
        """B6-01 exact form: ruling unread over the file limit."""
        files = _b6_01_files(_padded(
            gate_ruling(2, extra=HOLD_EXTRA), 1200097))
        report = self._run(files)
        self._assert_blocked(report, RULING_2, "file limit")

    def test_r16_6_01_ruling_malformed_record_go(self):
        """B6-01 damage form: ruling does not decode."""
        files = _b6_01_files(MALFORMED_RULING)
        report = self._run(files)
        f2 = self._assert_blocked(report, RULING_2, "not read in full")
        self.assertIn("malformed", f2.lower())

    def test_r16_6_01_ruling_truncated_settled_neighbour_position(self):
        """B6-01 truncated form, in its settled held position.

        The truncated form of the defect ruling stands in the
        held neighbour position of fix pass 5, on the scope
        settling recorded in the unit report: at the capture
        level a truncated later counted source is held with no
        text, exactly as the truncated No Go ruling of the held
        neighbour is held, and the capture holds nothing by
        which the two can be told apart, so the row stands as
        its read neighbour form stands, present at 3 of 3.
        """
        files = _b6_01_files(
            gate_ruling(2, extra=HOLD_EXTRA) + "TRUNCATED\n")
        report = self._run(files)
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present", "F-2")
        self.assertIn("3 of 3 approved", f2)

    # ------------------------------------------------------
    # Defect form, R16-6-02
    # ------------------------------------------------------

    def test_r16_6_02_disagreement_names_unread_record(self):
        """B6-02 exact form: disagreement omits the unread record."""
        files = _b6_02_files(_padded(
            gate_record(2, extra=HOLD_EXTRA), 1200097))
        report = self._run(files)
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present but not derivable", "F-2")
        self.assertIn("disagree", f2)
        self.assertIn("Hold", f2)
        self.assertIn("Go", f2)
        self.assertIn(RECORD_2, f2)
        self.assertIn("file limit", f2)
        self.assertNotIn("first-time approval rate:", f2)

    # ------------------------------------------------------
    # Read controls of the defect constructions
    # ------------------------------------------------------

    def test_r16_6_01_read_control_ruling_hold_disagreement(self):
        """B6-01 read control: record Go beside ruling Hold read."""
        files = _b6_01_files(gate_ruling(2, extra=HOLD_EXTRA))
        report = self._run(files)
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present but not derivable", "F-2")
        self.assertIn("disagree", f2)
        self.assertIn("Hold", f2)
        self.assertIn("Go", f2)
        self.assertNotIn("first-time approval rate:", f2)

    def test_r16_6_02_read_control_all_read_disagreement(self):
        """B6-02 read control: all three sources read, forms stated."""
        files = _b6_02_files(gate_record(2, extra=HOLD_EXTRA))
        report = self._run(files)
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present but not derivable", "F-2")
        self.assertIn("disagree", f2)
        self.assertIn("CLOSED-PASS", f2)
        self.assertIn("Hold", f2)
        self.assertIn("Go", f2)
        self.assertNotIn("first-time approval rate:", f2)

    # ------------------------------------------------------
    # Held controls
    # ------------------------------------------------------

    def test_r16_6_held_first_source_record_over_limit(self):
        """Held control: the cured first source position of fix pass 5."""
        files = _go_files()
        files[RECORD_2] = _padded(
            gate_record(2, extra=HOLD_EXTRA), 1200097)
        files[RULING_2] = gate_ruling(2, extra=GO_EXTRA)
        report = self._run(files)
        self._assert_blocked(report, RECORD_2, "file limit")

    def test_r16_6_held_both_read_disagreement(self):
        """Held control: record Hold beside ruling Go, both read."""
        files = _go_files()
        files[RECORD_2] = gate_record(2, extra=HOLD_EXTRA)
        files[RULING_2] = gate_ruling(2, extra=GO_EXTRA)
        report = self._run(files)
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present but not derivable", "F-2")
        self.assertIn("disagree", f2)
        self.assertIn("Hold", f2)
        self.assertIn("Go", f2)
        self.assertNotIn("first-time approval rate:", f2)

    def test_r16_6_held_ruling_no_go_read_beside_record_go(self):
        """Held neighbour: ruling No Go read beside record Go."""
        files = _go_files()
        files[RULING_2] = gate_ruling(
            2, extra="First ruling outcome: No Go.")
        report = self._run(files)
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present", "F-2")
        self.assertIn("3 of 3 approved", f2)

    def test_r16_6_held_ruling_no_go_truncated_beside_record_go(self):
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

    def test_r16_6_held_adjudication_truncated_beside_read_gates(self):
        """Held neighbour: an adjudication truncated, evidence only."""
        files = _go_files()
        files["steps/step-02-gate-adjudication.md"] = (
            "# Step 2 gate adjudication\n\nEvidence only.\n"
            "TRUNCATED\n")
        report = self._run(files)
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present", "F-2")
        self.assertIn("3 of 3 approved", f2)

    def test_r16_6_held_all_read_go_byte_for_byte(self):
        """Held control: all gates read with outcomes, 3 of 3."""
        report = self._run(_go_files())
        self.assertEqual(row_block(report, "F-2"), GO_READ_F2)


if __name__ == "__main__":
    import unittest
    unittest.main()
