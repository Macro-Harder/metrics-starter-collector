"""Slice 3 tests: step universe, gates, staffing family E-1, E-2, F-2.

Cases state their citations in the test design record form: EC
numbers for WV2-21 points and WV22 with metric and field numbers
for WV2-22 fields. Fixture trees stand built through the fixture
builder into temporary directories, and the product stands invoked
through the pre install invocation route, python3 -m
metrics_starter_collector with the root argument first, by the
run_tool harness in the fixture builder.
"""
import re
import unittest

from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     audit_paper_failed_signal,
                                     assert_reads_capture_only, build_case,
                                     build_cases, coverage_statement,
                                     gate_record, gate_ruling, metrics_record,
                                     path_ledger, row_block, run_tool,
                                     statement_segment, step_record,
                                     unmarked_case,
                                     tracked_tempdir)


def staffing_files(steps=(1, 2, 3), closure="CLOSED-PASS"):
    files = {}
    transitions = []
    for n in steps:
        files["steps/step-%02d-record.md" % n] = step_record(n)
        files["steps/step-%02d-gate-record.md" % n] = gate_record(n, closure)
        transitions.append(
            "Step %d IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 17:00." % n)
    files["PATH-LEDGER.md"] = path_ledger(
        "\n".join(transitions), ", ".join(str(s) for s in steps))
    files["TIER-RECORD.md"] = "# Tier record\n\nTier: Low. Base: 2.\n"
    files["wiki/wiki/synthesis/build-metrics-record.md"] = metrics_record(
        body="Step table stands complete for the fixture steps.")
    return files


def staffing_case(name, steps=(1, 2, 3), closure="CLOSED-PASS", features=()):
    return {"name": name, "features": tuple(features),
            "files": staffing_files(steps, closure)}


def build_one(case):
    return build_case(case, tracked_tempdir("msc_slice3_"))


class TestSlice3Staffing(FixtureTestCase):

    def test_f04_both_gate_names_read(self):
        """F-04. EC-09, EC-19. Gate record and gate ruling both read.

        The ruling name file stands as the sole source of one
        asserted subcount: Step 3 carries no gate record, only a
        gate ruling in the qualified form, so the qualified
        subcount of 1 can stand only if the ruling name is read.
        """
        case = staffing_case("f04-both-names")
        case["files"]["steps/step-01-gate-ruling.md"] = gate_ruling(1)
        del case["files"]["steps/step-03-gate-record.md"]
        case["files"]["steps/step-03-gate-ruling.md"] = gate_ruling(
            3, "CLOSED-QUALIFIED")
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")
        self.assertRegex(block, r"qualified[^\d]*1(?!\d)(?!\.\d)")
        self.assertRegex(block, r"plain[^\d]*2(?!\d)(?!\.\d)")

    def test_f04_step_with_neither_gate_name(self):
        """F-04. EC-09, EC-23. A step with neither gate name stands missing."""
        case = staffing_case("f04-neither-name")
        del case["files"]["steps/step-03-gate-record.md"]
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")
        self.assertIn("Step 3", block)

    def test_f03_metrics_record_stops_early_coverage_naming(self):
        """F-03. EC-42. Coverage naming where the metrics record stops early."""
        case = staffing_case("f03-stops-early")
        case["files"]["wiki/wiki/synthesis/build-metrics-record.md"] = (
            metrics_record(body="Step table stops at Step 1. "
                                "Steps 2 and 3 not stated."))
        root = build_one(case)
        result = run_tool(root)
        cov = coverage_statement(result.stdout)
        self.assertTrue(cov, "header coverage statement stands")
        self.assertIn("Step 2", cov)
        self.assertIn("Step 3", cov)

    def test_g01_exact_closure_state_matching_two_subcounts(self):
        """G-01. WV22 F-2 F3, WV22 F-2 F4. Exact closure matching, two subcounts."""
        case = staffing_case("g01-closures", steps=(1, 2, 3, 4))
        case["files"]["steps/step-01-gate-record.md"] = gate_record(1, "CLOSED-PASS")
        case["files"]["steps/step-02-gate-record.md"] = gate_record(2, "CLOSED-QUALIFIED")
        case["files"]["steps/step-03-gate-record.md"] = gate_record(3, "CLOSED-FAIL")
        case["files"]["steps/step-04-gate-record.md"] = gate_record(4, "CLOSED-PASS-EXTRA")
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present but not derivable", "F-2")
        self.assertRegex(block, r"plain[^\d]*1(?!\d)(?!\.\d)")
        self.assertRegex(block, r"qualified[^\d]*1(?!\d)(?!\.\d)")

    def test_g02_adjudication_as_first_ruling_source(self):
        """G-02. WV22 F-2 F1 to F4 exclusion limb; EC-09, EC-32.

        An outcome standing only in an adjudication record never
        counts, excluded from numerator and denominator alike: the
        F-2 row stands present but not derivable on the adjudication
        only fixture, with the reason naming the adjudication record
        kind, never stated as absence of a ruling.
        """
        case = staffing_case("g02-adjudication", steps=(1,))
        del case["files"]["steps/step-01-gate-record.md"]
        case["files"]["steps/step-01-gate-adjudication.md"] = gate_record(
            1, "CLOSED-PASS", extra="Adjudication states the first gate outcome.")
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present but not derivable", "F-2")
        reason = _row_substance(block).get("Reason", "")
        if not reason:
            for chunk in block.splitlines()[0].split(" | "):
                chunk = chunk.strip()
                if chunk.lower().startswith("reason:"):
                    reason = chunk.lower()
        self.assertIn("adjudication", reason,
                      "F-2 Reason part does not name the adjudication "
                      "record kind: %r" % (reason,))

    def test_g02_step_record_gate_histories_never_read(self):
        """G-02. WV22 F-2 F1. Gate histories inside step records never count."""
        case = staffing_case("g02-history", steps=(1,))
        del case["files"]["steps/step-01-gate-record.md"]
        case["files"]["steps/step-01-record.md"] = step_record(
            1, extra="Gate history inside this record claims CLOSED-PASS.")
        root = build_one(case)
        result = run_tool(root)
        assert_verdict(self, row_block(result.stdout, "F-2"),
                       "present but not derivable", "F-2")

    def test_g03_additions_over_base_with_ca9_three_figures(self):
        """G-03. WV22 E-2 F1, WV22 E-2 F2. Additions over base, three figures.

        Corrected at Step 15 round 1, item R15-02: the fixture
        step now states a roster additions entry, so the present
        verdict rests on that entry and not on a total minus
        base derivation the brief forbids.
        """
        case = staffing_case("g03-additions", steps=(1,))
        case["files"]["steps/step-01-record.md"] = step_record(
            1, base=2, total_spins=7, additions=1,
            extra="Detail total spins: 7. Stated total spins: 6.")
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "E-2")
        assert_verdict(self, block, "present", "E-2")
        self.assertIn("additions over base", block.lower())
        self.assertIn("total spins", block.lower())
        self.assertRegex(block, r"detail[^\d]*7(?!\d)(?!\.\d)")
        self.assertRegex(block, r"stated[^\d]*6(?!\d)(?!\.\d)")
        self.assertRegex(block, r"variance[^\d]*1(?!\d)(?!\.\d)")

    def test_g03_step_with_no_base_named_for_additions_only(self):
        """G-03. WV22 E-2 F3. No base named: the step stands named, no figure.

        Corrected at Step 15 round 1, item R15-02: Step 1 now
        states a roster additions entry, so the present verdict
        rests on that entry and not on a total minus base
        derivation the brief forbids.
        """
        case = staffing_case("g03-no-base", steps=(1, 2))
        case["files"]["steps/step-01-record.md"] = step_record(
            1, additions=1)
        case["files"]["steps/step-02-record.md"] = (
            "# Step 2 record\n\nNo base stated. Total spins: 5.\n")
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "E-2")
        assert_verdict(self, block, "present", "E-2")
        self.assertIn("Step 2", block)
        self.assertIn("missing-field", block)

    def test_g04_keeper_gate_in_qualified_subcount_no_t7_effect(self):
        """G-04. EC-09. Step 22 classed by content, qualified, no T-7 effect."""
        case = staffing_case("g04-keeper", steps=(22,))
        case["files"]["steps/step-22-gate-record.md"] = gate_record(
            22, "CLOSED-QUALIFIED",
            extra="Release gate record held by the Release-gate Keeper. Outcome: Go.")
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "F-2")
        self.assertRegex(block, r"qualified[^\d]*1(?!\d)(?!\.\d)")
        assert_verdict(self, row_block(result.stdout, "T-7"), "missing", "T-7")

    def test_g04_recycled_step_counted_once(self):
        """G-04. Spin 772 key: a recycled instance yields one key, counted once."""
        case = staffing_case("g04-recycled", steps=(2,))
        case["files"]["steps/step-02-gate-record.md"] = gate_record(2, "CLOSED-FAIL")
        case["files"]["steps/step-02-regate-record.md"] = gate_record(
            2, "CLOSED-QUALIFIED", extra="Recycled instance ruling.")
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")
        self.assertRegex(block, r"(denominator[^\d]*1(?!\d)(?!\.\d)|of 1(?!\d))")

    def test_g09_e1_present_with_coverage_remainder_named(self):
        """G-09. EC-28. WV22 E-1 F2. Present with the remainder named."""
        case = staffing_case("g09-coverage", steps=(1, 2, 3, 4))
        case["files"]["steps/step-04-record.md"] = (
            "# Step 4 record\n\nRoster stands. No base stated for this step.\n")
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "E-1")
        assert_verdict(self, block, "present", "E-1")
        self.assertIn("Step 4", block)
        self.assertRegex(block, r"(of 4 steps\b|(?<!\d)4 steps\b)")

    def test_e1_partial_coverage_without_defined_form_is_not_present(self):
        """E-1 negative case. EC-28. Partial coverage in no defined form."""
        case = staffing_case("e1-negative", steps=(1, 2))
        case["files"]["steps/step-01-record.md"] = "# Step 1 record\n\nRoster fragment only.\n"
        case["files"]["steps/step-02-record.md"] = "# Step 2 record\n\nRoster fragment only.\n"
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "E-1")
        assert_verdict(self, block, "present but not derivable", "E-1")
        self.assertIn("missing-field", block)

    def test_wv4_disputed_count_header_and_denominators(self):
        """WV-4. EC-42. Disputed count: both counts stated, neither picked."""
        case = staffing_case("wv4-disputed")
        case["files"]["wiki/wiki/synthesis/build-metrics-record.md"] = (
            metrics_record(body="Metrics record states the step universe as 2 steps."))
        root = build_one(case)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        cov = coverage_statement(result.stdout)
        self.assertTrue(cov, "header coverage statement stands")
        self.assertIn("build-metrics-record.md", cov)
        self.assertRegex(cov, r"(?<!\d)2 steps\b")
        self.assertRegex(cov, r"(?<!\d)3 steps\b")
        self.assertIn("disagrees", cov.lower())
        block = row_block(result.stdout, "E-1")
        self.assertIn("record disagrees", statement_segment(block))
        self.assertIn("Step 3", block)

    def test_e1_row_cross_check_marking_in_statement_line(self):
        """Cross check marking. EC-43. Record disagrees in the statement line."""
        case = staffing_case("e1-cross-check", steps=(1,))
        case["files"]["steps/step-01-record.md"] = step_record(1, team=3)
        case["files"]["wiki/wiki/synthesis/build-metrics-record.md"] = (
            metrics_record(body="Metrics record states E-1 for Step 1 as 9 of 2."))
        root = build_one(case)
        result = run_tool(root)
        segment = statement_segment(row_block(result.stdout, "E-1"))
        self.assertIn("record disagrees", segment)
        self.assertIn("build-metrics-record.md", segment)
        self.assertIn("3 of 2", segment)
        self.assertIn("9 of 2", segment)

    def test_f18_unknown_version_slice3_rows(self):
        """F-18 variant. EC-03. WV-2 refusal for E-1, E-2 and F-2."""
        case = staffing_case("f18-slice3")
        for n in (1, 2, 3):
            del case["files"]["steps/step-%02d-gate-record.md" % n]
        case["files"]["wiki/wiki/synthesis/build-metrics-record.md"] = (
            metrics_record(body="Step table stands.",
                           header_version="unknown-version-999"))
        root = build_one(case)
        result = run_tool(root)
        for code in ("E-1", "E-2"):
            block = row_block(result.stdout, code)
            assert_verdict(self, block, "present but not derivable", code)
            self.assertIn("unknown-definitions-version", block, code)
            self.assertIn("unknown-version-999", block, code)
        assert_verdict(self, row_block(result.stdout, "F-2"), "missing", "F-2")

    def test_step_universe_reads_capture_only(self):
        """Named reread test for Slice 3, plan Section 5. EC-04."""
        root = build_one(staffing_case("reread-slice3"))
        assert_reads_capture_only(self, root)

    def test_instance_key_restart_suffix_is_separate_instance(self):
        """Spin 772 key, F-18. EC-10, EC-19. A restart suffix names a new key."""
        case = staffing_case("key-restart", steps=(2,))
        case["features"] = ("restart-instance",)
        case["files"]["steps/step-02-record.md"] = step_record(
            2, extra="Instance marker: restart suffix R stands on this record.")
        case["files"]["steps/step-02r-record.md"] = (
            "# Step 2 record, restart instance R\n\n"
            "Build: metrics fixture build.\nBase: 2. Team staffed: 3 agents. "
            "Total spins: 4.\nReplaces instance: Step 2 plain instance.\n")
        case["files"]["steps/step-02r-gate-record.md"] = gate_record(2, "CLOSED-PASS")
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "E-1")
        assert_verdict(self, block, "present", "E-1")
        self.assertRegex(block, r"(of 2 steps\b|(?<!\d)2 steps\b)")

    def test_instance_key_recycled_inside_one_record_one_key(self):
        """Spin 772 key. EC-19. One record, first ruling and recycle, one key."""
        case = staffing_case("key-recycled", steps=(2,))
        case["features"] = ("recycled-instance",)
        case["files"]["steps/step-02-record.md"] = step_record(
            2, extra="First ruling stands, then a recycle marker stands "
                     "inside this same record for this same instance.")
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "E-1")
        assert_verdict(self, block, "present", "E-1")
        self.assertRegex(block, r"(of 1 step\b|(?<!\d)1 step\b|denominator[^\d]*1(?!\d))")

    def test_instance_key_same_key_across_four_record_kinds(self):
        """Spin 772 key, if and only if rule. EC-10, EC-12, EC-13, EC-19.

        A step record, a gate file, the path ledger and the metrics
        record giving the same step number and the same instance
        marker, here no marker, name one and the same instance.
        """
        case = staffing_case("key-same-across-kinds", steps=(1,))
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "E-1")
        assert_verdict(self, block, "present", "E-1")
        self.assertRegex(block, r"(of 1 step\b|(?<!\d)1 step\b|denominator[^\d]*1(?!\d))")
        cov = coverage_statement(result.stdout)
        self.assertNotIn("disagrees", cov.lower())

    def test_instance_key_different_marker_never_merged(self):
        """Spin 772 key. EC-19, EC-32. Replaced figures stay under their own key."""
        case = staffing_case("key-not-merged", steps=(3,))
        case["features"] = ("restart-instance", "figure-credited-to-other-step")
        case["files"]["steps/step-03-record.md"] = step_record(
            3, extra="Replaced instance figures stand named as replaced "
                     "under the replaced instance key.")
        case["files"]["steps/step-03r-gate-record.md"] = gate_record(3, "CLOSED-PASS")
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")
        self.assertIn("replaced", block.lower())

    def test_gate_alias_regate_record_counts_as_gate_file(self):
        """Gate alias set, Margin M4 List 2. EC-09. The regate form stands in the set."""
        case = staffing_case("alias-regate", steps=(5,))
        del case["files"]["steps/step-05-gate-record.md"]
        case["files"]["steps/step-05-regate-record.md"] = gate_record(5, "CLOSED-PASS")
        root = build_one(case)
        result = run_tool(root)
        assert_verdict(self, row_block(result.stdout, "F-2"), "present", "F-2")

    def test_gate_alias_round_and_reaudit_variants_read(self):
        """Gate alias set, Margin M4 List 2. EC-09. Ruling variants stand in the set."""
        case = staffing_case("alias-variants", steps=(6,))
        del case["files"]["steps/step-06-gate-record.md"]
        case["files"]["steps/step-06-gate-ruling-round-2.md"] = gate_ruling(6)
        case["files"]["steps/step-06-gate-ruling-reaudit.md"] = gate_ruling(6)
        root = build_one(case)
        result = run_tool(root)
        assert_verdict(self, row_block(result.stdout, "F-2"), "present", "F-2")

    def test_gate_alias_near_match_name_not_read(self):
        """Gate alias set, Margin M4 List 2. EC-22. A near match name stands outside."""
        case = staffing_case("alias-near-match", steps=(7,))
        del case["files"]["steps/step-07-gate-record.md"]
        case["features"] = ("near-match-name",)
        case["files"]["steps/step-07-gate-notes.md"] = gate_record(7, "CLOSED-PASS")
        root = build_one(case)
        result = run_tool(root)
        assert_verdict(self, row_block(result.stdout, "F-2"),
                       "present but not derivable", "F-2")

    def test_gate_alias_both_names_disagreement_reported(self):
        """Gate alias set, Margin M4 List 2. EC-09. Both names read, disagreement shown."""
        case = staffing_case("alias-disagreement", steps=(1,))
        case["files"]["steps/step-01-gate-record.md"] = gate_record(1, "CLOSED-PASS")
        case["files"]["steps/step-01-gate-ruling.md"] = gate_ruling(1, "CLOSED-FAIL")
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "F-2")
        self.assertIn("disagree", block.lower())

    def test_f05_unmarked_signal_one(self):
        """F-05 unmarked, switch M-05, signal-one. EC-20. No correcting record."""
        root = build_one(unmarked_case("f05-m05-s1", "F-05", "signal-one", False))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("step-01-audit-paper.md", result.stdout)
        self.assertIn("signal-one", result.stdout)

    def test_f05_unmarked_signal_two(self):
        """F-05 unmarked, switch M-05, signal-two. EC-20. No correcting record."""
        root = build_one(unmarked_case("f05-m05-s2", "F-05", "signal-two", False))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("step-01-audit-paper.md", result.stdout)
        self.assertIn("signal-two", result.stdout)

    def test_f05_unmarked_signal_three(self):
        """F-05 unmarked, switch M-05, signal-three. EC-20. No correcting record."""
        root = build_one(unmarked_case("f05-m05-s3", "F-05", "signal-three", False))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("step-01-audit-paper.md", result.stdout)
        self.assertIn("signal-three", result.stdout)

    def test_f06_unmarked_signal_one(self):
        """F-06 unmarked, switch M-05, signal-one. EC-20. One correcting record stands."""
        root = build_one(unmarked_case("f06-m05-s1", "F-06", "signal-one", True))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("step-01-audit-paper.md", result.stdout)
        self.assertIn("signal-one", result.stdout)

    def test_f06_unmarked_signal_two(self):
        """F-06 unmarked, switch M-05, signal-two. EC-20. One correcting record stands."""
        root = build_one(unmarked_case("f06-m05-s2", "F-06", "signal-two", True))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("step-01-audit-paper.md", result.stdout)
        self.assertIn("signal-two", result.stdout)

    def test_f06_unmarked_signal_three(self):
        """F-06 unmarked, switch M-05, signal-three. EC-20. One correcting record stands."""
        root = build_one(unmarked_case("f06-m05-s3", "F-06", "signal-three", True))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("step-01-audit-paper.md", result.stdout)
        self.assertIn("signal-three", result.stdout)

    def test_f05_f06_pair_relation_in_prose_form(self):
        """F-05 and F-06 pair relation, plan Section 2A condition four.

        Pair case in prose form, outside the factory: the two trees
        stand built side by side through build_cases, one case table
        per tree. The trees agree in every piece except one position:
        the F-05 tree holds the unmarked audit paper under switch
        M-05 with no correcting record standing, and the F-06 tree
        holds the same paper under the same switch and the same
        failed signal, signal-one, with one correcting record
        standing. The relation asserted is that the pair differs in
        the correcting record position alone, so any report
        difference between the two runs stands charged to that
        position and to no other difference.
        """
        first = unmarked_case("pair-f05", "F-05", "signal-one", False)
        second = unmarked_case("pair-f06", "F-06", "signal-one", True)
        built = build_cases((first, second), tracked_tempdir("msc_pair_"))
        first_result = run_tool(built["pair-f05"])
        second_result = run_tool(built["pair-f06"])
        self.assertEqual(first_result.returncode, 0, first_result.stderr)
        self.assertEqual(second_result.returncode, 0, second_result.stderr)
        self.assertIn("step-01-audit-paper.md", first_result.stdout)
        self.assertIn("step-01-audit-paper.md", second_result.stdout)
        self.assertIn("signal-one", first_result.stdout)
        self.assertIn("signal-one", second_result.stdout)
        self.assertIn("correcting", second_result.stdout.lower())

    def test_wv21_gate_ruling_habit_same_f2_row(self):
        """WV2-21 habit four. EC-09, EC-04, EC-32.

        Two shapes on equivalent content: gate files under the record
        name in the first shape and under the ruling name throughout
        in the second. The F-2 row stands compared verdict, value and
        denominator under EC-04 and must not differ between shapes.
        """
        first = staffing_case("wv21-shape-first", features=("gate-record-name",))
        second = staffing_case("wv21-shape-second", features=("gate-ruling-name",))
        for n in (1, 2, 3):
            second["files"]["steps/step-%02d-gate-ruling.md" % n] = (
                second["files"].pop("steps/step-%02d-gate-record.md" % n))
        built = build_cases((first, second), tracked_tempdir("msc_wv21_"))
        first_block = row_block(run_tool(built["wv21-shape-first"]).stdout, "F-2")
        second_block = row_block(run_tool(built["wv21-shape-second"]).stdout, "F-2")
        assert_verdict(self, first_block, "present", "F-2")
        assert_verdict(self, second_block, "present", "F-2")
        self.assertEqual(
            _row_substance(first_block), _row_substance(second_block),
            "F-2 row parts differ between shapes under EC-04: first "
            "shape %r, second shape %r; shape difference: gate files "
            "under the ruling name throughout"
            % (_row_substance(first_block), _row_substance(second_block)))

    def test_wv21_second_shape_e1_e2_substance_same(self):
        """WV2-21 row points. EC-28, EC-29, EC-04. E-1 and E-2 on habit content."""
        first = staffing_case("wv21-rows-first", features=("gate-record-name",))
        second = staffing_case("wv21-rows-second", features=("gate-ruling-name",))
        for n in (1, 2, 3):
            second["files"]["steps/step-%02d-gate-ruling.md" % n] = (
                second["files"].pop("steps/step-%02d-gate-record.md" % n))
        built = build_cases((first, second), tracked_tempdir("msc_wv21r_"))
        first_out = run_tool(built["wv21-rows-first"]).stdout
        second_out = run_tool(built["wv21-rows-second"]).stdout
        for code in ("E-1", "E-2"):
            first_block = row_block(first_out, code)
            second_block = row_block(second_out, code)
            self.assertEqual(
                _row_substance(first_block), _row_substance(second_block),
                "row %s parts differ between shapes under EC-04: first "
                "shape %r, second shape %r; shape difference: gate "
                "files under the ruling name throughout"
                % (code, _row_substance(first_block),
                   _row_substance(second_block)))

    def test_wv22_e1_f1_staffed_list_in_named_feeder_only(self):
        """WV22 E-1 F1. EC-28. A list for another step counts for nothing."""
        case = staffing_case("wv22-e1-f1", steps=(1, 2))
        case["files"]["steps/step-02-record.md"] = (
            "# Step 2 record\n\nStaffed list standing here names Step 1 only.\n")
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "E-1")
        assert_verdict(self, block, "present", "E-1")
        self.assertIn("Step 2", block)
        coverage = _row_substance(block).get("Row coverage", "")
        self.assertRegex(
            coverage, r"covered step 1\s*;\s*remainder step 2\b",
            "E-1 Row coverage part does not stand in the remainder "
            "form, covered Step 1 with remainder Step 2 named: %r"
            % (coverage,))
        self.assertNotIn("Step 2 staffed", block)

    def test_wv22_e1_f2_base_count_same_step(self):
        """WV22 E-1 F2. EC-28. List and base count must stand for the same step."""
        case = staffing_case("wv22-e1-f2", steps=(1,))
        case["files"]["steps/step-01-record.md"] = (
            "# Step 1 record\n\nNamed agents: 3. Base count stands "
            "for Step 9 in this text and for no step in this tree.\n")
        root = build_one(case)
        result = run_tool(root)
        assert_verdict(self, row_block(result.stdout, "E-1"),
                       "present but not derivable", "E-1")

    def test_wv22_e2_f1_addition_entries_labelled(self):
        """WV22 E-2 F1. EC-29. Additions printed labelled, never unlabelled."""
        case = staffing_case("wv22-e2-f1", steps=(1,))
        case["files"]["steps/step-01-record.md"] = step_record(
            1, additions=1)
        case["features"] = ("additions-over-base-stated",)
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "E-2")
        assert_verdict(self, block, "present", "E-2")
        self.assertIn("additions over base", block.lower())

    def test_wv22_e2_f2_total_only_step_split_form(self):
        """WV22 E-2 F2. EC-29. A total only step: present for total, not for E-2."""
        case = staffing_case("wv22-e2-f2", steps=(1,))
        case["features"] = ("total-only-step",)
        case["files"]["steps/step-01-record.md"] = (
            "# Step 1 record\n\nTotal spins: 6. No addition entries stand.\n")
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "E-2")
        assert_verdict(self, block, "present but not derivable", "E-2")
        self.assertIn("total spins", block.lower())

    def test_wv22_e2_f3_total_alone_never_additions(self):
        """WV22 E-2 F3. EC-29. A total alone yields no additions figure.

        In the form its Slice 1 twin uses: the verdict form stands
        asserted, total spins stands in the block, not derivable
        stands in the block, and no figure stands in the additions
        position for the total alone step.
        """
        case = staffing_case("wv22-e2-f3", steps=(1,))
        case["files"]["steps/step-01-roster.md"] = (
            "# Step 1 roster\n\nNamed agents: 3. Base: 2.\n"
            "Total standing alone: 9. "
            "No addition entries in the roster form stand.\n")
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "E-2")
        self.assertIn("total spins", block.lower())
        self.assertIn("not derivable", block.lower())
        self.assertNotRegex(block.lower(),
                            r"additions over base[^|]*9(?!\d)")

    def test_e2_total_and_base_alone_no_additions_figure(self):
        """R15-02, correctness F1. D4R-16, DG-03 second case.

        Probe form of the correctness paper: three steps whose
        step records each state Base: 2, Team staffed: 3 agents,
        Total spins: 4, with no roster addition entries and no
        named agents anywhere. No additions figure may be formed
        as total minus base: the row stands present but not
        derivable for E-2 as defined, the total quantity stands,
        and each step stands named in the second case, with the
        absent countable input named as the missing item.
        """
        case = staffing_case("e2-total-base-alone", steps=(1, 2, 3))
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "E-2")
        assert_verdict(self, block, "present but not derivable", "E-2")
        for n in (1, 2, 3):
            self.assertNotRegex(block, r"Step %d: 2(?!\d)" % n)
            self.assertIn("Step %d stands in the second case" % n, block)
        self.assertIn("total spins", block.lower())
        self.assertRegex(block, r"total spins Step 1:\s*4(?!\d)")
        lowered = block.lower()
        self.assertIn("no roster addition entries", lowered)
        self.assertIn("no named agents", lowered)
        self.assertIn("countable form", lowered)

    def test_e2_roster_artifact_total_and_base_no_additions_figure(self):
        """R15-02, correctness F1, roster locus. D4R-16, DG-03.

        A roster artifact stands for the step, the step record
        states a total and a base, and no roster addition entries
        stand anywhere: the roster route forms no additions
        figure as total minus base either, and the row stands
        present but not derivable on the total alone.
        """
        case = staffing_case("e2-roster-artifact-alone", steps=(1,))
        case["files"]["steps/step-01-roster-artifact.md"] = (
            "# Step 1 roster artifact\n\nNamed agents: 3. Base: 2.\n")
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "E-2")
        assert_verdict(self, block, "present but not derivable", "E-2")
        self.assertNotRegex(block, r"Step 1: 2(?!\d)")
        self.assertIn("total spins", block.lower())

    def test_e2_additions_only_class_states_total_position_and_reconciliation(self):
        """R15-09, correctness F5. D4R-16 mirror class, WV2-13.

        Probe form of the correctness paper: three steps whose
        records each carry Roster additions over base: 1 and state
        no total spins figure in any record. The row reports both
        positions labelled, in the split form: the additions
        quantity stands on its roster addition entries, the total
        quantity is not derivable for each step because no total
        stands for it, each step stands stated as additions only,
        and the reconciliation clause states that the metric
        carries no total to reconcile against, instead of naming
        a per step total spins series that does not stand.
        """
        case = staffing_case("e2-additions-only", steps=(1, 2, 3))
        for n in (1, 2, 3):
            case["files"]["steps/step-%02d-record.md" % n] = (
                "# Step %d record\n\nBuild: metrics fixture build.\n"
                "Base: 2. Team staffed: 3 agents.\n"
                "Roster additions over base: 1.\n" % n)
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "E-2")
        assert_verdict(self, block, "present", "E-2")
        self.assertRegex(block, r"additions over base, Step 1: 1(?!\d)")
        lowered = block.lower()
        for n in (1, 2, 3):
            self.assertIn("step %d is additions only" % n, lowered)
            self.assertRegex(
                block, r"Step %d total spins: not derivable" % n)
        self.assertIn("no total stands for it", lowered)
        self.assertIn("the metric carries no total to reconcile "
                      "against", lowered)
        self.assertNotIn("per step series of total spins", lowered)

    def test_wv22_f2_f1_outcome_in_one_named_place(self):
        """WV22 F-2 F1. EC-32. Scattered outcomes count for nothing."""
        case = staffing_case("wv22-f2-f1", steps=(1,))
        del case["files"]["steps/step-01-gate-record.md"]
        case["files"]["steps/step-01-record.md"] = step_record(
            1, extra="An outcome word stands scattered in this record only.")
        root = build_one(case)
        result = run_tool(root)
        assert_verdict(self, row_block(result.stdout, "F-2"),
                       "present but not derivable", "F-2")

    def test_wv22_f2_f2_outcome_words(self):
        """WV22 F-2 F2. EC-32. Go, Hold, Recycle and Kill under the approval test."""
        case = staffing_case("wv22-f2-f2", steps=(1, 2, 3, 4))
        words = {1: "Go, closes the step, no send back before closure.",
                 2: "Hold, closes nothing, the step stands to be ruled again.",
                 3: "Recycle, the step stands sent back.",
                 4: "Kill, the step stands failed, nothing closed as approved."}
        for n, text in words.items():
            case["files"]["steps/step-%02d-gate-record.md" % n] = gate_record(
                n, "CLOSED-PASS", extra="First ruling outcome: " + text)
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")
        self.assertRegex(block, r"plain[^\d]*1(?!\d)(?!\.\d)")

    def test_wv22_f2_f3_f4_subcounts_travel_with_rate(self):
        """WV22 F-2 F3, WV22 F-2 F4. EC-32. Subcounts under one denominator."""
        case = staffing_case("wv22-f2-f34", steps=(1, 2))
        case["files"]["steps/step-01-gate-record.md"] = gate_record(1, "CLOSED-PASS")
        case["files"]["steps/step-02-gate-record.md"] = gate_record(2, "CLOSED-QUALIFIED")
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")
        self.assertRegex(block, r"plain[^\d]*1(?!\d)(?!\.\d)")
        self.assertRegex(block, r"qualified[^\d]*1(?!\d)(?!\.\d)")
        self.assertRegex(block, r"(denominator[^\d]*2(?!\d)(?!\.\d)|of 2(?!\d))")


    def test_f22_no_degraded_marking_on_f2_row(self):
        """F-22 degraded forms, Slice 3 negative limb. EC-32.

        No degraded marking stands on an F-2 row: the two degraded
        forms belong to T-4 and T-7 alone, and F-2 carries none.
        """
        case = staffing_case("f22-f2-negative")
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")
        self.assertNotIn("degraded", block.lower())
        self.assertNotIn("counted, not marked", block.lower())

    def test_f26_ca2_06_case_form_recorded_by_step_name(self):
        """F-26 CA2-06 case form. EC-29; DG-03; R12-08 deferral form.

        The case records, by step name, which CA2-06 case its built
        fixture tree builds, and asserts the E-2 row in that case
        form. Step 1 builds the second case: the stated total and
        the base position both stand, and no roster addition entries
        and no named agents stand for that step in a countable form.
        Step 2 builds the subtraction case: a specific arithmetic
        input, the base position, stands absent for that step. A
        tree whose built case cannot be recorded fails in this form.
        """
        case = staffing_case("f26-ca2-06", steps=(1, 2))
        case["files"]["steps/step-01-record.md"] = (
            "# Step 1 record\n\nBuild: metrics fixture build.\n"
            "Base: 2. Total spins: 6.\n")
        case["files"]["steps/step-02-record.md"] = (
            "# Step 2 record\n\nBuild: metrics fixture build.\n"
            "Total spins: 5. No base stated for this step.\n")
        recorded = {}
        for n in (1, 2):
            text = case["files"]["steps/step-%02d-record.md" % n]
            has_total = "Total spins:" in text
            has_base = "Base:" in text
            has_entries = "Roster additions" in text
            has_named = "Named agents:" in text
            if has_total and has_base and not has_entries and not has_named:
                recorded["Step %d" % n] = "second-case"
            elif has_total and not has_base:
                recorded["Step %d" % n] = "subtraction-case"
            else:
                self.fail("built CA2-06 case cannot be recorded by "
                          "step name for Step %d" % n)
        self.assertEqual(recorded.get("Step 1"), "second-case")
        self.assertEqual(recorded.get("Step 2"), "subtraction-case")
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "E-2")
        self.assertIn("Step 2", block)
        self.assertNotRegex(
            block.lower(), r"additions over base step 2:\s*\d")
        self.assertIn("Step 1", block)
        self.assertRegex(block, r"total spins Step 1:\s*6(?!\d)")
        self.assertRegex(block.lower(), r"base[^\d]*2(?!\d)")
        lowered = block.lower()
        self.assertIn("no roster addition entries", lowered)
        self.assertIn("no named agents", lowered)
        self.assertIn("countable form", lowered)

    def test_f27_figure_credited_to_described_step_pointer_names_source(self):
        """F-27 credited step, Slice 3 placement. EC-29.

        A figure stored on one step record describing another step
        stands credited to the described step, and the pointer on
        the row names where the figure was found: the record of the
        step that stores it.

        Corrected at Step 15 round 1, item R15-02: Step 2 now
        states a roster additions entry, so the present verdict
        rests on that entry and not on a total minus base
        derivation the brief forbids.
        """
        case = staffing_case("f27-credited", steps=(1, 2),
                             features=("figure-credited-to-other-step",))
        case["files"]["steps/step-01-record.md"] = step_record(
            1, extra="Total spins for Step 2: 7.")
        case["files"]["steps/step-02-record.md"] = step_record(
            2, additions=1)
        root = build_one(case)
        result = run_tool(root)
        block = row_block(result.stdout, "E-2")
        assert_verdict(self, block, "present", "E-2")
        self.assertRegex(block, r"Step 2:\s*7(?!\d)")
        self.assertNotRegex(block, r"Step 1:\s*7(?!\d)")
        self.assertIn("step-01-record.md", block)

    def test_f18_recycle_inside_one_record_f2_q4_visible(self):
        """Brief family F-18 recycle limb. EC-19, EC-32, EC-35.

        A recycle inside one record file counts as one instance,
        beside the standing E-1 assertion on the same tree, with
        the first ruling and the recycle both visible to the F-2
        and Q-4 derivations in their single counting forms.
        """
        case = staffing_case("f18-recycle-visibility", steps=(2,))
        case["features"] = ("recycled-instance",)
        case["files"]["steps/step-02-record.md"] = step_record(
            2, extra="First ruling stands, then a recycle marker stands "
                     "inside this same record for this same instance.")
        case["files"]["steps/step-02-gate-record.md"] = gate_record(
            2, "CLOSED-PASS",
            extra="First trace for step 2: 2 LANDED of 2 items "
                  "checked, 0 PARTIAL, 0 CONTRADICTED.")
        case["files"]["steps/step-02-trace-record.md"] = (
            "# Step 2 first trace record\n\nParts: 2 LANDED, "
            "1 PARTIAL, 0 CONTRADICTED. Stated total: 3 items "
            "checked.\n")
        root = build_one(case)
        result = run_tool(root)
        e1 = row_block(result.stdout, "E-1")
        assert_verdict(self, e1, "present", "E-1")
        self.assertRegex(
            e1, r"(of 1 step\b|(?<!\d)1 step\b|denominator[^\d]*1(?!\d))")
        f2 = row_block(result.stdout, "F-2")
        assert_verdict(self, f2, "present", "F-2")
        self.assertRegex(
            f2, r"(denominator[^\d]*1(?!\d)(?!\.\d)|of 1(?!\d))")
        q4 = row_block(result.stdout, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("Step 2", q4)


def row_block_verdict(block):
    from tests.fixture_builder import row_verdict
    return row_verdict(block)


def _row_substance(block):
    """Return the EC-04 compared parts of one row block, by label.

    The parts are taken by label from the first line of the
    block, in the parts_of form: verdict, then Value, Numerator,
    Denominator, Row coverage, Reason, and Pointer, each under
    its own label where the row carries it and absent where it
    does not, with gate name normalisation applied to every
    part, the four forms gate ruling, gate record, gate-ruling,
    and gate-record each replaced by the words gate file.
    """
    from tests.fixture_builder import row_verdict
    lines = [ln for ln in block.splitlines() if ln.strip()]
    first = lines[0] if lines else ""
    parts = {}
    for chunk in first.split(" | "):
        chunk = chunk.strip()
        if ": " in chunk:
            label, value = chunk.split(": ", 1)
            parts[label.strip()] = value.strip()
    substance = {"verdict": row_verdict(block)}
    for label in ("Value", "Numerator", "Denominator",
                  "Row coverage", "Reason", "Pointer"):
        if label in parts:
            value = parts[label].lower()
            for form in ("gate ruling", "gate record",
                         "gate-ruling", "gate-record"):
                value = value.replace(form, "gate file")
            substance[label] = re.sub(r"\s+", " ", value).strip()
    has_row_reason = "Reason" in substance
    for line in lines[1:]:
        lowered = line.lower()
        if not has_row_reason and lowered.startswith("reason:"):
            reason = lowered
            for form in ("gate ruling", "gate record",
                         "gate-ruling", "gate-record"):
                reason = reason.replace(form, "gate file")
            substance["Reason"] = re.sub(r"\s+", " ", reason).strip()
        if lowered.startswith("statement line:"):
            substance["Statement"] = re.sub(
                r"\s+", " ", lowered).strip()
    return substance


if __name__ == "__main__":
    unittest.main()
