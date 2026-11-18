"""Step 16 fix pass 5 unit 1 tests: the cost family.

Pinning tests for register items R16-5-01 (High, E-3),
R16-5-03 (Medium, E-4) and R16-5-04 (Medium, B-2) of Step 16
round 5. All three items stand on one shared locus, the
unread list of _ledger_data in derivation_core.py, which
collects only pieces standing not read past a limit, so a
damaged cost ledger stands in no unread list. The governing
rule of the pass: a piece not read in full, for whatever
reason, is not read. A cost ledger damaged by a TRUNCATED
marker, or standing as invalid UTF-8 bytes, carrying its
full figures in its file bytes, must take every cost row to
present but not derivable naming the ledger piece and its
state: E-3 must never stand missing over it, E-4 must never
state in its held text that no feeder states a per step
money figure over it, and B-2 must never state in its shows
text that the ledger carries no spent or budget figure over
it.

Six defect forms stand pinned, one per row per damage form.
Held controls stand pinned beside them: the read control of
the same ledger read in full, one test per row, standing
present at the register figures, and the over limit held
neighbour, one test per row, standing in the cured form of
round 1 naming the ledger piece and the file limit.

Trees are written through the Unit 1 module helpers of fix
pass 1, because the constructions turn on exact byte counts
and file byte forms. The product is invoked through
run_tool, which runs the module entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, row_block, run_tool)
from tests.test_h_step16_unit1 import (
    LEDGER_FULL, LEDGER_PATH, _base_files, _padded, _write_tree)

MALFORMED_LEDGER = LEDGER_FULL.encode("utf-8") + b"\xff\xfe\xfd\n"
TRUNCATED_LEDGER = LEDGER_FULL + "TRUNCATED\n"


class TestStep16Fix5Unit1(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    def _damaged_files(self, ledger):
        files = _base_files()
        files[LEDGER_PATH] = ledger
        return files

    def _assert_e3_damaged(self, report, state_word):
        block = row_block(report, "E-3")
        assert_verdict(self, block, "present but not derivable", "E-3")
        self.assertIn(LEDGER_PATH, block)
        self.assertIn(state_word, block.lower())
        self.assertNotIn("no token figure stands in it", block)
        self.assertNotIn(
            "no token figure stands in any feeder record", block)
        self.assertNotIn("no-feeder-record", block)

    def _assert_e4_damaged(self, report, state_word):
        block = row_block(report, "E-4")
        assert_verdict(self, block, "present but not derivable", "E-4")
        self.assertIn(LEDGER_PATH, block)
        self.assertIn(state_word, block.lower())
        self.assertNotIn(
            "no feeder states a per step money figure", block)

    def _assert_b2_damaged(self, report, state_word):
        block = row_block(report, "B-2")
        assert_verdict(self, block, "present but not derivable", "B-2")
        self.assertIn(LEDGER_PATH, block)
        self.assertIn(state_word, block.lower())
        self.assertNotIn("carries no spent or budget figure", block)
        self.assertNotIn(
            "no spent or budget figure for either side", block)

    # ------------------------------------------------------
    # Defect forms, R16-5-01, row E-3
    # ------------------------------------------------------

    def test_r16_5_01_e3_truncated_ledger(self):
        """R16-5-01 truncated form: E-3 missing over damage."""
        report = self._run(self._damaged_files(TRUNCATED_LEDGER))
        self._assert_e3_damaged(report, "truncated")

    def test_r16_5_01_e3_malformed_ledger(self):
        """R16-5-01 malformed form: E-3 missing over damage."""
        report = self._run(self._damaged_files(MALFORMED_LEDGER))
        self._assert_e3_damaged(report, "malformed")

    # ------------------------------------------------------
    # Defect forms, R16-5-03, row E-4
    # ------------------------------------------------------

    def test_r16_5_03_e4_truncated_ledger(self):
        """R16-5-03 truncated form: E-4 held claim over damage."""
        report = self._run(self._damaged_files(TRUNCATED_LEDGER))
        self._assert_e4_damaged(report, "truncated")

    def test_r16_5_03_e4_malformed_ledger(self):
        """R16-5-03 malformed form: E-4 held claim over damage."""
        report = self._run(self._damaged_files(MALFORMED_LEDGER))
        self._assert_e4_damaged(report, "malformed")

    # ------------------------------------------------------
    # Defect forms, R16-5-04, row B-2
    # ------------------------------------------------------

    def test_r16_5_04_b2_truncated_ledger(self):
        """R16-5-04 truncated form: B-2 shows claim over damage."""
        report = self._run(self._damaged_files(TRUNCATED_LEDGER))
        self._assert_b2_damaged(report, "truncated")

    def test_r16_5_04_b2_malformed_ledger(self):
        """R16-5-04 malformed form: B-2 shows claim over damage."""
        report = self._run(self._damaged_files(MALFORMED_LEDGER))
        self._assert_b2_damaged(report, "malformed")

    # ------------------------------------------------------
    # Read controls, the same ledger read in full
    # ------------------------------------------------------

    def test_r16_5_held_e3_read_control(self):
        """Read control: E-3 present at the register figures."""
        report = self._run(self._damaged_files(LEDGER_FULL))
        block = row_block(report, "E-3")
        assert_verdict(self, block, "present", "E-3")
        self.assertIn("Step 1 tokens 1000", block)
        self.assertIn("Step 2 tokens 2000", block)
        self.assertIn("Step 3 tokens 3000", block)

    def test_r16_5_held_e4_read_control(self):
        """Read control: E-4 present at the register figures."""
        report = self._run(self._damaged_files(LEDGER_FULL))
        block = row_block(report, "E-4")
        assert_verdict(self, block, "present", "E-4")
        self.assertIn("Step 1 money 10", block)
        self.assertIn("Step 2 money 20", block)
        self.assertIn("Step 3 money 30", block)

    def test_r16_5_held_b2_read_control(self):
        """Read control: B-2 present at the register figures."""
        report = self._run(self._damaged_files(LEDGER_FULL))
        block = row_block(report, "B-2")
        assert_verdict(self, block, "present", "B-2")
        self.assertIn(
            "money spent 60 against a money budget of 100", block)
        self.assertIn(
            "token spent 6000 against a token budget of 10000",
            block)

    # ------------------------------------------------------
    # Over limit held neighbours, cured from round 1
    # ------------------------------------------------------

    def test_r16_5_held_e3_over_limit_ledger(self):
        """Held neighbour: E-3 over limit form stands cured."""
        files = self._damaged_files(_padded(LEDGER_FULL, 1200097))
        report = self._run(files)
        block = row_block(report, "E-3")
        assert_verdict(self, block, "present but not derivable", "E-3")
        self.assertIn(LEDGER_PATH, block)
        self.assertIn("file limit", block)
        self.assertNotIn("no token figure stands in it", block)

    def test_r16_5_held_e4_over_limit_ledger(self):
        """Held neighbour: E-4 over limit form stands cured."""
        files = self._damaged_files(_padded(LEDGER_FULL, 1200097))
        report = self._run(files)
        block = row_block(report, "E-4")
        assert_verdict(self, block, "present but not derivable", "E-4")
        self.assertIn(LEDGER_PATH, block)
        self.assertIn("file limit", block)
        self.assertNotIn(
            "no feeder states a per step money figure", block)

    def test_r16_5_held_b2_over_limit_ledger(self):
        """Held neighbour: B-2 over limit form stands cured."""
        files = self._damaged_files(_padded(LEDGER_FULL, 1200097))
        report = self._run(files)
        block = row_block(report, "B-2")
        assert_verdict(self, block, "present but not derivable", "B-2")
        self.assertIn(LEDGER_PATH, block)
        self.assertIn("file limit", block)
        self.assertNotIn("carries no spent or budget figure", block)


if __name__ == "__main__":
    import unittest
    unittest.main()
