from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parent
RUNS_DIR = ROOT / "runs"
SOLUTIONS_DIR = ROOT / "solutions"

MODES = ("direct_answer", "plain_guidance", "coe_guided")
MODE_ALIASES = {
    "direct": "direct_answer",
    "direct_answer": "direct_answer",
    "plain": "plain_guidance",
    "plain_guidance": "plain_guidance",
    "coe": "coe_guided",
    "coe_guided": "coe_guided",
}
TRACK_ALIASES = {
    "baseline": "baseline",
    "bug_repair": "bug-repair",
    "bug-repair": "bug-repair",
    "expanded_scope": "expanded-scope",
    "expanded-scope": "expanded-scope",
    "fresh_generation": "fresh-generation",
    "fresh-generation": "fresh-generation",
}


CATALOG = {
    "A1": {
        "title": "Seam Carving",
        "task_cards": [
            "task_cards/A1_seam_carving_taskcard_v1.md",
            "task_cards/A1_bug_repair_taskcard_v0.md",
        ],
        "tracks": {
            "baseline": {
                "label": "fixed-protocol baseline / replication",
                "prompt_templates": {
                    "direct_answer": "prompts/a1/baseline_direct_answer_v0.md",
                    "plain_guidance": "prompts/a1/baseline_plain_guidance_v0.md",
                    "coe_guided": "prompts/a1/coe_multi_role_v0.md",
                },
                "protocol_files": [
                    "report/a1_eval_protocol_v0.md",
                    "report/a1_replication_summary_v0.md",
                ],
                "run_ids": {
                    "direct_answer": [
                        "2026-03-26_run_006",
                        "2026-03-26_run_010",
                        "2026-03-26_run_011",
                        "2026-03-26_run_012",
                    ],
                    "plain_guidance": [
                        "2026-03-26_run_007",
                        "2026-03-26_run_013",
                        "2026-03-26_run_014",
                        "2026-03-26_run_015",
                    ],
                    "coe_guided": [
                        "2026-03-27_run_008",
                        "2026-03-26_run_016",
                        "2026-03-26_run_017",
                        "2026-03-26_run_018",
                    ],
                },
                "metrics": [
                    {
                        "path": "metrics/a1_guidance_eval_v0.csv",
                        "summary_kind": "guidance_eval",
                    },
                    {
                        "path": "metrics/a1_codegen_perf_v0.csv",
                        "summary_kind": "a1_codegen_perf",
                    },
                ],
                "notes": "This track summarizes the fixed-protocol A1 baseline and replications; it does not launch new reruns.",
            },
            "bug-repair": {
                "label": "failure-case bug-repair benchmark",
                "prompt_templates": {
                    "direct_answer": "prompts/a1/bug_repair_direct_answer_v0.md",
                    "plain_guidance": "prompts/a1/bug_repair_plain_guidance_v0.md",
                    "coe_guided": "prompts/a1/bug_repair_coe_v0.md",
                },
                "protocol_files": [
                    "report/a1_bug_repair_protocol_v0.md",
                    "report/a1_bug_repair_summary_v0.md",
                ],
                "run_ids": {
                    "direct_answer": [
                        "2026-04-12_run_020",
                        "2026-04-12_run_023",
                        "2026-04-12_run_026",
                    ],
                    "plain_guidance": [
                        "2026-04-12_run_021",
                        "2026-04-12_run_024",
                        "2026-04-12_run_027",
                    ],
                    "coe_guided": [
                        "2026-04-12_run_022",
                        "2026-04-12_run_025",
                        "2026-04-12_run_028",
                    ],
                },
                "metrics": [
                    {
                        "path": "metrics/a1_failure_repair_eval_v0.csv",
                        "summary_kind": "bug_repair_eval",
                    }
                ],
                "notes": "This track surfaces the curated A1 failure cases and their scored repair results.",
            },
        },
    },
    "A2": {
        "title": "chapter5 rslt_inpainting",
        "task_cards": [
            "task_cards/A2_rslt_inpainting_taskcard_v1.md",
            "task_cards/A2_bug_repair_taskcard_v0.md",
        ],
        "tracks": {
            "baseline": {
                "label": "fixed-protocol baseline / replication",
                "prompt_templates": {
                    "direct_answer": "prompts/a2/baseline_direct_answer_v0.md",
                    "plain_guidance": "prompts/a2/baseline_plain_guidance_v0.md",
                    "coe_guided": "prompts/a2/coe_multi_role_v0.md",
                },
                "protocol_files": [
                    "report/a2_eval_protocol_v0.md",
                    "report/a2_replication_summary_v0.md",
                ],
                "run_ids": {
                    "direct_answer": [
                        "2026-04-12_run_030",
                        "2026-04-12_run_033",
                        "2026-04-12_run_036",
                        "2026-04-12_run_039",
                    ],
                    "plain_guidance": [
                        "2026-04-12_run_031",
                        "2026-04-12_run_034",
                        "2026-04-12_run_037",
                        "2026-04-12_run_040",
                    ],
                    "coe_guided": [
                        "2026-04-12_run_032",
                        "2026-04-12_run_035",
                        "2026-04-12_run_038",
                        "2026-04-12_run_041",
                    ],
                },
                "metrics": [
                    {
                        "path": "metrics/a2_guidance_eval_v0.csv",
                        "summary_kind": "guidance_eval",
                    },
                    {
                        "path": "metrics/a2_recovery_perf_v0.csv",
                        "summary_kind": "a2_recovery_perf",
                    },
                ],
                "notes": "This track summarizes the A2 fixed protocol on lena / barbara with random_pixel@50% and text@50%.",
            },
            "bug-repair": {
                "label": "failure-case bug-repair benchmark",
                "prompt_templates": {
                    "direct_answer": "prompts/a2/bug_repair_direct_answer_v0.md",
                    "plain_guidance": "prompts/a2/bug_repair_plain_guidance_v0.md",
                    "coe_guided": "prompts/a2/bug_repair_coe_v0.md",
                },
                "protocol_files": [
                    "report/a2_bug_repair_protocol_v0.md",
                    "report/a2_failure_case_design_v0.md",
                    "report/a2_bug_repair_summary_v0.md",
                ],
                "run_ids": {
                    "direct_answer": [
                        "2026-04-12_run_043",
                        "2026-04-12_run_046",
                        "2026-04-12_run_049",
                    ],
                    "plain_guidance": [
                        "2026-04-12_run_044",
                        "2026-04-12_run_047",
                        "2026-04-12_run_050",
                    ],
                    "coe_guided": [
                        "2026-04-12_run_045",
                        "2026-04-12_run_048",
                        "2026-04-12_run_051",
                    ],
                },
                "metrics": [
                    {
                        "path": "metrics/a2_failure_repair_eval_v0.csv",
                        "summary_kind": "bug_repair_eval",
                    }
                ],
                "notes": "This track surfaces the A2 curated bugs; it is a scored repair benchmark, not a new generation track.",
            },
            "expanded-scope": {
                "label": "expanded-scope validation",
                "prompt_templates": {
                    "direct_answer": "prompts/a2/baseline_direct_answer_v0.md",
                    "plain_guidance": "prompts/a2/baseline_plain_guidance_v0.md",
                    "coe_guided": "prompts/a2/coe_multi_role_v0.md",
                },
                "protocol_files": [
                    "report/a2_expanded_scope_protocol_v0.md",
                    "report/a2_expanded_scope_summary_v0.md",
                ],
                "run_ids": {
                    "direct_answer": ["2026-04-12_run_052"],
                    "plain_guidance": ["2026-04-12_run_053"],
                    "coe_guided": ["2026-04-12_run_054"],
                },
                "source_artifact_run_ids": {
                    "direct_answer": "2026-04-12_run_030",
                    "plain_guidance": "2026-04-12_run_031",
                    "coe_guided": "2026-04-12_run_032",
                },
                "metrics": [
                    {
                        "path": "metrics/a2_expanded_scope_eval_v0.csv",
                        "summary_kind": "expanded_scope_eval",
                    },
                    {
                        "path": "metrics/a2_expanded_scope_perf_v0.csv",
                        "summary_kind": "expanded_scope_perf",
                    },
                ],
                "notes": "Expanded-scope reuses the baseline-generated artifact and widens only the evaluation set.",
            },
            "fresh-generation": {
                "label": "fresh-generation replication",
                "prompt_templates": {
                    "direct_answer": "prompts/a2/baseline_direct_answer_v0.md",
                    "plain_guidance": "prompts/a2/baseline_plain_guidance_v0.md",
                    "coe_guided": "prompts/a2/coe_multi_role_v0.md",
                },
                "protocol_files": [
                    "report/a2_eval_protocol_v0.md",
                    "report/phase2_progress_report_2026-04-12.md",
                ],
                "run_ids": {
                    "direct_answer": ["2026-04-12_run_055"],
                    "plain_guidance": ["2026-04-12_run_056"],
                    "coe_guided": ["2026-04-12_run_057"],
                },
                "metrics": [
                    {
                        "path": "metrics/a2_guidance_eval_v0.csv",
                        "summary_kind": "guidance_eval",
                    },
                    {
                        "path": "metrics/a2_recovery_perf_v0.csv",
                        "summary_kind": "a2_recovery_perf",
                    },
                ],
                "notes": "Fresh-generation uses the same fixed protocol as baseline, but with newly materialized local artifacts.",
            },
        },
    },
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def normalize_case(value: str | None) -> str | None:
    if value is None:
        return None
    upper = value.strip().upper()
    if upper not in CATALOG:
        raise ValueError(f"Unsupported case: {value}")
    return upper


def normalize_mode(value: str | None) -> str | None:
    if value is None:
        return None
    key = value.strip().lower()
    if key not in MODE_ALIASES:
        raise ValueError(f"Unsupported mode: {value}")
    return MODE_ALIASES[key]


def normalize_track(value: str | None) -> str | None:
    if value is None:
        return None
    key = value.strip().lower()
    if key not in TRACK_ALIASES:
        raise ValueError(f"Unsupported track: {value}")
    return TRACK_ALIASES[key]


def prompt_choice(label: str, options: list[str]) -> str:
    print(f"Select {label}:")
    for index, option in enumerate(options, start=1):
        print(f"  {index}. {option}")
    while True:
        raw = input(f"{label}> ").strip()
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return options[idx]
        if raw in options:
            return raw
        print("Invalid choice, try again.")


def find_run_doc(run_id: str) -> str | None:
    matches = sorted(RUNS_DIR.glob(f"{run_id}_*.md"))
    return rel(matches[0]) if matches else None


def find_prompt_used(run_id: str) -> str | None:
    run_num = run_id.split("_")[-1]
    matches = sorted(SOLUTIONS_DIR.glob(f"**/generated/run_{run_num}_*/prompt_used.md"))
    return rel(matches[0]) if matches else None


def read_csv_rows(relative_path: str) -> list[dict[str, str]]:
    path = ROOT / relative_path
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def rows_by_run_id(rows: list[dict[str, str]], run_ids: list[str]) -> list[dict[str, str]]:
    run_id_set = set(run_ids)
    return [row for row in rows if row.get("run_id") in run_id_set]


def as_float(row: dict[str, str], key: str) -> float:
    return float(row[key])


def as_int(row: dict[str, str], key: str) -> int:
    return int(float(row[key]))


def safe_mean(values: list[float]) -> float | None:
    return mean(values) if values else None


def format_float(value: float | None, digits: int = 2) -> str:
    if value is None:
        return "n/a"
    return f"{value:.{digits}f}"


def summarize_guidance_eval(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return ["No guidance-eval rows matched this selection."]
    correct_ok = sum(1 for row in rows if row.get("correct") == "2")
    self_check_ok = sum(1 for row in rows if row.get("self_check") == "2")
    runnable_ok = sum(as_int(row, "runnable") for row in rows)
    artifact_complete = sum(1 for row in rows if row.get("artifact_complete") == "2")
    avg_time = safe_mean([as_float(row, "time_to_first_working_min") for row in rows])
    task_card_versions = sorted({row.get("task_card_version", "") for row in rows if row.get("task_card_version")})
    return [
        f"rows={len(rows)}",
        f"artifact_complete=2 -> {artifact_complete}/{len(rows)}",
        f"runnable=1 -> {runnable_ok}/{len(rows)}",
        f"correct=2 -> {correct_ok}/{len(rows)}",
        f"self_check=2 -> {self_check_ok}/{len(rows)}",
        f"avg_time_to_first_working_min={format_float(avg_time, 2)}",
        f"task_card_versions={', '.join(task_card_versions) if task_card_versions else 'none'}",
    ]


def summarize_a1_codegen_perf(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return ["No A1 performance rows matched this selection."]
    output_ok = sum(as_int(row, "output_ok") for row in rows)
    avg_total = safe_mean([as_float(row, "total_runtime_s") for row in rows])
    avg_width = safe_mean([as_float(row, "width_runtime_s") for row in rows])
    avg_height = safe_mean([as_float(row, "height_runtime_s") for row in rows])
    images = sorted({row.get("image_name", "") for row in rows})
    run_count = len({row.get("run_id") for row in rows})
    return [
        f"runs={run_count}",
        f"perf_rows={len(rows)}",
        f"output_ok=1 -> {output_ok}/{len(rows)}",
        f"avg_total_runtime_s={format_float(avg_total, 4)}",
        f"avg_width_runtime_s={format_float(avg_width, 4)}",
        f"avg_height_runtime_s={format_float(avg_height, 4)}",
        f"images={', '.join(images)}",
    ]


def summarize_bug_repair_eval(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return ["No bug-repair rows matched this selection."]
    diagnosis_ok = sum(as_int(row, "diagnosis_correct") for row in rows)
    patch_ok = sum(as_int(row, "patch_runnable") for row in rows)
    regression_ok = sum(as_int(row, "regression_pass") for row in rows)
    avg_fix_time = safe_mean([as_float(row, "time_to_fix_min") for row in rows])
    bug_ids = sorted({row.get("bug_id", "") for row in rows})
    return [
        f"rows={len(rows)}",
        f"bugs={', '.join(bug_ids)}",
        f"diagnosis_correct=1 -> {diagnosis_ok}/{len(rows)}",
        f"patch_runnable=1 -> {patch_ok}/{len(rows)}",
        f"regression_pass=1 -> {regression_ok}/{len(rows)}",
        f"avg_time_to_fix_min={format_float(avg_fix_time, 2)}",
    ]


def summarize_a2_recovery_perf(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return ["No A2 recovery-performance rows matched this selection."]
    output_ok = sum(as_int(row, "output_ok") for row in rows)
    avg_runtime = safe_mean([as_float(row, "runtime_s") for row in rows])
    avg_psnr = safe_mean([as_float(row, "psnr") for row in rows])
    avg_ssim = safe_mean([as_float(row, "ssim") for row in rows])
    avg_rse = safe_mean([as_float(row, "rse") for row in rows])
    images = sorted({row.get("image_name", "") for row in rows})
    corruptions = sorted({f"{row.get('corruption_mode')}@{row.get('corruption_ratio')}" for row in rows})
    run_count = len({row.get("run_id") for row in rows})
    return [
        f"runs={run_count}",
        f"perf_rows={len(rows)}",
        f"output_ok=1 -> {output_ok}/{len(rows)}",
        f"avg_runtime_s={format_float(avg_runtime, 4)}",
        f"avg_psnr={format_float(avg_psnr, 4)}",
        f"avg_ssim={format_float(avg_ssim, 4)}",
        f"avg_rse={format_float(avg_rse, 4)}",
        f"images={', '.join(images)}",
        f"corruptions={', '.join(corruptions)}",
    ]


def summarize_expanded_scope_eval(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return ["No expanded-scope eval rows matched this selection."]
    runnable_ok = sum(as_int(row, "runnable") for row in rows)
    output_ok = sum(as_int(row, "output_ok_count") for row in rows)
    case_count = sum(as_int(row, "case_count") for row in rows)
    image_counts = sorted({row.get("image_count", "") for row in rows})
    source_runs = sorted({row.get("source_artifact_run_id", "") for row in rows})
    return [
        f"rows={len(rows)}",
        f"runnable=1 -> {runnable_ok}/{len(rows)}",
        f"output_ok_count={output_ok}/{case_count}",
        f"image_count={', '.join(image_counts)}",
        f"source_artifact_run_ids={', '.join(source_runs)}",
    ]


def summarize_expanded_scope_perf(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return ["No expanded-scope perf rows matched this selection."]
    output_ok = sum(as_int(row, "output_ok") for row in rows)
    avg_runtime = safe_mean([as_float(row, "runtime_s") for row in rows])
    avg_psnr = safe_mean([as_float(row, "psnr") for row in rows])
    avg_ssim = safe_mean([as_float(row, "ssim") for row in rows])
    avg_rse = safe_mean([as_float(row, "rse") for row in rows])
    images = sorted({row.get("image_name", "") for row in rows})
    corruptions = sorted({f"{row.get('corruption_mode')}@{row.get('corruption_ratio')}" for row in rows})
    return [
        f"perf_rows={len(rows)}",
        f"output_ok=1 -> {output_ok}/{len(rows)}",
        f"avg_runtime_s={format_float(avg_runtime, 4)}",
        f"avg_psnr={format_float(avg_psnr, 4)}",
        f"avg_ssim={format_float(avg_ssim, 4)}",
        f"avg_rse={format_float(avg_rse, 4)}",
        f"images={', '.join(images)}",
        f"corruptions={', '.join(corruptions)}",
    ]


SUMMARY_HANDLERS = {
    "guidance_eval": summarize_guidance_eval,
    "a1_codegen_perf": summarize_a1_codegen_perf,
    "bug_repair_eval": summarize_bug_repair_eval,
    "a2_recovery_perf": summarize_a2_recovery_perf,
    "expanded_scope_eval": summarize_expanded_scope_eval,
    "expanded_scope_perf": summarize_expanded_scope_perf,
}


def build_selection(case_id: str, mode: str, track: str) -> dict:
    case_cfg = CATALOG[case_id]
    if track not in case_cfg["tracks"]:
        supported = ", ".join(case_cfg["tracks"].keys())
        raise ValueError(f"{case_id} does not support track '{track}'. Supported tracks: {supported}")
    track_cfg = case_cfg["tracks"][track]
    run_ids = track_cfg["run_ids"][mode]
    representative_run_id = run_ids[0]
    run_docs = [doc for doc in (find_run_doc(run_id) for run_id in run_ids) if doc]
    prompt_used = find_prompt_used(representative_run_id)

    materials = {
        "task_cards": case_cfg["task_cards"],
        "prompt_template": track_cfg["prompt_templates"][mode],
        "prompt_used": prompt_used,
        "protocol_files": track_cfg["protocol_files"],
        "representative_run_doc": find_run_doc(representative_run_id),
        "all_run_docs": run_docs,
    }

    if "source_artifact_run_ids" in track_cfg:
        source_run_id = track_cfg["source_artifact_run_ids"][mode]
        materials["source_artifact_run_id"] = source_run_id
        materials["source_prompt_used"] = find_prompt_used(source_run_id)
        materials["source_run_doc"] = find_run_doc(source_run_id)

    metric_blocks = []
    for metric_cfg in track_cfg["metrics"]:
        rows = rows_by_run_id(read_csv_rows(metric_cfg["path"]), run_ids)
        summary_lines = SUMMARY_HANDLERS[metric_cfg["summary_kind"]](rows)
        metric_blocks.append(
            {
                "path": metric_cfg["path"],
                "summary_kind": metric_cfg["summary_kind"],
                "summary_lines": summary_lines,
            }
        )

    return {
        "selection": {
            "case_id": case_id,
            "case_title": case_cfg["title"],
            "mode": mode,
            "track": track,
            "track_label": track_cfg["label"],
        },
        "notes": track_cfg["notes"],
        "materials": materials,
        "metrics": metric_blocks,
    }


def render_text(result: dict) -> str:
    selection = result["selection"]
    materials = result["materials"]
    prompt_used_display = materials.get("prompt_used")
    if not prompt_used_display and materials.get("source_prompt_used"):
        prompt_used_display = f"reused source artifact -> {materials['source_prompt_used']}"
    if not prompt_used_display:
        prompt_used_display = "not found"

    lines = [
        "Research Case CLI v0",
        "",
        "Selection",
        f"- case: {selection['case_id']} ({selection['case_title']})",
        f"- mode: {selection['mode']}",
        f"- track: {selection['track']} ({selection['track_label']})",
        "",
        "Prototype Scope",
        "- This CLI selects and summarizes existing research assets.",
        "- It does not rerun direct/plain/CoE experiments.",
        f"- note: {result['notes']}",
        "",
        "Materials",
        "- task_cards:",
    ]

    for path in materials["task_cards"]:
        lines.append(f"  - {path}")
    lines.extend(
        [
            f"- prompt_template: {materials['prompt_template']}",
            f"- prompt_used: {prompt_used_display}",
            "- protocol_files:",
        ]
    )
    for path in materials["protocol_files"]:
        lines.append(f"  - {path}")
    lines.extend(
        [
            f"- representative_run_doc: {materials.get('representative_run_doc') or 'not found'}",
            "- all_run_docs:",
        ]
    )
    for path in materials["all_run_docs"]:
        lines.append(f"  - {path}")

    if "source_artifact_run_id" in materials:
        lines.extend(
            [
                f"- source_artifact_run_id: {materials['source_artifact_run_id']}",
                f"- source_run_doc: {materials.get('source_run_doc') or 'not found'}",
                f"- source_prompt_used: {materials.get('source_prompt_used') or 'not found'}",
            ]
        )

    lines.append("")
    lines.append("Metrics Summary")
    for block in result["metrics"]:
        lines.append(f"- {block['path']} ({block['summary_kind']}):")
        for summary_line in block["summary_lines"]:
            lines.append(f"  - {summary_line}")
    return "\n".join(lines)


def render_json(result: dict) -> str:
    return json.dumps(result, ensure_ascii=False, indent=2)


def print_combinations() -> None:
    print("Supported combinations")
    for case_id, case_cfg in CATALOG.items():
        print(f"- {case_id}:")
        for track, track_cfg in case_cfg["tracks"].items():
            modes = ", ".join(track_cfg["run_ids"].keys())
            print(f"  - {track}: {modes}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Minimal CLI prototype for selecting existing A1/A2 research assets.")
    parser.add_argument("--case", dest="case_id", help="A1 or A2")
    parser.add_argument("--mode", help="direct_answer, plain_guidance, or coe_guided")
    parser.add_argument("--track", help="baseline, bug-repair, expanded-scope, or fresh-generation")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--list", action="store_true", help="Show supported case/mode/track combinations and exit.")
    return parser.parse_args()


def main() -> None:
    try:
        args = parse_args()
        if args.list:
            print_combinations()
            return

        case_id = normalize_case(args.case_id) if args.case_id else None
        if case_id is None:
            case_id = prompt_choice("case", sorted(CATALOG.keys()))

        case_tracks = sorted(CATALOG[case_id]["tracks"].keys())
        mode = normalize_mode(args.mode) if args.mode else None
        if mode is None:
            mode = prompt_choice("mode", list(MODES))

        track = normalize_track(args.track) if args.track else None
        if track is None:
            track = prompt_choice("track", case_tracks)

        result = build_selection(case_id, mode, track)
        if args.format == "json":
            print(render_json(result))
        else:
            print(render_text(result))
    except ValueError as exc:
        raise SystemExit(str(exc))


if __name__ == "__main__":
    main()
