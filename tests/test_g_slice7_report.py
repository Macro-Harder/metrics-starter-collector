"""Slice 7 tests: report completeness, determinism, read only surface."""
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

from tests.fixture_builder import (REPO_ROOT, STARTER_ORDER, FixtureTestCase,
                                     assert_verdict, base_case, build_tree,
                                     header_region, manifest, metrics_record,
                                     row_block, row_order, run_tool)
from tests.test_c_slice3_staffing import assert_wv4_disputed_form, wv4_table


class TestSlice7Report(FixtureTestCase):

    def test_f01_clean_tree_report_complete(self):
        root = build_tree(base_case())
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(row_order(result.stdout), STARTER_ORDER)
        self.assertIn("data quality", result.stdout.lower())

    def test_f08_sparse_tree_under_floor_no_usable_records(self):
        root = build_tree({"random.txt": "not a record\n",
                           "notes.txt": "plain notes\n"})
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("no usable records", result.stdout.lower())
        self.assertEqual(row_order(result.stdout), [])

    def test_f09_sparse_tree_just_over_floor_gets_17_rows(self):
        root = build_tree({"steps/step-01-record.md":
                           "# Step 1 record\n\nBuild: fixture build.\n"})
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(row_order(result.stdout), STARTER_ORDER)

    def test_f15_split_metrics_record_single_page_precedence_whole(self):
        table = base_case()
        table["wiki/wiki/synthesis/build-metrics-record-part-1.md"] = (
            "# Split copy\n\nSplit copy states Q-4 as 1 of 99.\n")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("1 of 99", row_block(result.stdout, "Q-4"))

    def test_determinism_two_runs_byte_identical(self):
        root = build_tree(base_case())
        first = run_tool(root)
        second = run_tool(root)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first.returncode, second.returncode)

    def test_determinism_under_different_timezone_byte_identical(self):
        root = build_tree(base_case())
        first = run_tool(root)
        shifted = run_tool(root, env_extra={"TZ": "Pacific/Kiritimati"})
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, shifted.stdout)

    def test_w10_5_determinism_under_c_locale_byte_identical(self):
        root = build_tree(base_case())
        first = run_tool(root)
        plain_c = run_tool(root, env_extra={"LC_ALL": "C", "LANG": "C"})
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, plain_c.stdout)

    def test_read_only_manifest_stdout_run(self):
        root = build_tree(base_case())
        before = manifest(root)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(manifest(root), before)

    def test_read_only_manifest_named_file_outside_tree(self):
        root = build_tree(base_case())
        before = manifest(root)
        dest = Path(root).parent / "report_outside.md"
        result = run_tool(root, extra=("--report", str(dest)))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(dest.is_file())
        self.assertEqual(manifest(root), before)

    def test_inside_tree_destination_refused_relative_form(self):
        root = build_tree(base_case())
        before = manifest(root)
        result = run_tool(root, extra=("--report", "inside.md"),
                          cwd=str(root))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(manifest(root), before)
        self.assertFalse((root / "inside.md").exists())

    def test_inside_tree_destination_refused_parent_segments(self):
        root = build_tree(base_case())
        before = manifest(root)
        sneaky = str(root / "steps" / ".." / "inside2.md")
        result = run_tool(root, extra=("--report", sneaky))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(manifest(root), before)

    def test_inside_tree_destination_refused_through_link(self):
        root = build_tree(base_case())
        before = manifest(root)
        link_dir = Path(root).parent / "linkdir"
        os.symlink(str(root), str(link_dir))
        result = run_tool(root, extra=("--report",
                                       str(link_dir / "inside3.md")))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(manifest(root), before)

    def test_inside_tree_destination_refused_root_itself(self):
        root = build_tree(base_case())
        before = manifest(root)
        result = run_tool(root, extra=("--report", str(root)))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(manifest(root), before)

    def test_delivery_failure_parent_directory_does_not_stand(self):
        root = build_tree(base_case())
        dest = Path(root).parent / "no_such_dir" / "report.md"
        result = run_tool(root, extra=("--report", str(dest)))
        self.assertEqual(result.returncode, 2)
        self.assertFalse(dest.exists())
        self.assertFalse(dest.parent.exists())
        self.assertTrue(result.stderr.strip())

    def test_delivery_failure_named_file_cannot_be_written(self):
        root = build_tree(base_case())
        dest = Path(root).parent / "blocked.md"
        if Path("/dev/full").exists():
            os.symlink("/dev/full", str(dest))
            result = run_tool(root, extra=("--report", str(dest)))
            self.assertEqual(result.returncode, 2)
            self.assertTrue(dest.is_symlink())
            self.assertEqual(os.readlink(str(dest)), "/dev/full")
        else:
            dest.mkdir()
            marker = dest / "prior.txt"
            marker.write_text("prior content\n", encoding="utf-8")
            result = run_tool(root, extra=("--report", str(dest)))
            self.assertEqual(result.returncode, 2)
            self.assertEqual(marker.read_text(encoding="utf-8"),
                             "prior content\n")
        self.assertTrue(result.stderr.strip())
        self.assertTrue("blocked.md" in result.stderr or
                        "report" in result.stderr.lower(), result.stderr)

    def test_delivery_failure_stdout_closes_during_printing(self):
        root = build_tree(base_case())
        full = open("/dev/full", "wb")
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "metrics_starter_collector",
                 str(root)],
                stdout=full, stderr=subprocess.PIPE, text=True,
                cwd=str(REPO_ROOT), timeout=120)
        finally:
            full.close()
        self.assertEqual(proc.returncode, 2)
        self.assertTrue(proc.stderr.strip())
        # Error context must name the delivery failure itself: the
        # delivery wording, the output destination, or the write
        # failure the full device raises. No limb stands that a run
        # could satisfy incidentally.
        self.assertTrue("deliver" in proc.stderr.lower() or
                        "stdout" in proc.stderr.lower() or
                        "standard output" in proc.stderr.lower() or
                        "no space" in proc.stderr.lower(), proc.stderr)

    def test_full_set_order_denominators_coverage_no_score(self):
        root = build_tree(base_case())
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(row_order(result.stdout), STARTER_ORDER)
        for code in STARTER_ORDER:
            block = row_block(result.stdout, code)
            self.assertTrue(block, code)
            self.assertIn("denominator", block.lower(), code)
        e1 = row_block(result.stdout, "E-1")
        self.assertRegex(e1, r"(denominator[^\d]*3(?!\d)(?!\.\d)|of 3 steps\b)")
        lowered = result.stdout.lower()
        self.assertNotRegex(lowered, r"\bscore\b")
        self.assertNotRegex(lowered, r"\bgrade\b")
        self.assertIn("coverage", lowered)
        self.assertIn("data quality", lowered)

    def test_header_identity_first_lines_in_order(self):
        root = build_tree(base_case())
        result = run_tool(root)
        head = header_region(result.stdout)
        lines = [ln for ln in head.splitlines() if ln.strip()]
        self.assertTrue(lines)
        def line_at(fragment):
            for idx, ln in enumerate(lines):
                if fragment.lower() in ln.lower():
                    return idx
            return -1
        root_at = line_at(str(root))
        if root_at < 0:
            root_at = 0 if str(root) in head else -1
        build_at = line_at("metrics fixture build")
        universe_at = line_at("step universe")
        pieces_at = line_at("pieces recognised")
        self.assertTrue(0 <= root_at < build_at < universe_at < pieces_at,
                        head[:600])
        all_lines = result.stdout.splitlines()
        live_idx = next((i for i, ln in enumerate(all_lines)
                         if "live" in ln.lower()), -1)
        row_idx = next((i for i, ln in enumerate(all_lines)
                        if ln.strip().lstrip("|#-*> ").startswith("T-1")),
                       -1)
        self.assertTrue(0 <= live_idx < row_idx,
                        "live line does not stand before the first row")

    def test_header_not_yet_recordable_kept_apart_from_not_found(self):
        table = base_case()
        table["registers/changes.md"] = (
            "# Record changes\n\nThe origin step field record change is "
            "not in force for this build.\n")
        root = build_tree(table)
        result = run_tool(root)
        head = header_region(result.stdout)
        nyr = [ln for ln in head.splitlines()
               if "not yet recordable" in ln.lower()]
        nf = [ln for ln in head.splitlines()
              if "not found" in ln.lower()
              and "not yet recordable" not in ln.lower()]
        self.assertTrue(nyr, head[:600])
        self.assertTrue(nf, head[:600])
        self.assertTrue(any(re.search(r"\d+", ln) for ln in nyr), nyr)
        self.assertTrue(any(re.search(r"\d+", ln) for ln in nf), nf)
        self.assertNotEqual(nyr[0], nf[0])

    def test_header_near_matches_never_counted_as_found(self):
        table = base_case()
        table["steps/step-01-records.md"] = "# Near match\n"
        root = build_tree(table)
        result = run_tool(root)
        self.assertIn("unrecognised", result.stdout.lower())
        self.assertIn("step-01-records.md", result.stdout)

    def test_suite_run_record_form_states_interpreter_platform_locale(self):
        record_path = Path(__file__).resolve().parent / "suite_run_record.txt"
        self.assertTrue(record_path.is_file(),
                        "suite run record artifact stands in the suite")
        text = record_path.read_text(encoding="utf-8")
        fields = {}
        for line in text.splitlines():
            if ":" in line and not line.startswith("Command"):
                key, _, value = line.partition(":")
                fields[key.strip().lower()] = value.strip()
        interp = None
        for line in text.splitlines():
            if line.startswith("Interpreter:"):
                interp = line.split(":", 1)[1].strip()
        self.assertTrue(interp, "full interpreter version string stands")
        self.assertRegex(interp, r"^\d+\.\d+\.\d+")
        self.assertIn("pinned", " ".join(fields.keys()).lower() + text.lower())
        self.assertIn("Python 3.12", text)
        major_minor = ".".join(interp.split(".")[:2])
        self.assertIn("Python " + major_minor, text)
        self.assertTrue(fields.get("platform"), "platform field stands")
        self.assertTrue(fields.get("locale"), "locale field stands")
        self.assertIn("LC_CTYPE", text)
        self.assertTrue(fields.get("filesystem encoding"),
                        "filesystem encoding field stands")

    def test_wv4_disputed_count_rerun_against_completed_header(self):
        root = build_tree(wv4_table())
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        assert_wv4_disputed_form(self, result)


if __name__ == "__main__":
    unittest.main()
