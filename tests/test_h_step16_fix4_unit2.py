"""Step 16 fix pass 4 unit 2 tests: the Q-3 unit.

Pinning tests for register items R16-4-03 (High, B4-01) and
the Q-3 part of R16-4-12 (Low, B4-10) of Step 16 round 4.
The governing rule of the pass: a piece not read in full, for
whatever reason, is not read. Where a register the Q-3 figure
rests on stands not read in full, Q-3 stands present but not
derivable naming the piece and the bound or the state, and
no measured zero or figure is claimed over it; the shows
text of the governed single register row asserts nothing
over the not read register. The measured zero form stands
only where every register stands read in full and holds no
entries.

Three defect forms stand pinned: the two register form of
spin 1137 Attack 3 (a defect register carrying Entry D1 and
Entry D2 and a fix register carrying Entry F1, each padded
over the file limit and unread, standing present at a
measured zero byte identical to the empty read form), its
variant with one register unread beside one empty register
read in full, and the single register shows text form (one
defect register carrying two entries, padded over the file
limit and unread, no fix register in the tree, standing
present but not derivable while its record shows text states
that a register stands and holds no entries). Held controls
stand pinned beside them, byte for byte: the read control of
the same registers read in full carrying the same three
entries, standing present at 1 escape per step for Steps 1,
2 and 3; the true measured zero, the same registers standing
empty and read in full; the missing form, no register
standing anywhere in the tree; and the cured neighbour row
E-3 in the read control report shape.

Trees are written through the Unit 1 module helpers of fix
pass 1, because the constructions turn on exact byte counts.
The product is invoked through run_tool, which runs the
module entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, row_block, run_tool)
from tests.test_h_step16_fix3_unit1 import _clean_files
from tests.test_h_step16_unit1 import _padded, _write_tree

DEFECT_REGISTER = ("# Defect register\n\nEntry D1: Origin "
                   "step: Step 1.\n\nEntry D2: Origin step: "
                   "Step 2.\n")
FIX_REGISTER = ("# Fix register\n\nEntry F1: Origin step: "
                "Step 3.\n")
EMPTY_DEFECT_REGISTER = "# Defect register\n\nNo entries stand.\n"
EMPTY_FIX_REGISTER = "# Fix register\n\nNo entries stand.\n"
DEFECT_PATH = "registers/defect-register.md"
FIX_PATH = "registers/fix-register.md"

READ_Q3 = (
    "Q-3 Escaped defects | Verdict: present | Value: Step 1: "
    "1 escapes; Step 2: 1 escapes; Step 3: 1 escapes | Row "
    "coverage: denominator step universe 3 steps | Reconciled "
    "against: the metric carries no total to reconcile "
    "against | Pointer: the fix and defect register entries "
    "(registers/defect-register.md)")

ZERO_Q3 = (
    "Q-3 Escaped defects | Verdict: present | Value: measured "
    "zero escapes; basis: both registers stand and hold no "
    "entries; CA2-10 exposure: the row reads the registers "
    "named in the capture only, and defects recorded outside "
    "those registers are not counted | Row coverage: "
    "denominator step universe 3 steps | Reconciled against: "
    "the metric carries no total to reconcile against | "
    "Pointer: the fix and defect register entries "
    "(registers/defect-register.md)")

MISSING_Q3 = (
    "Q-3 Escaped defects | Verdict: missing | Reason: What "
    "the record shows: no defect register and no fix register "
    "stands in the capture for this metric What follows: "
    "no-feeder-record no feeder record for the metric exists "
    "in the tree, so the row is missing (missing record) | "
    "Pointer: the fix and defect register entries "
    "(registers/defect-register.md)")

READ_E3 = (
    "E-3 Tokens per step | Verdict: present | Value: Step 1 "
    "tokens 1000; Step 2 tokens 2000; Step 3 tokens 3000 | "
    "Row coverage: denominator step universe 3 steps | "
    "Reconciled against: the metric carries no total to "
    "reconcile against | Pointer: registers/cost-ledger.md")


def _entry_files(defect, fix):
    files = _clean_files()
    if defect is not None:
        files[DEFECT_PATH] = defect
    if fix is not None:
        files[FIX_PATH] = fix
    return files


class TestStep16Fix4Unit2(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    # ------------------------------------------------------
    # Defect forms
    # ------------------------------------------------------

    def test_r16_4_03_two_registers_unread_over_file_limit(self):
        """B4-01: a measured zero over two unread registers."""
        files = _entry_files(_padded(DEFECT_REGISTER, 1200097),
                             _padded(FIX_REGISTER, 1200097))
        report = self._run(files)
        q3 = row_block(report, "Q-3")
        assert_verdict(self, q3, "present but not derivable", "Q-3")
        self.assertIn(DEFECT_PATH, q3)
        self.assertIn(FIX_PATH, q3)
        self.assertIn("file limit", q3)
        self.assertNotIn("measured zero escapes", q3)
        self.assertNotIn("hold no entries", q3)
        self.assertNotIn("1 escapes", q3)

    def test_r16_4_03_one_register_unread_one_empty_read(self):
        """B4-01 variant: one unread register, one empty read."""
        files = _entry_files(_padded(DEFECT_REGISTER, 1200097),
                             EMPTY_FIX_REGISTER)
        report = self._run(files)
        q3 = row_block(report, "Q-3")
        assert_verdict(self, q3, "present but not derivable", "Q-3")
        self.assertIn(DEFECT_PATH, q3)
        self.assertIn("file limit", q3)
        self.assertNotIn("measured zero escapes", q3)
        self.assertNotIn("hold no entries", q3)

    def test_r16_4_12_single_register_shows_text(self):
        """B4-10 Q-3 part: shows text over one unread register."""
        files = _entry_files(_padded(DEFECT_REGISTER, 1200097),
                             None)
        report = self._run(files)
        q3 = row_block(report, "Q-3")
        assert_verdict(self, q3, "present but not derivable", "Q-3")
        self.assertIn(DEFECT_PATH, q3)
        self.assertIn("file limit", q3)
        self.assertNotIn("holds no entries", q3)
        self.assertNotIn("a register stands and holds", q3)
        self.assertNotIn("measured zero escapes", q3)

    # ------------------------------------------------------
    # Held controls
    # ------------------------------------------------------

    def test_r16_4_held_read_control_byte_for_byte(self):
        """Read control: the same entries read in full."""
        files = _entry_files(DEFECT_REGISTER, FIX_REGISTER)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-3"), READ_Q3)

    def test_r16_4_held_true_zero_byte_for_byte(self):
        """Held control: empty registers read, a true zero."""
        files = _entry_files(EMPTY_DEFECT_REGISTER,
                             EMPTY_FIX_REGISTER)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-3"), ZERO_Q3)

    def test_r16_4_held_missing_byte_for_byte(self):
        """Held control: no register stands anywhere."""
        report = self._run(_clean_files())
        self.assertEqual(row_block(report, "Q-3"), MISSING_Q3)

    def test_r16_4_held_cured_neighbour_e3_byte_for_byte(self):
        """Held control: E-3 in the read control report shape."""
        files = _entry_files(DEFECT_REGISTER, FIX_REGISTER)
        report = self._run(files)
        self.assertEqual(row_block(report, "E-3"), READ_E3)


if __name__ == "__main__":
    import unittest
    unittest.main()
