"""Step 16 fix pass 5 unit 4 tests: the staffing present branches.

Pinning tests for register items R16-5-07 (Medium, C5-07
and B5-09 merged) and R16-5-08 (Medium, C5-08) of Step 16
round 5. The governing rule of the pass, in its extended
form: a piece not read in full, for whatever reason, is
not read.

R16-5-07: the bound and coverage of a present E-1 row
assert what a damaged uncovered step record holds,
stating that its step records list staffing with no base
count beside it, where the record states a base count
beside its staffing in its file bytes. Locus: _e1_bound,
which consults only the over limit staffing list for its
excepted steps, and the _derive_e1 present branch in the
same position for covered steps.
R16-5-08: the additions branch of a present E-2 row
asserts in its value and coverage lines that no total
spins figure stands for a step, over a damaged roster
artifact that carries that figure. Locus: _derive_e2,
the additions branch, whose not derivable loops consult
only the over limit staffing list, where the total alone
and no quantity branches of the same row consult the
damaged list as well since fix pass 4.

Held controls stand pinned beside the defect forms: the
over limit present forms of both rows, naming every
unread piece with its limit; the cured shows forms of
R16-4-12, every staffing piece damaged standing present
but not derivable naming every piece with its state; the
fix pass 2 over limit staffing limbs in their byte for
byte cured forms; and the read staffing rows byte for
byte.

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
from tests.test_h_step16_fix4_unit6 import (
    CURED_OVER_LIMIT_E1, CURED_OVER_LIMIT_E2, _roster_text)
from tests.test_h_step16_unit1 import _padded, _write_tree

FALSE_E1_LINK = "list staffing with no base count beside it"
MALFORMED_SUFFIX = b"\xff\xfe\xfd\n"


def _record_path(step):
    return "steps/step-%02d-record.md" % step


def _roster_path(step):
    return "steps/step-%02d-roster-artifact.md" % step


def _truncated_staffing(files, steps):
    for step in steps:
        files[_record_path(step)] = \
            files[_record_path(step)] + "TRUNCATED\n"
        files[_roster_path(step)] = \
            files[_roster_path(step)] + "TRUNCATED\n"
    return files


def _over_limit_staffing(files, steps):
    for step in steps:
        files[_record_path(step)] = _padded(
            files[_record_path(step)], 1200097)
        files[_roster_path(step)] = _padded(
            files[_roster_path(step)], 1200097)
    return files


def _e2_step1_files(roster):
    """C5-08 base: Step 1 additions read, its roster as given.

    The Step 1 record states Base 2, Team staffed 3 and
    roster additions over base 1, and no total spins figure
    stands in it. Steps 2 and 3 stand read in the clean form.
    """
    files = _clean_files()
    files[_record_path(1)] = (
        "# Step 1 record\n\nBuild: metrics fixture build.\n"
        "Base: 2. Team staffed: 3 agents.\n"
        "Roster additions over base: 1.\n")
    files[_roster_path(1)] = roster
    return files


def _e2_step3_files(roster):
    """Second loop base: Step 3 states no labelled quantity.

    The Step 3 record states Base 2 and Team staffed 3 and
    no additions entry and no total spins figure. Steps 1
    and 2 stand read in the clean form, with additions and
    totals. The Step 3 roster stands as given.
    """
    files = _clean_files()
    files[_record_path(3)] = (
        "# Step 3 record\n\nBuild: metrics fixture build.\n"
        "Base: 2. Team staffed: 3 agents.\n")
    files[_roster_path(3)] = roster
    return files


STEP1_ROSTER_TOTAL = (
    "# Step 1 roster artifact\n\nNamed agents: 2. Base: 2.\n"
    "Total spins: 9.\n")
STEP3_ROSTER_QUANTITIES = (
    "# Step 3 roster artifact\n\nNamed agents: 2. Base: 2.\n"
    "Roster additions over base: 1.\nTotal spins: 9.\n")


class TestStep16Fix5Unit4(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    def _bound(self, block):
        self.assertIn("Bound:", block)
        return block[block.find("Bound:"):]

    def _assert_e2_no_absence(self, block):
        self.assertNotIn(
            "no total spins figure stands for that step", block)
        self.assertNotIn(
            "state no total spins figure in any record", block)
        self.assertNotIn("no total stands for it", block)

    # ------------------------------------------------------
    # Defect forms, R16-5-07, row E-1 present bound
    # ------------------------------------------------------

    def test_r16_5_07_e1_bound_step3_truncated(self):
        """C5-07: Step 3 record and roster damaged, uncovered."""
        files = _truncated_staffing(_clean_files(), (3,))
        report = self._run(files)
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present", "E-1")
        bound = self._bound(e1)
        self.assertIn(_record_path(3), bound)
        self.assertIn(_roster_path(3), bound)
        self.assertIn("truncat", bound.lower())
        self.assertNotIn(FALSE_E1_LINK, e1)

    def test_r16_5_07_e1_bound_steps2_3_truncated(self):
        """B5-09: Steps 2 and 3 damaged, Step 1 covered alone."""
        files = _truncated_staffing(_clean_files(), (2, 3))
        report = self._run(files)
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present", "E-1")
        bound = self._bound(e1)
        for step in (2, 3):
            self.assertIn(_record_path(step), bound)
            self.assertIn(_roster_path(step), bound)
        self.assertIn("truncat", bound.lower())
        self.assertNotIn(FALSE_E1_LINK, e1)

    def test_r16_5_07_e1_bound_step3_malformed(self):
        """R16-5-07 malformed form: Step 3 pieces not valid text."""
        files = _clean_files()
        files[_record_path(3)] = \
            step_record(3).encode("utf-8") + MALFORMED_SUFFIX
        files[_roster_path(3)] = \
            _roster_text(3).encode("utf-8") + MALFORMED_SUFFIX
        report = self._run(files)
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present", "E-1")
        bound = self._bound(e1)
        self.assertIn(_record_path(3), bound)
        self.assertIn(_roster_path(3), bound)
        self.assertIn("not read in full", bound)
        self.assertNotIn(FALSE_E1_LINK, e1)

    def test_r16_5_07_e1_covered_step_roster_truncated(self):
        """Present branch: a covered step roster stands damaged.

        Every step is covered from its read step record, and
        the Step 2 roster artifact, carrying its pair in its
        file bytes, stands closed by a TRUNCATED marker, so
        the row must carry a bound naming that piece and its
        state, as its over limit form does.
        """
        files = _clean_files()
        files[_roster_path(2)] = \
            files[_roster_path(2)] + "TRUNCATED\n"
        report = self._run(files)
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present", "E-1")
        bound = self._bound(e1)
        self.assertIn(_roster_path(2), bound)
        self.assertIn("truncat", bound.lower())

    # ------------------------------------------------------
    # Defect forms, R16-5-08, row E-2 additions branch
    # ------------------------------------------------------

    def test_r16_5_08_e2_additions_roster_truncated(self):
        """C5-08: the Step 1 roster carries Total spins 9, damaged."""
        files = _e2_step1_files(STEP1_ROSTER_TOTAL + "TRUNCATED\n")
        report = self._run(files)
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present", "E-2")
        self.assertIn("Step 1 total spins: not derivable", e2)
        self.assertIn(_roster_path(1), e2)
        self.assertIn("truncat", e2.lower())
        self._assert_e2_no_absence(e2)

    def test_r16_5_08_e2_additions_roster_malformed(self):
        """R16-5-08 malformed form: the Step 1 roster not valid text."""
        roster = STEP1_ROSTER_TOTAL.encode("utf-8") + MALFORMED_SUFFIX
        files = _e2_step1_files(roster)
        report = self._run(files)
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present", "E-2")
        self.assertIn("Step 1 total spins: not derivable", e2)
        self.assertIn(_roster_path(1), e2)
        self.assertIn("not read in full", e2)
        self._assert_e2_no_absence(e2)

    def test_r16_5_08_e2_no_quantity_step_roster_truncated(self):
        """Second loop: Step 3 quantities stand in a damaged roster."""
        files = _e2_step3_files(
            STEP3_ROSTER_QUANTITIES + "TRUNCATED\n")
        report = self._run(files)
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present", "E-2")
        self.assertIn(
            "Step 3 additions over base and total spins: "
            "not derivable", e2)
        self.assertIn(_roster_path(3), e2)
        self.assertIn("truncat", e2.lower())

    # ------------------------------------------------------
    # Held controls, the over limit present forms
    # ------------------------------------------------------

    def test_r16_5_held_e1_bound_steps2_3_over_limit(self):
        """Held neighbour B5-09: the same steps over the file limit."""
        files = _over_limit_staffing(_clean_files(), (2, 3))
        report = self._run(files)
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present", "E-1")
        bound = self._bound(e1)
        for step in (2, 3):
            self.assertIn(_record_path(step), bound)
            self.assertIn(_roster_path(step), bound)
        self.assertIn("file limit", bound)
        self.assertNotIn(FALSE_E1_LINK, e1)

    def test_r16_5_held_e1_bound_step2_record_over_limit(self):
        """Held control: one uncovered step record over the limit."""
        files = _clean_files()
        files[_record_path(2)] = _padded(step_record(2), 1200097)
        report = self._run(files)
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present", "E-1")
        bound = self._bound(e1)
        self.assertIn(_record_path(2), bound)
        self.assertIn("file limit", bound)
        self.assertNotIn(FALSE_E1_LINK, e1)

    def test_r16_5_held_e1_covered_step_roster_over_limit(self):
        """Held control: a covered step roster over the limit."""
        files = _clean_files()
        files[_roster_path(2)] = _padded(_roster_text(2), 1200097)
        report = self._run(files)
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present", "E-1")
        bound = self._bound(e1)
        self.assertIn(_roster_path(2), bound)
        self.assertIn("file limit", bound)

    def test_r16_5_held_e2_additions_roster_over_limit(self):
        """Held control: the C5-08 construction over the file limit."""
        files = _e2_step1_files(_padded(STEP1_ROSTER_TOTAL, 1200097))
        report = self._run(files)
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present", "E-2")
        self.assertIn("Step 1 total spins: not derivable", e2)
        self.assertIn(_roster_path(1), e2)
        self.assertIn("file limit", e2)
        self._assert_e2_no_absence(e2)

    def test_r16_5_held_e2_no_quantity_step_roster_over_limit(self):
        """Held control: the second loop construction over the limit."""
        files = _e2_step3_files(
            _padded(STEP3_ROSTER_QUANTITIES, 1200097))
        report = self._run(files)
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present", "E-2")
        self.assertIn(
            "Step 3 additions over base and total spins: "
            "not derivable", e2)
        self.assertIn(_roster_path(3), e2)
        self.assertIn("file limit", e2)

    # ------------------------------------------------------
    # Held controls, the cured shows forms of R16-4-12
    # ------------------------------------------------------

    def test_r16_5_held_r16_4_12_e1_shows_truncated_staffing(self):
        """Held R16-4-12: E-1 shows text over truncated pieces."""
        files = _truncated_staffing(_clean_files(), (1, 2, 3))
        report = self._run(files)
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present but not derivable", "E-1")
        for step in (1, 2, 3):
            self.assertIn(_record_path(step), e1)
            self.assertIn(_roster_path(step), e1)
        self.assertIn("truncation marker", e1)
        self.assertIn("not read in full", e1)
        self.assertNotIn(
            "no step carries both a staffed count and a base "
            "count for the same step", e1)

    def test_r16_5_held_r16_4_12_e2_shows_truncated_staffing(self):
        """Held R16-4-12: E-2 shows text over truncated pieces."""
        files = _truncated_staffing(_clean_files(), (1, 2, 3))
        report = self._run(files)
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present but not derivable", "E-2")
        for step in (1, 2, 3):
            self.assertIn(_record_path(step), e2)
            self.assertIn(_roster_path(step), e2)
        self.assertIn("truncation marker", e2)
        self.assertIn("not read in full", e2)
        self.assertNotIn(
            "none states an additions over base figure or a "
            "total spins figure", e2)

    # ------------------------------------------------------
    # Held controls, fix pass 2 over limit limbs, byte for byte
    # ------------------------------------------------------

    def test_r16_5_held_fix2_e1_no_pair_over_limit_byte_for_byte(self):
        """Held control: fix pass 2 Unit 1 E-1 branch, cured form."""
        files = _over_limit_staffing(_clean_files(), (1, 2, 3))
        report = self._run(files)
        self.assertEqual(row_block(report, "E-1"),
                         CURED_OVER_LIMIT_E1)

    def test_r16_5_held_fix2_e2_no_quantity_over_limit_byte_for_byte(self):
        """Held control: fix pass 2 Unit 1 E-2 branch, cured form."""
        files = _over_limit_staffing(_clean_files(), (1, 2, 3))
        report = self._run(files)
        self.assertEqual(row_block(report, "E-2"),
                         CURED_OVER_LIMIT_E2)

    def test_r16_5_held_read_staffing_rows_byte_for_byte(self):
        """Held control: the read staffing form, unchanged."""
        report = self._run(_clean_files())
        self.assertEqual(row_block(report, "E-1"), READ_E1)
        self.assertEqual(row_block(report, "E-2"), READ_E2)


if __name__ == "__main__":
    import unittest
    unittest.main()
