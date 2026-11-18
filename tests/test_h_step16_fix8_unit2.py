"""Step 16 fix pass 8 unit 2 tests: the Q-1 lone feeder states unit.

Pinning tests for register item R16-8-02 (Low, B8-02) of
Step 16 round 8. The governing rule of the pass, in its
extended form: a piece not read in full, for whatever
reason, is not read.

R16-8-02: a lone plain audit paper feeder takes the
scattered evidence refusal, naming neither the feeder
piece, nor its limit, nor its state, in two states the
fix pass 7 predicate _q1_lone_separable does not reach:
(1) the unreadable state, driven in the dangling link
form and in the directory at its path form; and (2) the
duplicate identity disagreement state, the same file
name under audit/sub/ carrying differing content, the
capture merging the two paths into one piece with no
text. In every subform the piece stands as the only Q-1
feeder in its tree beside a Round 1 round record read in
full carrying no breakdown, each feeder carrying the
Round 2 breakdown in the form its state allows. Locus:
derivation_core.py, _q1_lone_separable and _derive_q1,
whose lone feeder branch returns true on the over limit
code, on the gate adjudication class, on a carrier class,
on the malformed state, and on the signal form of the
truncated state, and on no other position, so a collected
lone feeder in the unreadable state or the duplicate
state falls through to the scattered evidence refusal.
The separability the register decides: both states are
stated on the capture piece itself, and the carried
miniature feeder stands in the marker truncated state
only, so a state keyed cure touches no miniature cell.
The cure these tests pin: each subform takes the governed
not derivable form naming that piece and its state, never
the scattered evidence refusal, in the plain audit paper
class and in any collected class the branch already
reaches on the same state ground.

The carried boundary stands pinned beside the defect
forms, byte for byte in its standing form: the plain
audit paper in the marker truncated state, at the
step 02 path and at the step 17 path alike, stands
CARRIED IN FORM on the F-16 miniature cell ground, and
no test in this module presents it as cured. Held
controls stand pinned beside it: the cured separable
subforms of R16-7-05 in every state and class they stand
cured, including the unreadable state in the adjudication
class and in the named carrier class, the signal two and
signal three forms of the plain paper, the cured file
limit forms of R16-6-09 in both classes, the cured
carrier population of R16-6-08, the settled forms of
R16-5-11, the lone unread round record governed form,
the read and empty population forms, the step record
converse forms, and the scattered refusal standing for
evidence read in unlike forms.

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
from tests.test_h_step16_fix7_unit4 import (
    MALFORMED_SUFFIX, NO_BREAKDOWN_PAPER, NO_BREAKDOWN_ROUND1,
    ROUND1_PATH, ROUND1_TEXT, ROUND2_PATH, ROUND2_TEXT,
    SIGNAL_GAP, STEP17_PATH, _LIMIT_NAMING, _bound_segment)
from tests.test_h_step16_unit1 import _padded, _write_tree

SUB_PATH = "audit/sub/step-02-audit-paper.md"
SUB_TEXT_DIFFERING = (
    "# Round 2 paper\n\nPost triage breakdown: Critical 9, "
    "High 9, Medium 9, Low 9.\n")
SIGNAL_TWO_PAPER = (
    "# Round 2 paper\n\nRows stated in header: 3\n\n"
    "| Item | State |\n| --- | --- |\n| one | stands |\n\n"
    "Post triage breakdown: Critical 5, High 5, Medium 5, Low 5.\n")
SIGNAL_THREE_PAPER = (
    "# Round 2 paper\n\nContents: Alpha, Beta\n\n## Alpha\n\n"
    "Post triage breakdown: Critical 5, High 5, Medium 5, Low 5.\n")


def _dangling(root, rel):
    target = root / rel
    target.unlink()
    target.symlink_to(root / "no-such-target.md")


def _as_directory(root, rel):
    target = root / rel
    target.unlink()
    target.mkdir()


class TestStep16Fix8Unit2(FixtureTestCase):

    def _run(self, files, mutate=None):
        root = _write_tree(files)
        if mutate is not None:
            mutate(root)
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
        self.assertNotIn("Round 2: Critical 9", q1)
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
    # Defect forms, R16-8-02, the two states
    # ------------------------------------------------------

    def test_r16_8_02_plain_paper_unreadable_dangling_link(self):
        """B8-02 subform a: the plain paper as a dangling link."""
        files = self._lone_files(PLAIN_PATH, PLAIN_TEXT)
        report = self._run(
            files, lambda root: _dangling(root, PLAIN_PATH))
        self._assert_governed(report, PLAIN_PATH, "dangling link")

    def test_r16_8_02_plain_paper_unreadable_directory(self):
        """B8-02 subform b: the plain paper as a directory."""
        files = self._lone_files(PLAIN_PATH, PLAIN_TEXT)
        report = self._run(
            files, lambda root: _as_directory(root, PLAIN_PATH))
        self._assert_governed(report, PLAIN_PATH, "not a regular file")

    def test_r16_8_02_plain_paper_duplicate_identity(self):
        """B8-02 subform c: the plain paper in duplicate disagreement."""
        files = self._lone_files(PLAIN_PATH, PLAIN_TEXT)
        files[SUB_PATH] = SUB_TEXT_DIFFERING
        self._assert_governed(self._run(files), PLAIN_PATH, "duplicate")

    # ------------------------------------------------------
    # Read controls of the defect constructions
    # ------------------------------------------------------

    def test_r16_8_02_plain_paper_read_control(self):
        """Read control: the lone plain paper read counts Round 2."""
        files = self._lone_files(PLAIN_PATH, PLAIN_TEXT)
        self._assert_read_counts(
            self._run(files), "record form audit paper round record")

    def test_r16_8_02_duplicate_same_content_read_control(self):
        """Read control: two paths, one content, counts Round 2.

        The same file name under audit/sub/ carrying the
        same content merges into one read piece, so no
        disagreement stands and Round 2 counts from it.
        """
        files = self._lone_files(PLAIN_PATH, PLAIN_TEXT)
        files[SUB_PATH] = PLAIN_TEXT
        self._assert_read_counts(
            self._run(files), "record form audit paper round record")

    def test_r16_8_02_named_carrier_read_control(self):
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

    # ------------------------------------------------------
    # Held controls, the cured forms of R16-7-05
    # ------------------------------------------------------

    def test_r16_8_held_adjudication_unreadable_dangling_link(self):
        """Held R16-7-05 reach: the adjudication as a dangling link."""
        files = self._lone_files(ADJ_PATH, ADJ_TEXT)
        report = self._run(
            files, lambda root: _dangling(root, ADJ_PATH))
        self._assert_governed(report, ADJ_PATH, "dangling link")

    def test_r16_8_held_named_carrier_unreadable_dangling_link(self):
        """Held R16-7-05 reach: the named carrier as a dangling link."""
        files = _clean_files()
        files[ROUND1_PATH] = (
            "# Round 1 record\n\nNo breakdown stands in this "
            "record.\nThis record names %s as the carrier "
            "record for Round 2.\n" % FIX_PATH)
        files[FIX_PATH] = FIX_TABLE
        report = self._run(
            files, lambda root: _dangling(root, FIX_PATH))
        self._assert_governed(report, FIX_PATH, "dangling link")

    def test_r16_8_held_plain_paper_signal_two(self):
        """Held R16-7-05 reach: the plain paper failing signal two."""
        files = self._lone_files(PLAIN_PATH, SIGNAL_TWO_PAPER)
        self._assert_governed(self._run(files), PLAIN_PATH, "truncated")

    def test_r16_8_held_plain_paper_signal_three(self):
        """Held R16-7-05 reach: the plain paper failing signal three."""
        files = self._lone_files(PLAIN_PATH, SIGNAL_THREE_PAPER)
        self._assert_governed(self._run(files), PLAIN_PATH, "truncated")

    def test_r16_8_held_plain_paper_malformed(self):
        """Held R16-7-05: the lone plain paper as bad bytes."""
        files = self._lone_files(
            PLAIN_PATH, PLAIN_TEXT.encode("utf-8") + MALFORMED_SUFFIX)
        self._assert_governed(self._run(files), PLAIN_PATH, "UTF-8")

    def test_r16_8_held_plain_paper_signal_failed(self):
        """Held R16-7-05: the lone plain paper failing signal one."""
        files = self._lone_files(PLAIN_PATH, PLAIN_TEXT + SIGNAL_GAP)
        self._assert_governed(self._run(files), PLAIN_PATH, "truncated")

    def test_r16_8_held_adjudication_marker_truncated(self):
        """Held R16-7-05: the lone adjudication closed truncated."""
        files = self._lone_files(ADJ_PATH, ADJ_TEXT + "TRUNCATED\n")
        self._assert_governed(self._run(files), ADJ_PATH, "truncated")

    def test_r16_8_held_named_carrier_marker_truncated(self):
        """Held R16-7-05: the named carrier closed truncated."""
        files = _clean_files()
        files[ROUND1_PATH] = (
            "# Round 1 record\n\nNo breakdown stands in this "
            "record.\nThis record names %s as the carrier "
            "record for Round 2.\n" % FIX_PATH)
        files[FIX_PATH] = FIX_TABLE + "TRUNCATED\n"
        self._assert_governed(self._run(files), FIX_PATH, "truncated")

    # ------------------------------------------------------
    # Held controls, the cured forms of R16-6-09
    # ------------------------------------------------------

    def test_r16_8_held_lone_adjudication_over_limit(self):
        """Held R16-6-09: the lone adjudication over the file limit."""
        files = self._lone_files(ADJ_PATH, _padded(ADJ_TEXT, 1200097))
        self._assert_governed(self._run(files), ADJ_PATH, "file limit")

    def test_r16_8_held_lone_plain_paper_over_limit(self):
        """Held R16-6-09: the lone plain paper over the file limit."""
        files = self._lone_files(
            PLAIN_PATH, _padded(PLAIN_TEXT, 1200097))
        self._assert_governed(self._run(files), PLAIN_PATH, "file limit")

    # ------------------------------------------------------
    # The carried boundary, pinned standing exactly
    # ------------------------------------------------------

    def test_r16_8_boundary_plain_paper_marker_truncated_step02(self):
        """Boundary: the plain paper marker truncated, step 02 path.

        The plain audit paper in the marker truncated state
        stands CARRIED IN FORM, on the F-16 miniature cell
        ground, in the scattered form, naming neither piece
        nor state, at both paths, byte for byte as fix
        pass 7 Unit 4 held it.
        """
        files = self._lone_files(PLAIN_PATH, PLAIN_TEXT + "TRUNCATED\n")
        self._assert_scattered(self._run(files))

    def test_r16_8_boundary_plain_paper_marker_truncated_step17(self):
        """Boundary: the plain paper marker truncated, step 17 path."""
        files = self._lone_files(
            STEP17_PATH, PLAIN_TEXT + "TRUNCATED\n")
        self._assert_scattered(self._run(files))

    # ------------------------------------------------------
    # Held controls, the settled forms of R16-5-11
    # ------------------------------------------------------

    def test_r16_8_held_r16_5_11_form_a_adjudication_bound(self):
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

    def test_r16_8_held_r16_5_11_form_c_correcting_names_other_only(self):
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

    def test_r16_8_held_single_unread_round_record_byte_for_byte(self):
        """Held control: the lone unread round record governed form."""
        files = _clean_files()
        files[ROUND1_PATH] = _padded(ROUND1_TEXT, 1200097)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-1"), SINGLE_UNREAD_Q1)

    def test_r16_8_held_read_population_byte_for_byte(self):
        """Held control: every population record read in full."""
        files = _clean_files()
        files[ROUND1_PATH] = ROUND1_TEXT
        files[ROUND2_PATH] = ROUND2_TEXT
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-1"), READ_Q1)

    def test_r16_8_held_empty_population_byte_for_byte(self):
        """Held control: no round record stands, population empty."""
        report = self._run(_clean_files())
        self.assertEqual(row_block(report, "Q-1"), EMPTY_POPULATION_Q1)

    def test_r16_8_held_step_record_converse_read(self):
        """Held converse: a step record carrying a breakdown, read."""
        files = _clean_files()
        files["steps/step-02-record.md"] = step_record(
            2, extra="Post triage breakdown: Critical 5, High 5, "
                     "Medium 5, Low 5.")
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-1"), EMPTY_POPULATION_Q1)

    def test_r16_8_held_step_record_converse_unread(self):
        """Held converse: the same step record standing unread."""
        files = _clean_files()
        files["steps/step-02-record.md"] = _padded(
            step_record(
                2, extra="Post triage breakdown: Critical 5, "
                         "High 5, Medium 5, Low 5."), 1200097)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-1"), EMPTY_POPULATION_Q1)

    def test_r16_8_held_scattered_for_read_evidence(self):
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
