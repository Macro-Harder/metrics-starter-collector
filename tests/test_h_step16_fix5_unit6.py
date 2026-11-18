"""Step 16 fix pass 5 unit 6 tests: the Q-1 population.

Pinning tests for register item R16-5-11 (Low, C5-10 and
B5-02) of Step 16 round 5. The governing rule of the pass,
in its extended form: a piece not read in full, for
whatever reason, is not read.

R16-5-11: a bounded Q-1 population omits a standing feeder
in silence on three routes outside the narrowed helper
reach of fix pass 4 Unit 6: form A, a gate adjudication
class piece, a feeder class the derivation itself counts
from; form B, an audit paper at a path carrying neither
the round word nor the red paper marker, a path form the
derivation itself counts from; and form C, the correcting
record position, whose call of the present result the
helper does not serve, the row standing byte identical
whether the Round 2 record stands unread or absent. Each
form stands proven a feeder by its read control in the
same construction. No count is taken from any unread
piece in any form.

The cure these tests pin: the population bound names
every feeder piece standing not read in full whose round
the population omits, across the feeder classes and path
forms the derivation itself counts from, gate
adjudications and audit papers in any counted path form
beside audit round records, and in the correcting record
position beside the counted position.

Held controls stand pinned beside the defect forms: the
cured charged form of R16-4-10, in its over limit and
truncated forms; the read controls of forms A, B and C,
byte for byte; the correcting record form with the Round
2 record absent, byte for byte, in which the truncated
Round 1 record the correction stands for is counted
through the correction and stands named nowhere as
omitted; the single unread feeder not derivable form,
byte for byte; and the read and empty population forms,
byte for byte.

Trees are written through the Unit 1 module helpers of fix
pass 1, because the constructions turn on exact byte
counts. The product is invoked through run_tool, which
runs the module entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, row_block, run_tool)
from tests.test_h_step16_fix3_unit1 import _clean_files
from tests.test_h_step16_fix4_unit6 import (
    EMPTY_POPULATION_Q1, READ_Q1, ROUND1_PATH, ROUND1_TEXT,
    ROUND2_PATH, ROUND2_TEXT, SINGLE_UNREAD_Q1)
from tests.test_h_step16_unit1 import _padded, _write_tree

ADJ_PATH = "steps/step-02-gate-adjudication.md"
ADJ_TEXT = ("# Step 2 gate adjudication\n\nRound 2 post triage "
            "breakdown: Critical 5, High 5, Medium 5, Low 5.\n")
PLAIN_PATH = "audit/step-02-audit-paper.md"
PLAIN_TEXT = ("# Round 2 paper\n\nPost triage breakdown: Critical 5, "
              "High 5, Medium 5, Low 5.\n")
CORR_PATH = "audit/correcting-record.md"
CORR_TEXT = ("# Correcting record\n\ncorrected total: Critical 0, "
             "High 1, Medium 2, Low 3.\n")

READ_Q1_A = (
    "Q-1 Findings per audit round, by severity | Verdict: "
    "present | Value: bounded form: population, the rounds "
    "with records standing: Round 1, Round 2; excluded: "
    "none; qualifying round counts: Round 1: Critical 0, "
    "High 1, Medium 2, Low 3, scale flow scale, record form "
    "round record; Round 2: Critical 5, High 5, Medium 5, "
    "Low 5, scale flow scale, record form gate adjudication "
    "| Row coverage: denominator step universe 3 steps | "
    "Reconciled against: the metric carries no total to "
    "reconcile against | Pointer: the round record, or a "
    "record the round record names, for each round counted "
    "(audit/step-01-round-record.md)")

READ_Q1_B = (
    "Q-1 Findings per audit round, by severity | Verdict: "
    "present | Value: bounded form: population, the rounds "
    "with records standing: Round 1, Round 2; excluded: "
    "none; qualifying round counts: Round 1: Critical 0, "
    "High 1, Medium 2, Low 3, scale flow scale, record form "
    "round record; Round 2: Critical 5, High 5, Medium 5, "
    "Low 5, scale flow scale, record form audit paper round "
    "record | Row coverage: denominator step universe 3 "
    "steps | Reconciled against: the metric carries no "
    "total to reconcile against | Pointer: the round "
    "record, or a record the round record names, for each "
    "round counted (audit/step-01-round-record.md)")

CORRECTED_Q1 = (
    "Q-1 Findings per audit round, by severity | Verdict: "
    "present | Value: bounded form: population, the rounds "
    "with records standing: Round 1; excluded: none; "
    "qualifying round counts: Round 1: Critical 0, High 1, "
    "Medium 2, Low 3, scale flow scale, record form "
    "correcting record audit/correcting-record.md | Row "
    "coverage: denominator step universe 3 steps | "
    "Reconciled against: the metric carries no total to "
    "reconcile against | Pointer: the round record, or a "
    "record the round record names, for each round counted "
    "(audit/correcting-record.md)")

_LIMIT_NAMING = (
    ", which stands not read past a limit: the file limit "
    "of 1000000 bytes was crossed")


def _bound_segment(block):
    at = block.find("population bound:")
    return block[at:] if at >= 0 else ""


def _correction_files():
    files = _clean_files()
    files[ROUND1_PATH] = ROUND1_TEXT + "TRUNCATED\n"
    files[CORR_PATH] = CORR_TEXT
    return files


class TestStep16Fix5Unit6(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    # ------------------------------------------------------
    # Defect form A: the gate adjudication class
    # ------------------------------------------------------

    def test_r16_5_11_form_a_adjudication_over_limit(self):
        """C5-10 form A: a Round 2 gate adjudication unread."""
        files = _clean_files()
        files[ROUND1_PATH] = ROUND1_TEXT
        files[ADJ_PATH] = _padded(ADJ_TEXT, 1200097)
        report = self._run(files)
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present", "Q-1")
        self.assertIn(
            "population, the rounds with records standing: "
            "Round 1", q1)
        self.assertIn(
            "Round 1: Critical 0, High 1, Medium 2, Low 3", q1)
        self.assertIn(
            "population bound: the population stands bounded "
            "by " + ADJ_PATH + _LIMIT_NAMING, q1)
        self.assertNotIn("Round 2: Critical 5", q1)
        self.assertNotIn(
            "records standing: Round 1, Round 2", q1)

    def test_r16_5_11_form_a_adjudication_truncated(self):
        """B5-02 form A damaged form: the adjudication truncated."""
        files = _clean_files()
        files[ROUND1_PATH] = ROUND1_TEXT
        files[ADJ_PATH] = ADJ_TEXT + "TRUNCATED\n"
        report = self._run(files)
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present", "Q-1")
        bound = _bound_segment(q1)
        self.assertIn(ADJ_PATH, bound)
        self.assertIn("truncation marker", bound)
        self.assertNotIn("Round 2: Critical 5", q1)

    def test_r16_5_11_form_a_read_control_byte_for_byte(self):
        """Read control: the adjudication read counts Round 2."""
        files = _clean_files()
        files[ROUND1_PATH] = ROUND1_TEXT
        files[ADJ_PATH] = ADJ_TEXT
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-1"), READ_Q1_A)

    # ------------------------------------------------------
    # Defect form B: the plain audit paper path form
    # ------------------------------------------------------

    def test_r16_5_11_form_b_plain_paper_over_limit(self):
        """C5-10 form B: a Round 2 audit paper, plain path, unread."""
        files = _clean_files()
        files[ROUND1_PATH] = ROUND1_TEXT
        files[PLAIN_PATH] = _padded(PLAIN_TEXT, 1200097)
        report = self._run(files)
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present", "Q-1")
        self.assertIn(
            "population, the rounds with records standing: "
            "Round 1", q1)
        self.assertIn(
            "Round 1: Critical 0, High 1, Medium 2, Low 3", q1)
        self.assertIn(
            "population bound: the population stands bounded "
            "by " + PLAIN_PATH + _LIMIT_NAMING, q1)
        self.assertNotIn("Round 2: Critical 5", q1)
        self.assertNotIn(
            "records standing: Round 1, Round 2", q1)

    def test_r16_5_11_form_b_plain_paper_truncated(self):
        """B5-02 form B damaged form: the plain paper truncated."""
        files = _clean_files()
        files[ROUND1_PATH] = ROUND1_TEXT
        files[PLAIN_PATH] = PLAIN_TEXT + "TRUNCATED\n"
        report = self._run(files)
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present", "Q-1")
        bound = _bound_segment(q1)
        self.assertIn(PLAIN_PATH, bound)
        self.assertIn("truncation marker", bound)
        self.assertNotIn("Round 2: Critical 5", q1)

    def test_r16_5_11_form_b_read_control_byte_for_byte(self):
        """Read control: the plain paper read counts Round 2."""
        files = _clean_files()
        files[ROUND1_PATH] = ROUND1_TEXT
        files[PLAIN_PATH] = PLAIN_TEXT
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-1"), READ_Q1_B)

    # ------------------------------------------------------
    # Defect form C: the correcting record position
    # ------------------------------------------------------

    def test_r16_5_11_form_c_correcting_record_round2_unread(self):
        """C5-10 form C: a Round 2 record unread beside a correction."""
        files = _correction_files()
        files[ROUND2_PATH] = _padded(ROUND2_TEXT, 1200097)
        report = self._run(files)
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present", "Q-1")
        self.assertIn(
            "Round 1: Critical 0, High 1, Medium 2, Low 3, "
            "scale flow scale, record form correcting record "
            "audit/correcting-record.md", q1)
        bound = _bound_segment(q1)
        self.assertIn(ROUND2_PATH + _LIMIT_NAMING, bound)
        self.assertNotIn(ROUND1_PATH, bound)
        self.assertNotIn("Round 2: Critical 5", q1)
        self.assertNotEqual(q1, CORRECTED_Q1)

    def test_r16_5_11_form_c_correcting_record_round2_truncated(self):
        """Form C damaged form: the Round 2 record stands truncated."""
        files = _correction_files()
        files[ROUND2_PATH] = ROUND2_TEXT + "TRUNCATED\n"
        report = self._run(files)
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present", "Q-1")
        bound = _bound_segment(q1)
        self.assertIn(ROUND2_PATH, bound)
        self.assertIn("truncation marker", bound)
        self.assertNotIn(ROUND1_PATH, bound)
        self.assertNotEqual(q1, CORRECTED_Q1)

    def test_r16_5_11_form_c_absent_control_byte_for_byte(self):
        """Held control: no Round 2 record stands beside the correction.

        The truncated Round 1 record is the piece the
        correcting record stands for; its round is counted
        through the correction, so no population bound
        stands and the row stands exactly as it stands
        today.
        """
        report = self._run(_correction_files())
        self.assertEqual(row_block(report, "Q-1"), CORRECTED_Q1)

    def test_r16_5_11_form_c_read_control_byte_for_byte(self):
        """Held control: the Round 2 record read beside the correction."""
        files = _correction_files()
        files[ROUND2_PATH] = ROUND2_TEXT
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-1"), CORRECTED_Q1)

    # ------------------------------------------------------
    # Held controls: the cured charged form and populations
    # ------------------------------------------------------

    def test_r16_5_held_r16_4_10_over_limit_byte_held(self):
        """Held R16-4-10: the charged audit round record form."""
        files = _clean_files()
        files[ROUND1_PATH] = ROUND1_TEXT
        files[ROUND2_PATH] = _padded(ROUND2_TEXT, 1200097)
        report = self._run(files)
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present", "Q-1")
        self.assertIn(
            "population bound: the population stands bounded "
            "by audit/step-02-round-record.md" + _LIMIT_NAMING,
            q1)
        self.assertNotIn("Round 2: Critical 5", q1)

    def test_r16_5_held_r16_4_10_truncated_form(self):
        """Held R16-4-10 damage form: the Round 2 record truncated."""
        files = _clean_files()
        files[ROUND1_PATH] = ROUND1_TEXT
        files[ROUND2_PATH] = ROUND2_TEXT + "TRUNCATED\n"
        report = self._run(files)
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present", "Q-1")
        bound = _bound_segment(q1)
        self.assertIn(ROUND2_PATH, bound)
        self.assertIn("truncation marker", bound)
        self.assertNotIn("Round 2: Critical 5", q1)

    def test_r16_5_held_q1_read_population_byte_for_byte(self):
        """Held control: every population record read in full."""
        files = _clean_files()
        files[ROUND1_PATH] = ROUND1_TEXT
        files[ROUND2_PATH] = ROUND2_TEXT
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-1"), READ_Q1)

    def test_r16_5_held_q1_single_unread_byte_for_byte(self):
        """Held control: one round record unread, not derivable form."""
        files = _clean_files()
        files[ROUND1_PATH] = _padded(ROUND1_TEXT, 1200097)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-1"),
                         SINGLE_UNREAD_Q1)

    def test_r16_5_held_q1_empty_population_byte_for_byte(self):
        """Held control: no round record stands, population empty."""
        report = self._run(_clean_files())
        self.assertEqual(row_block(report, "Q-1"),
                         EMPTY_POPULATION_Q1)


if __name__ == "__main__":
    import unittest
    unittest.main()
