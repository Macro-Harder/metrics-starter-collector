"""Step 16 fix pass 6 unit 2 tests: the staffing present branches.

Pinning tests for register items R16-6-03 (Medium, C6-01
and B6-03 merged) and R16-6-04 (Low, C6-06 and B6-04
merged) of Step 16 round 6. The governing rule of the
pass, in its extended form: a piece not read in full, for
whatever reason, is not read.

R16-6-03: a present E-1 row in the marked instance branch
omits a marked instance standing in an unread step record,
with no bound naming the piece, its limit, or its state.
C6-01 drives the Step 2 restart instance record at
steps/step-02r-record.md carrying its pair in its file
bytes, padded over the file limit and closed by a
TRUNCATED marker in turn, the row byte identical to the
control in which that record stands read carrying no pair,
against the read control counting the instance from it.
B6-03 drives the marked instance record at
steps/step-02a-record.md in the same two states, against
its two read controls. Locus: derivation_core.py,
_derive_e1_marked, whose present branch forms its coverage
from the covered and uncovered instance keys alone and
consults no not read state. The cure these tests pin: a
present E-1 row in the marked branch carries a bound
naming every marked instance record standing not read in
full, with its bound or state, in the over limit and
damaged states alike.

R16-6-04: the totals set second case of E-2 asserts that
no roster addition entries and no named agents stand for
a step in a countable form, over a damaged roster artifact
carrying both in its file bytes. C6-06 drives the clause
in the additions branch coverage, naming the roster piece
and its truncation nowhere; B6-04 drives the clause in the
totals branch shows text, the piece named in one clause
and the absence asserted in the next. Locus:
derivation_core.py, _derive_e2, the totals set second
case, in both loops that form the clause. The cure these
tests pin: the second case clause stands only where the
roster of the step stands read in full, and a step whose
roster stands not read in full takes the not derivable
naming of that piece and its state in place of any
countable form absence claim, in every clause of the
shows text alike.

Held controls stand pinned beside the defect forms: the
cured plain present branch and bound forms of E-1 from
fix pass 5; the cured additions branch of E-2; the
governed second case form on a roster read carrying a
base count only; and the read staffing rows byte for byte.

Trees are written through the Unit 1 module helpers of fix
pass 1, because the constructions turn on exact byte
counts. The product is invoked through run_tool, which
runs the module entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, gate_record, row_block,
    run_tool, step_record)
from tests.test_h_step16_fix2_unit1 import READ_E1, READ_E2
from tests.test_h_step16_fix3_unit1 import _clean_files
from tests.test_h_step16_fix4_unit6 import _roster_text
from tests.test_h_step16_unit1 import _padded, _write_tree

SECOND_CASE = "stands in the second case"
ABSENCE_CLAUSE = "stand for that step in a countable form"
FALSE_E1_LINK = "list staffing with no base count beside it"
MALFORMED_SUFFIX = b"\xff\xfe\xfd\n"

RESTART_PATH = "steps/step-02r-record.md"
MARKED_PATH = "steps/step-02a-record.md"
ROSTER_1 = "steps/step-01-roster-artifact.md"

RESTART_PAIR = (
    "# Step 2 record, restart instance R\n\n"
    "Build: metrics fixture build.\n"
    "Base: 2. Team staffed: 3 agents. Total spins: 4.\n")
RESTART_NO_PAIR = (
    "# Step 2 record, restart instance R\n\n"
    "Build: metrics fixture build.\n"
    "Team staffed: 3 agents. Total spins: 4.\n")
MARKED_PAIR = (
    "# Step 2 record, instance A\n\n"
    "Build: metrics fixture build.\n"
    "Base: 2. Team staffed: 5 agents. Total spins: 4.\n")
MARKED_NO_PAIR = (
    "# Step 2 record, instance A\n\n"
    "Build: metrics fixture build.\n"
    "Team staffed: 5 agents. Total spins: 4.\n")


def _record_path(step):
    return "steps/step-%02d-record.md" % step


def _roster_path(step):
    return "steps/step-%02d-roster-artifact.md" % step


def _c6_01_files(restart_record):
    files = _clean_files()
    files[RESTART_PATH] = restart_record
    files["steps/step-02r-gate-record.md"] = gate_record(2)
    return files


def _b6_03_files(marked_record):
    files = _clean_files()
    files[MARKED_PATH] = marked_record
    return files


STEP1_ROSTER_ADDITIONS = (
    "# Step 1 roster artifact\n\nNamed agents: 2. Base: 2.\n"
    "Roster additions over base: 1.\n")
STEP1_ROSTER_BASE_ONLY = (
    "# Step 1 roster artifact\n\nBase: 2.\n")
STEP1_ROSTER_TOTAL = (
    "# Step 1 roster artifact\n\nNamed agents: 2. Base: 2.\n"
    "Total spins: 9.\n")


def _c6_06_files(roster):
    """C6-06 base: Step 1 record read, its roster as given.

    The Step 1 record states Base 2, Team staffed 3 and
    Total spins 4, and no additions entry. Steps 2 and 3
    stand read in the clean form, whose rosters carry
    additions entries, so the row stands in the additions
    branch and Step 1 stands in its totals set.
    """
    files = _clean_files()
    files[_record_path(1)] = (
        "# Step 1 record\n\nBuild: metrics fixture build.\n"
        "Base: 2. Team staffed: 3 agents. Total spins: 4.\n")
    files[ROSTER_1] = roster
    return files


def _b6_04_files(roster):
    """B6-04 base: no additions entry stands in any record.

    The step records for Steps 1 to 3 state Base 2 and
    Total spins 4 and no additions entry, and the rosters
    for Steps 2 and 3 stand read carrying a base count
    only, so the row stands in the totals branch. The
    Step 1 roster stands as given.
    """
    files = _clean_files()
    for step in (1, 2, 3):
        files[_record_path(step)] = step_record(step)
        files[_roster_path(step)] = (
            "# Step %d roster artifact\n\nBase: 2.\n" % step)
    files[ROSTER_1] = roster
    return files


B6_04_ROSTER = (
    "# Step 1 roster artifact\n\nNamed agents: 3. Base: 2.\n"
    "Roster additions over base: 1.\nTotal spins: 9.\n")


class TestStep16Fix6Unit2(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    def _bound(self, block):
        self.assertIn("Bound:", block)
        return block[block.find("Bound:"):]

    # ------------------------------------------------------
    # Defect forms, R16-6-03, C6-01, restart instance
    # ------------------------------------------------------

    def test_r16_6_03_c6_01_restart_record_over_limit(self):
        """C6-01 file limit form: the restart record stands unread."""
        files = _c6_01_files(_padded(RESTART_PAIR, 1200097))
        report = self._run(files)
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present", "E-1")
        self.assertIn("Step 2: 3 of 2", e1)
        bound = self._bound(e1)
        self.assertIn(RESTART_PATH, bound)
        self.assertIn("file limit", bound)

    def test_r16_6_03_c6_01_restart_record_truncated(self):
        """C6-01 damaged form: the restart record closed truncated."""
        files = _c6_01_files(RESTART_PAIR + "TRUNCATED\n")
        report = self._run(files)
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present", "E-1")
        self.assertIn("Step 2: 3 of 2", e1)
        bound = self._bound(e1)
        self.assertIn(RESTART_PATH, bound)
        self.assertIn("truncat", bound.lower())

    def test_r16_6_03_c6_01_read_control_pair_counted(self):
        """C6-01 read control: the restart pair counts from it."""
        report = self._run(_c6_01_files(RESTART_PAIR))
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present", "E-1")
        self.assertIn("Step 2 instance R: 3 of 2", e1)

    def test_r16_6_03_c6_01_read_control_no_pair_no_bound(self):
        """C6-01 no pair control: read carrying no pair, no bound."""
        report = self._run(_c6_01_files(RESTART_NO_PAIR))
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present", "E-1")
        self.assertIn("Step 2 instance R", e1)
        self.assertNotIn("Bound:", e1)

    # ------------------------------------------------------
    # Defect forms, R16-6-03, B6-03, marked instance A
    # ------------------------------------------------------

    def test_r16_6_03_b6_03_marked_record_over_limit(self):
        """B6-03 file limit form: the marked record stands unread."""
        files = _b6_03_files(_padded(MARKED_PAIR, 1200097))
        report = self._run(files)
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present", "E-1")
        self.assertIn("Step 2 instance A", e1)
        bound = self._bound(e1)
        self.assertIn(MARKED_PATH, bound)
        self.assertIn("file limit", bound)

    def test_r16_6_03_b6_03_marked_record_truncated(self):
        """B6-03 damaged form: the marked record closed truncated."""
        files = _b6_03_files(MARKED_PAIR + "TRUNCATED\n")
        report = self._run(files)
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present", "E-1")
        self.assertIn("Step 2 instance A", e1)
        bound = self._bound(e1)
        self.assertIn(MARKED_PATH, bound)
        self.assertIn("truncat", bound.lower())

    def test_r16_6_03_b6_03_read_control_pair_counted(self):
        """B6-03 read control: the marked pair counts from it."""
        report = self._run(_b6_03_files(MARKED_PAIR))
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present", "E-1")
        self.assertIn("Step 2 instance A: 5 of 2", e1)

    def test_r16_6_03_b6_03_read_control_no_pair_no_bound(self):
        """B6-03 no pair control: read carrying no pair, no bound."""
        report = self._run(_b6_03_files(MARKED_NO_PAIR))
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present", "E-1")
        self.assertIn("Step 2 instance A", e1)
        self.assertNotIn("Bound:", e1)

    # ------------------------------------------------------
    # Defect forms, R16-6-04, C6-06, additions branch
    # ------------------------------------------------------

    def test_r16_6_04_c6_06_roster_truncated_no_absence(self):
        """C6-06: the Step 1 roster carries both entries, damaged."""
        files = _c6_06_files(STEP1_ROSTER_ADDITIONS + "TRUNCATED\n")
        report = self._run(files)
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present", "E-2")
        self.assertNotIn("Step 1 " + SECOND_CASE, e2)
        self.assertNotIn(ABSENCE_CLAUSE, e2)
        self.assertIn(ROSTER_1, e2)
        self.assertIn("truncat", e2.lower())
        self.assertIn("not derivable", e2)

    def test_r16_6_04_c6_06_roster_malformed_no_absence(self):
        """C6-06 damage form: the Step 1 roster not valid text."""
        roster = STEP1_ROSTER_ADDITIONS.encode("utf-8") \
            + MALFORMED_SUFFIX
        files = _c6_06_files(roster)
        report = self._run(files)
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present", "E-2")
        self.assertNotIn("Step 1 " + SECOND_CASE, e2)
        self.assertNotIn(ABSENCE_CLAUSE, e2)
        self.assertIn(ROSTER_1, e2)
        self.assertIn("not read in full", e2)

    def test_r16_6_04_c6_06_read_control_additions_counted(self):
        """C6-06 read control: the roster read counts its additions."""
        report = self._run(_c6_06_files(STEP1_ROSTER_ADDITIONS))
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present", "E-2")
        self.assertIn("Step 1: 1", e2)
        self.assertNotIn("Step 1 " + SECOND_CASE, e2)

    def test_r16_6_04_c6_06_clean_control_second_case_stands(self):
        """C6-06 clean control: a base only roster, clause governed."""
        report = self._run(_c6_06_files(STEP1_ROSTER_BASE_ONLY))
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present", "E-2")
        self.assertIn("Step 1 " + SECOND_CASE, e2)
        self.assertIn(ABSENCE_CLAUSE, e2)

    # ------------------------------------------------------
    # Defect forms, R16-6-04, B6-04, totals branch
    # ------------------------------------------------------

    def test_r16_6_04_b6_04_roster_truncated_no_absence(self):
        """B6-04: the Step 1 roster carries both entries, damaged."""
        files = _b6_04_files(B6_04_ROSTER + "TRUNCATED\n")
        report = self._run(files)
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present but not derivable", "E-2")
        self.assertNotIn("Step 1 " + SECOND_CASE, e2)
        self.assertIn(ROSTER_1, e2)
        self.assertIn("truncat", e2.lower())
        self.assertIn("Step 2 " + SECOND_CASE, e2)
        self.assertIn("Step 3 " + SECOND_CASE, e2)

    def test_r16_6_04_b6_04_read_control_additions_counted(self):
        """B6-04 read control: the roster read counts its additions."""
        report = self._run(_b6_04_files(B6_04_ROSTER))
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present", "E-2")
        self.assertIn("additions over base, Step 1: 1", e2)
        self.assertNotIn("Step 1 " + SECOND_CASE, e2)

    def test_r16_6_04_b6_04_clean_control_second_case_stands(self):
        """B6-04 clean control: a base only roster, clause governed."""
        report = self._run(_b6_04_files(STEP1_ROSTER_BASE_ONLY))
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present but not derivable", "E-2")
        self.assertIn("Step 1 " + SECOND_CASE, e2)
        self.assertIn(ABSENCE_CLAUSE, e2)

    # ------------------------------------------------------
    # Held controls, fix pass 5 cured forms
    # ------------------------------------------------------

    def test_r16_6_held_plain_e1_bound_step3_truncated(self):
        """Held control: the cured plain E-1 bound of fix pass 5."""
        files = _clean_files()
        for step in (3,):
            files[_record_path(step)] = \
                files[_record_path(step)] + "TRUNCATED\n"
            files[_roster_path(step)] = \
                files[_roster_path(step)] + "TRUNCATED\n"
        report = self._run(files)
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present", "E-1")
        bound = self._bound(e1)
        self.assertIn(_record_path(3), bound)
        self.assertIn(_roster_path(3), bound)
        self.assertIn("truncat", bound.lower())
        self.assertNotIn(FALSE_E1_LINK, e1)

    def test_r16_6_held_plain_e1_covered_roster_over_limit(self):
        """Held control: a covered step roster over the limit."""
        files = _clean_files()
        files[_roster_path(2)] = _padded(_roster_text(2), 1200097)
        report = self._run(files)
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present", "E-1")
        bound = self._bound(e1)
        self.assertIn(_roster_path(2), bound)
        self.assertIn("file limit", bound)

    def test_r16_6_held_e2_additions_branch_roster_truncated(self):
        """Held control: the cured E-2 additions branch of fix pass 5."""
        files = _clean_files()
        files[_record_path(1)] = (
            "# Step 1 record\n\nBuild: metrics fixture build.\n"
            "Base: 2. Team staffed: 3 agents.\n"
            "Roster additions over base: 1.\n")
        files[ROSTER_1] = STEP1_ROSTER_TOTAL + "TRUNCATED\n"
        report = self._run(files)
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present", "E-2")
        self.assertIn("Step 1 total spins: not derivable", e2)
        self.assertIn(ROSTER_1, e2)
        self.assertIn("truncat", e2.lower())
        self.assertNotIn(
            "no total spins figure stands for that step", e2)

    def test_r16_6_held_read_staffing_rows_byte_for_byte(self):
        """Held control: the read staffing form, unchanged."""
        report = self._run(_clean_files())
        self.assertEqual(row_block(report, "E-1"), READ_E1)
        self.assertEqual(row_block(report, "E-2"), READ_E2)


if __name__ == "__main__":
    import unittest
    unittest.main()
