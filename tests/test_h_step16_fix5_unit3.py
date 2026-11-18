"""Step 16 fix pass 5 unit 3 tests: the Q-4 completion unit.

Pinning tests for register items R16-5-09 (Medium, C5-09
and B5-06 merged), R16-5-10 (Medium, B5-08) and R16-5-12
(Low, C5-11 and B5-07 merged) of Step 16 round 5. The
governing rule of the pass, in its extended form: a piece
not read in full, for whatever reason, is not read, and its
converse from R16-4-11: a piece that is no feeder flips
nothing.

R16-5-09: a malformed trace statement standing in a read
feeder in the Counts form or the full trace form reaches no
branch of _malformed_trace_statements, which scans only for
the first trace line form, so its step stands nowhere on
the row, alone and beside a counted trace alike.
R16-5-10: a trace feeder standing unread for a step already
counted escapes the present branch bound, which collects
only feeders for steps outside the parsed traces, so the
row falls back to a gate trace for that step in silence.
R16-5-12: an unread audit paper that is no trace feeder,
its path carrying neither the purple word nor the round
record form the candidate reading requires, flips Q-4 from
missing to present but not derivable, because
_trace_feeders_not_read consults the audit paper class with
no path test.

Held controls stand pinned beside the defect forms: the
read controls of every defect construction, and every cured
Q-4 form of fix pass 4 Unit 1 in its charged form (R16-4-01,
R16-4-02, R16-4-06, R16-4-07 and R16-4-11), together with
the genuinely absent missing form and the read control at
8 LANDED of 8, byte for byte where the earlier units pinned
them byte for byte.

Trees are written through the Unit 1 module helpers of fix
pass 1, because the constructions turn on exact byte
counts. The product is invoked through run_tool, which runs
the module entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, gate_record, gate_ruling,
    row_block, run_tool)
from tests.test_h_step16_fix3_unit1 import (
    ABSENT_Q4, READ_Q4, TRACE_2, TRACE_3, _clean_files,
    _trace_gate_files)
from tests.test_h_step16_fix4_unit1 import (
    ADJUDICATION_PATH, ADJUDICATION_TEXT, COMPANION_PATH,
    COMPANION_TEXT, MALFORMED_TRACE_2, PURPLE_PATH, PURPLE_TEXT,
    RULING_PATH, RULING_TEXT)
from tests.test_h_step16_unit1 import _padded, _write_tree

PURPLE_COUNTS_BAD_C5 = (
    "# Step 2 Purple paper\n\nCounts: items checked stand "
    "here. LANDED figures stand here, no counts stated\n")
PURPLE_COUNTS_BAD_B5 = (
    "# Step 2 Purple paper\n\nCounts: items checked stand "
    "here. LANDED figures, no counts stated\n")
PURPLE_COUNTS_READ = (
    "# Step 2 Purple paper\n\nCounts: 4 items checked. "
    "LANDED 4, PARTIAL 0, CONTRADICTED 0\n")
FULL_TRACE_BAD = "Summary: full trace figures stand here, no counts stated."
FULL_TRACE_READ = ("Summary: full trace 4 of 4 LANDED, "
                   "PARTIAL 0, CONTRADICTED 0.")
TRACE_2_SMALL = ("First trace for step 2: 2 LANDED of 2 items "
                 "checked, 0 PARTIAL, 0 CONTRADICTED.")
BLUE_PATH = "audit/step-02-blue-paper.md"
BLUE_TEXT = "# Step 2 blue paper\n\nNo trace content stands here.\n"
PLAIN_PATH = "audit/step-02-audit-paper.md"
PLAIN_COUNTS_TEXT = (
    "# Audit paper\n\nCounts: 4 items checked. LANDED 4, "
    "PARTIAL 0, CONTRADICTED 0\n")
MALFORMED_BYTES = b"\xff\xfe\xfd gate record, not valid text\n"


def _assert_no_absence(test, block):
    test.assertNotIn("no first trace record stands", block)
    test.assertNotIn("no feeder record for the metric exists",
                     block)
    test.assertNotIn("no-feeder-record", block)


class TestStep16Fix5Unit3(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    # ------------------------------------------------------
    # Defect forms, R16-5-09, malformed statement forms
    # ------------------------------------------------------

    def test_r16_5_09_counts_form_alone_c5(self):
        """C5-09: a malformed Counts statement alone, read."""
        files = _clean_files()
        files[PURPLE_PATH] = PURPLE_COUNTS_BAD_C5
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn("Step 2", q4)
        self.assertIn(PURPLE_PATH, q4)
        _assert_no_absence(self, q4)

    def test_r16_5_09_full_trace_form_alone(self):
        """B5-06: a malformed full trace statement alone, read."""
        files = _clean_files()
        files[RULING_PATH] = gate_ruling(2, extra=FULL_TRACE_BAD)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn("Step 2", q4)
        self.assertIn(RULING_PATH, q4)
        _assert_no_absence(self, q4)

    def test_r16_5_09_counts_form_beside_counted(self):
        """B5-06 beside form: a malformed Counts step dropped."""
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

    def test_r16_5_09_full_trace_form_beside_counted(self):
        """B5-06 width: a malformed full trace step dropped."""
        files = _clean_files()
        files["steps/step-03-gate-record.md"] = gate_record(
            3, extra=TRACE_3)
        files[RULING_PATH] = gate_ruling(2, extra=FULL_TRACE_BAD)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Step 2", q4)
        self.assertIn("uncounted", q4)

    # ------------------------------------------------------
    # Defect form, R16-5-10, same step fallback
    # ------------------------------------------------------

    def test_r16_5_10_same_step_companion_unread_bound(self):
        """B5-08: a same step companion unread, no bound."""
        files = _clean_files()
        files["steps/step-02-gate-record.md"] = gate_record(
            2, extra=TRACE_2_SMALL)
        files["steps/step-03-gate-record.md"] = gate_record(
            3, extra=TRACE_3)
        files[COMPANION_PATH] = _padded(COMPANION_TEXT, 1200097)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("Step 2, 2 LANDED of 2 items checked", q4)
        self.assertIn("totals 6 LANDED", q4)
        self.assertIn("Bound:", q4)
        bound = q4[q4.find("Bound:"):]
        self.assertIn(COMPANION_PATH, bound)
        self.assertIn("file limit", bound)

    # ------------------------------------------------------
    # Defect forms, R16-5-12, non feeder audit paper
    # ------------------------------------------------------

    def test_r16_5_12_blue_paper_unread_stays_missing(self):
        """C5-11: an unread blue paper is no trace feeder."""
        files = _clean_files()
        files[BLUE_PATH] = _padded(BLUE_TEXT, 1200097)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)

    def test_r16_5_12_plain_paper_unread_stays_missing(self):
        """B5-07: an unread plain audit paper is no feeder."""
        files = _clean_files()
        files[PLAIN_PATH] = _padded(PLAIN_COUNTS_TEXT, 1200097)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)

    # ------------------------------------------------------
    # Read controls of the defect constructions
    # ------------------------------------------------------

    def test_r16_5_held_counts_read_control(self):
        """Read control: the Purple Counts paper read in full."""
        files = _clean_files()
        files[PURPLE_PATH] = PURPLE_COUNTS_READ
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn(PURPLE_PATH, q4)

    def test_r16_5_held_full_trace_read_control(self):
        """Read control: the ruling full trace read in full."""
        files = _clean_files()
        files[RULING_PATH] = gate_ruling(2, extra=FULL_TRACE_READ)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)

    def test_r16_5_held_same_step_companion_read_control(self):
        """Read control B5-08: the companion read stands first."""
        files = _clean_files()
        files["steps/step-02-gate-record.md"] = gate_record(
            2, extra=TRACE_2_SMALL)
        files["steps/step-03-gate-record.md"] = gate_record(
            3, extra=TRACE_3)
        files[COMPANION_PATH] = COMPANION_TEXT
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("Step 2, 4 LANDED of 4 items checked", q4)
        self.assertIn("totals 8 LANDED", q4)
        self.assertIn(COMPANION_PATH, q4)

    def test_r16_5_held_blue_paper_read_control(self):
        """Read control C5-11: the blue paper read stays missing."""
        files = _clean_files()
        files[BLUE_PATH] = BLUE_TEXT
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)

    def test_r16_5_held_plain_paper_read_control(self):
        """Read control B5-07: the plain paper read stays missing."""
        files = _clean_files()
        files[PLAIN_PATH] = PLAIN_COUNTS_TEXT
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)

    # ------------------------------------------------------
    # Held controls, the cured forms of fix pass 4 Unit 1
    # ------------------------------------------------------

    def test_r16_5_held_r16_4_01_companion_unread(self):
        """Held R16-4-01: a step companion feeder unread."""
        files = _clean_files()
        files[COMPANION_PATH] = _padded(COMPANION_TEXT, 1200097)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn(COMPANION_PATH, q4)
        self.assertIn("file limit", q4)
        _assert_no_absence(self, q4)

    def test_r16_5_held_r16_4_01_purple_paper_unread(self):
        """Held R16-4-01: a Purple paper feeder unread."""
        files = _clean_files()
        files[PURPLE_PATH] = _padded(PURPLE_TEXT, 1200097)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn(PURPLE_PATH, q4)
        self.assertIn("file limit", q4)
        _assert_no_absence(self, q4)

    def test_r16_5_held_r16_4_02_gates_truncated(self):
        """Held R16-4-02: damaged gates in the truncated form."""
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

    def test_r16_5_held_r16_4_02_gates_malformed(self):
        """Held R16-4-02: damaged gates in the malformed form."""
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

    def test_r16_5_held_r16_4_07_malformed_alone(self):
        """Held R16-4-07: one malformed first trace, read."""
        files = _clean_files()
        files["steps/step-02-gate-record.md"] = gate_record(
            2, extra=MALFORMED_TRACE_2)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn("Step 2", q4)
        self.assertIn("steps/step-02-gate-record.md", q4)
        _assert_no_absence(self, q4)

    def test_r16_5_held_r16_4_07_malformed_beside(self):
        """Held R16-4-07: a malformed step named uncounted."""
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

    def test_r16_5_held_r16_4_06_step3_gate_unread(self):
        """Held R16-4-06: present totals omit an unread Step 3."""
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

    def test_r16_5_held_r16_4_06_step2_gate_unread(self):
        """Held R16-4-06: present totals omit an unread Step 2."""
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

    def test_r16_5_held_r16_4_11_adjudication_unread(self):
        """Held R16-4-11: an unread adjudication flips nothing."""
        files = _clean_files()
        files[ADJUDICATION_PATH] = _padded(
            ADJUDICATION_TEXT, 1200097)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)

    def test_r16_5_held_read_control_byte_for_byte(self):
        """Held control: the gate records read, 8 LANDED of 8."""
        files = _trace_gate_files(lambda text: text)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), READ_Q4)

    def test_r16_5_held_absent_feeder_byte_for_byte(self):
        """Held control: no gate records, genuinely absent."""
        files = _clean_files()
        for path in [path for path in files if "gate" in path]:
            del files[path]
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)


if __name__ == "__main__":
    import unittest
    unittest.main()
