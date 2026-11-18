"""Step 16 fix pass 6 unit 5 tests: the Q-1 feeder reach.

Pinning tests for register items R16-6-08 (Low, C6-03 and
B6-07 merged) and R16-6-09 (Low, C6-07) of Step 16 round 6.
The governing rule of the pass, in its extended form: a
piece not read in full, for whatever reason, is not read.

R16-6-08: a bounded Q-1 population omits a standing carrier
record feeder in silence, in every carrier form both papers
prove: a round record read in full names the carrier for
the next round, the carrier carries that round breakdown
in its file bytes and stands not read in full, and no
population bound clause names the carrier piece, its
limit, or its state. Read controls count the next round
from the carrier in each form. Carrier forms: the fix
register (round table form, also closed by a TRUNCATED
marker in turn), the defect register round summary, the
audit register round entry, and the gate record round
section. Locus: derivation_core.py, _q1_unread_round_pieces
at its class test, which collects audit papers and gate
adjudications only, while _q1_carrier_candidates counts
breakdowns from any piece a round record names as its
carrier.

R16-6-09: a lone unread Q-1 feeder takes the scattered
evidence refusal, a present but not derivable block naming
neither the feeder piece, nor its limit, nor its state.
Two feeder classes, each the only Q-1 feeder in its tree:
a Step 2 gate adjudication carrying the Round 2 breakdown
padded over the file limit, and an audit paper on a plain
path carrying the same breakdown padded the same way, each
standing on a base whose round record stands read carrying
no breakdown. Locus: derivation_core.py, _derive_q1, whose
damaged feeder branch collects truncated papers standing
on round record or red paper paths only.

The cure these tests pin: the population bound names every
carrier record standing not read in full whose round the
population omits, across the carrier classes the
derivation itself counts from, in the counted and
correcting positions alike, with the settled corrected_path
exclusion of fix pass 5 kept in terms; and a lone feeder
standing not read in full, in any class the row counts
from, takes the governed not derivable form naming that
piece and its bound or state, never the scattered evidence
refusal. One scope settling stands recorded in the unit
report in full: the lone feeder cure as first formed took
every not read state, and the truncated state broke the
governed miniature cells, which rest on a truncated audit
paper standing in the scattered form, so the lone position
stands narrowed to the not read past a limit state, the
state both charged C6-07 forms stand on.

Held controls stand pinned beside the defect forms: the
cured charged forms of R16-5-11 in their settled form,
including the correcting record position naming the other
unread record only; the lone unread round record governed
form naming the piece, byte for byte; the read population
and empty population forms, byte for byte; and the step
record converse forms, read and unread alike flipping
nothing.

Trees are written through the Unit 1 module helpers of fix
pass 1, because the constructions turn on exact byte
counts. The product is invoked through run_tool, which
runs the module entry route as a subprocess.
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
from tests.test_h_step16_unit1 import _padded, _write_tree

ROUND1_PATH = "audit/step-01-round-record.md"
ROUND2_PATH = "audit/step-02-round-record.md"
ROUND2_TEXT = ("# Round 2\n\nPost triage breakdown: Critical 5, "
               "High 5, Medium 5, Low 5.\n")
NO_BREAKDOWN_ROUND1 = (
    "# Round 1 record\n\nNo breakdown stands in this record.\n")

FIX_PATH = "registers/fix-register.md"
FIX_TABLE = (
    "# Fix register\n\n| Round | Post triage breakdown | "
    "Triage run | Severity scale |\n| --- | --- | --- | --- |\n"
    "| Round 2 | Critical 7, High 7, Medium 7, Low 7 | Triage "
    "has run for Round 2 | Flow scale |\n")
DEFECT_PATH = "registers/defect-register.md"
DEFECT_SUMMARY = (
    "# Defect register\n\n## Round summary: Round 2\n\n"
    "Post triage breakdown: Critical 7, High 7, Medium 7, "
    "Low 7\nTriage run: Triage has run for Round 2\n"
    "Severity scale: Flow scale\n")
AUDIT_REG_PATH = "registers/audit-register.md"
AUDIT_REG_ENTRY = (
    "# Audit register\n\n## Round entry: Round 2\n\n"
    "Post triage breakdown: Critical 7, High 7, Medium 7, "
    "Low 7\nTriage run: Triage has run for Round 2\n"
    "Severity scale: Flow scale\n")
GATE2_PATH = "steps/step-02-gate-record.md"
GATE_SECTION = (
    "# Step 2 gate record\n\nClosure state: CLOSED-PASS.\n\n"
    "## Round section: Round 2\n\n### Post triage breakdown\n\n"
    "Critical 7, High 7, Medium 7, Low 7\n\n### Triage run\n\n"
    "Triage has run for Round 2.\n\n### Severity scale\n\n"
    "Flow scale\n")

_LIMIT_NAMING = (
    ", which stands not read past a limit: the file limit "
    "of 1000000 bytes was crossed")


def _naming_round1(carrier_path):
    return ("# Round 1\n\nPost triage breakdown: Critical 0, "
            "High 1, Medium 2, Low 3.\nThis record names %s "
            "as the carrier record for Round 2.\n" % carrier_path)


def _bound_segment(block):
    at = block.find("population bound:")
    return block[at:] if at >= 0 else ""


def _carrier_files(carrier_path, carrier_content):
    files = _clean_files()
    files[ROUND1_PATH] = _naming_round1(carrier_path)
    files[carrier_path] = carrier_content
    return files


def _correction_files():
    files = _clean_files()
    files[ROUND1_PATH] = (
        "# Round 1\n\nPost triage breakdown: Critical 0, "
        "High 1, Medium 2, Low 3.\nTRUNCATED\n")
    files[CORR_PATH] = CORR_TEXT
    return files


class TestStep16Fix6Unit5(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    def _assert_carrier_bound(self, report, carrier_path):
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present", "Q-1")
        self.assertIn(
            "population, the rounds with records standing: "
            "Round 1", q1)
        self.assertIn(
            "Round 1: Critical 0, High 1, Medium 2, Low 3", q1)
        self.assertIn(
            "population bound: the population stands bounded "
            "by " + carrier_path + _LIMIT_NAMING, q1)
        self.assertNotIn("Round 2: Critical 7", q1)
        self.assertNotIn(
            "records standing: Round 1, Round 2", q1)
        return q1

    def _assert_carrier_read(self, report, form_words):
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present", "Q-1")
        self.assertIn(
            "records standing: Round 1, Round 2", q1)
        self.assertIn(
            "Round 2: Critical 7, High 7, Medium 7, Low 7", q1)
        self.assertIn(form_words, q1)
        self.assertNotIn("population bound:", q1)
        return q1

    # ------------------------------------------------------
    # Defect forms, R16-6-08: the carrier population
    # ------------------------------------------------------

    def test_r16_6_08_carrier_fix_register_over_limit(self):
        """C6-03 and B6-07 form one: the fix register carrier."""
        files = _carrier_files(FIX_PATH, _padded(FIX_TABLE, 1200097))
        self._assert_carrier_bound(self._run(files), FIX_PATH)

    def test_r16_6_08_carrier_fix_register_truncated(self):
        """B6-07 truncated form: the fix register closed by a marker."""
        files = _carrier_files(FIX_PATH, FIX_TABLE + "TRUNCATED\n")
        report = self._run(files)
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present", "Q-1")
        bound = _bound_segment(q1)
        self.assertIn(FIX_PATH, bound)
        self.assertIn("truncation marker", bound)
        self.assertNotIn("Round 2: Critical 7", q1)

    def test_r16_6_08_carrier_defect_register_over_limit(self):
        """B6-07 form two: the defect register round summary."""
        files = _carrier_files(
            DEFECT_PATH, _padded(DEFECT_SUMMARY, 1200097))
        self._assert_carrier_bound(self._run(files), DEFECT_PATH)

    def test_r16_6_08_carrier_audit_register_over_limit(self):
        """B6-07 audit register form: the round entry carrier."""
        files = _carrier_files(
            AUDIT_REG_PATH, _padded(AUDIT_REG_ENTRY, 1200097))
        self._assert_carrier_bound(self._run(files), AUDIT_REG_PATH)

    def test_r16_6_08_carrier_gate_record_over_limit(self):
        """C6-03 form two and B6-07 form three: the gate record."""
        files = _carrier_files(
            GATE2_PATH, _padded(GATE_SECTION, 1200097))
        self._assert_carrier_bound(self._run(files), GATE2_PATH)

    def test_r16_6_08_carrier_in_correcting_position(self):
        """R16-6-08 correcting position: the carrier beside a correction."""
        files = _correction_files()
        files[CORR_PATH] = (
            CORR_TEXT + "This record names %s as the carrier "
            "record for Round 2.\n" % FIX_PATH)
        files[FIX_PATH] = _padded(FIX_TABLE, 1200097)
        report = self._run(files)
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present", "Q-1")
        self.assertIn(
            "Round 1: Critical 0, High 1, Medium 2, Low 3, "
            "scale flow scale, record form correcting record "
            "audit/correcting-record.md", q1)
        bound = _bound_segment(q1)
        self.assertIn(FIX_PATH + _LIMIT_NAMING, bound)
        self.assertNotIn(ROUND1_PATH, bound)
        self.assertNotIn("Round 2: Critical 7", q1)

    # ------------------------------------------------------
    # Read controls, R16-6-08: each carrier form counted
    # ------------------------------------------------------

    def test_r16_6_08_carrier_fix_register_read_control(self):
        """Read control: the fix register carrier read counts Round 2."""
        files = _carrier_files(FIX_PATH, FIX_TABLE)
        self._assert_carrier_read(
            self._run(files), "fix register round table")

    def test_r16_6_08_carrier_defect_register_read_control(self):
        """Read control: the defect register carrier read counts."""
        files = _carrier_files(DEFECT_PATH, DEFECT_SUMMARY)
        self._assert_carrier_read(
            self._run(files), "defect register round summary")

    def test_r16_6_08_carrier_audit_register_read_control(self):
        """Read control: the audit register carrier read counts."""
        files = _carrier_files(AUDIT_REG_PATH, AUDIT_REG_ENTRY)
        self._assert_carrier_read(
            self._run(files), "audit register round entry")

    def test_r16_6_08_carrier_gate_record_read_control(self):
        """Read control: the gate record carrier read counts."""
        files = _carrier_files(GATE2_PATH, GATE_SECTION)
        self._assert_carrier_read(
            self._run(files), "gate record round section")

    # ------------------------------------------------------
    # Defect forms, R16-6-09: the lone feeder refusal
    # ------------------------------------------------------

    def _assert_lone_governed(self, report, feeder_path):
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present but not derivable", "Q-1")
        self.assertIn(feeder_path, q1)
        self.assertIn("file limit", q1)
        self.assertNotIn("scattered", q1)
        self.assertNotIn("no-post-triage-breakdown", q1)
        self.assertNotIn("Round 2: Critical 5", q1)
        return q1

    def test_r16_6_09_lone_adjudication_over_limit(self):
        """C6-07 form one: a lone gate adjudication unread."""
        files = _clean_files()
        files[ROUND1_PATH] = NO_BREAKDOWN_ROUND1
        files[ADJ_PATH] = _padded(ADJ_TEXT, 1200097)
        self._assert_lone_governed(self._run(files), ADJ_PATH)

    def test_r16_6_09_lone_adjudication_truncated_boundary(self):
        """Scope boundary as settled in pass 6, widened in pass 7.

        The charged C6-07 forms stand on the file limit state
        in both classes, and in pass 6 this truncated lone
        adjudication form stood in the scattered form, outside
        the narrowed cure, because the governed miniature
        cells rest on a truncated audit paper standing in
        that form. Round 7 item R16-7-05 separates this form
        from the miniature cells by its class, the gate
        adjudication class, which the miniature feeder does
        not stand in, and charges it to fix pass 7 Unit 4, so
        it now takes the governed not derivable form naming
        the piece and its truncation state. The plain audit
        paper in the marker truncated state stands in the
        scattered form still, as the boundary it is.
        """
        files = _clean_files()
        files[ROUND1_PATH] = NO_BREAKDOWN_ROUND1
        files[ADJ_PATH] = ADJ_TEXT + "TRUNCATED\n"
        report = self._run(files)
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present but not derivable", "Q-1")
        self.assertIn(ADJ_PATH, q1)
        self.assertIn("truncated", q1)
        self.assertNotIn("scattered", q1)
        self.assertNotIn("no-post-triage-breakdown", q1)

    def test_r16_6_09_lone_plain_paper_over_limit(self):
        """C6-07 form two: a lone audit paper on a plain path."""
        files = _clean_files()
        files[ROUND1_PATH] = NO_BREAKDOWN_ROUND1
        files[PLAIN_PATH] = _padded(PLAIN_TEXT, 1200097)
        self._assert_lone_governed(self._run(files), PLAIN_PATH)

    def test_r16_6_09_lone_adjudication_read_control(self):
        """Read control: the lone adjudication read counts Round 2."""
        files = _clean_files()
        files[ROUND1_PATH] = NO_BREAKDOWN_ROUND1
        files[ADJ_PATH] = ADJ_TEXT
        report = self._run(files)
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present", "Q-1")
        self.assertIn(
            "Round 2: Critical 5, High 5, Medium 5, Low 5", q1)
        self.assertIn("record form gate adjudication", q1)

    def test_r16_6_09_lone_plain_paper_read_control(self):
        """Read control: the lone plain paper read counts Round 2."""
        files = _clean_files()
        files[ROUND1_PATH] = NO_BREAKDOWN_ROUND1
        files[PLAIN_PATH] = PLAIN_TEXT
        report = self._run(files)
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present", "Q-1")
        self.assertIn(
            "Round 2: Critical 5, High 5, Medium 5, Low 5", q1)
        self.assertIn("record form audit paper round record", q1)

    # ------------------------------------------------------
    # Held controls: the settled forms of fix pass 5
    # ------------------------------------------------------

    def test_r16_6_held_r16_5_11_form_a_adjudication_bound(self):
        """Held R16-5-11 form A: the adjudication bound stands."""
        files = _clean_files()
        files[ROUND1_PATH] = (
            "# Round 1\n\nPost triage breakdown: Critical 0, "
            "High 1, Medium 2, Low 3.\n")
        files[ADJ_PATH] = _padded(ADJ_TEXT, 1200097)
        report = self._run(files)
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present", "Q-1")
        self.assertIn(
            "population bound: the population stands bounded "
            "by " + ADJ_PATH + _LIMIT_NAMING, q1)
        self.assertNotIn("Round 2: Critical 5", q1)

    def test_r16_6_held_r16_5_11_form_c_correcting_names_other_only(self):
        """Held R16-5-11 form C: the bound names the other record only."""
        files = _correction_files()
        files[ROUND2_PATH] = _padded(ROUND2_TEXT, 1200097)
        report = self._run(files)
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present", "Q-1")
        bound = _bound_segment(q1)
        self.assertIn(ROUND2_PATH + _LIMIT_NAMING, bound)
        self.assertNotIn(ROUND1_PATH, bound)
        self.assertNotIn("Round 2: Critical 5", q1)

    def test_r16_6_held_single_unread_round_record_byte_for_byte(self):
        """Held control: the lone unread round record governed form."""
        files = _clean_files()
        files[ROUND1_PATH] = _padded(
            "# Round 1\n\nPost triage breakdown: Critical 0, "
            "High 1, Medium 2, Low 3.\n", 1200097)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-1"),
                         SINGLE_UNREAD_Q1)

    def test_r16_6_held_read_population_byte_for_byte(self):
        """Held control: every population record read in full."""
        files = _clean_files()
        files[ROUND1_PATH] = (
            "# Round 1\n\nPost triage breakdown: Critical 0, "
            "High 1, Medium 2, Low 3.\n")
        files[ROUND2_PATH] = ROUND2_TEXT
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-1"), READ_Q1)

    def test_r16_6_held_empty_population_byte_for_byte(self):
        """Held control: no round record stands, population empty."""
        report = self._run(_clean_files())
        self.assertEqual(row_block(report, "Q-1"),
                         EMPTY_POPULATION_Q1)

    def test_r16_6_held_step_record_converse_read(self):
        """Held converse: a step record carrying a breakdown, read."""
        files = _clean_files()
        files["steps/step-02-record.md"] = step_record(
            2, extra="Post triage breakdown: Critical 5, High 5, "
                     "Medium 5, Low 5.")
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-1"),
                         EMPTY_POPULATION_Q1)

    def test_r16_6_held_step_record_converse_unread(self):
        """Held converse: the same step record standing unread."""
        files = _clean_files()
        files["steps/step-02-record.md"] = _padded(
            step_record(
                2, extra="Post triage breakdown: Critical 5, "
                         "High 5, Medium 5, Low 5."), 1200097)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-1"),
                         EMPTY_POPULATION_Q1)


if __name__ == "__main__":
    import unittest
    unittest.main()
