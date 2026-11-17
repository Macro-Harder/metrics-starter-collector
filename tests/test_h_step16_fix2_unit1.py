"""Step 16 fix pass 2 unit 1 tests: the R16-02 staffing limbs.

Pinning tests for register item R16-2-01 of Step 16 round 2, a
reopening of R16-02 in its staffing limbs (spin 1123, finding
B2-01, Medium). Where no read feeder supplies a staffed and base
pair or a labelled quantity, the E-1 no pair branch and the E-2
no quantity branch assert the contents of staffing pieces that
were never read, that no step carries both fields, that no
record states a total, and name no bound, no piece and no
limit; and the E-1 excepted branch for a step whose only feeder
stands unread misdescribes that unread record as listing
staffing with no base count. The cure these tests pin, in the
form Unit 1 of fix pass 1 gave the ledger rows: where a staffing
piece the row rests on stands unread past a limit, the row
stands present but not derivable with the bound and the piece
named, and no absence is asserted over the unread piece.

Three defect forms stand pinned, one per proven construction of
spin 1123: the round 1 case 1a construction on the tree byte
route, every step record and roster artifact over limit and not
read; the walk bound construction of Attack 2 seam 8, the cut
falling exactly on steps/step-01-record.md; and the combined
construction of Attack 2 seam 1, the Step 2 record unread over
the file limit beside a missing Step 2 roster, where the
excepted branch misdescribes the unread record and E-2 omits
the Step 2 position altogether.

Held controls stand pinned beside them: the ledger limbs of
R16-02 as Unit 1 left them, byte for byte in the affected rows
on the case 1a construction and on the walk bound directory
construction of spin 1122 section 6; the form where no staffing
piece stands in the capture at all, where E-1 and E-2 stand
missing with no bound claim invented; the case 1c first form,
where remaining steps supply pairs and totals and the cured
bound naming stands as Unit 1 left it; a piece at exactly
1,000,000 bytes read in full; and the read staffing form, where
the staffing pieces stand read and the standing E-1 and E-2
statements stand byte for byte as they stood.

Trees are written through the Unit 1 module helpers because the
constructions turn on exact byte counts and walk positions.
The product is invoked through run_tool, which runs the module
entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, row_block, run_tool,
    step_record)
from tests.test_h_step16_unit1 import (
    LEDGER_FULL, LEDGER_PATH, _add_filler, _base_files, _padded,
    _roster_files, _write_tree)

FILE_LIMIT = 1000000

LEDGER_E3_CASE1A = (
    "E-3 Tokens per step | Verdict: present but not derivable | "
    "Reason: What the record shows: broken link, the cost ledger "
    "token figure field in registers/cost-ledger.md, which stands "
    "not read past the limit named in its capture reason (not "
    "producible); form required, a cost ledger read in full, "
    "carrying its token figures; form held, the cost ledger "
    "stands in the tree at registers/cost-ledger.md, which stands "
    "not read past a limit: not read: the tree byte limit "
    "25000000 bytes was crossed, with a record part total of "
    "26731219 bytes in 40 files, and this piece stands past the "
    "limit in walk order What follows: over-limit-piece the row "
    "rests on a piece that was not read past the bound named, so "
    "the row is present but not derivable; missing stands "
    "reserved for the case where no feeder record stands in the "
    "tree, and no token figure is claimed absent from a piece "
    "that was not read | Pointer: registers/cost-ledger.md")

LEDGER_E4_CASE1A = (
    "E-4 Money cost per step | Verdict: present but not "
    "derivable | Reason: What the record shows: broken link, the "
    "per step money figure field in the cost ledger at "
    "registers/cost-ledger.md, which stands not read past the "
    "limit named in its capture reason (not producible); form "
    "required, a money figure stated by a feeder for the step "
    "itself, in a cost ledger read in full inside the root or in "
    "a step record position for that step; form held, the cost "
    "ledger stands in the tree at registers/cost-ledger.md, "
    "which stands not read past a limit: not read: the tree byte "
    "limit 25000000 bytes was crossed, with a record part total "
    "of 26731219 bytes in 40 files, and this piece stands past "
    "the limit in walk order, and no per step money figure is "
    "taken from a piece that was not read What follows: "
    "over-limit-piece the row rests on a piece that was not read "
    "past the bound named, so the row is present but not "
    "derivable, and no per step money figure is claimed absent "
    "from a piece that was not read | Pointer: the cost ledger "
    "entry or the step record budget position for each step "
    "counted (registers/cost-ledger.md)")

LEDGER_B2_CASE1A = (
    "B-2 Total cost against budget | Verdict: present but not "
    "derivable | Reason: What the record shows: broken link, the "
    "ledger figure fields for spent and budget in "
    "registers/cost-ledger.md, which stand not read past the "
    "limit named in its capture reason (not producible); form "
    "required, spent and budget figures taken from ledger "
    "feeders inside the root only, on both sides, read in full; "
    "form held, the cost ledger stands in the tree at "
    "registers/cost-ledger.md, which stands not read past a "
    "limit: not read: the tree byte limit 25000000 bytes was "
    "crossed, with a record part total of 26731219 bytes in 40 "
    "files, and this piece stands past the limit in walk order "
    "What follows: over-limit-piece the row rests on a piece "
    "that was not read past the bound named, so the row is "
    "present but not derivable, and no spent or budget figure is "
    "claimed absent from a piece that was not read | Pointer: "
    "the place inside the root where a cost ledger would stand, "
    "stated as looked for and not found, with step records named "
    "as context only (registers/cost-ledger.md)\n"
    "Statement line: build state naming: the build stands in "
    "progress, and no recognised piece states a halt in its own "
    "words")

WALK_BOUND_DETAIL = (
    "not visited: the whole walk bound of 10000 entries was "
    "crossed before this piece was visited, and the piece was "
    "not read")

LEDGER_E3_WALK = (
    "E-3 Tokens per step | Verdict: present but not derivable | "
    "Reason: What the record shows: broken link, the cost ledger "
    "token figure field in registers/cost-ledger.md, which stands "
    "not read past the limit named in its capture reason (not "
    "producible); form required, a cost ledger read in full, "
    "carrying its token figures; form held, the cost ledger "
    "stands in the tree at registers/cost-ledger.md, which stands "
    "not read past a limit: " + WALK_BOUND_DETAIL + " What "
    "follows: over-limit-piece the row rests on a piece that was "
    "not read past the bound named, so the row is present but not "
    "derivable; missing stands reserved for the case where no "
    "feeder record stands in the tree, and no token figure is "
    "claimed absent from a piece that was not read | Pointer: "
    "registers/cost-ledger.md")

LEDGER_E4_WALK = (
    "E-4 Money cost per step | Verdict: present but not "
    "derivable | Reason: What the record shows: broken link, the "
    "per step money figure field in the cost ledger at "
    "registers/cost-ledger.md, which stands not read past the "
    "limit named in its capture reason (not producible); form "
    "required, a money figure stated by a feeder for the step "
    "itself, in a cost ledger read in full inside the root or in "
    "a step record position for that step; form held, the cost "
    "ledger stands in the tree at registers/cost-ledger.md, "
    "which stands not read past a limit: " + WALK_BOUND_DETAIL +
    ", and no per step money figure is taken from a piece that "
    "was not read What follows: over-limit-piece the row rests "
    "on a piece that was not read past the bound named, so the "
    "row is present but not derivable, and no per step money "
    "figure is claimed absent from a piece that was not read | "
    "Pointer: the cost ledger entry or the step record budget "
    "position for each step counted (registers/cost-ledger.md)")

LEDGER_B2_WALK = (
    "B-2 Total cost against budget | Verdict: present but not "
    "derivable | Reason: What the record shows: broken link, the "
    "ledger figure fields for spent and budget in "
    "registers/cost-ledger.md, which stand not read past the "
    "limit named in its capture reason (not producible); form "
    "required, spent and budget figures taken from ledger "
    "feeders inside the root only, on both sides, read in full; "
    "form held, the cost ledger stands in the tree at "
    "registers/cost-ledger.md, which stands not read past a "
    "limit: " + WALK_BOUND_DETAIL + " What follows: "
    "over-limit-piece the row rests on a piece that was not read "
    "past the bound named, so the row is present but not "
    "derivable, and no spent or budget figure is claimed absent "
    "from a piece that was not read | Pointer: the place inside "
    "the root where a cost ledger would stand, stated as looked "
    "for and not found, with step records named as context only "
    "(registers/cost-ledger.md)\n"
    "Statement line: build state naming: the build stands in "
    "progress, and no recognised piece states a halt in its own "
    "words")

READ_E1 = (
    "E-1 Agents staffed against base | Verdict: present | "
    "Value: staffed against base, Steps 1 to 3 in step order: "
    "3 of 2, 3 of 2, 3 of 2 | Row coverage: Steps 1 to 3 as "
    "kept; denominator step universe 3 steps; steps counted: "
    "Step 1, Step 2, Step 3 | Reconciled against: the staffed "
    "and base counts in the step record and roster for each "
    "covered step, with the coverage bound restated here: "
    "covered Steps 1 to 3; remainder none | Pointer: the step "
    "record and roster for each step counted "
    "(steps/step-01-record.md)")

READ_E2 = (
    "E-2 Spin-ups per step | Verdict: present | Value: two "
    "labelled quantities: additions over base, Step 1: 0 and "
    "Step 2: 0 and Step 3: 0, present on Steps 1, 2 and 3 only "
    "and not derivable for the remaining steps; total spins for "
    "the step, Steps 1 to 3 in step order: 4, 4, 4 | Row "
    "coverage: total spins, Steps 1 to 3; additions over base, "
    "Steps 1, 2 and 3 only | Reconciled against: the per step "
    "series of total spins stated in the step records and "
    "rosters for the steps counted | Pointer: the roster and "
    "the step record for each step counted "
    "(steps/step-01-record.md)")


def _case1a_files():
    """The round 1 case 1a tree: every staffing piece unread."""
    files = _base_files()
    files.update(_roster_files())
    files[LEDGER_PATH] = LEDGER_FULL
    _add_filler(files, 26730000)
    return files


def _seam1_files():
    """Attack 2 seam 1: Step 2 record unread, its roster absent."""
    files = _base_files()
    for n in (1, 3):
        files["steps/step-%02d-roster-artifact.md" % n] = (
            "# Step %d roster artifact\n\nNamed agents: 2. "
            "Base: 2.\nRoster additions over base: 0.\n" % n)
    files["steps/step-02-record.md"] = _padded(
        step_record(2), 1200097)
    return files


class TestStep16Fix2Unit1(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    def test_r16_2_01_case1a_no_pair_no_quantity_name_bound(self):
        """B2-01 form 1: case 1a, no pair and no quantity branch."""
        report = self._run(_case1a_files())
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present but not derivable", "E-1")
        self.assertIn("steps/step-01-record.md", e1)
        self.assertIn("tree byte limit", e1)
        self.assertNotIn(
            "no step carries both a staffed count and a base "
            "count", e1)
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present but not derivable", "E-2")
        self.assertIn("steps/step-01-record.md", e2)
        self.assertIn("tree byte limit", e2)
        self.assertNotIn(
            "none states an additions over base figure or a "
            "total spins figure", e2)

    def test_r16_2_01_walk_bound_cut_on_step_record(self):
        """B2-01 form 2: seam 8, the cut on step-01-record.md."""
        files = _base_files()
        files.update(_roster_files())
        files[LEDGER_PATH] = LEDGER_FULL
        for index in range(9993):
            files["zz-filler-%05d.md" % index] = ""
        report = self._run(files)
        self.assertIn(
            "Piece steps/step-01-record.md | step record |",
            report)
        self.assertIn(
            "Coverage piece not read in full: "
            "steps/step-01-record.md | step record | 98 bytes | "
            "over limit | over-limit-piece: not visited: the "
            "whole walk bound of 10000 entries was crossed "
            "before this piece was visited", report)
        e3 = row_block(report, "E-3")
        assert_verdict(self, e3, "present", "E-3")
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present but not derivable", "E-1")
        self.assertIn("steps/step-01-record.md", e1)
        self.assertIn("whole walk bound", e1)
        self.assertNotIn(
            "no step carries both a staffed count and a base "
            "count", e1)
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present but not derivable", "E-2")
        self.assertIn("steps/step-01-record.md", e2)
        self.assertIn("whole walk bound", e2)
        self.assertNotIn(
            "none states an additions over base figure or a "
            "total spins figure", e2)

    def test_r16_2_01_excepted_branch_unread_step_record(self):
        """B2-01 form 3: seam 1, the excepted branch misdescribes."""
        report = self._run(_seam1_files())
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present", "E-1")
        self.assertIn("Step 1: 3 of 2", e1)
        self.assertIn("Step 3: 3 of 2", e1)
        self.assertIn("Bound:", e1)
        bound = e1[e1.find("Bound:"):]
        self.assertIn("steps/step-02-record.md", bound)
        self.assertIn("file limit", bound)
        self.assertNotIn(
            "list staffing with no base count beside it", e1)
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present", "E-2")
        self.assertIn("steps/step-02-record.md", e2)
        self.assertIn("file limit", e2)

    def test_r16_2_held_ledger_rows_case1a_byte_for_byte(self):
        """Held control: the Unit 1 ledger rows on case 1a."""
        report = self._run(_case1a_files())
        self.assertEqual(row_block(report, "E-3"), LEDGER_E3_CASE1A)
        self.assertEqual(row_block(report, "E-4"), LEDGER_E4_CASE1A)
        self.assertEqual(row_block(report, "B-2"), LEDGER_B2_CASE1A)

    def test_r16_2_held_ledger_rows_walk_bound_byte_for_byte(self):
        """Held control: spin 1122 section 6 walk bound ledger rows.

        The construction is the base tree plus 10,050 empty
        directories under audit/, the form on which the naming
        duty for the ledger rows stood discharged by evidence.
        The ledger rows stand byte for byte as Unit 1 left them.
        """
        files = _base_files()
        files.update(_roster_files())
        files[LEDGER_PATH] = LEDGER_FULL
        root = _write_tree(files)
        for index in range(10050):
            (root / "audit" / ("d%05d" % index)).mkdir(
                parents=True, exist_ok=True)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        report = result.stdout
        self.assertEqual(row_block(report, "E-3"), LEDGER_E3_WALK)
        self.assertEqual(row_block(report, "E-4"), LEDGER_E4_WALK)
        self.assertEqual(row_block(report, "B-2"), LEDGER_B2_WALK)

    def test_r16_2_held_no_staffing_piece_stands_missing(self):
        """Held control: no staffing piece stands in the capture.

        This is the no evidence form: no step record and no
        roster artifact stands, so E-1 and E-2 stand missing in
        their standing words and no bound claim is invented over
        a piece that does not stand.
        """
        files = _base_files()
        for path in [path for path in files
                     if path.startswith("steps/")]:
            del files[path]
        files[LEDGER_PATH] = LEDGER_FULL
        report = self._run(files)
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "missing", "E-1")
        self.assertIn(
            "no step record and no roster artifact stands in "
            "the capture for this metric", e1)
        self.assertNotIn("not read past a limit", e1)
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "missing", "E-2")
        self.assertIn(
            "no step record and no roster artifact stands in "
            "the capture for this metric", e2)
        self.assertNotIn("not read past a limit", e2)

    def test_r16_2_held_case1c_remaining_feeders_supply(self):
        """Held control: case 1c first form, as Unit 1 left it."""
        files = _base_files()
        files.update(_roster_files())
        files["steps/step-02-record.md"] = _padded(
            step_record(2), 1200097)
        report = self._run(files)
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present", "E-1")
        self.assertIn("2 of 2", e1)
        self.assertIn("Bound:", e1)
        bound = e1[e1.find("Bound:"):]
        self.assertIn("steps/step-02-record.md", bound)
        self.assertIn("file limit", bound)
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present", "E-2")
        self.assertIn("steps/step-02-record.md", e2)
        self.assertIn("file limit", e2)
        self.assertNotIn(
            "no total spins figure stands for that step", e2)

    def test_r16_2_held_piece_exactly_at_file_limit(self):
        """Held control: a piece at exactly the file limit reads."""
        files = _base_files()
        files["steps/step-02-record.md"] = _padded(
            step_record(2), FILE_LIMIT)
        report = self._run(files)
        self.assertIn(
            "Piece steps/step-02-record.md | step record | "
            "1000000 bytes | read in full", report)
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present", "E-1")

    def test_r16_2_held_read_staffing_rows_byte_for_byte(self):
        """Held control: the read staffing form, unchanged."""
        files = _base_files()
        files.update(_roster_files())
        files[LEDGER_PATH] = LEDGER_FULL
        report = self._run(files)
        self.assertEqual(row_block(report, "E-1"), READ_E1)
        self.assertEqual(row_block(report, "E-2"), READ_E2)


if __name__ == "__main__":
    import unittest
    unittest.main()
