"""Step 16 fix pass 6 unit 3 tests: the Q-4 statement scan.

Pinning tests for register items R16-6-06 (Medium, C6-02
and B6-06 merged) and R16-6-07 (Low, C6-04) of Step 16
round 6. The governing rule of the pass, in its extended
form: a piece not read in full, for whatever reason, is
not read, and its converse: a piece that is no feeder
flips nothing.

R16-6-06: a malformed gate record tally statement alone
takes Q-4 missing under the no feeder record code, while
its counted sibling counts, and beside a counted Step 3
trace the malformed Step 2 stands nowhere on the row.
C6-02 drives two wordings of the tally form in a read
Step 2 gate record; B6-06 drives the gate tally wording
in the alone and beside forms. Locus: derivation_core.py,
_malformed_trace_statements, whose scan reaches the first
trace line form, the Counts form and the full trace form,
and reaches no tally form in any feeder class. The cure
these tests pin: the scan reaches the tally statement
form, in the alone position taking the governed not
derivable form naming the step and the feeder piece, and
in the beside position naming the step uncounted in the
present row coverage.

R16-6-07: a malformed first trace line in a read blue
audit paper flips Q-4 from missing to present but not
derivable, while the counted form in the same paper flips
nothing. Locus: derivation_core.py,
_malformed_trace_statements, whose first trace line
branch carries no audit paper path test, where its Counts
branch applies one. The cure these tests pin: the first
trace line branch applies the same path test inside the
audit paper class that its Counts branch,
_trace_candidates and _trace_feeders_not_read apply, so a
malformed statement in a paper that is no feeder flips
nothing, in its read and unread positions alike.

Held controls stand pinned beside the defect forms: every
cured Q-4 form of fix pass 5 (the Counts form, the full
trace form, the same step fallback holding on the line
limit route, and the non feeder boundary of R16-5-12),
together with the held trace record Parts and verdict
counts forms of the round 6 correctness sweep, and the
genuinely absent missing form.

Trees are written through the Unit 1 module helpers of fix
pass 1, because the constructions turn on exact byte
counts. The product is invoked through run_tool, which
runs the module entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, gate_record, gate_ruling,
    row_block, run_tool)
from tests.test_h_step16_fix3_unit1 import (
    ABSENT_Q4, READ_Q4, TRACE_2, TRACE_3, _clean_files)
from tests.test_h_step16_fix4_unit1 import (
    COMPANION_PATH, COMPANION_TEXT, MALFORMED_TRACE_2,
    PURPLE_PATH, PURPLE_TEXT, RULING_PATH)
from tests.test_h_step16_fix5_unit3 import (
    FULL_TRACE_BAD, FULL_TRACE_READ, PURPLE_COUNTS_BAD_B5,
    PURPLE_COUNTS_BAD_C5)
from tests.test_h_step16_unit1 import _padded, _write_tree

GATE_2 = "steps/step-02-gate-record.md"
BLUE_PATH = "audit/step-02-blue-paper.md"
PLAIN_PATH = "audit/step-02-audit-paper.md"
TRACE_RECORD_PATH = "steps/step-01-trace-record.md"

TALLY_C6_A_BAD = (
    "Trace for step 2: 2 of 2 LANDED, PARTIAL and "
    "CONTRADICTED figures stand here, no counts stated")
TALLY_C6_A_READ = (
    "Trace for step 2: 2 of 2 LANDED, 0 PARTIAL, "
    "0 CONTRADICTED")
TALLY_C6_B_BAD = (
    "Trace tally for step 2: 2 of 2 items checked. LANDED "
    "figures stand here, no counts stated")
TALLY_C6_B_READ = (
    "Trace tally for step 2: 2 of 2 LANDED, 0 PARTIAL, "
    "0 CONTRADICTED")
TALLY_B6_BAD = (
    "Gate tally: items checked stand here. LANDED figures "
    "stand here, no counts stated")
TALLY_B6_READ = "Gate tally: 2 of 2 LANDED, 0 PARTIAL, 0 CONTRADICTED"

BLUE_BAD_FIRST_TRACE = (
    "# Step 2 blue paper\n\nFirst trace for step 2: LANDED "
    "figures stand here, no counts stated\n")
BLUE_READ_FIRST_TRACE = (
    "# Step 2 blue paper\n\nFirst trace for step 2: 4 LANDED "
    "of 4 items checked, 0 PARTIAL, 0 CONTRADICTED\n")
BLUE_TEXT = "# Step 2 blue paper\n\nNo trace content stands here.\n"
PLAIN_COUNTS_TEXT = (
    "# Audit paper\n\nCounts: 4 items checked. LANDED 4, "
    "PARTIAL 0, CONTRADICTED 0\n")
TRACE_2_SMALL = (
    "First trace for step 2: 2 LANDED of 2 items "
    "checked, 0 PARTIAL, 0 CONTRADICTED.")
PARTS_BAD = (
    "# Step 1 trace record\n\nParts: LANDED figures stand "
    "here, no counts stated.\n")
VERDICT_COUNTS_BAD = (
    "# Step 1 trace record\n\nVerdict counts:\n"
    "- LANDED: figures stand here\n"
    "Rows traced: figures stand here\n")


def _assert_no_absence(test, block):
    test.assertNotIn("no first trace record stands", block)
    test.assertNotIn("no feeder record for the metric exists",
                     block)
    test.assertNotIn("no-feeder-record", block)


class TestStep16Fix6Unit3(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    def _alone_tally_files(self, tally_line):
        files = _clean_files()
        files[GATE_2] = gate_record(2, extra=tally_line)
        return files

    def _assert_alone_tally_cured(self, report):
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn("Step 2", q4)
        self.assertIn(GATE_2, q4)
        _assert_no_absence(self, q4)

    # ------------------------------------------------------
    # Defect forms, R16-6-06, C6-02, both wordings
    # ------------------------------------------------------

    def test_r16_6_06_c6_02_tally_wording_one_alone(self):
        """C6-02 wording one: a malformed tally alone, read."""
        report = self._run(self._alone_tally_files(TALLY_C6_A_BAD))
        self._assert_alone_tally_cured(report)

    def test_r16_6_06_c6_02_tally_wording_two_alone(self):
        """C6-02 wording two: a malformed trace tally alone."""
        report = self._run(self._alone_tally_files(TALLY_C6_B_BAD))
        self._assert_alone_tally_cured(report)

    def test_r16_6_06_c6_02_tally_wording_one_beside_counted(self):
        """C6-02 beside form: a malformed tally step dropped."""
        files = self._alone_tally_files(TALLY_C6_A_BAD)
        files["steps/step-03-gate-record.md"] = gate_record(
            3, extra=TRACE_3)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Step 2", q4)
        self.assertIn("uncounted", q4)

    # ------------------------------------------------------
    # Defect forms, R16-6-06, B6-06, alone and beside
    # ------------------------------------------------------

    def test_r16_6_06_b6_06_gate_tally_alone(self):
        """B6-06 alone form: a malformed gate tally, read."""
        report = self._run(self._alone_tally_files(TALLY_B6_BAD))
        self._assert_alone_tally_cured(report)

    def test_r16_6_06_b6_06_gate_tally_beside_counted(self):
        """B6-06 beside form: a malformed tally step dropped."""
        files = self._alone_tally_files(TALLY_B6_BAD)
        files["steps/step-03-gate-record.md"] = gate_record(
            3, extra=TRACE_3)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Step 2", q4)
        self.assertIn("uncounted", q4)

    # ------------------------------------------------------
    # Defect form, R16-6-07, C6-04, converse limb
    # ------------------------------------------------------

    def test_r16_6_07_c6_04_blue_paper_malformed_first_trace_read(self):
        """C6-04: a malformed first trace in a read blue paper."""
        files = _clean_files()
        files[BLUE_PATH] = BLUE_BAD_FIRST_TRACE
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)

    # ------------------------------------------------------
    # Counted form controls of the defect constructions
    # ------------------------------------------------------

    def test_r16_6_06_c6_02_tally_wording_one_counted_control(self):
        """C6-02 counted control: wording one in counted form."""
        report = self._run(self._alone_tally_files(TALLY_C6_A_READ))
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("Step 2, 2 of 2 LANDED", q4)
        self.assertIn("totals 2 LANDED", q4)

    def test_r16_6_06_c6_02_tally_wording_two_counted_control(self):
        """C6-02 counted control: wording two in counted form."""
        report = self._run(self._alone_tally_files(TALLY_C6_B_READ))
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("Step 2, 2 of 2 LANDED", q4)
        self.assertIn("totals 2 LANDED", q4)

    def test_r16_6_06_b6_06_gate_tally_counted_control(self):
        """B6-06 counted control: the gate tally counted."""
        report = self._run(self._alone_tally_files(TALLY_B6_READ))
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("Step 2, 2 of 2 LANDED", q4)
        self.assertIn("totals 2 LANDED", q4)

    def test_r16_6_07_c6_04_blue_paper_counted_control(self):
        """C6-04 counted control: the counted form flips nothing."""
        files = _clean_files()
        files[BLUE_PATH] = BLUE_READ_FIRST_TRACE
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)

    # ------------------------------------------------------
    # Held controls, the cured Q-4 forms of fix pass 5
    # ------------------------------------------------------

    def test_r16_6_held_counts_form_alone(self):
        """Held control: the cured Counts form alone, fix pass 5."""
        files = _clean_files()
        files[PURPLE_PATH] = PURPLE_COUNTS_BAD_C5
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn("Step 2", q4)
        self.assertIn(PURPLE_PATH, q4)
        _assert_no_absence(self, q4)

    def test_r16_6_held_counts_form_beside_counted(self):
        """Held control: the cured Counts form beside a trace."""
        files = _clean_files()
        files["steps/step-03-gate-record.md"] = gate_record(
            3, extra=TRACE_3)
        files[PURPLE_PATH] = PURPLE_COUNTS_BAD_B5
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Step 2", q4)
        self.assertIn("uncounted", q4)

    def test_r16_6_held_full_trace_form_alone(self):
        """Held control: the cured full trace form alone."""
        files = _clean_files()
        files[RULING_PATH] = gate_ruling(2, extra=FULL_TRACE_BAD)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn("Step 2", q4)
        self.assertIn(RULING_PATH, q4)
        _assert_no_absence(self, q4)

    def test_r16_6_held_full_trace_read_control(self):
        """Held control: the full trace form read counted."""
        files = _clean_files()
        files[RULING_PATH] = gate_ruling(2, extra=FULL_TRACE_READ)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)

    def test_r16_6_held_same_step_fallback_line_limit_route(self):
        """Held control: the same step bound on the line limit."""
        files = _clean_files()
        files[GATE_2] = gate_record(2, extra=TRACE_2_SMALL)
        files["steps/step-03-gate-record.md"] = gate_record(
            3, extra=TRACE_3)
        files[COMPANION_PATH] = COMPANION_TEXT + ("x" * 70000) + "\n"
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("Step 2, 2 LANDED of 2 items checked", q4)
        self.assertIn("totals 6 LANDED", q4)
        self.assertIn("Bound:", q4)
        bound = q4[q4.find("Bound:"):]
        self.assertIn(COMPANION_PATH, bound)
        self.assertIn("line limit", bound)

    def test_r16_6_held_blue_paper_unread_non_feeder_boundary(self):
        """Held R16-5-12: an unread blue paper flips nothing."""
        files = _clean_files()
        files[BLUE_PATH] = _padded(BLUE_TEXT, 1200097)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)

    def test_r16_6_held_plain_paper_unread_non_feeder_boundary(self):
        """Held R16-5-12: an unread plain paper flips nothing."""
        files = _clean_files()
        files[PLAIN_PATH] = _padded(PLAIN_COUNTS_TEXT, 1200097)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)

    def test_r16_6_held_blue_paper_unread_malformed_first_trace(self):
        """Held converse, unread position: a blue paper unread."""
        files = _clean_files()
        files[BLUE_PATH] = _padded(BLUE_BAD_FIRST_TRACE, 1200097)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)

    def test_r16_6_held_purple_paper_malformed_first_trace(self):
        """Held feeder position: a Purple paper is a feeder."""
        files = _clean_files()
        files[PURPLE_PATH] = (
            "# Step 2 Purple paper\n\n" + MALFORMED_TRACE_2 + "\n")
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn("Step 2", q4)
        self.assertIn(PURPLE_PATH, q4)
        _assert_no_absence(self, q4)

    # ------------------------------------------------------
    # Held controls, trace record forms and the absent form
    # ------------------------------------------------------

    def test_r16_6_held_trace_record_parts_malformed(self):
        """Held control: a malformed Parts line in a trace record."""
        files = _clean_files()
        files[TRACE_RECORD_PATH] = PARTS_BAD
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn(TRACE_RECORD_PATH, q4)
        _assert_no_absence(self, q4)

    def test_r16_6_held_trace_record_verdict_counts_malformed(self):
        """Held control: a malformed verdict counts block."""
        files = _clean_files()
        files[TRACE_RECORD_PATH] = VERDICT_COUNTS_BAD
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn(TRACE_RECORD_PATH, q4)
        _assert_no_absence(self, q4)

    def test_r16_6_held_read_control_byte_for_byte(self):
        """Held control: the gate records read, 8 LANDED of 8."""
        files = _clean_files()
        for step, trace in ((2, TRACE_2), (3, TRACE_3)):
            files["steps/step-%02d-gate-record.md" % step] = \
                gate_record(step, extra=trace)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), READ_Q4)

    def test_r16_6_held_absent_feeder_byte_for_byte(self):
        """Held control: no gate records, genuinely absent."""
        files = _clean_files()
        for path in [path for path in files if "gate" in path]:
            del files[path]
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)


if __name__ == "__main__":
    import unittest
    unittest.main()
