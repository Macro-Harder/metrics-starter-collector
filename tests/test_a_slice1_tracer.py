"""Slice 1 tracer tests, restart run.

End to end on one path, in tracer form. The module asserts the
Slice 1 position in the plan test mapping: E-1, E-2 and Q-4 present
in tracer form, the T-1 refusal with code date-only-form, pointer
and reason checks, the exit numbers, Contracts 1 and 2 in minimal
form, split form assembly, the unknown definitions version refusal
scoped to the rows Slice 1 derives, the golden identity facts in
tracer form on the F-16 miniature, the WV2-21 habit cases this
slice owns, and the WV2-22 field entries for the metrics Slice 1
derives or refuses. Every tree is built through the fixture builder
into a temporary directory, and the product is invoked through the
pre install route, python3 -m metrics_starter_collector from the
public repo root, root argument first, then the optional report
argument in its two word form.
"""
import re
import subprocess
import sys
import unittest
from pathlib import Path

from tests.fixture_builder import (
    F16_FILE_COUNT,
    REASON_CODES,
    FixtureTestCase,
    STARTER_ORDER,
    assert_reads_capture_only,
    assert_two_part_form,
    assert_verdict,
    build_case,
    build_cases,
    clean_files,
    data_quality_entry_for,
    data_quality_section,
    f16_miniature_case,
    measure_tree,
    metrics_text,
    row_block,
    row_order,
    row_verdict,
    single_page_metrics_record_files,
    tracked_tempdir,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def run_tool(root, extra=()):
    """Run the product through the module entry route as a subprocess."""
    cmd = [sys.executable, "-m", "metrics_starter_collector", str(root)]
    cmd.extend(extra)
    return subprocess.run(cmd, capture_output=True, text=True,
                          cwd=str(REPO_ROOT), timeout=120)


def run_tool_no_root(extra=()):
    """Run the product with no root argument, as a subprocess."""
    cmd = [sys.executable, "-m", "metrics_starter_collector"]
    cmd.extend(extra)
    return subprocess.run(cmd, capture_output=True, text=True,
                          cwd=str(REPO_ROOT), timeout=120)


def step_record_text(step, base=2, team=2, total_spins=4, extra=""):
    return ("# Step %d record\n\nBuild: metrics fixture build.\n"
            "Base: %d. Team staffed: %d agents. Total spins: %d.\n%s\n"
            % (step, base, team, total_spins, extra))


def roster_text(step, base=2, additions=0):
    return ("# Step %d roster\n\nNamed agents: 2. Base: %d.\n"
            "Roster additions over base: %d.\n" % (step, base, additions))


def gate_record_text(step, trace="2 LANDED of 2 items checked, "
                                 "0 PARTIAL, 0 CONTRADICTED"):
    return ("# Step %d gate record\n\nClosure state: CLOSED-PASS.\n"
            "First trace for step %d: %s.\n" % (step, step, trace))


def gate_ruling_text(step, trace="2 LANDED of 2 items checked, "
                                 "0 PARTIAL, 0 CONTRADICTED"):
    return ("# Step %d gate ruling\n\nClosure state: CLOSED-PASS.\n"
            "First trace for step %d: %s.\n" % (step, step, trace))


def ledger_text(transitions, steps="1, 2, 3", extra=""):
    return ("# Path ledger\n\nSteps stated: %s.\n\n## Transitions\n\n"
            "%s\n%s\n" % (steps, transitions, extra))


def full_clock_transitions(steps=(1, 2, 3)):
    return "\n".join(
        "Step %d IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 17:00."
        % n for n in steps)


def date_only_transitions(steps=(1, 2, 3)):
    return "\n".join(
        "Step %d IN PROGRESS 2026-11-01, closed 2026-11-02." % n
        for n in steps)


def clean_case(name, ledger=None, metrics=None, features=()):
    return {"name": name, "features": tuple(features),
            "files": clean_files(ledger=ledger, metrics=metrics)}


def _substance_normalised(text):
    value = text.lower()
    value = value.replace("gate-ruling", "gate-file")
    value = value.replace("gate-record", "gate-file")
    value = value.replace("gate ruling", "gate file")
    value = value.replace("gate record", "gate file")
    return re.sub(r"\s+", " ", value).strip()


def _row_substance(block):
    """Return the EC-04 compared parts of one row block, normalised.

    The form follows the Slice 7 _row_substance helper: verdict,
    value or its stated absence, numerator and denominator where
    the metric is a share, step coverage, pointer in substance,
    and reason in substance where the verdict is not present.
    """
    substance = {"verdict": row_verdict(block)}
    lines = block.splitlines()
    first = lines[0] if lines else ""
    segments = [segment.strip() for segment in first.split(" | ")]
    value_segments = []
    for segment in segments[2:]:
        if segment.startswith("Pointer:"):
            substance["pointer"] = _substance_normalised(segment)
        elif segment.lower().startswith("denominator"):
            substance["coverage"] = _substance_normalised(segment)
        else:
            value_segments.append(segment)
    value = "; ".join(value_segments)
    if value:
        substance["value"] = _substance_normalised(value)
        share = re.search(r"(\d+) of (\d+)", value)
        if share:
            substance["numerator"] = share.group(1)
            substance["share denominator"] = share.group(2)
    reason = " ".join(line for line in lines
                      if line.startswith("Reason:"))
    if reason:
        substance["reason"] = _substance_normalised(reason)
    return substance


class TestSlice1Tracer(FixtureTestCase):

    def build(self, case):
        return build_case(case, tracked_tempdir("msc_slice1_"))

    def test_tracer_end_to_end_full_set_on_clean_tree(self):
        """Contract 2 in tracer form: all 17 rows print, in order."""
        root = self.build(clean_case("tracer-clean"))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(row_order(result.stdout), STARTER_ORDER)

    def test_tracer_present_rows_e1_e2_q4_in_tracer_form(self):
        """WV22 E-1 F1 F2, WV22 E-2 F1 F2, WV22 Q-4 F1 F2 F3; EC-28, EC-29, EC-35."""
        root = self.build(clean_case("tracer-present"))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        for code in ("E-1", "E-2", "Q-4"):
            assert_verdict(self, row_block(result.stdout, code),
                           "present", code)

    def test_t1_refusal_date_only_form(self):
        """T-1 refusal under W8-3; EC-24; WV22 T-1 F1 F2."""
        root = self.build(clean_case(
            "t1-date-only", ledger=ledger_text(date_only_transitions()),
            features=("date-only-timestamps",)))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "T-1")
        assert_verdict(self, block, "missing", "T-1")
        self.assertIn("date-only-form", block)
        self.assertIn("PATH-LEDGER.md", block)

    def test_wv22_t1_f1_opening_timestamp_form(self):
        """WV22 T-1 F1: a time of day on the opening entry counts, a date only does not."""
        built = build_cases(
            (clean_case("t1-f1-full",
                        ledger=ledger_text(full_clock_transitions()),
                        features=("full-clock-timestamps",)),
             clean_case("t1-f1-date",
                        ledger=ledger_text(date_only_transitions()),
                        features=("date-only-timestamps",))),
            tracked_tempdir("msc_slice1_"))
        full = run_tool(built["t1-f1-full"])
        assert_verdict(self, row_block(full.stdout, "T-1"),
                       "present", "T-1")
        dated = run_tool(built["t1-f1-date"])
        block = row_block(dated.stdout, "T-1")
        assert_verdict(self, block, "missing", "T-1")
        self.assertIn("date-only-form", block)

    def test_wv22_t1_f2_both_transitions_required(self):
        """WV22 T-1 F2: opening in form and closing date only fails the step.

        Corrected at Step 15 round 1, item R15-03: the step fails,
        and under the D4R-03 aggregation rule the row stands
        present on the passing steps alone, with Step 1 named as
        failing on the date only condition, in place of the
        partial-span refusal this test pinned before the fix.
        """
        ledger = ledger_text(
            "Step 1 IN PROGRESS 2026-11-01 09:00, closed 2026-11-02.\n"
            "Step 2 IN PROGRESS 2026-11-02 09:00, closed 2026-11-02 17:00.\n"
            "Step 3 IN PROGRESS 2026-11-03 09:00, closed 2026-11-03 17:00.")
        root = self.build(clean_case("t1-f2-mixed", ledger=ledger))
        result = run_tool(root)
        block = row_block(result.stdout, "T-1")
        assert_verdict(self, block, "present", "T-1")
        self.assertNotIn("partial-span", block)
        self.assertIn("Step 2 elapsed 8 hours", block)
        self.assertIn("Step 3 elapsed 8 hours", block)
        self.assertNotIn("Step 1 elapsed", block)
        self.assertIn("Step 1", block)
        self.assertIn("date only", block.lower())

    def test_wv22_t1_f1_time_outside_transitions_counts_for_nothing(self):
        """WV22 T-1 F1: a time of day outside the transition entries counts for nothing."""
        case = clean_case("t1-outside",
                          ledger=ledger_text(date_only_transitions()))
        case["files"]["steps/step-01-record.md"] = step_record_text(
            1, extra="Work ran 09:00 to 17:00 on the day.")
        root = self.build(case)
        result = run_tool(root)
        block = row_block(result.stdout, "T-1")
        assert_verdict(self, block, "missing", "T-1")
        self.assertIn("date-only-form", block)

    def test_wv22_e1_f1_f2_staffed_and_base_for_same_step(self):
        """WV22 E-1 F1 F2; EC-28: both fields must stand for the same step."""
        case = clean_case("e1-same-step")
        case["files"]["steps/step-02-roster.md"] = (
            "# Step 2 roster\n\nNamed agents: 2.\n"
            "Roster additions over base: 0.\n")
        root = self.build(case)
        result = run_tool(root)
        block = row_block(result.stdout, "E-1")
        assert_verdict(self, block, "present", "E-1")
        self.assertIn("Step 2", block)

    def test_wv22_e1_f2_base_for_a_different_step_does_not_count(self):
        """WV22 E-1 F2: a base count standing for another step counts for nothing here."""
        case = clean_case("e1-other-step")
        case["files"]["steps/step-02-record.md"] = (
            "# Step 2 record\n\nBuild: metrics fixture build.\n"
            "Team staffed: 2 agents. Total spins: 4.\n")
        case["files"]["steps/step-02-roster.md"] = (
            "# Step 2 roster\n\nNamed agents: 2.\n"
            "Roster additions over base: 0.\n")
        root = self.build(case)
        result = run_tool(root)
        block = row_block(result.stdout, "E-1")
        assert_verdict(self, block, "present", "E-1")
        self.assertIn("Step 2", block)
        self.assertNotIn("Step 2 staffed", block)
        self.assertRegex(block, r"(of 3 steps\b|(?<!\d)3 steps\b)")

    def test_wv22_e2_f1_additions_labelled(self):
        """WV22 E-2 F1; EC-29: additions print labelled as additions over base."""
        root = self.build(clean_case(
            "e2-additions", features=("additions-over-base-stated",)))
        result = run_tool(root)
        block = row_block(result.stdout, "E-2")
        assert_verdict(self, block, "present", "E-2")
        self.assertIn("additions over base", block.lower())

    def test_wv22_e2_f2_total_spins_labelled_beside_additions(self):
        """WV22 E-2 F2; EC-29: total spins print labelled, beside and never merged."""
        root = self.build(clean_case("e2-split"))
        result = run_tool(root)
        block = row_block(result.stdout, "E-2")
        assert_verdict(self, block, "present", "E-2")
        lowered = block.lower()
        self.assertIn("additions over base", lowered)
        self.assertIn("total spins", lowered)

    def test_wv22_e2_f3_total_alone_never_counts_as_additions(self):
        """WV22 E-2 F3; EC-29: a total alone yields no additions figure."""
        case = clean_case("e2-total-only", features=("total-only-step",))
        for n in (1, 2, 3):
            case["files"]["steps/step-%02d-roster.md" % n] = (
                "# Step %d roster\n\nNamed agents: 2. Base: 2.\n" % n)
        root = self.build(case)
        result = run_tool(root)
        block = row_block(result.stdout, "E-2")
        self.assertIn("total spins", block.lower())
        self.assertIn("not derivable", block.lower())

    def test_wv22_q4_f1_first_trace_identified_not_a_later_trace(self):
        """WV22 Q-4 F1; EC-35: the first trace counts, a later trace does not."""
        case = clean_case("q4-first")
        case["files"]["steps/step-01-gate-record.md"] = gate_record_text(
            1, trace="2 LANDED of 2 items checked, 0 PARTIAL, "
                     "0 CONTRADICTED")
        case["files"]["steps/step-01-trace-record.md"] = (
            "# Step 1 later trace record\n\nParts: 9 LANDED, 0 PARTIAL, "
            "0 CONTRADICTED. Stated total: 9 items checked.\n")
        root = self.build(case)
        result = run_tool(root)
        block = row_block(result.stdout, "Q-4")
        assert_verdict(self, block, "present", "Q-4")
        self.assertNotIn("9 LANDED", block)

    def test_wv22_q4_f2_f3_parts_sum_to_stated_total(self):
        """WV22 Q-4 F2 F3; EC-35: parts by class sum to the stated total."""
        root = self.build(clean_case(
            "q4-sum", features=("first-trace-per-counted-step",)))
        result = run_tool(root)
        block = row_block(result.stdout, "Q-4")
        assert_verdict(self, block, "present", "Q-4")
        self.assertRegex(block, r"(?<!\d)6 LANDED\b")
        self.assertRegex(block, r"(?<!\d)0 PARTIAL\b")
        self.assertRegex(block, r"(?<!\d)0 CONTRADICTED\b")
        self.assertRegex(block, r"(?<!\d)6 items checked\b")

    def test_wv22_q4_f3_sum_test_exception_beside_reconciled_steps(self):
        """WV22 Q-4 F3; EC-35: one excepted step, the build verdict stays present."""
        case = clean_case("q4-excepted", features=("parts-fail-sum",))
        case["files"]["steps/step-02-gate-record.md"] = gate_record_text(
            2, trace="2 LANDED, 1 PARTIAL, 0 CONTRADICTED summing to 3 "
                     "against a stated total of 2 items checked")
        root = self.build(case)
        result = run_tool(root)
        block = row_block(result.stdout, "Q-4")
        assert_verdict(self, block, "present", "Q-4")
        self.assertIn("Step 2", block)

    def test_wv22_q4_f3_all_contributions_excepted_is_not_derivable(self):
        """WV22 Q-4 F3; EC-35: every contribution excepted, the row is not derivable."""
        case = clean_case("q4-all-excepted", features=("parts-fail-sum",))
        for n in (1, 2, 3):
            case["files"]["steps/step-%02d-gate-record.md" % n] = (
                gate_record_text(
                    n, trace="2 LANDED, 1 PARTIAL, 0 CONTRADICTED summing "
                             "to 3 against a stated total of 2 items "
                             "checked"))
        root = self.build(case)
        result = run_tool(root)
        block = row_block(result.stdout, "Q-4")
        assert_verdict(self, block, "present but not derivable", "Q-4")

    def test_f19_mapping_force_statement_refused_and_absent_file_figure(self):
        """Brief family F-19 mapping test; D4R-25, R-256: force refused, absent file not recorded."""
        case = clean_case(
            "f19-mapping",
            metrics=metrics_text(body_extra=(
                "Record change statement: the per step money field "
                "for every step stands IN FORCE and is asserted "
                "present as a field of the step records for E-4.\n"
                "Tokens for Step 1: 5000, recorded in "
                "registers/cost-ledger.md.\n")))
        root = self.build(case)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        money = row_block(result.stdout, "E-4")
        assert_verdict(self, money, "present but not derivable", "E-4")
        self.assertIn("missing-field", money)
        tokens = row_block(result.stdout, "E-3")
        assert_verdict(self, tokens, "missing", "E-3")
        self.assertIn("registers/cost-ledger.md", tokens)
        self.assertIn("R-256", tokens)

    def test_f18_unknown_definitions_version_slice1_rows(self):
        """F-18 scoped to Slice 1 rows; EC-03: feeders standing take the refusal."""
        root = self.build(clean_case(
            "f18-slice1",
            metrics=metrics_text(header_version="unknown-version-999"),
            features=("unknown-definitions-version",)))
        result = run_tool(root)
        for code in ("E-1", "E-2", "Q-4"):
            block = row_block(result.stdout, code)
            assert_verdict(self, block, "present but not derivable", code)
            self.assertIn("unknown-definitions-version", block, code)
            self.assertIn("unknown-version-999", block, code)

    def test_f18_unknown_version_metric_without_feeder_stays_missing(self):
        """F-18 second limb; EC-03: a metric with no feeder record stays missing."""
        case = clean_case(
            "f18-no-feeder",
            metrics=metrics_text(header_version="unknown-version-999"))
        for n in (1, 2, 3):
            del case["files"]["steps/step-%02d-gate-record.md" % n]
        root = self.build(case)
        result = run_tool(root)
        block = row_block(result.stdout, "Q-4")
        assert_verdict(self, block, "missing", "Q-4")

    def test_two_part_reason_form_label_order_and_code_position(self):
        """A7-10: label order and code position, on a row and on an entry."""
        case = clean_case(
            "two-part", ledger=ledger_text(
                "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02."))
        case["files"]["steps/step-02-record.md"] = (
            "# Step 2 record\n\nBuild: metrics fixture build.\n")
        case["malformations"] = (
            {"switch": "M-01", "target": "steps/step-02-record.md",
             "target_kind": "SR", "state": "not-valid-text"},)
        root = self.build(case)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "T-1")
        assert_two_part_form(self, block, "date-only-form", "T-1 reason line")
        entry = data_quality_entry_for(result.stdout, "step-02-record.md")
        self.assertTrue(entry, "data quality entry for the malformed piece")
        assert_two_part_form(self, entry, "malformed-piece",
                             "data quality entry")

    def test_two_part_reason_form_no_code_fits_case(self):
        """A7-10: one reason line and one entry carry the no code fits wording."""
        case = clean_case("no-code-fits", ledger=ledger_text(
            "Step 1 IN PROGRESS 2026-11-01 09:00 UTC, first timestamp "
            "stands with its basis stated as UTC."))
        case["files"]["steps/step-03-gate-record.md"] = (
            "# Step 3 gate record\n\nClosing ruling at 2026-11-03 17:00 "
            "with no time basis stated.\nClosure state: CLOSED-PASS.\n")
        root = self.build(case)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "B-1")
        assert_verdict(self, block, "present but not derivable", "B-1")
        assert_two_part_form(self, block, "no code fits", "B-1 reason line")
        section = data_quality_section(result.stdout)
        self.assertTrue(section, "data quality section stands")
        found = False
        import re
        for chunk in re.split(r"\n\s*\n", section):
            if "no code fits" in chunk.lower() and \
                    "what the record shows" in chunk.lower():
                assert_two_part_form(self, chunk, "no code fits",
                                     "data quality entry")
                found = True
        self.assertTrue(found, "one data quality entry carries the no "
                               "code fits wording at its second part start")

    def test_pointer_and_reason_on_all_rows_of_damaged_tree(self):
        """Pointer and reason checks on all 17 rows of a damaged tree."""
        root = self.build(clean_case(
            "damaged", ledger=ledger_text(
                "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.")))
        result = run_tool(root)
        for code in STARTER_ORDER:
            block = row_block(result.stdout, code)
            self.assertTrue(block, code)
            self.assertRegex(block, r"Pointer:[^\n]*\.md", code)
            if row_verdict(block) != "present":
                self.assertIn("Reason", block, code)
                self.assertTrue(
                    any(reason_code in block
                        for reason_code in REASON_CODES),
                    "no reason code stands on the row for " + code)

    def test_exit_zero_on_completed_report(self):
        """Exit contract: a completed report exits 0."""
        root = self.build(clean_case("exit-zero"))
        self.assertEqual(run_tool(root).returncode, 0)

    def test_exit_two_on_no_arguments(self):
        """Exit contract and grammar: no root argument exits 2 with usage."""
        result = run_tool_no_root()
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage", (result.stderr + result.stdout).lower())

    def test_exit_two_on_extra_argument(self):
        """Grammar: an argument beyond root and report exits 2."""
        root = self.build(clean_case("exit-extra"))
        result = run_tool(root, extra=("extra-position",))
        self.assertEqual(result.returncode, 2)

    def test_exit_two_on_unknown_option(self):
        """Grammar: an option other than the report option exits 2."""
        root = self.build(clean_case("exit-unknown"))
        result = run_tool(root, extra=("--bogus",))
        self.assertEqual(result.returncode, 2)

    def test_exit_two_on_help_and_version_forms_barred(self):
        """Grammar: help and version forms are barred in version 1."""
        root = self.build(clean_case("exit-barred"))
        self.assertEqual(run_tool(root, extra=("--help",)).returncode, 2)
        self.assertEqual(run_tool(root, extra=("--version",)).returncode, 2)

    def test_exit_two_on_report_without_path_and_repeated_report(self):
        """Grammar: a report word with no path, and a repeated report, exit 2."""
        root = self.build(clean_case("exit-report-form"))
        self.assertEqual(run_tool(root, extra=("--report",)).returncode, 2)
        out = Path(root).parent / "r1.md"
        result = run_tool(root, extra=("--report", str(out),
                                       "--report", str(out)))
        self.assertEqual(result.returncode, 2)

    def test_report_argument_two_word_form_writes_the_named_file(self):
        """Grammar: root first, then the report argument in its two word form."""
        root = self.build(clean_case("report-file"))
        out = Path(root).parent / "named-report.md"
        result = run_tool(root, extra=("--report", str(out)))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(out.is_file())
        text = out.read_text(encoding="utf-8")
        self.assertEqual(row_order(text), STARTER_ORDER)

    def test_exit_one_on_unreadable_input(self):
        """Exit contract: a root that cannot be read at all exits 1."""
        parent = tracked_tempdir("msc_slice1_")
        result = run_tool(parent / "no_such_root")
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("No module named", result.stderr)

    def test_exit_one_on_file_as_root(self):
        """Exit contract: a file given as the root exits 1."""
        root = self.build(clean_case("exit-file-root"))
        result = run_tool(root / "PATH-LEDGER.md")
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("No module named", result.stderr)

    def test_contract1_direct_minimal(self):
        """Contract 1 in minimal form: derivations read the one capture only."""
        capture_root = self.build(clean_case("contract1-capture"))
        assert_reads_capture_only(self, capture_root, count_reads=True)
        root = self.build(clean_case("contract1-run"))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("latest record timestamp", result.stdout.lower())
        self.assertNotIn("run time:", result.stdout.lower())

    def test_contract2_direct_minimal(self):
        """Contract 2 in minimal form: the full set prints in starter order."""
        root = self.build(clean_case("contract2"))
        result = run_tool(root)
        self.assertEqual(row_order(result.stdout), STARTER_ORDER)
        for code in STARTER_ORDER:
            self.assertTrue(row_block(result.stdout, code),
                            "row missing for " + code)

    def test_tracer_reads_capture_only(self):
        """Named reread test for Slice 1, plan Section 5."""
        root = self.build(clean_case("reread"))
        assert_reads_capture_only(self, root)

    def test_split_form_assembly_page_order(self):
        """Split form assembly under D-08; EC-06, EC-04 for the D-1 row."""
        case = clean_case("split-order", features=("split-metrics-record",))
        del case["files"]["wiki/wiki/synthesis/build-metrics-record.md"]
        case["files"]["wiki/wiki/synthesis/build-metrics-record-part-z.md"] = (
            "# Metrics record page stated first\n\nPage order: 1.\n\n"
            "## Decision table\n\n"
            "| Item | Origin step | Raised | Presented | Ruled |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| Q-1 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | "
            "2026-11-01 13:00 |\n")
        case["files"]["wiki/wiki/synthesis/build-metrics-record-part-a.md"] = (
            "# Metrics record page stated second\n\nPage order: 2.\n\n"
            "| Q-2 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | "
            "2026-11-01 11:00 |\n")
        root = self.build(case)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        self.assertRegex(block, r"median[^\d]*2(?!\d)(?!\.\d)")

    def test_split_form_missing_page_tables_absent(self):
        """Split form assembly under D-08; EC-06: a missing page supplies no tables."""
        case = clean_case("split-missing",
                          features=("split-metrics-record",))
        del case["files"]["wiki/wiki/synthesis/build-metrics-record.md"]
        case["files"]["wiki/wiki/synthesis/build-metrics-record-part-1.md"] = (
            "# Metrics record page 1\n\nPage order: 1.\n\n"
            "Decision table stands on page 2, which is absent.\n")
        root = self.build(case)
        result = run_tool(root)
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "missing", "D-1")

    def test_split_form_single_page_precedence(self):
        """Split form assembly under D-08; EC-06: the single page form governs."""
        case = clean_case("split-precedence")
        case["files"]["wiki/wiki/synthesis/build-metrics-record-part-1.md"] = (
            "# Split copy\n\nSplit copy states the D-1 figure as 4242 "
            "hours.\n")
        root = self.build(case)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        self.assertNotIn("4242", block)

    def test_wv21_ec06_split_shape_same_verdicts_as_single_page(self):
        """EC-06, EC-04, EC-13: split and single page shapes agree row by row."""
        single = clean_case("shape-single",
                            features=("single-page-metrics-record",))
        split = clean_case("shape-split",
                           features=("split-metrics-record",
                                     "second-shape-habits"))
        del split["files"]["wiki/wiki/synthesis/build-metrics-record.md"]
        split["files"][
            "wiki/wiki/synthesis/build-metrics-record-part-1.md"] = (
            "# Build metrics record, page 1\n\nPage order: 1.\n\n"
            "Build: metrics fixture build.\n\nStep table stands "
            "complete for the fixture steps.\n")
        split["files"][
            "wiki/wiki/synthesis/build-metrics-record-part-2.md"] = (
            "# Build metrics record, page 2\n\nPage order: 2.\n\n"
            "## Decision table\n\n"
            "| Item | Origin step | Raised | Presented | Ruled |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| Q-1 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | "
            "2026-11-01 13:00 |\n")
        built = build_cases((single, split), tracked_tempdir("msc_slice1_"))
        first = run_tool(built["shape-single"])
        second = run_tool(built["shape-split"])
        for code in STARTER_ORDER:
            self.assertEqual(
                _row_substance(row_block(first.stdout, code)),
                _row_substance(row_block(second.stdout, code)),
                "row substance differs between shapes on %s, shape "
                "difference: metrics record split across pages" % code)

    def test_wv21_ec09_gate_ruling_name_same_verdicts(self):
        """EC-09, EC-04, EC-19, EC-28: gate files under the ruling name read the same."""
        record_shape = clean_case("gate-record-shape",
                                  features=("gate-record-name",))
        ruling_case = clean_case("gate-ruling-shape",
                                 features=("gate-ruling-name",
                                           "second-shape-habits"))
        for n in (1, 2, 3):
            old = ruling_case["files"].pop(
                "steps/step-%02d-gate-record.md" % n)
            ruling_case["files"]["steps/step-%02d-gate-ruling.md" % n] = (
                old.replace("gate record", "gate ruling"))
        built = build_cases((record_shape, ruling_case),
                            tracked_tempdir("msc_slice1_"))
        first = run_tool(built["gate-record-shape"])
        second = run_tool(built["gate-ruling-shape"])
        for code in ("E-1", "E-2", "Q-4"):
            self.assertEqual(
                _row_substance(row_block(first.stdout, code)),
                _row_substance(row_block(second.stdout, code)),
                "row substance differs between shapes on %s, shape "
                "difference: gate files under the ruling name" % code)

    def test_step_universe_includes_step_evidenced_only_by_regate_record(self):
        """Step universe variant gate test; EC-09, EC-10."""
        case = clean_case("regate-only")
        del case["files"]["steps/step-02-record.md"]
        del case["files"]["steps/step-02-gate-record.md"]
        case["files"]["steps/step-02-regate-record.md"] = (
            gate_record_text(2).replace("gate record", "regate record"))
        root = self.build(case)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "E-1")
        assert_verdict(self, block, "present", "E-1")
        self.assertIn("Step 2", block)
        self.assertRegex(block, r"(denominator[^\d]*3(?!\d)(?!\.\d)|"
                                r"of 3 steps\b|(?<!\d)3 steps\b)")

    def test_golden_identity_facts_in_tracer_form_on_f16_miniature(self):
        """Golden identity facts in tracer form; EC-01, EC-02, EC-10, EC-42."""
        case = f16_miniature_case()
        root = self.build(case)
        self.assertEqual(measure_tree(root)["files"], F16_FILE_COUNT)
        for step in range(1, 24):
            self.assertTrue(
                (root / ("steps/step-%02d-record.md" % step)).is_file(),
                "step record to Step 23 stands for step %d" % step)
        metrics = (root / "wiki/wiki/synthesis/build-metrics-record.md"
                   ).read_text(encoding="utf-8")
        self.assertIn("Step 18 row.", metrics)
        self.assertNotIn("Step 19 row.", metrics)
        ledger = (root / "PATH-LEDGER.md").read_text(encoding="utf-8")
        self.assertIn("Step 18 closed", ledger)
        paper = (root / "audit/step-17-audit-paper.md").read_text(
            encoding="utf-8")
        self.assertIn("TRUNCATED", paper)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        for code in ("E-1", "E-2", "Q-4"):
            assert_verdict(self, row_block(result.stdout, code),
                           "present", code)
        block = row_block(result.stdout, "T-1")
        assert_verdict(self, block, "missing", "T-1")
        self.assertIn("date-only-form", block)
        self.assertIn("Step 13", row_block(result.stdout, "Q-4"))

    def test_header_coverage_and_data_quality_sections_present(self):
        """Report head and sections; EC-41, EC-42."""
        root = self.build(clean_case("sections"))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(str(root), result.stdout)
        self.assertIn("coverage", result.stdout.lower())
        self.assertIn("piece inventory", result.stdout.lower())
        self.assertIn("data quality", result.stdout.lower())

    def test_no_score_grade_or_estimated_figure_in_report(self):
        """Closed report content; EC-49."""
        root = self.build(clean_case("closed-content"))
        result = run_tool(root)
        lowered = result.stdout.lower()
        for word in ("score:", "grade:", "digest", "estimated"):
            self.assertNotIn(word, lowered)

    def test_determinism_same_tree_same_rows(self):
        """Determinism; EC-48: two runs on one unchanged tree agree."""
        root = self.build(clean_case("determinism"))
        first = run_tool(root)
        second = run_tool(root)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)


if __name__ == "__main__":
    unittest.main()
