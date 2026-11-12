"""Slice 2 capture integrity tests: piece states, limits, links, walk order."""
import os
import re
import unittest
from pathlib import Path

from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree,
                                     coverage_statement,
                                     data_quality_entry_for, link_tree,
                                     metrics_record, piece_entry_for,
                                     row_block, run_tool, step_record)


def pieces_recognised_count(report):
    match = re.search(r"(\d+)\s+pieces recognised", report)
    return int(match.group(1)) if match else None


class TestSlice2Capture(FixtureTestCase):

    def test_f10_malformed_non_utf8_piece(self):
        table = base_case()
        table["steps/step-02-record.md"] = b"\xff\xfe\x00 not utf8 \x80\x81"
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("malformed", result.stdout.lower())
        self.assertIn("step-02-record.md", result.stdout)

    def test_f10_malformed_piece_reason_code(self):
        table = base_case()
        table["steps/step-02-record.md"] = b"\xff\xfe\x00 not utf8 \x80\x81"
        root = build_tree(table)
        result = run_tool(root)
        self.assertIn("malformed-piece", result.stdout)

    def test_f11_tree_over_file_size_limit(self):
        table = base_case()
        table["steps/step-02-record.md"] = "x" * 1000001
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("over limit", result.stdout.lower())
        self.assertIn("over-limit-piece", result.stdout)
        entry = piece_entry_for(result.stdout, "step-02-record.md")
        self.assertIn("over limit", entry.lower())

    def test_f11_tree_over_line_limit(self):
        table = base_case()
        table["steps/step-02-record.md"] = "y" * 65537
        root = build_tree(table)
        result = run_tool(root)
        entry = piece_entry_for(result.stdout, "step-02-record.md")
        self.assertTrue(entry)
        self.assertIn("over limit", entry.lower())
        self.assertIn("over-limit-piece", result.stdout)
        self.assertIn("step-02-record.md", result.stdout)

    def test_f11_tree_over_tree_byte_limit(self):
        # Intended tree size arithmetic: 30 recognised step records of
        # 900,000 bytes each give a record part of 27,000,000 bytes,
        # over the 25,000,000 byte record part tree limit, with every
        # file under the 1,000,000 byte single file limit.
        table = base_case(steps=tuple(range(1, 31)))
        for n in range(1, 31):
            table["steps/step-%02d-record.md" % n] = "z" * 900000
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout.replace(",", ""), r"270\d{5}")
        self.assertRegex(result.stdout.replace(",", ""),
                         r"(?<!\d)25000000(?!\d)")
        cov = coverage_statement(result.stdout)
        self.assertIn("not read", cov.lower())
        self.assertIn("step-30-record.md", cov)

    def test_f11_tree_over_file_count_limit(self):
        # Record part file count limit: 2,005 gate records stand in
        # the record part, over the 2,000 file limit.
        table = base_case(steps=(1,))
        for n in range(1, 2006):
            table["steps/step-%04d-gate-record.md" % n] = (
                "# Step %d gate record\n\nClosure state: CLOSED-PASS.\n" % n)
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, r"(?<!\d)(?<!\d\.)2000(?!\d)(?!\.\d)")
        cov = coverage_statement(result.stdout)
        self.assertIn("not read", cov.lower())
        self.assertIn("step-2005-gate-record.md", cov)

    def test_f15_near_match_names_listed_unrecognised_not_read(self):
        table = base_case()
        table["steps/step-01-records.md"] = step_record(1)
        table["DECISION-QUEU.md"] = "# Near match queue\n"
        root = build_tree(table)
        result = run_tool(root)
        self.assertIn("unrecognised", result.stdout.lower())
        self.assertIn("step-01-records.md", result.stdout)
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "missing", "D-1")

    def test_f15_near_match_nearest_pattern_note(self):
        table = base_case()
        table["steps/step-09-records.md"] = step_record(9)
        root = build_tree(table)
        result = run_tool(root)
        entry = piece_entry_for(result.stdout, "step-09-records.md")
        self.assertTrue(entry)
        self.assertIn("step-09-record.md", entry)

    def test_w10_2_feeder_name_outside_lists_counts_not_found(self):
        table = base_case()
        table["QUEUE-DECISIONS-FINAL.md"] = (
            "# A feeder under a name form outside the closed lists\n\n"
            "| Item | Origin step | Raised | Presented | Ruled |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| X-1 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | 2026-11-01 12:00 |\n")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("unrecognised", result.stdout.lower())
        self.assertIn("QUEUE-DECISIONS-FINAL.md", result.stdout)
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "missing", "D-1")

    def test_f15b_duplicate_identity_differing_content(self):
        table = base_case()
        table["steps/step-01-record.md"] = step_record(
            1, base=2, team=3,
            extra="Original content marker ORIGONLY stands here.")
        table["copy/step-01-record.md"] = step_record(
            1, base=2, team=99,
            extra="Duplicate content marker DUPONLY99 stands here.")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("steps/step-01-record.md", result.stdout)
        self.assertIn("copy/step-01-record.md", result.stdout)
        entry = piece_entry_for(result.stdout, "step-01-record.md")
        self.assertIn("not read in full", entry.lower())
        self.assertIn("duplicate", entry.lower())
        self.assertIn("disagreement", entry.lower())
        block = row_block(result.stdout, "E-1")
        self.assertNotIn("99", block)
        self.assertNotIn("DUPONLY99", block)
        self.assertNotIn("ORIGONLY", block)
        self.assertNotIn("3 of 2", block)
        # The duplicate piece is counted once: the pieces recognised
        # count on the duplicate tree equals the count on the same
        # tree without the copy, so a product counting the piece
        # twice raises the count and fails here.
        single_table = dict(table)
        del single_table["copy/step-01-record.md"]
        single_root = build_tree(single_table)
        single_result = run_tool(single_root)
        self.assertEqual(single_result.returncode, 0, single_result.stderr)
        self.assertIsNotNone(pieces_recognised_count(result.stdout))
        self.assertEqual(pieces_recognised_count(result.stdout),
                         pieces_recognised_count(single_result.stdout))

    def test_split_page_damaged_supplies_no_tables(self):
        table = base_case()
        del table["wiki/wiki/synthesis/build-metrics-record.md"]
        table["wiki/wiki/synthesis/build-metrics-record-part-1.md"] = (
            b"\xff\xfe damaged split page \x80")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "missing", "D-1")
        table2 = base_case()
        del table2["wiki/wiki/synthesis/build-metrics-record.md"]
        table2["wiki/wiki/synthesis/build-metrics-record-part-1.md"] = (
            "x" * 1000001)
        root2 = build_tree(table2)
        result2 = run_tool(root2)
        self.assertEqual(result2.returncode, 0, result2.stderr)
        block2 = row_block(result2.stdout, "D-1")
        assert_verdict(self, block2, "missing", "D-1")
        self.assertIn("over limit", result2.stdout.lower())

    def test_link_traversal_outside_root_not_followed(self):
        outside_root = build_tree({"outside.md": "outside the root\n"})
        root = build_tree(base_case())
        os.symlink(str(outside_root / "outside.md"),
                   str(root / "steps" / "linked.md"))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("outside the root", result.stdout)

    def test_link_target_inside_root_followed_at_most_once(self):
        base_root = build_tree(base_case())
        base_result = run_tool(base_root)
        self.assertEqual(base_result.returncode, 0, base_result.stderr)
        base_count = pieces_recognised_count(base_result.stdout)
        self.assertIsNotNone(base_count)
        root = build_tree(base_case())
        os.symlink(str(root / "steps" / "step-01-record.md"),
                   str(root / "steps" / "step-01-record-link.md"))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("step-01-record-link.md", result.stdout)
        self.assertEqual(pieces_recognised_count(result.stdout), base_count)

    def test_whole_walk_bound_names_crossing(self):
        table = {}
        for n in range(10050):
            table["bulk/file-%05d.txt" % n] = "bulk\n"
        table.update(base_case(steps=(1,)))
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, r"(?<!\d)(?<!\d\.)10000(?!\d)(?!\.\d)")
        self.assertIn("not visited", result.stdout.lower())
        cov = coverage_statement(result.stdout)
        self.assertRegex(cov, r"(?<!\d)(?<!\d\.)10000(?!\d)(?!\.\d)")
        self.assertIn("not visited", cov.lower())

    def test_a7_4_walk_order_sample_where_limit_cuts_capture(self):
        table = base_case()
        table["steps/step-03-record.md"] = "x" * 1000001
        root = build_tree(table)
        result = run_tool(root)
        entry = data_quality_entry_for(result.stdout, "step-03-record.md")
        self.assertTrue(entry)
        self.assertTrue("1000000" in entry.replace(",", "") or
                        "file limit" in entry.lower(), entry[:400])
        self.assertIn("step-03-record.md", entry)
        self.assertIn("bias", entry.lower())
        first_at = entry.find("steps/step-01-record.md")
        second_at = entry.find("steps/step-02-record.md")
        self.assertTrue(0 <= first_at < second_at,
                        "sampled entries not in sorted relative path order")

    def test_unreadable_piece_marked_and_run_continues(self):
        table = base_case()
        root = build_tree(table)
        target = root / "steps" / "step-02-record.md"
        target.unlink()
        target.mkdir()
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = piece_entry_for(result.stdout, "step-02-record.md")
        self.assertTrue(entry)
        self.assertIn("unreadable", entry.lower())
        self.assertIn("unreadable-piece", entry)

    def test_piece_quality_stated_apart_from_verdict(self):
        table = base_case()
        table["steps/step-02-record.md"] = b"\xff\xfe\x00 bad \x80"
        root = build_tree(table)
        result = run_tool(root)
        self.assertIn("data quality", result.stdout.lower())
        self.assertIn("malformed", result.stdout.lower())
        entry = piece_entry_for(result.stdout, "step-02-record.md")
        self.assertIn("malformed", entry.lower())


if __name__ == "__main__":
    unittest.main()
