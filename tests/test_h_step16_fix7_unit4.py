"""Step 16 fix pass 7 unit 4 tests: the Q-1 lone feeder unit.

Pinning tests for register item R16-7-05 (Low, B7-05) of
Step 16 round 7. The governing rule of the pass, in its
extended form: a piece not read in full, for whatever
reason, is not read.

R16-7-05: a lone Q-1 feeder takes the scattered evidence
refusal, naming neither the feeder piece, nor its limit,
nor its state, in the subforms of the R16-6-09 residual
that a capture visible property separates from the
governed F-16 miniature cells. The separable subforms,
one per separation: (a) a Step 2 gate adjudication
carrying the Round 2 breakdown closed by a TRUNCATED
marker, separated by its class, which the settled reach
of R16-6-09 does not cover; (b) the same adjudication
standing as invalid UTF-8 bytes, and (c) an audit paper
on a plain path carrying the breakdown standing as
invalid UTF-8 bytes, separated by the malformed state;
(d) the same two pieces failing completeness signal one
in their own texts, separated by the capture reason
naming the failed signal; (e) a fix register carrying
the Round 2 round table closed by a TRUNCATED marker
and named as carrier by a read round record, separated
by that naming. In every subform the only Q-1 feeder in
its tree stands beside a Round 1 round record read in
full carrying no breakdown, and its read control counts
Round 2 from the piece. Locus: derivation_core.py,
_derive_q1, the lone feeder branch, whose filter
_piece_over_limit_not_read takes the over limit code
only and lets every other not read state of a collected
lone feeder fall through to the scattered refusal. The
cure these tests pin: each separable subform takes the
governed not derivable form naming that piece and its
bound or state, never the scattered evidence refusal.

The carried boundary stands pinned beside the defect
forms, byte for byte in its standing form: the plain
audit paper in the marker truncated state, at the
step 02 path and at the step 17 path alike, stands as
a governed boundary position CARRIED IN FORM in the
round 7 register, capture indistinguishable from the
F-16 miniature cells, and no test in this module
presents it as cured. Held controls stand pinned
beside it: the cured file limit forms of R16-6-09 in
both classes, the settled forms of R16-5-11, the lone
unread round record governed form, the read and empty
population forms, the step record converse forms, and
the scattered refusal standing for evidence read in
unlike forms.

Trees are written through the Unit 1 module helpers of
fix pass 1, because the constructions turn on exact
byte counts. The product is invoked through run_tool,
which runs the module entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, row_block, run_tool,
    step_record)
from tests.test_h_step16_fix3_unit1 import _clean_files
from tests.test_h_step16_fix4_unit6 import (
    EMPTY_POPULATION_Q1, READ_Q1, SINGLE_UNREAD_Q1)
from tests.test_h_step16_fix5_unit6 import (
    ADJ_PATH, ADJ_TEXT, CORR_PATH, CORR_TEXT, PLAIN_PATH,
    PLAIN_TEXT)
from tests.test_h_step16_fix6_unit5 import FIX_PATH, FIX_TABLE
from tests.test_h_step16_unit1 import _padded, _write_tree

ROUND1_PATH = "audit/step-01-round-record.md"
ROUND2_PATH = "audit/step-02-round-record.md"
STEP17_PATH = "audit/step-17-audit-paper.md"
ROUND1_TEXT = ("# Round 1\n\nPost triage breakdown: Critical 0, "
               "High 1, Medium 2, Low 3.\n")
ROUND2_TEXT = ("# Round 2\n\nPost triage breakdown: Critical 5, "
               "High 5, Medium 5, Low 5.\n")
NO_BREAKDOWN_ROUND1 = (
    "# Round 1 record\n\nNo breakdown stands in this record.\n")
SIGNAL_GAP = "Finding 1 stands.\nFinding 3 stands.\n"
SIGNAL_SOUND = ("Finding 1 stands.\nFinding 2 stands.\n"
                "Finding 3 stands.\n")
MALFORMED_SUFFIX = b"\xff\xfe\xfd\n"
NO_BREAKDOWN_PAPER = (
    "# Round 2 paper\n\nNo breakdown stands in this paper.\n")

_LIMIT_NAMING = (
    ", which stands not read past a limit: the file limit "
    "of 1000000 bytes was crossed")


def _bound_segment(block):
    at = block.find("population bound:")
    return block[at:] if at >= 0 else ""


class TestStep16Fix7Unit4(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    def _lone_files(self, feeder_path, feeder_content):
        files = _clean_files()
        files[ROUND1_PATH] = NO_BREAKDOWN_ROUND1
        files[feeder_path] = feeder_content
        return files

    def _assert_governed(self, report, feeder_path, state_word):
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present but not derivable", "Q-1")
        self.assertIn(feeder_path, q1)
        self.assertIn(state_word, q1)
        self.assertNotIn("scattered", q1)
        self.assertNotIn("no-post-triage-breakdown", q1)
        self.assertNotIn("Round 2: Critical 5", q1)
        self.assertNotIn("Round 2: Critical 7", q1)
        return q1

    def _assert_scattered(self, report):
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present but not derivable", "Q-1")
        self.assertIn("scattered", q1)
        self.assertIn("no-post-triage-breakdown", q1)
        return q1

    def _assert_read_counts(self, report, form_words):
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present", "Q-1")
        self.assertIn(
            "Round 2: Critical 5, High 5, Medium 5, Low 5", q1)
        self.assertIn(form_words, q1)
        self.assertNotIn("scattered", q1)
        return q1

    # ------------------------------------------------------
    # Defect forms, R16-7-05, the separable subforms
    # ------------------------------------------------------

    def test_r16_7_05_adjudication_marker_truncated(self):
        """B7-05 subform a: a lone adjudication closed truncated."""
        files = self._lone_files(ADJ_PATH, ADJ_TEXT + "TRUNCATED\n")
        self._assert_governed(self._run(files), ADJ_PATH, "truncated")

    def test_r16_7_05_adjudication_malformed(self):
        """B7-05 subform b: a lone adjudication as bad bytes."""
        files = self._lone_files(
            ADJ_PATH, ADJ_TEXT.encode("utf-8") + MALFORMED_SUFFIX)
        self._assert_governed(self._run(files), ADJ_PATH, "UTF-8")

    def test_r16_7_05_plain_paper_malformed(self):
        """B7-05 subform c: a lone plain paper as bad bytes."""
        files = self._lone_files(
            PLAIN_PATH, PLAIN_TEXT.encode("utf-8") + MALFORMED_SUFFIX)
        self._assert_governed(self._run(files), PLAIN_PATH, "UTF-8")

    def test_r16_7_05_adjudication_signal_failed(self):
        """B7-05 subform d: a lone adjudication failing signal one."""
        files = self._lone_files(ADJ_PATH, ADJ_TEXT + SIGNAL_GAP)
        self._assert_governed(self._run(files), ADJ_PATH, "truncated")

    def test_r16_7_05_plain_paper_signal_failed(self):
        """B7-05 subform d: a lone plain paper failing signal one."""
        files = self._lone_files(PLAIN_PATH, PLAIN_TEXT + SIGNAL_GAP)
        self._assert_governed(self._run(files), PLAIN_PATH, "truncated")

    def test_r16_7_05_named_carrier_marker_truncated(self):
        """B7-05 subform e: a named carrier closed truncated."""
        files = _clean_files()
        files[ROUND1_PATH] = (
            "# Round 1 record\n\nNo breakdown stands in this "
            "record.\nThis record names %s as the carrier "
            "record for Round 2.\n" % FIX_PATH)
        files[FIX_PATH] = FIX_TABLE + "TRUNCATED\n"
        self._assert_governed(self._run(files), FIX_PATH, "truncated")

    # ------------------------------------------------------
    # Read controls of the defect constructions
    # ------------------------------------------------------

    def test_r16_7_05_adjudication_read_control(self):
        """Read control: the lone adjudication read counts Round 2."""
        files = self._lone_files(ADJ_PATH, ADJ_TEXT)
        self._assert_read_counts(
            self._run(files), "record form gate adjudication")

    def test_r16_7_05_plain_paper_read_control(self):
        """Read control: the lone plain paper read counts Round 2."""
        files = self._lone_files(PLAIN_PATH, PLAIN_TEXT)
        self._assert_read_counts(
            self._run(files), "record form audit paper round record")

    def test_r16_7_05_named_carrier_read_control(self):
        """Read control: the named carrier read counts Round 2."""
        files = _clean_files()
        files[ROUND1_PATH] = (
            "# Round 1 record\n\nNo breakdown stands in this "
            "record.\nThis record names %s as the carrier "
            "record for Round 2.\n" % FIX_PATH)
        files[FIX_PATH] = FIX_TABLE
        report = self._run(files)
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present", "Q-1")
        self.assertIn(
            "Round 2: Critical 7, High 7, Medium 7, Low 7", q1)
        self.assertIn("fix register round table", q1)
        self.assertNotIn("population bound:", q1)

    def test_r16_7_05_adjudication_sound_signal_control(self):
        """Read control: the adjudication with a sound sequence."""
        files = self._lone_files(ADJ_PATH, ADJ_TEXT + SIGNAL_SOUND)
        self._assert_read_counts(
            self._run(files), "record form gate adjudication")

    def test_r16_7_05_plain_paper_sound_signal_control(self):
        """Read control: the plain paper with a sound sequence."""
        files = self._lone_files(PLAIN_PATH, PLAIN_TEXT + SIGNAL_SOUND)
        self._assert_read_counts(
            self._run(files), "record form audit paper round record")

    # ------------------------------------------------------
    # Held controls, the cured forms of R16-6-09
    # ------------------------------------------------------

    def test_r16_7_held_lone_adjudication_over_limit(self):
        """Held R16-6-09: the lone adjudication over the file limit."""
        files = self._lone_files(ADJ_PATH, _padded(ADJ_TEXT, 1200097))
        self._assert_governed(self._run(files), ADJ_PATH, "file limit")

    def test_r16_7_held_lone_plain_paper_over_limit(self):
        """Held R16-6-09: the lone plain paper over the file limit."""
        files = self._lone_files(
            PLAIN_PATH, _padded(PLAIN_TEXT, 1200097))
        self._assert_governed(self._run(files), PLAIN_PATH, "file limit")

    # ------------------------------------------------------
    # The carried boundary, pinned standing exactly
    # ------------------------------------------------------

    def test_r16_7_boundary_plain_paper_marker_truncated_step02(self):
        """Boundary: the plain paper marker truncated, step 02 path.

        The plain audit paper in the marker truncated state
        stands CARRIED IN FORM in the round 7 register, in
        the scattered form, naming neither piece nor state.
        """
        files = self._lone_files(PLAIN_PATH, PLAIN_TEXT + "TRUNCATED\n")
        self._assert_scattered(self._run(files))

    def test_r16_7_boundary_plain_paper_marker_truncated_step17(self):
        """Boundary: the plain paper marker truncated, step 17 path.

        The neighbouring step 17 form of the same boundary
        position, the form the F-16 miniature feeder stands
        in, standing in the scattered form exactly.
        """
        files = self._lone_files(
            STEP17_PATH, PLAIN_TEXT + "TRUNCATED\n")
        self._assert_scattered(self._run(files))

    # ------------------------------------------------------
    # Held controls, the settled forms of R16-5-11
    # ------------------------------------------------------

    def test_r16_7_held_r16_5_11_form_a_adjudication_bound(self):
        """Held R16-5-11 form A: the adjudication bound stands."""
        files = _clean_files()
        files[ROUND1_PATH] = ROUND1_TEXT
        files[ADJ_PATH] = _padded(ADJ_TEXT, 1200097)
        report = self._run(files)
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present", "Q-1")
        self.assertIn(
            "population bound: the population stands bounded "
            "by " + ADJ_PATH + _LIMIT_NAMING, q1)
        self.assertNotIn("Round 2: Critical 5", q1)

    def test_r16_7_held_r16_5_11_form_c_correcting_names_other_only(self):
        """Held R16-5-11 form C: the bound names the other record only."""
        files = _clean_files()
        files[ROUND1_PATH] = ROUND1_TEXT + "TRUNCATED\n"
        files[CORR_PATH] = CORR_TEXT
        files[ROUND2_PATH] = _padded(ROUND2_TEXT, 1200097)
        report = self._run(files)
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present", "Q-1")
        bound = _bound_segment(q1)
        self.assertIn(ROUND2_PATH + _LIMIT_NAMING, bound)
        self.assertNotIn(ROUND1_PATH, bound)
        self.assertNotIn("Round 2: Critical 5", q1)

    def test_r16_7_held_single_unread_round_record_byte_for_byte(self):
        """Held control: the lone unread round record governed form."""
        files = _clean_files()
        files[ROUND1_PATH] = _padded(ROUND1_TEXT, 1200097)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-1"), SINGLE_UNREAD_Q1)

    def test_r16_7_held_read_population_byte_for_byte(self):
        """Held control: every population record read in full."""
        files = _clean_files()
        files[ROUND1_PATH] = ROUND1_TEXT
        files[ROUND2_PATH] = ROUND2_TEXT
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-1"), READ_Q1)

    def test_r16_7_held_empty_population_byte_for_byte(self):
        """Held control: no round record stands, population empty."""
        report = self._run(_clean_files())
        self.assertEqual(row_block(report, "Q-1"), EMPTY_POPULATION_Q1)

    def test_r16_7_held_step_record_converse_read(self):
        """Held converse: a step record carrying a breakdown, read."""
        files = _clean_files()
        files["steps/step-02-record.md"] = step_record(
            2, extra="Post triage breakdown: Critical 5, High 5, "
                     "Medium 5, Low 5.")
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-1"), EMPTY_POPULATION_Q1)

    def test_r16_7_held_step_record_converse_unread(self):
        """Held converse: the same step record standing unread."""
        files = _clean_files()
        files["steps/step-02-record.md"] = _padded(
            step_record(
                2, extra="Post triage breakdown: Critical 5, "
                         "High 5, Medium 5, Low 5."), 1200097)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-1"), EMPTY_POPULATION_Q1)

    def test_r16_7_held_scattered_for_read_evidence(self):
        """Held control: read evidence in unlike forms, scattered.

        A read audit paper carrying no breakdown beside a
        read round record carrying no breakdown: no feeder
        stands not read in full, so the scattered evidence
        refusal stands in its reserved form.
        """
        files = self._lone_files(PLAIN_PATH, NO_BREAKDOWN_PAPER)
        self._assert_scattered(self._run(files))


if __name__ == "__main__":
    import unittest
    unittest.main()
