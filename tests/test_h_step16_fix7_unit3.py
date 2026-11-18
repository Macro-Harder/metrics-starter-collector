"""Step 16 fix pass 7 unit 3 tests: the E-2 second case unit.

Pinning tests for register item R16-7-04 (Low, B7-04) of
Step 16 round 7. The governing rule of the pass, in its
extended form: a piece not read in full, for whatever
reason, is not read.

R16-7-04: the second case clause of E-2 asserts that no
named agents stand for a step in a countable form over a
step companion standing not read in full and carrying the
named agents line in its file bytes, in both branches of
the row. In the additions branch form, the Step 1 roster
artifact read carrying a base count only beside the
Step 1 step companion at steps/step-01-notes.md carrying
Named agents: 3 and padded over the file limit, E-2 stood
present with its coverage stating Step 1 in the second
case with no roster addition entries and no named agents
in a countable form, byte identical to the control in
which no companion stands in the tree at all. In the
totals branch form, the same companion closed by a
TRUNCATED marker, the shows text first named the
companion with its truncation state and then asserted
the second case absence in the next clause. Locus:
derivation_core.py, _derive_e2, the second case condition
in both loops, whose named agents test ranges over step
records, rosters, opening records and step companions
alike, with _roster_not_read_naming at its roster only
reach, which the fix pass 6 Unit 2 cure consults. The
cure these tests pin: the second case clause stands only
where every staffing piece the clause condition ranges
over stands read in full for the step, and a step with
any such piece not read in full takes the not derivable
naming of that piece and its state in place of any
countable form absence claim, in both row branches and
in every clause of the shows text alike, on the same
naming form the roster cure established.

Held controls stand pinned beside the defect forms: the
cured roster form of fix pass 6 Unit 2, the clause over
a damaged roster artifact taking the not derivable
naming in both branches; the cured additions branch of
fix pass 5 Unit 4; the governed second case form on a
roster read carrying a base count only, in both
branches; and the read rows byte for byte.

Trees are written through the Unit 1 module helpers of
fix pass 1, because the constructions turn on exact byte
counts. The product is invoked through run_tool, which
runs the module entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, row_block, run_tool,
    step_record)
from tests.test_h_step16_fix2_unit1 import READ_E1, READ_E2
from tests.test_h_step16_fix3_unit1 import _clean_files
from tests.test_h_step16_fix6_unit2 import (
    B6_04_ROSTER, ROSTER_1, STEP1_ROSTER_ADDITIONS,
    STEP1_ROSTER_BASE_ONLY, STEP1_ROSTER_TOTAL,
    _b6_04_files, _c6_06_files)
from tests.test_h_step16_unit1 import _padded, _write_tree

SECOND_CASE = "stands in the second case"
ABSENCE_CLAUSE = "stand for that step in a countable form"
COMPANION_1 = "steps/step-01-notes.md"
MALFORMED_SUFFIX = b"\xff\xfe\xfd\n"

COMPANION_NAMED = "# Step 1 notes\n\nNamed agents: 3.\n"
COMPANION_BOTH = (
    "# Step 1 notes\n\nNamed agents: 3.\n"
    "Roster additions over base: 1.\n")


def _record_path(step):
    return "steps/step-%02d-record.md" % step


def _roster_path(step):
    return "steps/step-%02d-roster-artifact.md" % step


def _additions_files(companion):
    files = _c6_06_files(STEP1_ROSTER_BASE_ONLY)
    if companion is not None:
        files[COMPANION_1] = companion
    return files


def _totals_files(companion):
    files = _b6_04_files(STEP1_ROSTER_BASE_ONLY)
    if companion is not None:
        files[COMPANION_1] = companion
    return files


class TestStep16Fix7Unit3(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    def _assert_cured(self, report, verdict, bound_word):
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, verdict, "E-2")
        self.assertNotIn("Step 1 " + SECOND_CASE, e2)
        self.assertNotIn(
            "Step 1 stands in the second case", e2)
        self.assertIn(COMPANION_1, e2)
        self.assertIn(bound_word, e2.lower())
        self.assertIn("not derivable", e2)
        self.assertIn(
            "no roster addition entries and no named agents "
            "are claimed absent for that step", e2)
        return e2

    # ------------------------------------------------------
    # Defect forms, additions branch
    # ------------------------------------------------------

    def test_r16_7_04_additions_companion_over_limit_named(self):
        """B7-04 additions form: companion over limit, named line."""
        files = _additions_files(_padded(COMPANION_NAMED, 1200097))
        report = self._run(files)
        e2 = self._assert_cured(report, "present", "file limit")
        self.assertIn("Step 2", e2)

    def test_r16_7_04_additions_companion_over_limit_both(self):
        """B7-04 additions form: companion over limit, both lines."""
        files = _additions_files(_padded(COMPANION_BOTH, 1200097))
        report = self._run(files)
        self._assert_cured(report, "present", "file limit")

    def test_r16_7_04_additions_companion_truncated_named(self):
        """B7-04 additions form: companion closed truncated."""
        files = _additions_files(COMPANION_NAMED + "TRUNCATED\n")
        report = self._run(files)
        self._assert_cured(report, "present", "truncat")

    # ------------------------------------------------------
    # Defect forms, totals branch
    # ------------------------------------------------------

    def test_r16_7_04_totals_companion_truncated_named(self):
        """B7-04 totals form: companion closed truncated."""
        files = _totals_files(COMPANION_NAMED + "TRUNCATED\n")
        report = self._run(files)
        e2 = self._assert_cured(
            report, "present but not derivable", "truncat")
        self.assertIn("Step 2 " + SECOND_CASE, e2)
        self.assertIn("Step 3 " + SECOND_CASE, e2)

    def test_r16_7_04_totals_companion_over_limit_named(self):
        """B7-04 totals form: companion padded over the limit."""
        files = _totals_files(_padded(COMPANION_NAMED, 1200097))
        report = self._run(files)
        e2 = self._assert_cured(
            report, "present but not derivable", "file limit")
        self.assertIn("Step 2 " + SECOND_CASE, e2)

    def test_r16_7_04_totals_companion_malformed_named(self):
        """B7-04 totals form: companion standing as bad bytes."""
        companion = COMPANION_NAMED.encode("utf-8") \
            + MALFORMED_SUFFIX
        files = _totals_files(companion)
        report = self._run(files)
        self._assert_cured(
            report, "present but not derivable", "not read in full")

    # ------------------------------------------------------
    # Read controls of the defect constructions
    # ------------------------------------------------------

    def test_r16_7_04_additions_read_companion_named_only(self):
        """Read control: companion read, named line alone."""
        report = self._run(_additions_files(COMPANION_NAMED))
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present", "E-2")
        self.assertNotIn("Step 1 " + SECOND_CASE, e2)
        self.assertNotIn("not derivable, the roster", e2)

    def test_r16_7_04_additions_read_companion_both_counted(self):
        """Read control: companion read carrying both lines."""
        report = self._run(_additions_files(COMPANION_BOTH))
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present", "E-2")
        self.assertIn("Step 1: 1", e2)
        self.assertNotIn("Step 1 " + SECOND_CASE, e2)

    def test_r16_7_04_totals_read_companion_named_only(self):
        """Read control: companion read in the totals base."""
        report = self._run(_totals_files(COMPANION_NAMED))
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present but not derivable", "E-2")
        self.assertNotIn("Step 1 " + SECOND_CASE, e2)
        self.assertIn("Step 2 " + SECOND_CASE, e2)

    def test_r16_7_04_totals_read_companion_both_counted(self):
        """Read control: companion both lines counts additions."""
        report = self._run(_totals_files(COMPANION_BOTH))
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present", "E-2")
        self.assertIn("Step 1: 1", e2)
        self.assertNotIn("Step 1 " + SECOND_CASE, e2)

    # ------------------------------------------------------
    # Held controls, the cured roster form of fix pass 6
    # ------------------------------------------------------

    def test_r16_7_held_roster_truncated_additions_branch(self):
        """Held control: damaged roster, additions branch cure."""
        files = _c6_06_files(STEP1_ROSTER_ADDITIONS + "TRUNCATED\n")
        report = self._run(files)
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present", "E-2")
        self.assertNotIn("Step 1 " + SECOND_CASE, e2)
        self.assertNotIn(ABSENCE_CLAUSE, e2)
        self.assertIn(ROSTER_1, e2)
        self.assertIn("truncat", e2.lower())
        self.assertIn("not derivable", e2)

    def test_r16_7_held_roster_truncated_totals_branch(self):
        """Held control: damaged roster, totals branch cure."""
        files = _b6_04_files(B6_04_ROSTER + "TRUNCATED\n")
        report = self._run(files)
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present but not derivable", "E-2")
        self.assertNotIn("Step 1 " + SECOND_CASE, e2)
        self.assertIn(ROSTER_1, e2)
        self.assertIn("truncat", e2.lower())
        self.assertIn("Step 2 " + SECOND_CASE, e2)
        self.assertIn("Step 3 " + SECOND_CASE, e2)

    # ------------------------------------------------------
    # Held controls, governed second case and cured branch
    # ------------------------------------------------------

    def test_r16_7_held_clean_second_case_additions_branch(self):
        """Held control: base only roster, additions branch."""
        report = self._run(_additions_files(None))
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present", "E-2")
        self.assertIn("Step 1 " + SECOND_CASE, e2)
        self.assertIn(ABSENCE_CLAUSE, e2)

    def test_r16_7_held_clean_second_case_totals_branch(self):
        """Held control: base only roster, totals branch."""
        report = self._run(_totals_files(None))
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present but not derivable", "E-2")
        self.assertIn("Step 1 " + SECOND_CASE, e2)
        self.assertIn(ABSENCE_CLAUSE, e2)

    def test_r16_7_held_cured_additions_branch_fix5(self):
        """Held control: the cured additions branch of fix pass 5."""
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

    def test_r16_7_held_read_rows_byte_for_byte(self):
        """Held control: the read staffing rows, unchanged."""
        report = self._run(_clean_files())
        self.assertEqual(row_block(report, "E-1"), READ_E1)
        self.assertEqual(row_block(report, "E-2"), READ_E2)


if __name__ == "__main__":
    import unittest
    unittest.main()
