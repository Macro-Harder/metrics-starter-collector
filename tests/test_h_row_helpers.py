"""Direct tests for the shared row extraction rule.

The sample report below uses prefixed Markdown rows, the settled
report row form the extraction rule is tied to. The negative case
proves that text from the next row stands outside the block the rule
returns for the row before it.
"""
import unittest

from tests.fixture_builder import FixtureTestCase, row_block, row_verdict

SAMPLE_REPORT = (
    "# Report\n"
    "\n"
    "Coverage statement: the tree stands read.\n"
    "\n"
    "| T-1 | missing | date-only-form | PATH-LEDGER.md |\n"
    "| T-2 | missing | date-only-form | PATH-LEDGER.md |\n"
    "- E-1 | present | figure 2 of 1 | steps/step-01-record.md |\n"
    "E-2 | present but not derivable | missing-field | "
    "steps/step-03-record.md | marker NEXTROWONLY\n"
    "Q-4 | present | figure 8 of 10 | steps/step-01-trace.md |\n"
    "\n"
    "## Data quality\n"
    "\n"
    "No entry.\n"
)


class TestRowHelpers(FixtureTestCase):

    def test_row_block_isolates_prefixed_markdown_rows(self):
        block = row_block(SAMPLE_REPORT, "E-1")
        self.assertIn("2 of 1", block)
        self.assertEqual(row_verdict(block), "present")
        t1 = row_block(SAMPLE_REPORT, "T-1")
        self.assertEqual(row_verdict(t1), "missing")
        e2 = row_block(SAMPLE_REPORT, "E-2")
        self.assertEqual(row_verdict(e2), "present but not derivable")

    def test_row_block_excludes_next_row_text(self):
        block = row_block(SAMPLE_REPORT, "E-1")
        self.assertNotIn("NEXTROWONLY", block)
        self.assertNotIn("missing-field", block)
        e2 = row_block(SAMPLE_REPORT, "E-2")
        self.assertIn("NEXTROWONLY", e2)
        self.assertNotIn("8 of 10", e2)


if __name__ == "__main__":
    unittest.main()
