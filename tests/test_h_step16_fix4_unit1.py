"""Step 16 fix pass 4 unit 1 tests: the Q-4 completion unit.

Pinning tests for register items R16-4-01 (High, C4-01),
R16-4-02 (High, B4-03), R16-4-06 (Medium, C4-03 and B4-05
merged), R16-4-07 (Medium, B4-04) and R16-4-11 (Low, B4-09)
of Step 16 round 4. The governing rule of the pass: a piece
not read in full, for whatever reason, is not read. The Q-4
unread test must cover the full feeder set the derivation
itself sources through _trace_candidates (trace records,
step companions, gate records, gate rulings and Purple audit
papers), must exclude non feeder classes (gate adjudications),
must count a damaged feeder (truncated or malformed) as not
read, must surface a malformed trace statement in a read
feeder on the row instead of dropping its step in silence or
taking a bare missing, and must carry a bound on a present
row naming every step whose trace feeder stands not read and
whose contribution the totals therefore omit.

Nine defect forms stand pinned. Held controls stand pinned
beside them: the read controls of the companion and the
Purple paper, the trace word Purple path variant, the gate
ruling form, the mixed limits form, seam 1 (one gate unread,
one gate absent), seam 4 (a trace statement in a step record
while the gates stand unread), a damaged piece that is not a
Q-4 feeder class, and the three fix pass 3 forms byte for
byte (the read control at 8 LANDED of 8, the neighbouring
trace named piece branch, and the genuinely absent feeder
missing form).

Trees are written through the Unit 1 module helpers of fix
pass 1, because the constructions turn on exact byte counts
and walk positions. The product is invoked through run_tool,
which runs the module entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, gate_record, gate_ruling,
    row_block, run_tool, step_record)
from tests.test_h_step16_fix3_unit1 import (
    ABSENT_Q4, NEIGHBOUR_Q4, READ_Q4, TRACE_2, TRACE_3,
    _clean_files, _trace_gate_files)
from tests.test_h_step16_unit1 import _padded, _write_tree

TRACE_1 = ("First trace for step 1: 4 LANDED of 4 items "
           "checked, 0 PARTIAL, 0 CONTRADICTED.")
MALFORMED_TRACE_2 = ("First trace for step 2: LANDED figures "
                     "stand here, no counts stated.")
COMPANION_PATH = "steps/step-02-notes.md"
PURPLE_PATH = "audit/step2-purple-paper.md"
PURPLE_TRACE_PATH = "audit/step2-purple-trace-paper.md"
ADJUDICATION_PATH = "steps/step-02-gate-adjudication.md"
RULING_PATH = "steps/step-02-gate-ruling.md"
MALFORMED_BYTES = b"\xff\xfe\xfd gate record, not valid text\n"

COMPANION_TEXT = "# Step 2 notes\n\n" + TRACE_2 + "\n"
PURPLE_TEXT = ("# Step 2 Purple paper\n\nCounts: 4 items "
               "checked. LANDED 4, PARTIAL 0, CONTRADICTED 0\n")
ADJUDICATION_TEXT = (
    "# Step 2 gate adjudication\n\nEvidence beside the step 2 "
    "gate record; counted as a gate file in no count.\n")
RULING_TEXT = gate_ruling(
    2, extra="Summary: full trace 4 of 4 LANDED, PARTIAL 0, "
             "CONTRADICTED 0.")


def _assert_no_absence(test, block):
    test.assertNotIn("no first trace record stands", block)
    test.assertNotIn("no feeder record for the metric exists",
                     block)
    test.assertNotIn("no-feeder-record", block)


class TestStep16Fix4Unit1(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    # ------------------------------------------------------
    # Defect forms
    # ------------------------------------------------------

    def test_r16_4_01_companion_unread_over_file_limit(self):
        """C4-01 first form: a step companion feeder unread."""
        files = _clean_files()
        files[COMPANION_PATH] = _padded(COMPANION_TEXT, 1200097)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn(COMPANION_PATH, q4)
        self.assertIn("file limit", q4)
        _assert_no_absence(self, q4)

    def test_r16_4_01_purple_paper_unread_over_file_limit(self):
        """C4-01 second form: a Purple paper feeder unread."""
        files = _clean_files()
        files[PURPLE_PATH] = _padded(PURPLE_TEXT, 1200097)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn(PURPLE_PATH, q4)
        self.assertIn("file limit", q4)
        _assert_no_absence(self, q4)

    def test_r16_4_02_gates_truncated_carry_trace(self):
        """B4-03 truncated form: damaged gates, traces visible."""
        files = _clean_files()
        for step, trace in ((2, TRACE_2), (3, TRACE_3)):
            files["steps/step-%02d-gate-record.md" % step] = \
                gate_record(step, extra=trace) + "TRUNCATED\n"
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn("steps/step-02-gate-record.md", q4)
        self.assertIn("steps/step-03-gate-record.md", q4)
        self.assertIn("truncated", q4.lower())
        _assert_no_absence(self, q4)

    def test_r16_4_02_gates_malformed_bytes(self):
        """B4-03 malformed form: gate records do not decode."""
        files = _clean_files()
        for step in (2, 3):
            files["steps/step-%02d-gate-record.md" % step] = \
                MALFORMED_BYTES
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn("steps/step-02-gate-record.md", q4)
        self.assertIn("steps/step-03-gate-record.md", q4)
        self.assertIn("malformed", q4.lower())
        _assert_no_absence(self, q4)

    def test_r16_4_07_malformed_statement_alone(self):
        """B4-04 second form: one malformed statement, read."""
        files = _clean_files()
        files["steps/step-02-gate-record.md"] = gate_record(
            2, extra=MALFORMED_TRACE_2)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn("Step 2", q4)
        self.assertIn("steps/step-02-gate-record.md", q4)
        _assert_no_absence(self, q4)

    def test_r16_4_07_malformed_statement_beside_counted(self):
        """B4-04 first form: malformed step dropped in silence."""
        files = _clean_files()
        files["steps/step-02-gate-record.md"] = gate_record(
            2, extra=MALFORMED_TRACE_2)
        files["steps/step-03-gate-record.md"] = gate_record(
            3, extra=TRACE_3)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Step 2", q4)
        self.assertIn("uncounted", q4)

    def test_r16_4_06_mixed_step3_gate_unread(self):
        """C4-03 form: present totals omit an unread Step 3."""
        files = _clean_files()
        files["steps/step-02-gate-record.md"] = gate_record(
            2, extra=TRACE_2)
        files["steps/step-03-gate-record.md"] = _padded(
            gate_record(3, extra=TRACE_3), 1200097)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Bound:", q4)
        bound = q4[q4.find("Bound:"):]
        self.assertIn("steps/step-03-gate-record.md", bound)
        self.assertIn("file limit", bound)

    def test_r16_4_06_mixed_step2_gate_unread(self):
        """B4-05 form: present totals omit an unread Step 2."""
        files = _clean_files()
        files["steps/step-02-gate-record.md"] = _padded(
            gate_record(2, extra=TRACE_2), 1200097)
        files["steps/step-03-gate-record.md"] = gate_record(
            3, extra=TRACE_3)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Bound:", q4)
        bound = q4[q4.find("Bound:"):]
        self.assertIn("steps/step-02-gate-record.md", bound)
        self.assertIn("file limit", bound)

    def test_r16_4_11_adjudication_unread_alone(self):
        """B4-09: an unread adjudication alone flips missing."""
        files = _clean_files()
        files[ADJUDICATION_PATH] = _padded(
            ADJUDICATION_TEXT, 1200097)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)

    # ------------------------------------------------------
    # Held controls
    # ------------------------------------------------------

    def test_r16_4_held_companion_read_control(self):
        """Read control: the companion alone, read in full."""
        files = _clean_files()
        files[COMPANION_PATH] = COMPANION_TEXT
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("Step 2, 4 LANDED of 4 items checked", q4)
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn(COMPANION_PATH, q4)

    def test_r16_4_held_purple_paper_read_control(self):
        """Read control: the Purple paper alone, read in full."""
        files = _clean_files()
        files[PURPLE_PATH] = PURPLE_TEXT
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn(PURPLE_PATH, q4)

    def test_r16_4_held_purple_trace_word_path_variant(self):
        """Boundary control: a trace word Purple path, unread."""
        files = _clean_files()
        files[PURPLE_TRACE_PATH] = _padded(PURPLE_TEXT, 1200097)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn(PURPLE_TRACE_PATH, q4)
        _assert_no_absence(self, q4)

    def test_r16_4_held_gate_ruling_unread(self):
        """Seam 6 ruling form: an unread ruling takes the cure."""
        files = _clean_files()
        files[RULING_PATH] = _padded(RULING_TEXT, 1200097)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn(RULING_PATH, q4)
        self.assertIn("file limit", q4)
        _assert_no_absence(self, q4)

    def test_r16_4_held_mixed_limits_each_named(self):
        """Seam 2: two gates unread under two different limits."""
        files = _clean_files()
        files["steps/step-02-gate-record.md"] = _padded(
            gate_record(2, extra=TRACE_2), 1200097)
        files["steps/step-03-gate-record.md"] = \
            gate_record(3, extra=TRACE_3) + ("x" * 70000) + "\n"
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn("steps/step-02-gate-record.md", q4)
        self.assertIn("steps/step-03-gate-record.md", q4)
        self.assertIn("file limit", q4)
        self.assertIn("line limit", q4)
        _assert_no_absence(self, q4)

    def test_r16_4_held_one_gate_unread_one_gate_absent(self):
        """Seam 1: one gate unread, the Step 3 gate deleted."""
        files = _clean_files()
        files["steps/step-02-gate-record.md"] = _padded(
            gate_record(2, extra=TRACE_2), 1200097)
        del files["steps/step-03-gate-record.md"]
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn("steps/step-02-gate-record.md", q4)
        self.assertIn("file limit", q4)
        self.assertNotIn("steps/step-03-gate-record.md", q4)
        _assert_no_absence(self, q4)

    def test_r16_4_held_step_record_trace_gates_unread(self):
        """Seam 4: a step record trace, the gates unread."""
        files = _trace_gate_files(
            lambda text: _padded(text, 1200097))
        files["steps/step-01-record.md"] = step_record(
            1, extra=TRACE_1)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn("steps/step-02-gate-record.md", q4)
        self.assertIn("steps/step-03-gate-record.md", q4)
        self.assertIn("file limit", q4)
        _assert_no_absence(self, q4)

    def test_r16_4_held_damaged_non_feeder_standing_form(self):
        """Control: a truncated adjudication is no Q-4 feeder."""
        files = _clean_files()
        files[ADJUDICATION_PATH] = ADJUDICATION_TEXT + \
            "TRUNCATED\n"
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)

    def test_r16_4_held_read_control_byte_for_byte(self):
        """Fix pass 3 control: the gate records read in full."""
        files = _trace_gate_files(lambda text: text)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), READ_Q4)

    def test_r16_4_held_neighbouring_trace_piece_byte_for_byte(self):
        """Fix pass 3 control: an unread trace named piece."""
        files = _clean_files()
        files["steps/step-01-trace-record.md"] = _padded(
            "# Step 1 trace record\n\nParts: 2 LANDED, "
            "1 PARTIAL, 0 CONTRADICTED. Stated total: 2 items "
            "checked.\n", 1200097)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), NEIGHBOUR_Q4)

    def test_r16_4_held_absent_feeder_byte_for_byte(self):
        """Fix pass 3 control: no gate records in the tree."""
        files = _clean_files()
        for path in [path for path in files if "gate" in path]:
            del files[path]
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)


if __name__ == "__main__":
    import unittest
    unittest.main()
