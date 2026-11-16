"""Slice 2 tests: capture integrity and limits.

Every case in this module states, in its first line, the EC point
numbers it asserts from Part 1 of the Step 13 test design record and,
where a capture state gates a feeder field, the WV22 field numbers it
asserts from Part 3 of that record, in the record citation form.

Trees are built through tests.fixture_builder into temporary
directories. The product is invoked through the pre install invocation
route only: a subprocess running python3 -m metrics_starter_collector
from the public repo root, with the root argument first.
"""
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

from tests.fixture_builder import (
    F11_CASES,
    F11_SETTINGS,
    FixtureTestCase,
    build_case,
    build_cases,
    coverage_statement,
    data_quality_entry_for,
    f10_cases,
    measure_tree,
    piece_entry_for,
    row_block,
    slice2_make_case as make_case,
    tracked_tempdir,
)

REPO_ROOT = Path(__file__).resolve().parent.parent

FILE_LIMIT = 1000000
TREE_BYTES_LIMIT = 25000000
TREE_FILES_LIMIT = 2000
LINE_LIMIT = 65536
WALK_LIMIT = 10000


def run_product(root):
    """Invoke the product through the pre install invocation route.

    The command is python3 -m metrics_starter_collector with the root
    argument first, run as a subprocess with the public repo root as
    its working directory, as plan Sections 4 and 9 state.
    """
    cmd = [sys.executable, "-m", "metrics_starter_collector", str(root)]
    return subprocess.run(cmd, capture_output=True, text=True,
                          cwd=str(REPO_ROOT), timeout=300)


def step_record(step, pad=0):
    text = ("# Step %d record\n\nBase: 2. Team staffed: 2 agents. "
            "Total spins: 4.\n" % step)
    if pad:
        text = text + ("x" * pad) + "\n"
    return text


def roster_artifact(step):
    return ("# Step %d roster artifact\n\nNamed agents: 2. Base: 2.\n"
            "Roster additions over base: 0.\n" % step)


def base_files():
    files = {
        "PATH-LEDGER.md": (
            "# Path ledger\n\nSteps stated: 1, 2, 3.\n\n"
            "## Transitions\n\n"
            "Step 1 IN PROGRESS 2026-11-01 09:00, closed "
            "2026-11-01 17:00.\n"
            "Step 2 IN PROGRESS 2026-11-02 09:00, closed "
            "2026-11-02 17:00.\n"
            "Step 3 IN PROGRESS 2026-11-03 09:00, closed "
            "2026-11-03 17:00.\n"),
    }
    for step in (1, 2, 3):
        files["steps/step-%02d-record.md" % step] = step_record(step)
        files["steps/step-%02d-roster-artifact.md" % step] = (
            roster_artifact(step))
    files["steps/step-01-gate-record.md"] = (
        "# Step 1 gate record\n\nClosure state: CLOSED-PASS.\n")
    return files


def build(case):
    scratch = tracked_tempdir("msc_slice2_")
    return build_case(case, scratch)


def pieces_recognised_count(report):
    match = re.search(r"(\d+)\s+pieces recognised", report)
    return int(match.group(1)) if match else None


class TestSlice2Capture(FixtureTestCase):

    def test_contract1_capture_is_one_snapshot(self):
        """EC-47, EC-48. Contract 1: one capture, one report state."""
        root = build(make_case("contract1-snapshot"))
        first = run_product(root)
        self.assertEqual(first.returncode, 0, first.stderr)
        target = root / "steps" / "step-02-record.md"
        target.write_text(step_record(2) + "Changed after capture.\n",
                          encoding="utf-8")
        second = run_product(root)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertNotEqual(first.stdout, second.stdout)
        again = run_product(root)
        self.assertEqual(second.stdout, again.stdout)

    def test_contract1_piece_counted_once_in_inventory(self):
        """EC-23, EC-46. Contract 1: each piece stands once."""
        root = build(make_case("contract1-once"))
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = piece_entry_for(result.stdout, "step-01-record.md")
        self.assertTrue(entry)
        count = pieces_recognised_count(result.stdout)
        self.assertIsNotNone(count)
        measured = measure_tree(root)
        self.assertLessEqual(count, measured["files"])

    def test_malformed_piece_state_and_reason_code(self):
        """EC-20. WV22 Q-1 F1, WV22 Q-1 F2, WV22 Q-1 F3."""
        case = make_case(
            "malformed-round",
            files={"audit/step1-round-record.md": (
                "# Round record, step 1\n\nPost triage severity "
                "breakdown, flow scale: Critical 0, High 1, "
                "Medium 2, Low 3.\n")},
            malformations=(
                {"switch": "M-01",
                 "target": "audit/step1-round-record.md",
                 "target_kind": "AP",
                 "state": "not-valid-text"},))
        root = build(case)
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = piece_entry_for(result.stdout, "step1-round-record.md")
        self.assertTrue(entry)
        self.assertIn("malformed", entry.lower())
        self.assertIn("malformed-piece", result.stdout)
        self.assertIn("data quality", result.stdout.lower())

    def test_f10_pair_malformed_changes_affected_metric_only(self):
        """EC-20. WV22 Q-1 F1. WV22 E-1 F1, WV22 E-1 F2."""
        scratch = tracked_tempdir("msc_slice2_f10_")
        built = build_cases(f10_cases(), scratch)
        sound = run_product(built["f10-sound"])
        damaged = run_product(built["f10-malformed"])
        self.assertEqual(sound.returncode, 0, sound.stderr)
        self.assertEqual(damaged.returncode, 0, damaged.stderr)
        sound_e1 = row_block(sound.stdout, "E-1")
        damaged_e1 = row_block(damaged.stdout, "E-1")
        self.assertEqual(sound_e1, damaged_e1)
        self.assertNotEqual(row_block(sound.stdout, "Q-1"),
                            row_block(damaged.stdout, "Q-1"))
        entry = piece_entry_for(damaged.stdout,
                                "step-01-round-record.md")
        self.assertTrue(entry)
        self.assertIn("malformed", entry.lower())

    def test_truncated_marked_piece_state(self):
        """EC-20. WV22 T-7 F1."""
        case = make_case(
            "truncated-marked",
            files={"audit/step1-red.md": (
                "# Step 1 red paper\n\nRound outcome: the round "
                "closed with findings recorded.\n")},
            malformations=(
                {"switch": "M-02",
                 "target": "audit/step1-red.md",
                 "target_kind": "AP",
                 "state": "marked-truncated"},))
        root = build(case)
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = piece_entry_for(result.stdout, "step1-red.md")
        self.assertTrue(entry)
        self.assertIn("truncated", entry.lower())
        self.assertIn("truncated-no-correcting-record",
                      result.stdout)

    def test_truncated_unmarked_signal_piece_state(self):
        """EC-20. WV22 T-7 F1."""
        case = make_case(
            "truncated-unmarked",
            files={"audit/step1-red.md": (
                "# Step 1 red paper\n\nContents: section one, "
                "section two, section three.\n\n"
                "## Section one\n\nText of section one.\n")},
            malformations=(
                {"switch": "M-05",
                 "target": "audit/step1-red.md",
                 "target_kind": "AP",
                 "state": "signal-failed",
                 "signal": "signal-three"},))
        root = build(case)
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = piece_entry_for(result.stdout, "step1-red.md")
        self.assertTrue(entry)
        self.assertIn("truncated", entry.lower())

    def test_over_limit_file_piece_state(self):
        """EC-20, EC-21. WV22 E-1 F1, WV22 E-1 F2."""
        case = make_case(
            "over-limit-file",
            files={"steps/step-02-record.md":
                   step_record(2, pad=FILE_LIMIT)})
        root = build(case)
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = piece_entry_for(result.stdout, "step-02-record.md")
        self.assertTrue(entry)
        self.assertIn("over limit", entry.lower())
        self.assertIn("over-limit-piece", result.stdout)
        self.assertNotIn("malformed", entry.lower())

    def test_over_limit_line_piece_state(self):
        """EC-20, EC-21."""
        case = make_case(
            "over-limit-line",
            files={"steps/step-02-record.md":
                   "# Step 2 record\n" + ("y" * (LINE_LIMIT + 1))})
        root = build(case)
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = piece_entry_for(result.stdout, "step-02-record.md")
        self.assertTrue(entry)
        self.assertIn("over limit", entry.lower())
        self.assertIn("over-limit-piece", result.stdout)
        self.assertIn("65536", result.stdout.replace(",", ""))

    def test_unreadable_piece_state_and_run_continues(self):
        """EC-20. WV22 E-1 F1, WV22 E-1 F2."""
        root = build(make_case("unreadable-piece"))
        target = root / "steps" / "step-02-record.md"
        target.unlink()
        target.mkdir()
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = piece_entry_for(result.stdout, "step-02-record.md")
        self.assertTrue(entry)
        self.assertIn("unreadable", entry.lower())
        self.assertIn("unreadable-piece", entry)

    def test_form_state_is_not_a_quality_state(self):
        """EC-20. List 4 bound: date only form is not damage."""
        files = base_files()
        files["PATH-LEDGER.md"] = (
            "# Path ledger\n\nSteps stated: 1, 2, 3.\n\n"
            "## Transitions\n\n"
            "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-01.\n"
            "Step 2 IN PROGRESS 2026-11-02, closed 2026-11-02.\n"
            "Step 3 IN PROGRESS 2026-11-03, closed 2026-11-03.\n")
        root = build(make_case("form-not-quality", files=files))
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = piece_entry_for(result.stdout, "PATH-LEDGER.md")
        self.assertTrue(entry)
        lowered = entry.lower()
        self.assertNotIn("truncated", lowered)
        self.assertNotIn("malformed", lowered)
        self.assertNotIn("over limit", lowered)
        self.assertNotIn("unreadable", lowered)
        block = row_block(result.stdout, "T-1")
        self.assertIn("date-only-form", block)

    def test_f11_settings_carry_the_section7_numbers(self):
        """Fixture check, EC-21. The F-11 settings state the plan limits as numbers."""
        self.assertEqual(F11_SETTINGS["largest-file-bytes"],
                         FILE_LIMIT)
        self.assertEqual(F11_SETTINGS["tree-total-bytes"],
                         TREE_BYTES_LIMIT)
        self.assertEqual(F11_SETTINGS["tree-file-count"],
                         TREE_FILES_LIMIT)
        self.assertEqual(F11_SETTINGS["longest-line-bytes"],
                         LINE_LIMIT)
        self.assertEqual(F11_SETTINGS["whole-walk-entries"],
                         WALK_LIMIT)
        self.assertEqual(len(F11_CASES), 10)

    def test_f11_built_counts_match_the_stating_entry(self):
        """Fixture check, EC-21. Built counts, whole tree, filler only except for figures largest-file-bytes and longest-line-bytes, whose counts are carried by the one record piece, per figure."""
        expected = {
            ("largest-file-bytes", "at-limit"):
                {"files": 1, "total_bytes": 1000000},
            ("largest-file-bytes", "one-over"):
                {"files": 1, "total_bytes": 1000001},
            ("tree-total-bytes", "at-limit"):
                {"files": 25, "total_bytes": 25000000},
            ("tree-total-bytes", "one-over"):
                {"files": 26, "total_bytes": 25000001},
            ("tree-file-count", "at-limit"):
                {"files": 2000, "total_bytes": 0},
            ("tree-file-count", "one-over"):
                {"files": 2001, "total_bytes": 0},
            ("longest-line-bytes", "at-limit"):
                {"files": 1, "total_bytes": 65536,
                 "longest_line": 65536},
            ("longest-line-bytes", "one-over"):
                {"files": 1, "total_bytes": 65537,
                 "longest_line": 65537},
            ("whole-walk-entries", "at-limit"):
                {"files": 0, "dirs": 10000, "total_bytes": 0},
            ("whole-walk-entries", "one-over"):
                {"files": 0, "dirs": 10001, "total_bytes": 0},
        }
        scratch = tracked_tempdir("msc_slice2_f11_")
        for case in F11_CASES:
            spec = case["f11"]
            key = (spec["figure"], spec["position"])
            with self.subTest(figure=spec["figure"],
                              position=spec["position"]):
                root = build_case(case, scratch)
                measured = measure_tree(root)
                for field, value in expected[key].items():
                    self.assertEqual(measured[field], value,
                                     "%s %s" % (key, field))

    def test_f11_at_limit_is_not_over_limit(self):
        """EC-21. At the limit stands inside the limit, per figure."""
        scratch = tracked_tempdir("msc_slice2_f11_at_")
        for case in F11_CASES:
            if case["f11"]["position"] != "at-limit":
                continue
            with self.subTest(figure=case["f11"]["figure"]):
                root = build_case(case, scratch)
                result = run_product(root)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertNotIn("over-limit-piece", result.stdout)

    def test_f11_one_over_file_and_line_marked_over_limit(self):
        """EC-21. One unit over the file and line limits is over."""
        scratch = tracked_tempdir("msc_slice2_f11_over_")
        for case in F11_CASES:
            spec = case["f11"]
            if spec["position"] != "one-over":
                continue
            if spec["figure"] not in ("largest-file-bytes",
                                      "longest-line-bytes"):
                continue
            with self.subTest(figure=spec["figure"]):
                root = build_case(case, scratch)
                result = run_product(root)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("over limit", result.stdout.lower())
                self.assertIn("over-limit-piece", result.stdout)

    def test_f11_tree_over_tree_byte_limit(self):
        """EC-21, EC-42. Record part bytes over 25000000."""
        files = {}
        for step in range(1, 31):
            files["steps/step-%02d-record.md" % step] = (
                step_record(step, pad=900000))
        root = build(make_case("tree-over-bytes", files=files))
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        cleaned = result.stdout.replace(",", "")
        self.assertRegex(cleaned, r"(?<!\d)25000000(?!\d)")
        cov = coverage_statement(result.stdout)
        self.assertIn("not read", cov.lower())
        self.assertIn("step-30-record.md", cov)

    def test_f11_tree_over_file_count_limit(self):
        """EC-21, EC-42. Record part files over 2000."""
        files = {}
        for number in range(1, 2006):
            files["audit/step%d-fix-register.md" % number] = (
                "# Fix register %d\n\nEntries: none stated.\n"
                % number)
        root = build(make_case("tree-over-count", files=files))
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        cleaned = result.stdout.replace(",", "")
        self.assertRegex(cleaned, r"(?<!\d)2000(?!\d)")
        cov = coverage_statement(result.stdout)
        self.assertIn("not read", cov.lower())

    def test_tree_limits_measured_on_the_record_part(self):
        """EC-21. WV-8: tree limits are measured on the record part."""
        files = {}
        for number in range(2500):
            files["bulk/filler-%04d.txt" % number] = "bulk\n"
        root = build(make_case("record-part-scope", files=files))
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "E-1")
        self.assertIn("present", block.lower())
        self.assertNotIn("over-limit-piece",
                         piece_entry_for(result.stdout,
                                         "step-01-record.md"))

    def test_near_match_names_listed_unrecognised_not_read(self):
        """EC-22."""
        files = {
            "steps/step-01-records.md": step_record(1),
            "DECISION-QUEU.md": "# Near match queue\n",
        }
        root = build(make_case("near-match", files=files))
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("unrecognised", result.stdout.lower())
        self.assertIn("step-01-records.md", result.stdout)
        self.assertIn("DECISION-QUEU.md", result.stdout)

    def test_a7_3_nearest_closed_pattern_note(self):
        """EC-22. A7-3: the nearest closed pattern is named."""
        files = {"steps/step-09-records.md": step_record(9)}
        root = build(make_case("nearest-pattern", files=files))
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = piece_entry_for(result.stdout, "step-09-records.md")
        self.assertTrue(entry)
        self.assertIn("step-09-record.md", entry)

    def test_duplicate_identity_counted_once_both_paths_listed(self):
        """EC-46. WV-14 piece identity with differing content."""
        files = {
            "steps/step-01-record.md": step_record(
                1) + "Original content marker ORIGONLY.\n",
            "copy/step-01-record.md": (
                "# Step 1 record\n\nBase: 2. Team staffed: 99 "
                "agents. Total spins: 4.\n"
                "Duplicate content marker DUPONLY99.\n"),
        }
        root = build(make_case("duplicate-identity", files=files))
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("steps/step-01-record.md", result.stdout)
        self.assertIn("copy/step-01-record.md", result.stdout)
        entry = piece_entry_for(result.stdout, "step-01-record.md")
        self.assertIn("not read in full", entry.lower())
        self.assertIn("duplicate", entry.lower())
        block = row_block(result.stdout, "E-1")
        self.assertNotIn("DUPONLY99", block)
        self.assertNotIn("99", block)
        single_files = dict(files)
        del single_files["copy/step-01-record.md"]
        single = build(make_case("duplicate-single",
                                 files=single_files))
        single_result = run_product(single)
        self.assertEqual(pieces_recognised_count(result.stdout),
                         pieces_recognised_count(single_result.stdout))

    def test_split_page_damaged_supplies_no_tables(self):
        """EC-06, EC-20. A damaged split page supplies no tables."""
        files = base_files()
        files["wiki/wiki/synthesis/build-metrics-record-part-1.md"] = (
            b"\xff\xfe damaged split page \x80")
        root = build(make_case("split-damaged", files=files))
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "D-1")
        self.assertIn("missing", block.lower())
        entry = piece_entry_for(
            result.stdout, "build-metrics-record-part-1.md")
        self.assertTrue(entry)
        self.assertIn("malformed", entry.lower())

    def test_link_traversal_outside_root_not_followed(self):
        """EC-22. WV-14: a link outside the root is not followed."""
        outside = build(make_case(
            "link-outside-target",
            files={"outside.md": "outside the root marker\n"}))
        root = build(make_case("link-outside"))
        os.symlink(str(outside / "outside.md"),
                   str(root / "steps" / "linked.md"))
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("outside the root marker", result.stdout)

    def test_link_target_inside_root_followed_at_most_once(self):
        """EC-46. WV-14: an inside target is followed at most once."""
        base_root = build(make_case("link-inside-base"))
        base_result = run_product(base_root)
        self.assertEqual(base_result.returncode, 0, base_result.stderr)
        base_count = pieces_recognised_count(base_result.stdout)
        self.assertIsNotNone(base_count)
        root = build(make_case(
            "link-inside",
            links={"steps/step-01-record-link.md":
                   "steps/step-01-record.md"}))
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("step-01-record-link.md", result.stdout)
        self.assertEqual(pieces_recognised_count(result.stdout),
                         base_count)

    def test_whole_walk_bound_names_the_crossing(self):
        """EC-21, EC-42, EC-47. The 10000 entry walk bound."""
        dirs = tuple("bulk/entry-%05d" % n for n in range(10050))
        root = build(make_case("walk-over", dirs=dirs))
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        cleaned = result.stdout.replace(",", "")
        self.assertRegex(cleaned, r"(?<!\d)10000(?!\d)")
        self.assertIn("not visited", result.stdout.lower())
        cov = coverage_statement(result.stdout)
        self.assertIn("not visited", cov.lower())

    def test_whole_walk_at_the_bound_has_not_crossed(self):
        """EC-21, EC-47. Exactly 10000 entries visited crosses nothing."""
        scratch = tracked_tempdir("msc_slice2_walk_at_")
        case = [c for c in F11_CASES
                if c["f11"]["figure"] == "whole-walk-entries"
                and c["f11"]["position"] == "at-limit"][0]
        root = build_case(case, scratch)
        self.assertEqual(measure_tree(root)["dirs"], 10000)
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("not visited", result.stdout.lower())

    def test_a7_4_walk_order_sample_where_limit_cuts_capture(self):
        """EC-42, EC-44. A7-4 walk order sample, sorted path order."""
        files = {"steps/step-03-record.md":
                 step_record(3, pad=FILE_LIMIT)}
        root = build(make_case("walk-order-sample", files=files))
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = data_quality_entry_for(result.stdout,
                                       "step-03-record.md")
        self.assertTrue(entry)
        self.assertIn("step-03-record.md", entry)
        self.assertIn("bias", entry.lower())
        cleaned = entry.replace(",", "")
        self.assertTrue("1000000" in cleaned
                        or "file limit" in entry.lower())
        first_at = entry.find("steps/step-01-record.md")
        second_at = entry.find("steps/step-02-record.md")
        self.assertTrue(0 <= first_at < second_at)

    def test_partial_reading_named_in_both_places(self):
        """EC-42, EC-47. Partial in coverage and in run cost together."""
        files = {"steps/step-02-record.md":
                 step_record(2, pad=FILE_LIMIT)}
        root = build(make_case("partial-two-places", files=files))
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        cov = coverage_statement(result.stdout)
        self.assertIn("partial", cov.lower())
        self.assertIn("step-02-record.md", cov)
        self.assertIn("run cost", result.stdout.lower())
        self.assertGreaterEqual(result.stdout.lower().count("partial"),
                                2)

    def test_w8r05_file_size_at_half_and_twice(self):
        """EC-21. W8R-05 second tier, file size.

        Product limit is unchanged at 1000000 bytes. The test values
        500000 bytes and 2000000 bytes are test values only.
        """
        half = build(make_case(
            "w8r05-file-half",
            files={"steps/step-02-record.md":
                   step_record(2) + ("x" * 50000 + "\n") * 10}))
        half_result = run_product(half)
        self.assertEqual(half_result.returncode, 0, half_result.stderr)
        half_entry = piece_entry_for(half_result.stdout,
                                     "step-02-record.md")
        self.assertNotIn("over limit", half_entry.lower())
        twice = build(make_case(
            "w8r05-file-twice",
            files={"steps/step-02-record.md":
                   step_record(2, pad=2000000)}))
        twice_result = run_product(twice)
        self.assertEqual(twice_result.returncode, 0,
                         twice_result.stderr)
        twice_entry = piece_entry_for(twice_result.stdout,
                                      "step-02-record.md")
        self.assertIn("over limit", twice_entry.lower())
        self.assertIn("1000000",
                      twice_result.stdout.replace(",", ""))

    def test_w8r05_line_length_at_half_and_twice(self):
        """EC-21. W8R-05 second tier, line length.

        Product limit is unchanged at 65536 bytes. The test values
        32768 bytes and 131072 bytes are test values only.
        """
        half = build(make_case(
            "w8r05-line-half",
            files={"steps/step-02-record.md":
                   "# Step 2 record\n" + ("y" * 32768)}))
        half_result = run_product(half)
        half_entry = piece_entry_for(half_result.stdout,
                                     "step-02-record.md")
        self.assertNotIn("over limit", half_entry.lower())
        twice = build(make_case(
            "w8r05-line-twice",
            files={"steps/step-02-record.md":
                   "# Step 2 record\n" + ("y" * 131072)}))
        twice_result = run_product(twice)
        twice_entry = piece_entry_for(twice_result.stdout,
                                      "step-02-record.md")
        self.assertIn("over limit", twice_entry.lower())
        self.assertIn("65536",
                      twice_result.stdout.replace(",", ""))

    def test_w8r05_tree_bytes_at_half_and_twice(self):
        """EC-21. W8R-05 second tier, tree bytes.

        Product limit is unchanged at 25000000 bytes. The test values
        12500000 bytes and 50000000 bytes are test values only.
        """
        half_files = {}
        for step in range(1, 26):
            half_files["steps/step-%02d-record.md" % step] = (
                step_record(step) + ("x" * 50000 + "\n") * 10)
        half = build(make_case("w8r05-tree-half", files=half_files))
        half_result = run_product(half)
        self.assertEqual(half_result.returncode, 0, half_result.stderr)
        self.assertNotIn("over-limit-piece", half_result.stdout)
        twice_files = {}
        for step in range(1, 51):
            twice_files["steps/step-%02d-record.md" % step] = (
                step_record(step, pad=FILE_LIMIT))
        twice = build(make_case("w8r05-tree-twice", files=twice_files))
        twice_result = run_product(twice)
        self.assertEqual(twice_result.returncode, 0,
                         twice_result.stderr)
        self.assertIn("25000000",
                      twice_result.stdout.replace(",", ""))
        cov = coverage_statement(twice_result.stdout)
        self.assertIn("not read", cov.lower())

    def test_w8r05_file_count_at_half_and_twice(self):
        """EC-21. W8R-05 second tier, tree file count.

        Product limit is unchanged at 2000 files. The test values
        1000 files and 4000 files are test values only.
        """
        half_files = {}
        for number in range(1, 1001):
            half_files["audit/step%d-fix-register.md" % number] = (
                "# Fix register %d\n\nEntries: none stated.\n"
                % number)
        half = build(make_case("w8r05-count-half", files=half_files))
        half_result = run_product(half)
        self.assertEqual(half_result.returncode, 0, half_result.stderr)
        self.assertNotIn("over-limit-piece", half_result.stdout)
        twice_files = {}
        for number in range(1, 4001):
            twice_files["audit/step%d-fix-register.md" % number] = (
                "# Fix register %d\n\nEntries: none stated.\n"
                % number)
        twice = build(make_case("w8r05-count-twice",
                                files=twice_files))
        twice_result = run_product(twice)
        self.assertEqual(twice_result.returncode, 0,
                         twice_result.stderr)
        self.assertIn("2000",
                      coverage_statement(twice_result.stdout).replace(
                          ",", ""))
        self.assertIn("not read",
                      coverage_statement(twice_result.stdout).lower())

    def test_w8r05_walk_bound_at_half_and_twice(self):
        """EC-21. W8R-05 second tier, whole walk bound.

        Product limit is unchanged at 10000 entries. The test values
        5000 entries and 20000 entries are test values only.
        """
        half_dirs = tuple("bulk/entry-%05d" % n for n in range(5000))
        half = build(make_case("w8r05-walk-half", dirs=half_dirs))
        half_result = run_product(half)
        self.assertEqual(half_result.returncode, 0, half_result.stderr)
        self.assertNotIn("not visited", half_result.stdout.lower())
        twice_dirs = tuple("bulk/entry-%05d" % n for n in range(20000))
        twice = build(make_case("w8r05-walk-twice", dirs=twice_dirs))
        twice_result = run_product(twice)
        self.assertEqual(twice_result.returncode, 0,
                         twice_result.stderr)
        self.assertIn("not visited", twice_result.stdout.lower())
        self.assertIn("10000",
                      coverage_statement(twice_result.stdout).replace(
                          ",", ""))

    def test_wv221_same_piece_state_in_both_shapes(self):
        """EC-04, EC-20, EC-42, EC-46. WV22 Q-1 F1."""
        damaged = {"switch": "M-01",
                   "target": "audit/step1-round-record.md",
                   "target_kind": "AP",
                   "state": "not-valid-text"}
        round_file = {"audit/step1-round-record.md": (
            "# Round record, step 1\n\nPost triage severity "
            "breakdown, flow scale: Critical 0, High 1, Medium 2, "
            "Low 3.\n")}
        first = build(make_case("shape-one", files=round_file,
                                malformations=(damaged,)))
        second_files = dict(round_file)
        second_files["steps/step-01-gate-ruling.md"] = (
            "# Step 1 gate ruling\n\nClosure state: CLOSED-PASS.\n")
        second_case = make_case("shape-two", files=second_files,
                                malformations=(damaged,))
        second_case["files"] = dict(second_case["files"])
        del second_case["files"]["steps/step-01-gate-record.md"]
        second = build(second_case)
        first_result = run_product(first)
        second_result = run_product(second)
        self.assertEqual(first_result.returncode, 0,
                         first_result.stderr)
        self.assertEqual(second_result.returncode, 0,
                         second_result.stderr)
        first_entry = piece_entry_for(first_result.stdout,
                                      "step1-round-record.md")
        second_entry = piece_entry_for(second_result.stdout,
                                       "step1-round-record.md")
        self.assertIn("malformed", first_entry.lower())
        self.assertIn("malformed", second_entry.lower())
        self.assertEqual(row_block(first_result.stdout, "Q-1"),
                         row_block(second_result.stdout, "Q-1"))

    def test_walk_level_by_level_bound_reaches_shallow_piece(self):
        """R15-10. The walk stands level by level, brief Section 5.

        Breaker exhibit B15R1-B6 in its full form: one deep branch
        holding 10050 filler files and one recognisable piece at
        level two in a shallow branch. Under the brief walk order
        the piece is visited within the first entries, the bound
        crossing is named, and the partial report form issues with
        the full rows. A depth first walk spends the bound inside
        the deep branch and issues the no usable records form.
        """
        scratch = tracked_tempdir("msc_slice2_bfs_")
        root = scratch / "bfs-bound"
        deep = root / "a" / "deep"
        deep.mkdir(parents=True)
        for number in range(10050):
            (deep / ("filler-%05d.txt" % number)).write_bytes(b"")
        shallow = root / "c"
        shallow.mkdir(parents=True)
        (shallow / "step-01-record.md").write_text(
            step_record(1), encoding="utf-8")
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("No usable records", result.stdout)
        self.assertIn("step-01-record.md", result.stdout)
        self.assertIn("partial report", result.stdout.lower())
        cov = coverage_statement(result.stdout)
        cleaned = cov.replace(",", "")
        self.assertRegex(cleaned, r"(?<!\d)10000(?!\d)")
        self.assertIn("not visited", cov.lower())
        self.assertTrue(row_block(result.stdout, "E-1"))

    def test_walk_bound_before_any_piece_partial_not_floor(self):
        """R15-10. D4R-08 floor judged on the whole tree inventory.

        Bounded form of the same crossing: the walk bound is set
        to 5 in process, ten filler files stand at the root level
        ahead of one recognisable piece at the same level, so the
        bound is crossed before the piece is visited. The bound
        used is 5 in place of 10000 only to keep the exhibit
        small; the crossing is the same crossing, a bound reached
        before any recognisable piece is visited on a tree whose
        whole inventory holds one. The floor is judged on that
        whole inventory, so the partial report form issues, the
        crossing is named, the piece stands as not visited, and
        no row resting on it is reported as missing.
        """
        from tests.fixture_builder import capture_derive_render
        scratch = tracked_tempdir("msc_slice2_floor_")
        root = scratch / "floor-bound"
        root.mkdir(parents=True)
        for number in range(10):
            (root / ("filler-%02d.txt" % number)).write_bytes(b"")
        (root / "step-01-record.md").write_text(
            step_record(1), encoding="utf-8")
        capture_fn, derive_fn, render_fn = capture_derive_render(
            self, root)
        import metrics_starter_collector.shell_reader as shell
        standing = shell.WALK_BOUND
        shell.WALK_BOUND = 5
        try:
            captured = capture_fn(root)
            report = render_fn(derive_fn(captured))
        finally:
            shell.WALK_BOUND = standing
        self.assertNotIn("No usable records", report)
        self.assertIn("partial report", report.lower())
        self.assertIn("not visited", report.lower())
        self.assertIn("step-01-record.md", report)
        block = row_block(report, "E-1")
        self.assertTrue(block)
        self.assertNotIn("| missing |", block)
        self.assertIn("present but not derivable", block)

    def test_latest_timestamp_invalid_calendar_stamp_never_printed(self):
        """R15-11. The header latest stamp stands calendar validated.

        Breaker exhibit B15R1-B7: one stray line stating an
        impossible stamp, 9999-99-99 25:99, and one stating an
        impossible date alone, 2027-02-30. Neither is a record
        timestamp. The latest real stamp in the tree, the Step 3
        closing stamp of the path ledger, stands in the header.
        """
        files = {
            "steps/step-01-record.md": (
                step_record(1)
                + "Far review stamp 9999-99-99 25:99 noted in "
                  "passing.\n"),
            "steps/step-01-gate-record.md": (
                "# Step 1 gate record\n\nClosure state: "
                "CLOSED-PASS.\nReview date 2027-02-30 noted in "
                "passing.\n"),
        }
        root = build(make_case("latest-stamp", files=files))
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        latest_lines = [line for line in result.stdout.splitlines()
                        if line.startswith("Latest record timestamp:")]
        self.assertEqual(len(latest_lines), 1)
        self.assertIn("2026-11-03 17:00", latest_lines[0])
        self.assertNotIn("9999-99-99", latest_lines[0])
        self.assertNotIn("2027-02-30", latest_lines[0])

    def test_audit_directory_itself_is_not_a_record_piece(self):
        """R15-18. A directory is not a record piece, P-19.

        The audit directory must be descended into, and the audit
        paper inside it stands as a piece. The directory itself
        stands as no piece, is listed nowhere as an unreadable
        piece, and counts in no coverage or data quality position.
        """
        files = {"audit/step1-round-record.md": (
            "# Round record, step 1\n\nPost triage severity "
            "breakdown, flow scale: Critical 0, High 1, Medium 2, "
            "Low 3.\n")}
        root = build(make_case("audit-dir", files=files))
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("audit/step1-round-record.md", result.stdout)
        self.assertNotIn("Piece audit |", result.stdout)
        self.assertNotIn("Is a directory", result.stdout)
        cov = coverage_statement(result.stdout)
        self.assertNotIn("audit | audit paper", cov)

    def _signal_two_metrics_files(self, extra_before, header_line):
        table = (
            "## Decision table\n\n"
            "| Item | Origin step | Raised | Presented | Ruled |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| Q-1 | 3 | 2026-11-01 |  |  |\n"
            "| Q-2 | 3 | 2026-11-01 |  |  |\n")
        metrics = (
            "# Build metrics record\n\n"
            "Build: metrics fixture build.\n\n"
            "Step table stands.\n" + extra_before + header_line
            + table)
        return {"wiki/wiki/synthesis/build-metrics-record.md": metrics}

    def test_signal_two_unrelated_target_count_sentence_does_not_except(self):
        """R15-07. Breaker exhibit B15R1-B4, shell implementation.

        A metrics record holding a decision table of 2 data rows
        and a header line stating 99 rows stands truncated on
        signal two, and the D-1 row falls to missing. One
        unrelated sentence placed before the header line, stating
        a target count or a planned count for planning and saying
        nothing about the header count, does not carry the brief
        Section 5 exception: the exception attaches to the header
        count statement, so the piece still stands truncated, the
        signal still stands named, and D-1 still stands missing.
        """
        for label, sentence in (
                ("target", "A target count is kept for planning.\n"),
                ("planned", "A planned count is kept for planning.\n")):
            with self.subTest(sentence=label):
                files = self._signal_two_metrics_files(
                    sentence, "Rows stated in header: 99\n")
                root = build(make_case(
                    "unrelated-" + label, files=files))
                result = run_product(root)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("signal-two", result.stdout)
                entry = piece_entry_for(
                    result.stdout, "build-metrics-record.md")
                self.assertTrue(entry)
                self.assertIn("truncated", entry.lower())
                block = row_block(result.stdout, "D-1")
                self.assertTrue(block)
                self.assertIn("Verdict: missing", block)

    def test_signal_two_brief_form_header_count_exception_fires(self):
        """R15-07. The brief form of the signal two exception.

        Where the header count statement itself states the count
        as a planned count or as a target count, the signal does
        not fire under brief Section 5: the piece stands read in
        full, no signal two stands named for it, and the D-1 row
        stands present but not derivable from its decision table,
        complete on that ground.
        """
        for label, header_line in (
                ("planned",
                 "Rows stated in header: 99, stated as a planned "
                 "count.\n"),
                ("target",
                 "Rows stated in header: 99, stated as a target "
                 "count.\n")):
            with self.subTest(form=label):
                files = self._signal_two_metrics_files(
                    "", header_line)
                root = build(make_case(
                    "brief-form-" + label, files=files))
                result = run_product(root)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertNotIn("signal-two", result.stdout)
                entry = piece_entry_for(
                    result.stdout, "build-metrics-record.md")
                self.assertTrue(entry)
                self.assertNotIn("truncated", entry.lower())
                block = row_block(result.stdout, "D-1")
                self.assertTrue(block)
                self.assertIn("present but not derivable", block)

    def test_signal_two_unplanned_or_targeted_header_line_does_not_except(self):
        """C1B-03, shell limb. Negated and derived header wording.

        Confirmation exhibit C1B-03 in the shell form: a metrics
        record holding a decision table of 2 data rows and the
        header line Rows stated in header: 99, unplanned. states
        the opposite of the brief Section 5 exception condition,
        and the header line Rows stated in header: 99, targeted
        for review. states nothing about the count as a target
        count. Neither line excepts: the piece stands truncated
        on signal two, the signal stands named, and D-1 falls to
        missing, exactly as the plain miscount does.
        """
        for label, header_line in (
                ("unplanned",
                 "Rows stated in header: 99, unplanned.\n"),
                ("targeted",
                 "Rows stated in header: 99, targeted for "
                 "review.\n")):
            with self.subTest(form=label):
                files = self._signal_two_metrics_files(
                    "", header_line)
                root = build(make_case(
                    "negated-header-" + label, files=files))
                result = run_product(root)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("signal-two", result.stdout)
                entry = piece_entry_for(
                    result.stdout, "build-metrics-record.md")
                self.assertTrue(entry)
                self.assertIn("truncated", entry.lower())
                block = row_block(result.stdout, "D-1")
                self.assertTrue(block)
                self.assertIn("Verdict: missing", block)

    def test_signal_two_core_vocabulary_correction_honoured_at_capture(self):
        """C1B-05, shell limb. The core correction vocabulary.

        A record corrected in the core vocabulary, the line
        Corrected count: 2 standing over a header count of 99
        and a decision table of 2 data rows, is judged on the
        corrected count at capture as it is in the core: the
        piece stands read in full, no signal two stands named,
        and D-1 stands present but not derivable from its table.
        A core vocabulary correction stating a count of 4 the
        table does not hold still fails signal two, because the
        corrected count is the count tested.
        """
        files = self._signal_two_metrics_files(
            "Corrected count: 2\n", "Rows stated in header: 99\n")
        root = build(make_case("core-correction", files=files))
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("signal-two", result.stdout)
        entry = piece_entry_for(
            result.stdout, "build-metrics-record.md")
        self.assertTrue(entry)
        self.assertNotIn("truncated", entry.lower())
        block = row_block(result.stdout, "D-1")
        self.assertTrue(block)
        self.assertIn("present but not derivable", block)
        files = self._signal_two_metrics_files(
            "Corrected count: 4\n", "Rows stated in header: 99\n")
        root = build(make_case("core-correction-wrong", files=files))
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("signal-two", result.stdout)
        entry = piece_entry_for(
            result.stdout, "build-metrics-record.md")
        self.assertTrue(entry)
        self.assertIn("truncated", entry.lower())

    def test_latest_timestamp_impossible_time_date_does_not_leak(self):
        """C1B-04. A refused full stamp leaks no date into the header.

        Confirmation exhibit C1B-04 in its own terms: the Step 1
        record carries the line Far review stamp 2026-12-31
        25:00 noted in passing, an impossible time of day, and
        no record in the tree states 2026-12-31 standing alone.
        The header latest stamp is the tree real latest stamp,
        the Step 3 closing stamp of the path ledger, and the
        refused stamp date stands nowhere in that line. Direct
        calls on _latest_timestamp agree: a candidate set
        holding 2027-01-01 24:00 and a real 2026-11-03 17:00
        stamp returns the real stamp.
        """
        import metrics_starter_collector.shell_reader as shell
        self.assertEqual(
            shell._latest_timestamp([
                "Far review stamp 2027-01-01 24:00 noted.\n",
                "Real stamp 2026-11-03 17:00 stands.\n"]),
            "2026-11-03 17:00")
        files = {
            "steps/step-01-record.md": (
                step_record(1)
                + "Far review stamp 2026-12-31 25:00 noted in "
                  "passing.\n"),
        }
        root = build(make_case("latest-stamp-leak", files=files))
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        latest_lines = [line for line in result.stdout.splitlines()
                        if line.startswith("Latest record timestamp:")]
        self.assertEqual(len(latest_lines), 1)
        self.assertIn("2026-11-03 17:00", latest_lines[0])
        self.assertNotIn("2026-12-31", latest_lines[0])

    def test_latest_timestamp_date_standing_alone_still_prints(self):
        """C1B-04 control. A date standing alone keys as itself.

        The control the finding states: a date standing alone in
        a record, with no time of day beside it in that record,
        still keys at the start of its day and prints as itself
        in the header, ahead of every earlier full stamp.
        """
        import metrics_starter_collector.shell_reader as shell
        self.assertEqual(
            shell._latest_timestamp(
                ["Review date 2026-12-31 noted in passing.\n"]),
            "2026-12-31")
        files = {
            "steps/step-01-record.md": (
                step_record(1)
                + "Review date 2026-12-31 noted in passing.\n"),
        }
        root = build(make_case("latest-stamp-alone", files=files))
        result = run_product(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        latest_lines = [line for line in result.stdout.splitlines()
                        if line.startswith("Latest record timestamp:")]
        self.assertEqual(len(latest_lines), 1)
        self.assertEqual(
            latest_lines[0], "Latest record timestamp: 2026-12-31")

    def test_walk_listing_failure_surfaces_in_walk_note(self):
        """C1P-01. A directory that cannot be listed does not vanish.

        The listing of the audit directory, holding one round
        record, is forced to raise OSError in process, against a
        tree also holding one step record. The walk still returns
        the step record, and the failure surfaces in the capture
        in the walk note, naming the directory and the cause, in
        the plan Section 4 error form: the rendered report
        carries that note in its coverage statement and stands
        as a partial report, so the round record subtree does
        not vanish in silence.
        """
        from tests.fixture_builder import capture_derive_render
        scratch = tracked_tempdir("msc_slice2_walkfail_")
        root = scratch / "walk-listing-failure"
        (root / "steps").mkdir(parents=True)
        (root / "audit").mkdir(parents=True)
        (root / "steps" / "step-01-record.md").write_text(
            step_record(1), encoding="utf-8")
        (root / "audit" / "step1-round-record.md").write_text(
            "# Round record, step 1\n\nPost triage severity "
            "breakdown, flow scale: Critical 0, High 1, "
            "Medium 2, Low 3.\n", encoding="utf-8")
        capture_fn, derive_fn, render_fn = capture_derive_render(
            self, root)
        import metrics_starter_collector.shell_reader as shell
        standing_listdir = os.listdir

        def failing_listdir(path):
            if Path(path).name == "audit":
                raise OSError("forced listing failure")
            return standing_listdir(path)

        os.listdir = failing_listdir
        try:
            entries, damaged, walk_note, unvisited = \
                shell._walk_entries(root, root.resolve())
            captured = capture_fn(root)
            report = render_fn(derive_fn(captured))
        finally:
            os.listdir = standing_listdir
        self.assertIn("steps/step-01-record.md", entries)
        self.assertNotIn("audit/step1-round-record.md", entries)
        self.assertIsNotNone(walk_note)
        self.assertIn("audit", walk_note)
        self.assertIn("forced listing failure", walk_note)
        self.assertIn("audit", captured.walk_note)
        self.assertIn("forced listing failure", captured.walk_note)
        cov = coverage_statement(report)
        self.assertIn("walk note", cov)
        self.assertIn("forced listing failure", cov)
        self.assertIn("partial report", report.lower())

    def test_run_cost_limit_listing_failure_only_names_no_walk_bound(self):
        """Fix pass 2 unit 13. A listing failure is no bound crossing.

        The forced listing failure tree of the C1P-01 test, whose
        only walk failure is the directory listing failure: its
        walk note states the listing failure and states no bound
        crossing, and its coverage statement states the listing
        failure truly. Its run cost line must therefore name no
        whole walk bound in its Limit part, because that bound
        was never crossed on this tree. The Limit part stands in
        the line grammar fallback form, no limit crossed, and the
        Reading part still stands partial on the listing failure.
        """
        from tests.fixture_builder import capture_derive_render
        scratch = tracked_tempdir("msc_slice2_runcost_")
        root = scratch / "walk-listing-failure-run-cost"
        (root / "steps").mkdir(parents=True)
        (root / "audit").mkdir(parents=True)
        (root / "steps" / "step-01-record.md").write_text(
            step_record(1), encoding="utf-8")
        (root / "audit" / "step1-round-record.md").write_text(
            "# Round record, step 1\n\nPost triage severity "
            "breakdown, flow scale: Critical 0, High 1, "
            "Medium 2, Low 3.\n", encoding="utf-8")
        capture_fn, derive_fn, render_fn = capture_derive_render(
            self, root)
        import metrics_starter_collector.shell_reader as shell
        standing_listdir = os.listdir

        def failing_listdir(path):
            if Path(path).name == "audit":
                raise OSError("forced listing failure")
            return standing_listdir(path)

        os.listdir = failing_listdir
        try:
            captured = capture_fn(root)
            report = render_fn(derive_fn(captured))
        finally:
            os.listdir = standing_listdir
        self.assertIsNotNone(captured.walk_note)
        self.assertIn("could not be listed", captured.walk_note)
        self.assertIn("forced listing failure", captured.walk_note)
        self.assertNotIn("whole walk bound", captured.walk_note)
        cov = coverage_statement(report)
        self.assertIn("forced listing failure", cov)
        run_cost_lines = [line for line in report.splitlines()
                          if line.startswith("Run cost: ")]
        self.assertEqual(len(run_cost_lines), 1)
        run_cost = run_cost_lines[0]
        limit_part = run_cost.split("Limit: ", 1)[1].split(
            " | Reading:", 1)[0]
        self.assertNotIn("whole walk bound", run_cost)
        self.assertEqual(limit_part, "no limit crossed")
        self.assertIn("Reading: partial", run_cost)

    def test_run_cost_limit_walk_bound_crossing_keeps_bound_wording(self):
        """Fix pass 2 unit 13 control. A bound crossing keeps its Limit.

        The bounded form of the bound crossing, as the R15-10
        bounded test states it: the walk bound is set to 5 in
        process, ten filler files stand at the root level ahead
        of one recognisable piece at the same level, so the walk
        note states the bound crossing. The bound used is 5 in
        place of 10000 only to keep the exhibit small; the
        crossing is the same crossing. On such a tree the run
        cost line Limit part keeps the whole walk bound wording,
        and the Reading part stands partial.
        """
        from tests.fixture_builder import capture_derive_render
        scratch = tracked_tempdir("msc_slice2_runcost_bound_")
        root = scratch / "walk-bound-run-cost"
        root.mkdir(parents=True)
        for number in range(10):
            (root / ("filler-%02d.txt" % number)).write_bytes(b"")
        (root / "step-01-record.md").write_text(
            step_record(1), encoding="utf-8")
        capture_fn, derive_fn, render_fn = capture_derive_render(
            self, root)
        import metrics_starter_collector.shell_reader as shell
        standing = shell.WALK_BOUND
        shell.WALK_BOUND = 5
        try:
            captured = capture_fn(root)
            report = render_fn(derive_fn(captured))
        finally:
            shell.WALK_BOUND = standing
        self.assertIsNotNone(captured.walk_note)
        self.assertIn("whole walk bound", captured.walk_note)
        self.assertIn("was reached", captured.walk_note)
        run_cost_lines = [line for line in report.splitlines()
                          if line.startswith("Run cost: ")]
        self.assertEqual(len(run_cost_lines), 1)
        run_cost = run_cost_lines[0]
        limit_part = run_cost.split("Limit: ", 1)[1].split(
            " | Reading:", 1)[0]
        self.assertIn("whole walk bound", limit_part)
        self.assertIn("Reading: partial", run_cost)

    def test_floor_line_listing_failure_only_names_no_walk_crossing(self):
        """Fix pass 2 unit 14. A listing failure is no walk crossing.

        The floor form exhibit of the unit 13 deviation: a tree
        holding no recognisable piece, whose only subdirectory
        has its listing forced to raise OSError in process, so
        the capture holds no pieces and a walk note stands. The
        walk note states only the directory listing failure and
        states no bound crossing. The floor line, the no usable
        records line, must therefore name no walk crossing: it
        states the note as a walk note, in the words the coverage
        statement uses, and the listing failure sentence itself
        stands in it truly, naming the directory and its cause.
        """
        from tests.fixture_builder import capture_derive_render
        scratch = tracked_tempdir("msc_slice2_floorfail_")
        root = scratch / "floor-listing-failure"
        (root / "audit").mkdir(parents=True)
        (root / "audit" / "step1-round-record.md").write_text(
            "# Round record, step 1\n\nPost triage severity "
            "breakdown, flow scale: Critical 0, High 1, "
            "Medium 2, Low 3.\n", encoding="utf-8")
        capture_fn, derive_fn, render_fn = capture_derive_render(
            self, root)
        import metrics_starter_collector.shell_reader as shell
        standing_listdir = os.listdir

        def failing_listdir(path):
            if Path(path).name == "audit":
                raise OSError("forced listing failure")
            return standing_listdir(path)

        os.listdir = failing_listdir
        try:
            captured = capture_fn(root)
            report = render_fn(derive_fn(captured))
        finally:
            os.listdir = standing_listdir
        self.assertEqual(captured.pieces, [])
        self.assertIsNotNone(captured.walk_note)
        self.assertIn("could not be listed", captured.walk_note)
        self.assertIn("forced listing failure", captured.walk_note)
        self.assertNotIn("whole walk bound", captured.walk_note)
        lines = report.splitlines()
        self.assertEqual(len(lines), 3)
        floor = lines[2]
        self.assertTrue(floor.startswith("No usable records: "))
        self.assertNotIn("walk crossing", floor)
        self.assertIn("walk note: ", floor)
        self.assertIn("could not be listed", floor)
        self.assertIn("forced listing failure", floor)

    def test_floor_line_walk_bound_crossing_keeps_crossing_wording(self):
        """Fix pass 2 unit 14 control. A bound crossing keeps its name.

        The bounded form of the bound crossing on a floor tree:
        the walk bound is set to 5 in process and ten filler
        files stand at the root level, with no recognisable
        piece anywhere in the tree, so the capture holds no
        pieces and the walk note states the bound crossing.
        The bound used is 5 in place of 10000 only to keep the
        exhibit small; the crossing is the same crossing. On
        such a tree the floor line keeps the walk crossing
        wording, naming the whole walk bound in its reached
        form, as the unit 8 floor ground states.
        """
        from tests.fixture_builder import capture_derive_render
        scratch = tracked_tempdir("msc_slice2_floorbound_")
        root = scratch / "floor-walk-bound"
        root.mkdir(parents=True)
        for number in range(10):
            (root / ("filler-%02d.txt" % number)).write_bytes(b"")
        capture_fn, derive_fn, render_fn = capture_derive_render(
            self, root)
        import metrics_starter_collector.shell_reader as shell
        standing = shell.WALK_BOUND
        shell.WALK_BOUND = 5
        try:
            captured = capture_fn(root)
            report = render_fn(derive_fn(captured))
        finally:
            shell.WALK_BOUND = standing
        self.assertEqual(captured.pieces, [])
        self.assertIsNotNone(captured.walk_note)
        self.assertIn("whole walk bound", captured.walk_note)
        self.assertIn("was reached", captured.walk_note)
        lines = report.splitlines()
        self.assertEqual(len(lines), 3)
        floor = lines[2]
        self.assertTrue(floor.startswith("No usable records: "))
        self.assertIn("walk crossing: ", floor)
        self.assertIn("whole walk bound", floor)
        self.assertIn("was reached", floor)

    def test_floor_line_bound_and_listing_failure_keeps_crossing(self):
        """Fix pass 2 unit 14 control. Both sentences keep the crossing.

        A floor tree whose walk note carries both sentences:
        the walk bound is set to 5 in process, ten filler files
        stand at the root level, and the only subdirectory has
        its listing forced to raise OSError in process, so no
        recognisable piece stands in the capture and the note
        states the bound crossing first and the listing failure
        second. Because the bound crossing the first sentence
        states did cross, the floor line keeps the walk
        crossing wording, and the listing failure sentence
        stands in it beside the crossing sentence.
        """
        from tests.fixture_builder import capture_derive_render
        scratch = tracked_tempdir("msc_slice2_floorboth_")
        root = scratch / "floor-bound-and-listing-failure"
        (root / "audit").mkdir(parents=True)
        (root / "audit" / "step1-round-record.md").write_text(
            "# Round record, step 1\n", encoding="utf-8")
        for number in range(10):
            (root / ("filler-%02d.txt" % number)).write_bytes(b"")
        capture_fn, derive_fn, render_fn = capture_derive_render(
            self, root)
        import metrics_starter_collector.shell_reader as shell
        standing = shell.WALK_BOUND
        standing_listdir = os.listdir

        def failing_listdir(path):
            if Path(path).name == "audit":
                raise OSError("forced listing failure")
            return standing_listdir(path)

        shell.WALK_BOUND = 5
        os.listdir = failing_listdir
        try:
            captured = capture_fn(root)
            report = render_fn(derive_fn(captured))
        finally:
            shell.WALK_BOUND = standing
            os.listdir = standing_listdir
        self.assertEqual(captured.pieces, [])
        self.assertIsNotNone(captured.walk_note)
        self.assertIn("whole walk bound", captured.walk_note)
        self.assertIn("was reached", captured.walk_note)
        self.assertIn("could not be listed", captured.walk_note)
        lines = report.splitlines()
        self.assertEqual(len(lines), 3)
        floor = lines[2]
        self.assertTrue(floor.startswith("No usable records: "))
        self.assertIn("walk crossing: ", floor)
        self.assertIn("whole walk bound", floor)
        self.assertIn("could not be listed", floor)
        self.assertIn("forced listing failure", floor)


if __name__ == "__main__":
    unittest.main()
