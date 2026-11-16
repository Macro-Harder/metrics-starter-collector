"""Slice 5 tests: rounds and quality family T-7, Q-1, Q-3, Q-4.

Authored fresh for the restart run under the test design record at
design/steps/step-13r-test-design-record.md. Each case states, in its
first line, the EC points and the WV22 field entries it asserts, in
the citation forms that record states. Trees are built through the
fixture builder (build_case, build_cases, f10_cases) into temporary
directories, and the product is invoked through the pre install
invocation route: python3 -m metrics_starter_collector, root first,
from the public repo root, as the run_tool harness performs it.
"""
import re
import unittest
from unittest import mock

from tests.fixture_builder import (FixtureTestCase, assert_two_part_form,
                                     assert_verdict,
                                     assert_reads_capture_only, build_case,
                                     capture_derive_render,
                                     build_cases, data_quality_section,
                                     decision_table,
                                     f10_cases, gate_record,
                                     gate_ruling, metrics_record, queue_file,
                                     row_block, row_verdict, run_tool,
                                     single_page_metrics_record_files,
                                     slice5_make_case as make_case,
                                     split_metrics_record_files,
                                     statement_segment, step_record,
                                     tracked_tempdir)

TRUNCATED = ("# Audit paper\n\nFindings so far: Critical 1, High 2.\n"
             "This paper ends mid sentence with no closing total and no\n")

ROUND_BREAKDOWN = ("Post triage breakdown, flow scale: Critical 1, "
                   "High 2, Medium 0, Low 0.\n")


def base_files():
    files = {}
    transitions = []
    for n in (1, 2, 3):
        files["steps/step-%02d-record.md" % n] = step_record(n)
        files["steps/step-%02d-gate-record.md" % n] = gate_record(n)
        transitions.append(
            "Step %d IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 "
            "17:00." % n)
    files["PATH-LEDGER.md"] = (
        "# Path ledger\n\nSteps stated: 1, 2, 3.\n\n## Transitions\n\n"
        + "\n".join(transitions) + "\n")
    files["TIER-RECORD.md"] = "# Tier record\n\nTier: Low. Base: 2.\n"
    files.update(single_page_metrics_record_files(metrics_record(
        body="Step table stands complete for the fixture steps.")))
    return files


def run_case(case):
    parent = tracked_tempdir("msc_slice5_")
    tree = build_case(case, parent)
    return run_tool(tree)


def assert_ca10_before_count(test, block, count_text):
    lowered = block.lower()
    pop_at = lowered.find("population")
    excl_at = lowered.find("excluded")
    count_at = block.find(count_text)
    test.assertTrue(0 <= pop_at < excl_at, block[:500])
    test.assertTrue(0 <= excl_at < count_at,
                    "exclusion list does not stand before the count")


def disagreements_block(report):
    lowered = report.lower()
    at = lowered.find("disagreements")
    if at < 0:
        return ""
    tail = report[at:]
    lines = tail.splitlines()
    kept = [lines[0]]
    for line in lines[1:]:
        stripped = line.strip()
        if stripped.startswith("#") and "disagreement" not in \
                stripped.lower():
            break
        kept.append(line)
    return "\n".join(kept)


class TestSlice5RoundsQuality(FixtureTestCase):

    # --------------------------------------------------------------
    # Truncation family F-05, F-06, F-06b, and the zero family.
    # --------------------------------------------------------------

    def test_f05_truncated_paper_no_correcting_record(self):
        """EC-20, EC-33. F-05 marked form under switch M-02."""
        case = make_case("f05", {"audit/step-01-red.md": TRUNCATED},
                         malformations=(
                             {"switch": "M-02",
                              "target": "audit/step-01-red.md",
                              "target_kind": "AP",
                              "state": "marked-truncated"},))
        result = run_case(case)
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present but not derivable", "Q-1")
        self.assertIn("truncated-no-correcting-record", block)
        self.assertIn("incomplete", result.stdout.lower())

    def test_f05_unmarked_truncation_signal_failed_q1(self):
        """EC-20, EC-33. Unmarked truncation under switch M-05."""
        paper = ("# Audit paper\n\nPost triage breakdown, flow scale: "
                 "Critical 1, High 2.\nThis paper carries no closing "
                 "total and no completion statement of any kind.\n")
        case = make_case("f05-unmarked", {"audit/step-01-red.md": paper},
                         malformations=(
                             {"switch": "M-05",
                              "target": "audit/step-01-red.md",
                              "target_kind": "AP",
                              "state": "signal-failed",
                              "signal": "signal-one"},))
        result = run_case(case)
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present but not derivable", "Q-1")

    def test_f06_truncated_paper_with_correcting_record(self):
        """EC-20, EC-33. F-06 marked form under switch M-03."""
        correction = ("# Correction\n\nThe truncated paper "
                      "audit/step-01-red.md corrected total: Critical 1, "
                      "High 2, Medium 0, Low 0, post triage breakdown.\n")
        case = make_case("f06", {
            "audit/step-01-red.md": TRUNCATED,
            "audit/step-01-correction.md": correction},
            malformations=(
                {"switch": "M-03", "target": "audit/step-01-red.md",
                 "target_kind": "AP", "state": "marked-truncated",
                 "correcting_piece": "audit/step-01-correction.md",
                 "citation": "corrected total: Critical 1"},))
        result = run_case(case)
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present", "Q-1")
        self.assertIn("step-01-correction.md", block)
        self.assertIn("Critical 1", block)
        self.assertIn("High 2", block)

    def test_f06b_repaired_truncation_present_with_repair_cited(self):
        """EC-20, EC-33. F-06b repaired form under switch M-04."""
        repaired = (TRUNCATED +
                    "\n## Completion section\n\nThis piece was found "
                    "truncated. This file, audit/step-01-red.md, supplies "
                    "the missing content in place: post triage breakdown "
                    "Critical 1, High 2, Medium 0, Low 0.\n")
        case = make_case("f06b", {"audit/step-01-red.md": repaired},
                         malformations=(
                             {"switch": "M-04",
                              "target": "audit/step-01-red.md",
                              "target_kind": "AP",
                              "state": "repaired-truncated",
                              "repaired_piece": "audit/step-01-red.md",
                              "citation": "supplies the missing content "
                                          "in place"},))
        result = run_case(case)
        self.assertIn("repair", result.stdout.lower())
        self.assertNotIn("unrepaired truncation", result.stdout.lower())
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present", "Q-1")

    def test_f07_placeholder_zero_against_measured_zero(self):
        """EC-16, EC-34; WV22 Q-3 F1. Placeholder zero, then measured."""
        case = make_case("f07-placeholder", {
            "registers/defect-register.md": (
                "# Defect register\n\nEscaped defects printed as 0 with "
                "no measurement basis stated.\n")})
        result = run_case(case)
        block = row_block(result.stdout, "Q-3")
        assert_verdict(self, block, "present but not derivable", "Q-3")
        self.assertIn("no-measurement-basis", block)
        case2 = make_case("f07-measured", {
            "registers/defect-register.md": (
                "# Defect register\n\nEscaped defects: 0. Measurement "
                "basis: every register entry was triaged in full on "
                "2026-11-02 and no entry escaped. Entry D-1: origin "
                "step Step 1, as judged at triage.\n")})
        result2 = run_case(case2)
        block2 = row_block(result2.stdout, "Q-3")
        assert_verdict(self, block2, "present", "Q-3")
        self.assertIn("measurement basis", block2.lower())

    def test_f07b_zero_with_correcting_record_basis(self):
        """EC-34; WV22 Q-3 F1. Zero basis supplied by a correction."""
        case = make_case("f07b", {
            "registers/defect-register.md": (
                "# Defect register\n\nEscaped defects: 0.\n"),
            "registers/correction.md": (
                "# Correction\n\nThe zero for escaped defects in the "
                "defect register is corrected: its measurement basis is "
                "a full triage of every register entry, none escaped.\n")})
        result = run_case(case)
        block = row_block(result.stdout, "Q-3")
        assert_verdict(self, block, "present", "Q-3")
        self.assertIn("correction.md", block)

    def test_q3_printed_zero_never_stated_as_measured_zero(self):
        """EC-34, EC-49; WV22 Q-3 F1. Printed zero in the record."""
        extra = single_page_metrics_record_files(metrics_record(
            body="Escapes attributed (Q-3): 0, none known."))
        result = run_case(make_case("q3-printed-zero", extra))
        block = row_block(result.stdout, "Q-3")
        assert_verdict(self, block, "present but not derivable", "Q-3")
        self.assertIn("no-measurement-basis", block)

    def test_q3_contested_origin_step_carried_under_d18(self):
        """EC-34, EC-43; WV22 Q-3 F1. Contested origin step, D-18."""
        extra = {
            "registers/defect-register.md": (
                "# Defect register\n\nEntry D-9: defect disposition, "
                "origin step Step 2.\n")}
        extra.update(single_page_metrics_record_files(metrics_record(
            body="Metrics record states the step universe as 1 step.")))
        result = run_case(make_case("q3-contested", extra))
        block = row_block(result.stdout, "Q-3")
        segment = statement_segment(block)
        self.assertIn("record disagrees", segment)
        self.assertIn("Step 2", segment)
        self.assertIn("build-metrics-record.md", segment)

    def test_wv22_q3_f1_origin_field_absent_from_every_entry(self):
        """EC-16, EC-34; WV22 Q-3 F1. No origin field on any entry."""
        case = make_case("q3-no-origin-field", {
            "registers/fix-register.md": (
                "# Fix register\n\nEntry one: a fix entry carrying no "
                "origin step field.\n"),
            "registers/defect-register.md": (
                "# Defect register\n\nEntry one: a defect entry "
                "carrying no origin step field.\n")})
        result = run_case(case)
        block = row_block(result.stdout, "Q-3")
        assert_verdict(self, block, "present but not derivable", "Q-3")
        self.assertIn("missing-field", block)

    def test_wv22_q3_f2_copied_origin_value_does_not_count(self):
        """EC-34; WV22 Q-3 F2. Origin value copied, not triage judged."""
        case = make_case("q3-copied-origin", {
            "registers/defect-register.md": (
                "# Defect register\n\nEntry D-4: found in Step 2, "
                "closed in Step 3. Origin step: Step 2, copied from "
                "the finding step field, with no triage judgement "
                "stated for the origin.\n")})
        result = run_case(case)
        block = row_block(result.stdout, "Q-3")
        assert_verdict(self, block, "present but not derivable", "Q-3")

    # --------------------------------------------------------------
    # T-7 rounds.
    # --------------------------------------------------------------

    def test_f12_empty_tables_with_stale_text_t7_limb(self):
        """EC-14, EC-27. F-12 empty round tables with stale text."""
        extra = single_page_metrics_record_files(metrics_record(
            body="Loop round table: no rows. Text states no loop "
                 "step has run yet. Audit round table: no rows."))
        result = run_case(make_case("f12", extra))
        block = row_block(result.stdout, "T-7")
        assert_verdict(self, block, "present but not derivable", "T-7")
        self.assertNotIn("0 rounds", block)
        q1 = row_block(result.stdout, "Q-1")
        assert_verdict(self, q1, "missing", "Q-1")
        self.assertIn("no-feeder-record", q1)
        self.assertNotIn("0 rounds", q1)

    def test_g05_irreconcilable_counts_both_named(self):
        """EC-14, EC-27; WV22 T-7 F3. Both irreconcilable counts named."""
        case = make_case("g05", {
            "steps/step-01-record.md": step_record(
                1, extra="Loop step. Pass count in this record: "
                         "3 passes."),
            "steps/step-01-gate-record.md": gate_record(
                1, extra="Verdict record count for this step: 1 verdict "
                         "record stands.")})
        result = run_case(case)
        block = row_block(result.stdout, "T-7")
        assert_verdict(self, block, "present but not derivable", "T-7")
        self.assertIn("record-disagrees", block)
        self.assertRegex(block, r"pass count[^\d]*3(?!\d)")
        self.assertRegex(block, r"verdict[^\d]*1(?!\d)")

    def test_wv22_t7_f1_non_outcome_records_count_no_round(self):
        """EC-27; WV22 T-7 F1. Papers and checks record no outcome."""
        case = make_case("t7-f1", {
            "steps/step-01-record.md": step_record(
                1, extra="Loop step."),
            "audit/step-01-check.md": (
                "# Round check paper\n\nA check of Round 1 work. This "
                "paper records no outcome for any round.\n"),
            "registers/round-items.md": (
                "# Register items\n\nItem: Round 1 was looked at. No "
                "outcome stands recorded in this item.\n")})
        result = run_case(case)
        block = row_block(result.stdout, "T-7")
        assert_verdict(self, block, "present but not derivable", "T-7")
        self.assertNotIn("1 rounds", block)

    def test_wv22_t7_f2_board_ruling_in_step_record_counts_t7_only(self):
        """EC-27; WV22 T-7 F2. Board ruling in a step record, T-7 only."""
        case = make_case("t7-f2", {
            "steps/step-01-record.md": step_record(
                1, extra="Loop step. Board ruling held inside this "
                         "record: the board closes Round 1 of this "
                         "step. Work record for Round 1 stands in "
                         "audit/step-01-work.md."),
            "audit/step-01-work.md": (
                "# Round 1 work record\n\nThe work Round 1 disposed "
                "of stands stated here.\n")})
        result = run_case(case)
        block = row_block(result.stdout, "T-7")
        assert_verdict(self, block, "present", "T-7")
        self.assertRegex(block, r"Step 1: 1 rounds counted")
        q1 = row_block(result.stdout, "Q-1")
        self.assertNotIn("board ruling", q1.lower())
        q4 = row_block(result.stdout, "Q-4")
        self.assertNotIn("board ruling", q4.lower())

    def test_wv22_t7_f3_mapping_test_rounds_counted_once(self):
        """EC-27; WV22 T-7 F3, F4. Mapping and pairing, counted once."""
        case = make_case("t7-f3", {
            "steps/step-01-record.md": step_record(
                1, extra="Loop step."),
            "audit/step-01-outcomes.md": (
                "# Outcome records, step 1\n\nRound 1 closing outcome "
                "record: Round 1 closed. Round 2 closing outcome "
                "record: Round 2 closed. A ruling file closing "
                "statement names each round outcome separately: "
                "Round 1 outcome, Round 2 outcome.\n"),
            "audit/step-01-round1-paper.md": (
                "# Round 1 paper\n\nWork inside Round 1, one paper "
                "of several in the round.\n"),
            "audit/step-01-round1-work.md": (
                "# Round 1 work\n\nThe work Round 1 disposed of.\n"),
            "audit/step-01-round2-work.md": (
                "# Round 2 work\n\nThe work Round 2 disposed of.\n")})
        result = run_case(case)
        block = row_block(result.stdout, "T-7")
        assert_verdict(self, block, "present", "T-7")
        self.assertIn("2 rounds", block)

    def test_wv22_t7_f3_mapping_failure_two_closing_outcomes(self):
        """EC-27; WV22 T-7 F3. Two closing outcomes for one round."""
        case = make_case("t7-f3-fail", {
            "steps/step-01-record.md": step_record(
                1, extra="Loop step."),
            "audit/step-01-outcomes.md": (
                "# Outcome records, step 1\n\nRound 1 closing outcome "
                "record A: Round 1 closed. Round 1 closing outcome "
                "record B: Round 1 closed again.\n"),
            "audit/step-01-round1-work.md": (
                "# Round 1 work\n\nThe work Round 1 disposed of.\n")})
        result = run_case(case)
        block = row_block(result.stdout, "T-7")
        assert_verdict(self, block, "present but not derivable", "T-7")
        self.assertIn("Step 1", block)

    def test_wv22_t7_f4_unpaired_outcome_records_named_unpaired(self):
        """EC-27; WV22 T-7 F4. Outcome records with no pairing record."""
        case = make_case("t7-f4", {
            "steps/step-01-record.md": step_record(
                1, extra="Loop step."),
            "audit/step-01-outcomes.md": (
                "# Outcome records, step 1\n\nRound 1 closing outcome "
                "record: Round 1 closed. No further record for this "
                "step and round states the work disposed of.\n")})
        result = run_case(case)
        block = row_block(result.stdout, "T-7")
        assert_verdict(self, block, "present but not derivable", "T-7")
        self.assertIn("unpaired", block.lower())
        self.assertIn("Step 1", block)

    def test_f22_t7_counted_from_verdict_records_counted_not_marked(self):
        """EC-27; F-22 degraded form, D4R-10, D4R-11. Counted, not marked."""
        case = make_case("t7-f22-degraded", {
            "steps/step-01-record.md": step_record(
                1, extra="Loop step."),
            "audit/step-01-work.md": (
                "# Round 1 work record\n\nThe work Round 1 disposed "
                "of stands stated here.\n")})
        result = run_case(case)
        block = row_block(result.stdout, "T-7")
        assert_verdict(self, block, "present", "T-7")
        self.assertRegex(block, r"Step 1: 1 rounds counted")
        self.assertIn("counted from verdict records", block)
        self.assertIn("marked as counted", block)
        self.assertNotIn("1 rounds marked", block)

    def test_ca10_t7_population_and_exclusion_list(self):
        """EC-27. CA-10 population and exclusion list for T-7."""
        case = make_case("ca10-t7", {
            "steps/step-01-record.md": step_record(
                1, extra="Loop step. Rounds run in a loop for this "
                         "step."),
            "steps/step-02-record.md": step_record(
                2, extra="Loop step. A board ruling held inside this "
                         "record states 2 rounds for this step.")})
        result = run_case(case)
        block = row_block(result.stdout, "T-7")
        assert_ca10_before_count(self, block, "2 rounds")
        lowered = block.lower()
        pop_at = lowered.find("population")
        excl_at = lowered.find("excluded")
        pop_segment = block[pop_at:excl_at]
        self.assertIn("Step 1", pop_segment)
        self.assertIn("Step 2", pop_segment)
        excl_segment = block[excl_at:]
        self.assertIn("board ruling", excl_segment.lower())

    def test_t7_unmapped_rounds_no_code_fits_and_code_list_gap(self):
        """EC-27; S5-02. Unmapped rounds: no code fits, code list gap."""
        extra = single_page_metrics_record_files(metrics_record(
            body="## Loop round table\n\n(no rows yet)\n\n"
                 "No loop step has run yet.\n"))
        result = run_case(make_case("t7-unmapped-no-code-fits", extra))
        block = row_block(result.stdout, "T-7")
        assert_verdict(self, block, "present but not derivable", "T-7")
        assert_two_part_form(self, block, "no code fits",
                             "T-7 reason line")
        self.assertNotIn("missing-field", block)
        section = data_quality_section(result.stdout)
        self.assertTrue(section, "data quality section stands")
        gap_lines = [line for line in section.splitlines()
                     if "code list gap" in line.lower()]
        self.assertTrue(gap_lines,
                        "no code list gap entry stands for T-7")
        self.assertIn("T-7", gap_lines[0])
        assert_two_part_form(self, gap_lines[0], "no code fits",
                             "T-7 data quality entry")

    # --------------------------------------------------------------
    # Q-1 core cases.
    # --------------------------------------------------------------

    def test_f14_mixed_severity_scales(self):
        """EC-14, EC-33; WV22 Q-1 F3. F-14 mixed severity scales."""
        case = make_case("f14", {
            "audit/step-01-red.md": (
                "# Round 1\n\nPost triage breakdown on Scale A: "
                "Critical 1.\n"),
            "audit/step-02-red.md": (
                "# Round 2\n\nPost triage breakdown on Scale B: "
                "Critical 5.\n")})
        result = run_case(case)
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present but not derivable", "Q-1")
        self.assertIn("governing-scale-conflict", block)

    def test_g06_pre_triage_breakdown_refused(self):
        """EC-33; WV22 Q-1 F2. G-06 pre triage breakdown refused."""
        case = make_case("g06", {
            "audit/step-01-red.md": (
                "# Round 1 paper\n\nPre triage counts: Critical 4, "
                "High 4. No post triage breakdown stands.\n")})
        result = run_case(case)
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present but not derivable", "Q-1")
        self.assertIn("no-post-triage-breakdown", block)

    def test_g07_commissioned_scale_limited_and_attack_totals_refused(self):
        """EC-33; WV22 Q-1 F3, F4. G-07 commissioned scale, attacks."""
        case = make_case("g07", {
            "steps/step-01-gate-adjudication.md": (
                "# Adjudication\n\nA commissioned severity scale "
                "governs Round 1 only. Round 1 post triage breakdown: "
                "Critical 1, High 0, Medium 0, Low 0.\n"),
            "audit/step-02-red.md": (
                "# Round 2\n\nAttack totals: Critical 9, High 9. "
                "These grade attacks, not triaged findings.\n")})
        result = run_case(case)
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present but not derivable", "Q-1")
        self.assertIn("Round 2", block)
        self.assertIn("Critical 1", block)
        self.assertNotIn("Critical 9", block)
        self.assertNotIn("High 9", block)

    def test_wv6_conflicting_governing_adjudications(self):
        """EC-33, EC-43. WV-6 conflicting governing adjudications."""
        case = make_case("wv6", {
            "steps/step-01-gate-adjudication.md": (
                "# Adjudication A\n\nScale X governs Rounds 1 and 2.\n"),
            "steps/step-02-gate-adjudication.md": (
                "# Adjudication B\n\nScale Y governs Rounds 1 and 2.\n"),
            "audit/step-03-red.md": (
                "# Round 3\n\nPost triage breakdown: Critical 0, "
                "High 1, Medium 0, Low 0.\n")})
        result = run_case(case)
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present but not derivable", "Q-1")
        self.assertIn("governing-scale-conflict", block)
        self.assertIn("Round 1", block)
        self.assertIn("Round 2", block)

    def test_wv6_resolved_conflict_variant_not_blocked(self):
        """EC-33, EC-43. WV-6 resolved conflict variant."""
        case = make_case("wv6-resolved", {
            "steps/step-01-gate-adjudication.md": (
                "# Adjudication A\n\nScale X governs Round 1.\n"),
            "steps/step-02-gate-adjudication.md": (
                "# Adjudication B\n\nScale Y governs Round 1. This "
                "later governing statement resolves the conflict: "
                "Scale X governs Round 1.\n"),
            "audit/step-01-red.md": (
                "# Round 1\n\n" + ROUND_BREAKDOWN)})
        result = run_case(case)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present", "Q-1")
        self.assertIn("Critical 1", block)
        self.assertIn("High 2", block)
        self.assertIn("Medium 0", block)
        self.assertIn("Low 0", block)
        self.assertNotIn("governing-scale-conflict", block)

    def test_ca10_q1_population_and_exclusion_list_before_count(self):
        """EC-33. CA-10 population and exclusion list for Q-1."""
        case = make_case("ca10-q1", {
            "audit/step-01-red.md": (
                "# Round 1\n\nPost triage breakdown: Critical 1.\n"),
            "audit/step-02-red.md": (
                "# Round 2\n\nPre triage counts only: Critical 3.\n")})
        result = run_case(case)
        block = row_block(result.stdout, "Q-1")
        assert_ca10_before_count(self, block, "Critical 1")
        excl_at = block.lower().find("excluded")
        excl_segment = block[excl_at:]
        self.assertIn("Round 2", excl_segment)
        self.assertIn("no post triage breakdown", excl_segment.lower())

    def test_q1_bounded_form_prints_qualifying_round_counts_only(self):
        """EC-33; WV22 Q-1 F2, F5. Bounded form, qualifying rounds."""
        case = make_case("q1-bounded", {
            "audit/step-01-red.md": (
                "# Round 1\n\nPost triage breakdown: Critical 2, "
                "High 1, Medium 0, Low 0.\n"),
            "audit/step-02-red.md": (
                "# Round 2\n\nPre triage counts only: Critical 7.\n")})
        result = run_case(case)
        block = row_block(result.stdout, "Q-1")
        self.assertIn("bounded", block.lower())
        self.assertIn("Round 1", block)
        self.assertIn("Critical 2", block)
        self.assertNotIn("Critical 7", block)

    # --------------------------------------------------------------
    # Q-1 carrier forms, spin 773 headings, form by form.
    # The three heading texts are Post triage breakdown, Triage run,
    # and Severity scale, in that order, in every form.
    # --------------------------------------------------------------

    def _carrier_case(self, name, carrier_path, carrier_text):
        extra = {
            "audit/step-01-round-record.md": (
                "# Round 1 record\n\nRound record for Round 1. This "
                "record names %s as the carrier record for Round 1.\n"
                % carrier_path),
            carrier_path: carrier_text}
        return make_case(name, extra,
                         features=("flow-scale-breakdowns",))

    def _assert_carrier_counts(self, result, form_words):
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present", "Q-1")
        self.assertIn("Critical 1", block)
        self.assertIn("High 2", block)
        self.assertIn("flow", block.lower())
        self.assertIn(form_words, block.lower())
        return block

    def test_q1_carrier_form_one_fix_register_round_table(self):
        """EC-33; WV22 Q-1 F1, F2, F3, F5. Carrier form one."""
        carrier = (
            "# Fix register\n\n| Round | Post triage breakdown | "
            "Triage run | Severity scale |\n| --- | --- | --- | --- |\n"
            "| Round 1 | Critical 1, High 2, Medium 0, Low 0 | Triage "
            "has run for Round 1 | Flow scale |\n")
        case = self._carrier_case(
            "carrier-form-one", "registers/fix-register.md", carrier)
        self._assert_carrier_counts(run_case(case), "fix register")

    def test_q1_carrier_form_two_defect_register_round_summary(self):
        """EC-33; WV22 Q-1 F1, F2, F3, F5. Carrier form two."""
        carrier = (
            "# Defect register\n\n## Round summary: Round 1\n\n"
            "Post triage breakdown: Critical 1, High 2, Medium 0, "
            "Low 0\nTriage run: Triage has run for Round 1\n"
            "Severity scale: Flow scale\n")
        case = self._carrier_case(
            "carrier-form-two", "registers/defect-register.md", carrier)
        self._assert_carrier_counts(run_case(case), "defect register")

    def test_q1_carrier_form_three_audit_register_round_entry(self):
        """EC-33; WV22 Q-1 F1, F2, F3, F5. Carrier form three."""
        carrier = (
            "# Audit register\n\n## Round entry: Round 1\n\n"
            "Post triage breakdown: Critical 1, High 2, Medium 0, "
            "Low 0\nTriage run: Triage has run for Round 1\n"
            "Severity scale: Flow scale\n")
        case = self._carrier_case(
            "carrier-form-three", "registers/audit-register.md", carrier)
        self._assert_carrier_counts(run_case(case), "audit register")

    def test_q1_carrier_form_four_gate_record_round_section(self):
        """EC-33; WV22 Q-1 F1, F2, F3, F5. Carrier form four."""
        carrier = (
            "# Step 1 gate record\n\nClosure state: CLOSED-PASS.\n\n"
            "## Round section: Round 1\n\n### Post triage breakdown\n\n"
            "Critical 1, High 2, Medium 0, Low 0\n\n### Triage run\n\n"
            "Triage has run for Round 1.\n\n### Severity scale\n\n"
            "Flow scale\n")
        case = self._carrier_case(
            "carrier-form-four", "steps/step-01-gate-record.md", carrier)
        self._assert_carrier_counts(run_case(case), "gate record")

    def test_q1_carrier_headings_in_other_text_carry_nothing(self):
        """EC-33; WV22 Q-1 F1. Headings in other text carry nothing."""
        carrier = (
            "# Fix register\n\n| Round | Post-triage breakdown | "
            "Triage status | Scale used |\n| --- | --- | --- | --- |\n"
            "| Round 1 | Critical 1, High 2, Medium 0, Low 0 | Triage "
            "has run for Round 1 | Flow scale |\n")
        case = self._carrier_case(
            "carrier-wrong-text", "registers/fix-register.md", carrier)
        result = run_case(case)
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present but not derivable", "Q-1")
        self.assertIn("no-post-triage-breakdown", block)

    def test_q1_carrier_in_record_round_record_does_not_name(self):
        """EC-33; WV22 Q-1 F1. Carrier in a record no round names."""
        carrier = (
            "# Defect register\n\n## Round summary: Round 1\n\n"
            "Post triage breakdown: Critical 1, High 2, Medium 0, "
            "Low 0\nTriage run: Triage has run for Round 1\n"
            "Severity scale: Flow scale\n")
        case = make_case("carrier-unnamed",
                         {"registers/defect-register.md": carrier},
                         features=("flow-scale-breakdowns",))
        result = run_case(case)
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present but not derivable", "Q-1")

    def test_q1_carrier_scale_silent_case_states_no_pair(self):
        """EC-33; WV22 Q-1 F3, F5. Scale silent case, no pair stated."""
        carrier = (
            "# Defect register\n\n## Round summary: Round 1\n\n"
            "Post triage breakdown: Critical 1, High 2, Medium 0, "
            "Low 0\nTriage run: Triage has run for Round 1\n")
        case = self._carrier_case(
            "carrier-scale-silent", "registers/defect-register.md",
            carrier)
        result = run_case(case)
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present but not derivable", "Q-1")
        self.assertIn("no scale stated for that breakdown", block)
        self.assertIn("defect register", block.lower())

    def test_q1_carrier_commissioned_scale_under_scale_heading(self):
        """EC-33; WV22 Q-1 F3. Commissioned scale under the heading."""
        carrier = (
            "# Defect register\n\n## Round summary: Round 1\n\n"
            "Post triage breakdown: Critical 1, High 2, Medium 0, "
            "Low 0\nTriage run: Triage has run for Round 1\n"
            "Severity scale: Commissioned scale\n")
        case = self._carrier_case(
            "carrier-commissioned", "registers/defect-register.md",
            carrier)
        result = run_case(case)
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present but not derivable", "Q-1")
        self.assertIn("governing-scale-conflict", block)

    def test_f14_mixed_scales_in_carrier_form(self):
        """EC-14, EC-33; WV22 Q-1 F3, F5. F-14 inside a carrier form."""
        carrier = (
            "# Fix register\n\n| Round | Post triage breakdown | "
            "Triage run | Severity scale |\n| --- | --- | --- | --- |\n"
            "| Round 1 | Critical 1, High 0, Medium 0, Low 0 | Triage "
            "has run for Round 1 | Flow scale |\n"
            "| Round 2 | Critical 5, High 0, Medium 0, Low 0 | Triage "
            "has run for Round 2 | Commissioned scale |\n")
        extra = {
            "audit/step-01-round-record.md": (
                "# Round record\n\nRound record for Round 1 and for "
                "Round 2. This record names registers/fix-register.md "
                "as the carrier record for both rounds.\n"),
            "registers/fix-register.md": carrier}
        case = make_case("f14-carrier", extra,
                         features=("flow-scale-breakdowns",))
        result = run_case(case)
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present but not derivable", "Q-1")
        self.assertIn("governing-scale-conflict", block)
        self.assertIn("Round 2", block)

    def test_wv22_q1_f4_subject_bar_other_subject_counts_nothing(self):
        """EC-33; WV22 Q-1 F4. Subject bar: attacks graded, not findings."""
        carrier = (
            "# Defect register\n\n## Round summary: Round 1\n\n"
            "Post triage breakdown: Critical 9, High 9, Medium 0, "
            "Low 0, grading attacks only\nTriage run: Triage has run "
            "for Round 1\nSeverity scale: Flow scale\n")
        case = self._carrier_case(
            "carrier-subject-bar", "registers/defect-register.md",
            carrier)
        result = run_case(case)
        block = row_block(result.stdout, "Q-1")
        assert_verdict(self, block, "present but not derivable", "Q-1")
        self.assertNotIn("Critical 9", block)

    # --------------------------------------------------------------
    # Q-4 first trace.
    # --------------------------------------------------------------

    def test_g08_first_trace_by_record_order_with_form_precedence(self):
        """EC-15, EC-35; WV22 Q-4 F1, F2. G-08 first trace, precedence."""
        case = make_case("g08", {
            "steps/step-01-trace.md": (
                "# First trace\n\nParts: 8 LANDED, 2 PARTIAL, "
                "0 CONTRADICTED. Stated total: 10 items checked.\n"),
            "steps/step-01-gate-record.md": gate_record(
                1, extra="Later re-audit trace: 10 of 10 LANDED.")})
        result = run_case(case)
        block = row_block(result.stdout, "Q-4")
        assert_verdict(self, block, "present", "Q-4")
        self.assertIn("step-01-trace.md", block)
        self.assertRegex(block, r"(?<!\d)8(?!\d)")

    def test_wv22_q4_f1_correcting_record_identifies_first_trace(self):
        """EC-15, EC-35; WV22 Q-4 F1, F2. Identification by correction."""
        case = make_case("q4-f1", {
            "steps/step-01-trace.md": (
                "# Later trace\n\nParts: 1 LANDED, 0 PARTIAL, "
                "0 CONTRADICTED. Stated total: 1 item checked.\n"),
            "steps/step-01-correction.md": (
                "# Correction\n\nThe first trace record for Step 1 "
                "is steps/step-01-first-trace.md, identified under "
                "the first trace rule.\n"),
            "steps/step-01-first-trace.md": (
                "# First trace\n\nParts: 4 LANDED, 0 PARTIAL, "
                "0 CONTRADICTED. Stated total: 4 items checked.\n")})
        result = run_case(case)
        block = row_block(result.stdout, "Q-4")
        assert_verdict(self, block, "present", "Q-4")
        self.assertIn("step-01-first-trace.md", block)
        self.assertRegex(block, r"(?<!\d)4(?!\d)")

    def test_g09_q4_present_with_coverage_remainder_forms(self):
        """EC-35. G-09 present with coverage, remainder forms named."""
        case = make_case("g09", {
            "steps/step-01-trace.md": (
                "# Trace\n\nParts: 10 LANDED, 0 PARTIAL, "
                "0 CONTRADICTED. Stated total: 10 items checked.\n"),
            "steps/step-02-record.md": step_record(
                2, extra="No fold in trace as such: analogue only "
                         "step."),
            "steps/step-03-trace.md": (
                "# Trace\n\nParts: 0 LANDED, 0 PARTIAL, "
                "0 CONTRADICTED. Stated total: 0 items checked.\n")})
        result = run_case(case)
        block = row_block(result.stdout, "Q-4")
        assert_verdict(self, block, "present", "Q-4")
        self.assertIn("Step 2", block)
        self.assertIn("analogue", block.lower())
        self.assertIn("Step 3", block)
        self.assertIn("zero total", block.lower())

    def test_q4_partial_coverage_without_defined_form_is_not_present(self):
        """EC-35. Named negative case for Q-4 partial coverage."""
        case = make_case("q4-negative", {
            "steps/step-01-trace.md": (
                "# Trace fragment\n\nNo totals stand.\n")})
        result = run_case(case)
        block = row_block(result.stdout, "Q-4")
        assert_verdict(self, block, "present but not derivable", "Q-4")
        self.assertIn("missing-field", block)

    def test_q4_step_stating_no_trace_applies_is_excluded(self):
        """EC-35. Named case for the Q-4 not applicable population."""
        case = make_case("q4-not-applicable", {
            "steps/step-01-trace.md": (
                "# Trace\n\nParts: 4 LANDED, 0 PARTIAL, "
                "0 CONTRADICTED. Stated total: 4 items checked.\n"),
            "steps/step-02-record.md": step_record(
                2, extra="No trace applies to this step.")})
        result = run_case(case)
        block = row_block(result.stdout, "Q-4")
        assert_verdict(self, block, "present", "Q-4")
        self.assertIn("Step 2", block)
        self.assertIn("not applicable", block.lower())
        coverage_at = block.lower().find("not applicable")
        self.assertNotIn("uncovered", block[coverage_at:].lower())

    def test_q4_row_cross_check_marking_in_statement_line(self):
        """EC-35, EC-43. Named cross check marking case for Q-4."""
        extra = {
            "steps/step-01-trace.md": (
                "# Trace\n\nParts: 8 LANDED, 2 PARTIAL, "
                "0 CONTRADICTED. Stated total: 10 items checked.\n")}
        extra.update(single_page_metrics_record_files(metrics_record(
            body="Metrics record states Q-4 for Step 1 as 10 of 10.")))
        result = run_case(make_case("q4-cross-check", extra))
        block = row_block(result.stdout, "Q-4")
        segment = statement_segment(block)
        self.assertIn("record disagrees", segment)
        self.assertIn("build-metrics-record.md", segment)
        self.assertIn("8 of 10", segment)
        self.assertIn("10 of 10", segment)

    def test_q4_sum_test_one_contribution_excepted_build_present(self):
        """EC-35; WV22 Q-4 F2, F3. F-23 form: one contribution excepted."""
        case = make_case("q4-sum-one-excepted", {
            "steps/step-01-trace.md": (
                "# First trace, step 1\n\nParts: 4 LANDED, 0 PARTIAL, "
                "0 CONTRADICTED. Stated total: 4 items checked.\n"),
            "steps/step-02-trace.md": (
                "# First trace, step 2\n\nParts: 2 LANDED, 1 PARTIAL, "
                "0 CONTRADICTED. Stated total: 2 items checked.\n")})
        result = run_case(case)
        block = row_block(result.stdout, "Q-4")
        assert_verdict(self, block, "present", "Q-4")
        self.assertIn("Step 2", block)
        self.assertIn("excepted", block.lower())

    def test_q4_sum_test_all_contributions_excepted_not_derivable(self):
        """EC-35; WV22 Q-4 F3. F-23 form: every contribution excepted."""
        case = make_case("q4-sum-all-excepted", {
            "steps/step-01-trace.md": (
                "# First trace, step 1\n\nParts: 2 LANDED, 1 PARTIAL, "
                "0 CONTRADICTED. Stated total: 2 items checked.\n")})
        result = run_case(case)
        block = row_block(result.stdout, "Q-4")
        assert_verdict(self, block, "present but not derivable", "Q-4")
        self.assertIn("sum test", block.lower())

    def test_f23_other_metric_carries_no_sum_test_exception_form(self):
        """EC-27. F-23 other metric limb: no sum test exception form."""
        case = make_case("f23-other-metric", {
            "steps/step-01-record.md": step_record(
                1, extra="Loop step. Pass count in this record: "
                         "3 passes."),
            "steps/step-01-gate-record.md": gate_record(
                1, extra="Verdict record count for this step: 1 "
                         "verdict record stands.")})
        result = run_case(case)
        block = row_block(result.stdout, "T-7")
        assert_verdict(self, block, "present but not derivable", "T-7")
        self.assertNotIn("sum test", block.lower())
        self.assertNotIn("excepted", block.lower())

    # --------------------------------------------------------------
    # F-18 variant, F-10 pair, disagreements block, WV2-21 pair,
    # and the named reread test for this slice.
    # --------------------------------------------------------------

    def test_f18_unknown_version_slice5_rows(self):
        """EC-03, EC-27, EC-33, EC-34, EC-35. F-18 Slice 5 variant."""
        extra = {
            "steps/step-01-trace.md": (
                "# Trace\n\nParts: 8 LANDED, 2 PARTIAL, "
                "0 CONTRADICTED. Stated total: 10 items checked.\n"),
            "audit/step-01-red.md": (
                "# Round 1\n\n" + ROUND_BREAKDOWN)}
        extra.update(single_page_metrics_record_files(metrics_record(
            body="Step table stands.",
            header_version="unknown-version-999")))
        result = run_case(make_case("f18-slice5", extra))
        for code in ("T-7", "Q-1", "Q-4"):
            block = row_block(result.stdout, code)
            assert_verdict(self, block, "present but not derivable",
                           code)
            self.assertIn("unknown-definitions-version", block, code)
            self.assertIn("unknown-version-999", block, code)
        assert_verdict(self, row_block(result.stdout, "Q-3"),
                       "missing", "Q-3")

    def test_f10_malformed_piece_affected_q1_unaffected_e1(self):
        """EC-20, EC-28, EC-33. F-10 pair built through f10_cases()."""
        parent = tracked_tempdir("msc_slice5_f10_")
        built = build_cases(f10_cases(), parent)
        sound = run_tool(built["f10-sound"])
        malformed = run_tool(built["f10-malformed"])
        self.assertEqual(malformed.returncode, 0, malformed.stderr)
        self.assertNotIn("Traceback", malformed.stdout)
        self.assertNotIn("Traceback", malformed.stderr)
        self.assertIn("malformed", malformed.stdout.lower())
        self.assertIn("step-01-round-record.md", malformed.stdout)
        q1_sound = row_block(sound.stdout, "Q-1")
        q1_bad = row_block(malformed.stdout, "Q-1")
        self.assertTrue(q1_sound)
        self.assertTrue(q1_bad)
        self.assertNotEqual(row_verdict(q1_sound), row_verdict(q1_bad))
        self.assertIn("malformed", q1_bad.lower())
        e1_sound = row_block(sound.stdout, "E-1")
        e1_bad = row_block(malformed.stdout, "E-1")
        self.assertTrue(e1_sound)
        self.assertEqual(e1_sound, e1_bad)

    def test_disagreements_two_metrics_one_entry_per_metric(self):
        """EC-43. One disagreement, two metrics, one entry per metric."""
        extra = {
            "audit/step-01-round-record.md": (
                "# Round 1 record\n\nRound 1 post triage breakdown, "
                "flow scale: Critical 1, High 0, Medium 0, Low 0. "
                "First trace for Step 1: 4 LANDED of 4 items "
                "checked.\n"),
            "audit/step-01-audit-paper.md": (
                "# Audit paper\n\nFor Round 1 and Step 1 the same "
                "records state: post triage breakdown Critical 3, "
                "and first trace 2 LANDED of 4 items checked.\n")}
        result = run_case(make_case("disagree-two-metrics", extra))
        block = disagreements_block(result.stdout)
        self.assertTrue(block, result.stdout[:600])
        self.assertIn("Q-1", block)
        self.assertIn("Q-4", block)
        self.assertIn("step-01-round-record.md", block)
        self.assertIn("step-01-audit-paper.md", block)
        self.assertEqual(block.count("step-01-round-record.md"), 2)
        q1_segment = statement_segment(row_block(result.stdout, "Q-1"))
        q4_segment = statement_segment(row_block(result.stdout, "Q-4"))
        self.assertIn("record disagrees", q1_segment)
        self.assertIn("record disagrees", q4_segment)

    def test_disagreements_two_units_one_entry_per_unit(self):
        """EC-43. One disagreement, two units of Q-4, one entry each."""
        case = make_case("disagree-two-units", {
            "steps/step-01-trace.md": (
                "# First trace, step 1\n\nParts: 4 LANDED, 0 PARTIAL, "
                "0 CONTRADICTED. Stated total: 4 items checked.\n"),
            "steps/step-02-trace.md": (
                "# First trace, step 2\n\nParts: 4 LANDED, 0 PARTIAL, "
                "0 CONTRADICTED. Stated total: 4 items checked.\n"),
            "audit/step-01-audit-paper.md": (
                "# Audit paper\n\nThis paper states the first trace "
                "for Step 1 as 2 LANDED of 4 and the first trace for "
                "Step 2 as 2 LANDED of 4.\n")})
        result = run_case(case)
        block = disagreements_block(result.stdout)
        self.assertTrue(block, result.stdout[:600])
        self.assertIn("Q-4", block)
        self.assertIn("Step 1", block)
        self.assertIn("Step 2", block)
        self.assertEqual(block.count("Q-4"), 2)

    def test_disagreements_restatement_group_named_correction(self):
        """EC-43. Restatement group: named correction, no first line."""
        extra = {
            "registers/defect-register.md": (
                "# Defect register\n\nEntry D-9: defect disposition, "
                "origin step Step 2.\n"),
            "registers/correction.md": (
                "# Correction\n\nGoverning correction, named: the "
                "metrics record statement of the step universe is "
                "restated under this correction, and the register "
                "entry for D-9 governs.\n")}
        extra.update(single_page_metrics_record_files(metrics_record(
            body="Metrics record states the step universe as 1 step.")))
        result = run_case(make_case("disagree-restatement", extra))
        block = disagreements_block(result.stdout)
        self.assertTrue(block, result.stdout[:600])
        lowered = block.lower()
        self.assertIn("restatement", lowered)
        self.assertIn("correction", lowered)
        entry_at = lowered.find("q-3")
        self.assertTrue(entry_at >= 0, block[:500])
        self.assertNotIn("verdict was withheld",
                         block[entry_at:].lower())

    def _second_shape_files(self):
        files = base_files()
        for n in (1, 2, 3):
            del files["steps/step-%02d-gate-record.md" % n]
            files["steps/step-%02d-gate-ruling.md" % n] = gate_ruling(n)
        files["steps/step-01-record.md"] = step_record(
            1, extra="Tokens recorded for Step 1: 100 tokens. Money "
                     "spent for Step 1: 0.")
        record_text = metrics_record(
            body="Step table stands complete for the fixture steps.",
            decision_table=decision_table([
                "| Item one | 3 | 2026-11-01 09:00 | 2026-11-01 10:00 "
                "| 2026-11-01 12:00 |"]))
        head, sep, tail = record_text.partition("## Decision table")
        files.update(split_metrics_record_files(
            [head, sep + tail]))
        files["cost/cost-ledger.md"] = (
            "# Cost ledger\n\nStep 1 tokens: 100 tokens. Step 1 "
            "money spent: 0.\n")
        files["registers/decision-queue.md"] = queue_file([
            "| Item one | 3 | 2026-11-01 09:00 | 2026-11-01 10:00 "
            "| 2026-11-01 12:00 |"])
        return files

    def _slice5_substance(self):
        return {
            "audit/step-01-round-record.md": (
                "# Round 1 record\n\n" + ROUND_BREAKDOWN),
            "steps/step-01-trace.md": (
                "# First trace, step 1\n\nParts: 4 LANDED, 0 PARTIAL, "
                "0 CONTRADICTED. Stated total: 4 items checked.\n"),
            "registers/defect-register.md": (
                "# Defect register\n\nEntry D-1: origin step Step 1, "
                "as judged at triage.\n")}

    def test_wv21_slice5_rows_equivalent_across_second_shape(self):
        """EC-04, EC-14, EC-15, EC-16, EC-27, EC-33, EC-34, EC-35."""
        first_files = base_files()
        first_files["steps/step-01-record.md"] = step_record(
            1, extra="Tokens recorded for Step 1: 100 tokens. Money "
                     "spent for Step 1: 0.")
        first_files.update(single_page_metrics_record_files(
            metrics_record(
                body="Step table stands complete for the fixture "
                     "steps.",
                decision_table=decision_table([
                    "| Item one | 3 | 2026-11-01 09:00 | "
                    "2026-11-01 10:00 | 2026-11-01 12:00 |"]))))
        first_files.update(self._slice5_substance())
        second_files = self._second_shape_files()
        second_files.update(self._slice5_substance())
        parent = tracked_tempdir("msc_slice5_wv21_")
        built = build_cases(
            ({"name": "shape-one", "features": (), "files": first_files},
             {"name": "shape-two", "features": (),
              "files": second_files}), parent)
        first = run_tool(built["shape-one"])
        second = run_tool(built["shape-two"])
        for code in ("T-7", "Q-1", "Q-3", "Q-4"):
            one = row_block(first.stdout, code)
            two = row_block(second.stdout, code)
            self.assertTrue(one, code)
            self.assertTrue(two, code)
            self.assertEqual(
                row_verdict(one), row_verdict(two),
                "row %s differs between shapes on equivalent content; "
                "the shape difference is one of the four habits" % code)
        self.assertIn("Critical 1", row_block(first.stdout, "Q-1"))
        self.assertIn("Critical 1", row_block(second.stdout, "Q-1"))

    def test_wv21_slice5_disagreements_equivalent_across_shapes(self):
        """EC-20, EC-34, EC-43, EC-44. Q-3 entry on the first shape; same Q-3 verdict in both shapes."""
        extra = {
            "registers/defect-register.md": (
                "# Defect register\n\nEntry D-9: defect disposition, "
                "origin step Step 2.\n")}
        first_files = base_files()
        first_files.update(extra)
        first_files.update(single_page_metrics_record_files(
            metrics_record(
                body="Metrics record states the step universe as "
                     "1 step.")))
        second_files = self._second_shape_files()
        second_files.update(extra)
        parent = tracked_tempdir("msc_slice5_wv21b_")
        built = build_cases(
            ({"name": "shape-one", "features": (), "files": first_files},
             {"name": "shape-two", "features": (),
              "files": second_files}), parent)
        first = run_tool(built["shape-one"])
        second = run_tool(built["shape-two"])
        for report in (first.stdout,):
            block = disagreements_block(report)
            self.assertIn("Q-3", block)
        self.assertEqual(row_verdict(row_block(first.stdout, "Q-3")),
                         row_verdict(row_block(second.stdout, "Q-3")))

    def test_signal_two_unrelated_planned_or_target_in_core_does_not_except(self):
        """R15-07. Breaker exhibit B15R1-B4, core implementation.

        The core completeness check, _signal_failure, is called
        direct on a miscounted audit paper text: a severity table
        of 3 data rows under a header count of 5. An unrelated
        sentence placed before the header line, carrying the word
        planned, the words target count, or the words planned
        count and saying nothing about the header count, does not
        carry the brief Section 5 exception: the exception
        attaches to the header count statement, so the check
        still returns signal-two for every such text.
        """
        import metrics_starter_collector.derivation_core as core
        table = (
            "# Step 1 audit paper\n\nSeverity breakdown table. "
            "Rows stated in header: 5.\n"
            "| Severity | Count |\n| --- | --- |\n"
            "| Critical | 0 |\n| High | 1 |\n| Low | 2 |\n")
        self.assertEqual(core._signal_failure(table), "signal-two")
        for label, sentence in (
                ("planned", "Planned work is noted elsewhere.\n"),
                ("target", "A target count is kept for planning.\n"),
                ("planned-count",
                 "A planned count is kept for planning.\n")):
            with self.subTest(sentence=label):
                self.assertEqual(
                    core._signal_failure(sentence + table),
                    "signal-two")

    def test_signal_two_brief_form_header_count_exception_fires_in_core(self):
        """R15-07. The brief form of the exception, core check.

        Where the header count statement itself states the count
        as a planned count or as a target count, the core check
        returns no failure for the miscounted table, in the brief
        Section 5 form.
        """
        import metrics_starter_collector.derivation_core as core
        for label, stated in (
                ("planned",
                 "Rows stated in header: 5, stated as a planned "
                 "count."),
                ("target",
                 "Rows stated in header: 5, stated as a target "
                 "count.")):
            with self.subTest(form=label):
                text = (
                    "# Step 1 audit paper\n\nSeverity breakdown "
                    "table. " + stated + "\n"
                    "| Severity | Count |\n| --- | --- |\n"
                    "| Critical | 0 |\n| High | 1 |\n| Low | 2 |\n")
                self.assertIsNone(core._signal_failure(text))

    def test_rounds_family_reads_capture_only(self):
        """Plan Section 5 named reread test for Slice 5, Contract 1."""
        parent = tracked_tempdir("msc_slice5_reread_")
        tree = build_case(make_case("reread"), parent)
        assert_reads_capture_only(self, tree, count_reads=True)



    def test_q1_cross_check_failure_surfaced_on_row(self):
        """R15-14. Q-1 cross check failure stands surfaced on the row."""
        case = make_case("q1-cross-check-failure", {
            "audit/step-01-red.md": (
                "# Round 1\n\nPost triage breakdown: Critical 2, "
                "High 1, Medium 0, Low 0.\n"),
            "audit/step-02-red.md": (
                "# Round 2\n\nPre triage counts only: Critical 7.\n")})
        parent = tracked_tempdir("msc_slice5_")
        tree = build_case(case, parent)
        capture_fn, derive_fn, render_fn = capture_derive_render(self, tree)
        captured = capture_fn(tree)
        with mock.patch(
                "metrics_starter_collector.cross_check."
                "q1_cross_check_statement",
                side_effect=RuntimeError("q1 seam boom"), create=True):
            report = render_fn(derive_fn(captured))
        segment = statement_segment(row_block(report, "Q-1"))
        self.assertIn("error: operation q1_cross_check_statement", segment)
        self.assertIn("build-metrics-record.md", segment)
        self.assertIn("RuntimeError", segment)
        self.assertIn("q1 seam boom", segment)

    def test_q3_cross_check_failure_surfaced_on_row(self):
        """R15-14. Q-3 contested cross check failure stands surfaced."""
        extra = {
            "registers/defect-register.md": (
                "# Defect register\n\nEntry D-9: defect disposition, "
                "origin step Step 2.\n")}
        extra.update(single_page_metrics_record_files(metrics_record(
            body="Metrics record states the step universe as 1 step.")))
        parent = tracked_tempdir("msc_slice5_")
        tree = build_case(make_case("q3-cross-check-failure", extra), parent)
        capture_fn, derive_fn, render_fn = capture_derive_render(self, tree)
        captured = capture_fn(tree)
        with mock.patch(
                "metrics_starter_collector.cross_check."
                "q3_contested_statement",
                side_effect=RuntimeError("q3 seam boom")):
            report = render_fn(derive_fn(captured))
        segment = statement_segment(row_block(report, "Q-3"))
        self.assertIn("error: operation q3_contested_statement", segment)
        self.assertIn("build-metrics-record.md", segment)
        self.assertIn("RuntimeError", segment)
        self.assertIn("q3 seam boom", segment)

    def test_q4_cross_check_failure_surfaced_with_fallback_marking(self):
        """R15-14. Q-4 cross check failure surfaced, fallback not silent."""
        extra = {
            "steps/step-01-trace.md": (
                "# Trace\n\nParts: 8 LANDED, 2 PARTIAL, "
                "0 CONTRADICTED. Stated total: 10 items checked.\n")}
        extra.update(single_page_metrics_record_files(metrics_record(
            body="Metrics record states Q-4 for Step 1 as 10 of 10.")))
        parent = tracked_tempdir("msc_slice5_")
        tree = build_case(make_case("q4-cross-check-failure", extra), parent)
        capture_fn, derive_fn, render_fn = capture_derive_render(self, tree)
        captured = capture_fn(tree)
        with mock.patch(
                "metrics_starter_collector.cross_check."
                "q4_cross_check_statement",
                side_effect=RuntimeError("q4 seam boom")):
            report = render_fn(derive_fn(captured))
        segment = statement_segment(row_block(report, "Q-4"))
        self.assertIn("error: operation q4_cross_check_statement", segment)
        self.assertIn("build-metrics-record.md", segment)
        self.assertIn("RuntimeError", segment)
        self.assertIn("q4 seam boom", segment)
        self.assertIn("record disagrees", segment)

if __name__ == "__main__":
    unittest.main()

