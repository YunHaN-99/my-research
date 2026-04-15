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
MODE_DISPLAY_NAMES = {
    "direct_answer": "direct_answer",
    "plain_guidance": "plain_guidance",
    "coe_guided": "coe_guided",
}
STAGE_JUDGMENT = "A1 / A2 首轮主案例闭环已完成；当前中期重点是收束模板库、检查清单、错误分类、题库页和原型入口。"
FROZEN_CONCLUSIONS = [
    "`plain_guidance` / `coe_guided` 的核心优势，是提升自检覆盖、根因说明和回归说明的可复查性。",
    "在 A2 这类冻结协议任务上，结构化 guidance 未必显著改变最终恢复指标，但确实改善了过程质量与可解释性。",
]


CATALOG = {
    "A1": {
        "title": "Seam Carving",
        "problem_file": None,
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
        "title": "hw2-op2/src/chapter5_rslt.py::rslt_inpainting(...)",
        "problem_file": "problems/a2_requirement.md",
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

DEMO_SCENARIOS = {
    "advisor": {
        "title": "导师演示模式",
        "summary": "用单条命令串起“输入题目 -> 结构化表示 -> prompt 选择 -> run 结果 -> metrics 摘要”的研究链条。",
        "main_selection": {
            "case_id": "A2",
            "mode": "plain_guidance",
            "track": "baseline",
        },
        "input_preface": [
            ("problems/a2_requirement.md", ("目标：",), 1),
        ],
        "input_problem_sections": [
            ("problems/a2_requirement.md", "任务定义", 2),
            ("problems/a2_requirement.md", "输入", 2),
            ("problems/a2_requirement.md", "输出", 2),
        ],
        "structured_sections": [
            ("task_cards/A2_rslt_inpainting_taskcard_v1.md", "1. 题目一句话目标", 1),
            ("task_cards/A2_rslt_inpainting_taskcard_v1.md", "3. 核心模型", 3),
            ("task_cards/A2_rslt_inpainting_taskcard_v1.md", "5. 代码接口", 2),
            ("task_cards/A2_rslt_inpainting_taskcard_v1.md", "7. 评估指标与实验设计", 4),
        ],
        "mode_compare": {
            "case_id": "A2",
            "track": "baseline",
            "modes": list(MODES),
        },
        "extra_views": [
            {
                "label": "A2 bug-repair 证据",
                "case_id": "A2",
                "mode": "plain_guidance",
                "track": "bug-repair",
            },
            {
                "label": "A2 expanded-scope 证据",
                "case_id": "A2",
                "mode": "plain_guidance",
                "track": "expanded-scope",
            },
            {
                "label": "A2 fresh-generation 证据",
                "case_id": "A2",
                "mode": "plain_guidance",
                "track": "fresh-generation",
            },
            {
                "label": "A1 对照主案例",
                "case_id": "A1",
                "mode": "plain_guidance",
                "track": "baseline",
            },
        ],
        "task_bank_files": [
            "report/task_bank_index_v1.md",
            "report/task_bank_status_v1.md",
            "report/a2_expanded_scope_selected_entries_v1.md",
        ],
        "recommended_commands": [
            "python run_research_case.py --demo advisor",
            "python run_research_case.py --case A2 --mode plain_guidance --track bug-repair",
            "python run_research_case.py --case A2 --mode plain_guidance --track expanded-scope",
            "python run_research_case.py --case A1 --mode plain_guidance --track baseline",
        ],
        "demo_notes": [
            "主展示案例固定为 A2 baseline + plain_guidance，因为这条链路最适合展示结构化 guidance 如何进入固定协议评测。",
            "若导师继续追问“过程质量和最终指标的关系”，优先切到 A2 bug-repair 和 expanded-scope，而不是继续强调更多 rerun。",
            "若导师更关心题库结构，可顺手打开 task-bank 页面，说明当前正式条目已经整理到 16 个。",
        ],
    }
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def read_markdown_sections(relative_path: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current_heading: str | None = None
    buffer: list[str] = []
    for raw_line in read_text(relative_path).splitlines():
        if raw_line.startswith("## "):
            if current_heading is not None:
                sections[current_heading] = buffer
            current_heading = raw_line[3:].strip()
            buffer = []
            continue
        if current_heading is not None:
            buffer.append(raw_line.rstrip())
    if current_heading is not None:
        sections[current_heading] = buffer
    return sections


def strip_marker(line: str) -> str:
    stripped = line.strip()
    if not stripped:
        return stripped
    if stripped.startswith("- "):
        return stripped[2:].strip()
    if stripped[0].isdigit() and ". " in stripped:
        return stripped.split(". ", 1)[1].strip()
    return stripped


def extract_section_points(relative_path: str, heading: str, max_items: int) -> list[str]:
    sections = read_markdown_sections(relative_path)
    lines = sections.get(heading, [])
    points: list[str] = []
    for line in lines:
        stripped = strip_marker(line)
        if stripped.endswith(("：", ":")):
            continue
        if stripped:
            points.append(stripped)
        if len(points) >= max_items:
            break
    return points


def extract_prefixed_points(relative_path: str, prefixes: tuple[str, ...], max_items: int) -> list[str]:
    points: list[str] = []
    for line in read_text(relative_path).splitlines():
        stripped = line.strip()
        if any(stripped.startswith(prefix) for prefix in prefixes):
            points.append(stripped)
        if len(points) >= max_items:
            break
    return points


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


def collect_guidance_eval_stats(rows: list[dict[str, str]]) -> dict[str, object]:
    if not rows:
        return {}
    return {
        "rows": len(rows),
        "artifact_complete_ok": sum(1 for row in rows if row.get("artifact_complete") == "2"),
        "runnable_ok": sum(as_int(row, "runnable") for row in rows),
        "correct_ok": sum(1 for row in rows if row.get("correct") == "2"),
        "self_check_ok": sum(1 for row in rows if row.get("self_check") == "2"),
        "avg_time_to_first_working_min": safe_mean([as_float(row, "time_to_first_working_min") for row in rows]),
        "task_card_versions": sorted({row.get("task_card_version", "") for row in rows if row.get("task_card_version")}),
    }


def summarize_guidance_eval(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return ["No guidance-eval rows matched this selection."]
    stats = collect_guidance_eval_stats(rows)
    return [
        f"rows={stats['rows']}",
        f"artifact_complete=2 -> {stats['artifact_complete_ok']}/{stats['rows']}",
        f"runnable=1 -> {stats['runnable_ok']}/{stats['rows']}",
        f"correct=2 -> {stats['correct_ok']}/{stats['rows']}",
        f"self_check=2 -> {stats['self_check_ok']}/{stats['rows']}",
        f"avg_time_to_first_working_min={format_float(stats['avg_time_to_first_working_min'], 2)}",
        f"task_card_versions={', '.join(stats['task_card_versions']) if stats['task_card_versions'] else 'none'}",
    ]


def collect_a1_codegen_perf_stats(rows: list[dict[str, str]]) -> dict[str, object]:
    if not rows:
        return {}
    return {
        "run_count": len({row.get("run_id") for row in rows}),
        "perf_rows": len(rows),
        "output_ok": sum(as_int(row, "output_ok") for row in rows),
        "avg_total_runtime_s": safe_mean([as_float(row, "total_runtime_s") for row in rows]),
        "avg_width_runtime_s": safe_mean([as_float(row, "width_runtime_s") for row in rows]),
        "avg_height_runtime_s": safe_mean([as_float(row, "height_runtime_s") for row in rows]),
        "images": sorted({row.get("image_name", "") for row in rows}),
    }


def summarize_a1_codegen_perf(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return ["No A1 performance rows matched this selection."]
    stats = collect_a1_codegen_perf_stats(rows)
    return [
        f"runs={stats['run_count']}",
        f"perf_rows={stats['perf_rows']}",
        f"output_ok=1 -> {stats['output_ok']}/{stats['perf_rows']}",
        f"avg_total_runtime_s={format_float(stats['avg_total_runtime_s'], 4)}",
        f"avg_width_runtime_s={format_float(stats['avg_width_runtime_s'], 4)}",
        f"avg_height_runtime_s={format_float(stats['avg_height_runtime_s'], 4)}",
        f"images={', '.join(stats['images'])}",
    ]


def collect_bug_repair_eval_stats(rows: list[dict[str, str]]) -> dict[str, object]:
    if not rows:
        return {}
    return {
        "rows": len(rows),
        "bugs": sorted({row.get("bug_id", "") for row in rows}),
        "diagnosis_ok": sum(as_int(row, "diagnosis_correct") for row in rows),
        "patch_ok": sum(as_int(row, "patch_runnable") for row in rows),
        "regression_ok": sum(as_int(row, "regression_pass") for row in rows),
        "avg_time_to_fix_min": safe_mean([as_float(row, "time_to_fix_min") for row in rows]),
    }


def summarize_bug_repair_eval(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return ["No bug-repair rows matched this selection."]
    stats = collect_bug_repair_eval_stats(rows)
    return [
        f"rows={stats['rows']}",
        f"bugs={', '.join(stats['bugs'])}",
        f"diagnosis_correct=1 -> {stats['diagnosis_ok']}/{stats['rows']}",
        f"patch_runnable=1 -> {stats['patch_ok']}/{stats['rows']}",
        f"regression_pass=1 -> {stats['regression_ok']}/{stats['rows']}",
        f"avg_time_to_fix_min={format_float(stats['avg_time_to_fix_min'], 2)}",
    ]


def collect_a2_recovery_perf_stats(rows: list[dict[str, str]]) -> dict[str, object]:
    if not rows:
        return {}
    return {
        "run_count": len({row.get("run_id") for row in rows}),
        "perf_rows": len(rows),
        "output_ok": sum(as_int(row, "output_ok") for row in rows),
        "avg_runtime_s": safe_mean([as_float(row, "runtime_s") for row in rows]),
        "avg_psnr": safe_mean([as_float(row, "psnr") for row in rows]),
        "avg_ssim": safe_mean([as_float(row, "ssim") for row in rows]),
        "avg_rse": safe_mean([as_float(row, "rse") for row in rows]),
        "images": sorted({row.get("image_name", "") for row in rows}),
        "corruptions": sorted({f"{row.get('corruption_mode')}@{row.get('corruption_ratio')}" for row in rows}),
    }


def summarize_a2_recovery_perf(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return ["No A2 recovery-performance rows matched this selection."]
    stats = collect_a2_recovery_perf_stats(rows)
    return [
        f"runs={stats['run_count']}",
        f"perf_rows={stats['perf_rows']}",
        f"output_ok=1 -> {stats['output_ok']}/{stats['perf_rows']}",
        f"avg_runtime_s={format_float(stats['avg_runtime_s'], 4)}",
        f"avg_psnr={format_float(stats['avg_psnr'], 4)}",
        f"avg_ssim={format_float(stats['avg_ssim'], 4)}",
        f"avg_rse={format_float(stats['avg_rse'], 4)}",
        f"images={', '.join(stats['images'])}",
        f"corruptions={', '.join(stats['corruptions'])}",
    ]


def collect_expanded_scope_eval_stats(rows: list[dict[str, str]]) -> dict[str, object]:
    if not rows:
        return {}
    return {
        "rows": len(rows),
        "runnable_ok": sum(as_int(row, "runnable") for row in rows),
        "output_ok_count": sum(as_int(row, "output_ok_count") for row in rows),
        "case_count": sum(as_int(row, "case_count") for row in rows),
        "image_counts": sorted({row.get("image_count", "") for row in rows}),
        "source_runs": sorted({row.get("source_artifact_run_id", "") for row in rows}),
    }


def summarize_expanded_scope_eval(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return ["No expanded-scope eval rows matched this selection."]
    stats = collect_expanded_scope_eval_stats(rows)
    return [
        f"rows={stats['rows']}",
        f"runnable=1 -> {stats['runnable_ok']}/{stats['rows']}",
        f"output_ok_count={stats['output_ok_count']}/{stats['case_count']}",
        f"image_count={', '.join(stats['image_counts'])}",
        f"source_artifact_run_ids={', '.join(stats['source_runs'])}",
    ]


def collect_expanded_scope_perf_stats(rows: list[dict[str, str]]) -> dict[str, object]:
    if not rows:
        return {}
    return {
        "perf_rows": len(rows),
        "output_ok": sum(as_int(row, "output_ok") for row in rows),
        "avg_runtime_s": safe_mean([as_float(row, "runtime_s") for row in rows]),
        "avg_psnr": safe_mean([as_float(row, "psnr") for row in rows]),
        "avg_ssim": safe_mean([as_float(row, "ssim") for row in rows]),
        "avg_rse": safe_mean([as_float(row, "rse") for row in rows]),
        "images": sorted({row.get("image_name", "") for row in rows}),
        "corruptions": sorted({f"{row.get('corruption_mode')}@{row.get('corruption_ratio')}" for row in rows}),
    }


def summarize_expanded_scope_perf(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return ["No expanded-scope perf rows matched this selection."]
    stats = collect_expanded_scope_perf_stats(rows)
    return [
        f"perf_rows={stats['perf_rows']}",
        f"output_ok=1 -> {stats['output_ok']}/{stats['perf_rows']}",
        f"avg_runtime_s={format_float(stats['avg_runtime_s'], 4)}",
        f"avg_psnr={format_float(stats['avg_psnr'], 4)}",
        f"avg_ssim={format_float(stats['avg_ssim'], 4)}",
        f"avg_rse={format_float(stats['avg_rse'], 4)}",
        f"images={', '.join(stats['images'])}",
        f"corruptions={', '.join(stats['corruptions'])}",
    ]


SUMMARY_HANDLERS = {
    "guidance_eval": summarize_guidance_eval,
    "a1_codegen_perf": summarize_a1_codegen_perf,
    "bug_repair_eval": summarize_bug_repair_eval,
    "a2_recovery_perf": summarize_a2_recovery_perf,
    "expanded_scope_eval": summarize_expanded_scope_eval,
    "expanded_scope_perf": summarize_expanded_scope_perf,
}
SUMMARY_STAT_HANDLERS = {
    "guidance_eval": collect_guidance_eval_stats,
    "a1_codegen_perf": collect_a1_codegen_perf_stats,
    "bug_repair_eval": collect_bug_repair_eval_stats,
    "a2_recovery_perf": collect_a2_recovery_perf_stats,
    "expanded_scope_eval": collect_expanded_scope_eval_stats,
    "expanded_scope_perf": collect_expanded_scope_perf_stats,
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
        "problem_file": case_cfg.get("problem_file"),
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
        stats = SUMMARY_STAT_HANDLERS[metric_cfg["summary_kind"]](rows)
        metric_blocks.append(
            {
                "path": metric_cfg["path"],
                "summary_kind": metric_cfg["summary_kind"],
                "stats": stats,
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


def find_metric_block(result: dict, summary_kind: str) -> dict | None:
    for block in result["metrics"]:
        if block["summary_kind"] == summary_kind:
            return block
    return None


def build_mode_comparison(case_id: str, track: str, modes: list[str]) -> list[dict]:
    comparison = []
    for mode in modes:
        result = build_selection(case_id, mode, track)
        comparison.append(
            {
                "mode": mode,
                "selection": result["selection"],
                "guidance": find_metric_block(result, "guidance_eval"),
                "perf": (
                    find_metric_block(result, "a2_recovery_perf")
                    or find_metric_block(result, "a1_codegen_perf")
                    or find_metric_block(result, "expanded_scope_perf")
                ),
                "result": result,
            }
        )
    return comparison


def build_demo_result(name: str) -> dict:
    if name not in DEMO_SCENARIOS:
        supported = ", ".join(sorted(DEMO_SCENARIOS))
        raise ValueError(f"Unsupported demo scenario: {name}. Supported demos: {supported}")
    scenario = DEMO_SCENARIOS[name]
    main = scenario["main_selection"]
    main_result = build_selection(main["case_id"], main["mode"], main["track"])
    mode_compare_cfg = scenario["mode_compare"]
    mode_comparison = build_mode_comparison(
        mode_compare_cfg["case_id"],
        mode_compare_cfg["track"],
        mode_compare_cfg["modes"],
    )

    extra_results = []
    for item in scenario["extra_views"]:
        extra_results.append(
            {
                "label": item["label"],
                "result": build_selection(item["case_id"], item["mode"], item["track"]),
            }
        )

    input_preface_points: list[str] = []
    for relative_path, prefixes, max_items in scenario.get("input_preface", []):
        input_preface_points.extend(extract_prefixed_points(relative_path, prefixes, max_items))

    input_problem_points: list[str] = []
    for relative_path, heading, max_items in scenario["input_problem_sections"]:
        input_problem_points.extend(extract_section_points(relative_path, heading, max_items))

    structured_points: list[str] = []
    for relative_path, heading, max_items in scenario["structured_sections"]:
        structured_points.extend(extract_section_points(relative_path, heading, max_items))

    return {
        "name": name,
        "scenario": scenario,
        "main_result": main_result,
        "mode_comparison": mode_comparison,
        "extra_results": extra_results,
        "input_preface_points": input_preface_points,
        "input_problem_points": input_problem_points,
        "structured_points": structured_points,
    }


def render_demo_text(demo: dict) -> str:
    scenario = demo["scenario"]
    main_result = demo["main_result"]
    main_selection = main_result["selection"]
    main_materials = main_result["materials"]
    main_guidance = find_metric_block(main_result, "guidance_eval")
    main_perf = find_metric_block(main_result, "a2_recovery_perf") or find_metric_block(main_result, "a1_codegen_perf")
    lines = [
        f"{scenario['title']} v1",
        "",
        "一句话阶段判断",
        f"- {STAGE_JUDGMENT}",
        f"- 演示目标：{scenario['summary']}",
        "",
        "Step 1. 输入题目",
        f"- problem_file: {main_materials.get('problem_file') or 'none'}",
        f"- task_card: {main_materials['task_cards'][0]}",
    ]
    for point in demo["input_preface_points"]:
        lines.append(f"- {point}")
    for point in demo["input_problem_points"]:
        lines.append(f"- {point}")

    lines.extend(
        [
            "",
            "Step 2. 结构化表示",
            f"- 当前主案例：{main_selection['case_id']} ({main_selection['case_title']})",
            f"- 当前展示轨道：{main_selection['track']} ({main_selection['track_label']})",
        ]
    )
    for point in demo["structured_points"]:
        lines.append(f"- {point}")

    lines.extend(
        [
            "",
            "Step 3. Prompt 选择",
            f"- 当前展示模式：{MODE_DISPLAY_NAMES[main_selection['mode']]}",
            f"- prompt_template: {main_materials['prompt_template']}",
            f"- prompt_used: {main_materials.get('prompt_used') or 'not found'}",
            "- protocol_files:",
        ]
    )
    for path in main_materials["protocol_files"]:
        lines.append(f"  - {path}")
    lines.extend(
        [
            "- 同轨道可切换模式：",
        ]
    )
    for item in demo["mode_comparison"]:
        prompt_template = item["result"]["materials"]["prompt_template"]
        lines.append(f"  - {MODE_DISPLAY_NAMES[item['mode']]} -> {prompt_template}")

    lines.extend(
        [
            "",
            "Step 4. Run 结果",
            f"- representative_run_doc: {main_materials.get('representative_run_doc') or 'not found'}",
            "- all_run_docs:",
        ]
    )
    for path in main_materials["all_run_docs"]:
        lines.append(f"  - {path}")
    lines.append("- 同一研究链条下可继续展开：")
    for item in demo["extra_results"]:
        selection = item["result"]["selection"]
        run_doc = item["result"]["materials"].get("representative_run_doc") or "not found"
        lines.append(f"  - {item['label']} -> {selection['case_id']} / {selection['mode']} / {selection['track']} / {run_doc}")

    lines.append("")
    lines.append("Step 5. Metrics 摘要")
    if main_guidance and main_guidance["stats"]:
        stats = main_guidance["stats"]
        lines.extend(
            [
                f"- 当前展示模式 `{main_selection['mode']}` 的过程质量：",
                f"  - runnable=1 -> {stats['runnable_ok']}/{stats['rows']}",
                f"  - correct=2 -> {stats['correct_ok']}/{stats['rows']}",
                f"  - self_check=2 -> {stats['self_check_ok']}/{stats['rows']}",
                f"  - avg_time_to_first_working_min={format_float(stats['avg_time_to_first_working_min'], 2)}",
            ]
        )
    if main_perf and main_perf["stats"]:
        stats = main_perf["stats"]
        lines.extend(
            [
                f"- 当前展示模式 `{main_selection['mode']}` 的结果摘要：",
                f"  - output_ok=1 -> {stats['output_ok']}/{stats['perf_rows']}",
                f"  - avg_runtime_s={format_float(stats['avg_runtime_s'], 4)}",
                f"  - avg_psnr={format_float(stats.get('avg_psnr'), 4)}",
                f"  - avg_ssim={format_float(stats.get('avg_ssim'), 4)}",
                f"  - avg_rse={format_float(stats.get('avg_rse'), 4)}",
            ]
        )

    lines.append("- A2 baseline 三模式对比：")
    for item in demo["mode_comparison"]:
        guidance = item["guidance"]["stats"] if item["guidance"] else {}
        perf = item["perf"]["stats"] if item["perf"] else {}
        lines.append(
            "  - "
            + f"{MODE_DISPLAY_NAMES[item['mode']]}: "
            + f"runnable {guidance.get('runnable_ok', 'n/a')}/{guidance.get('rows', 'n/a')}, "
            + f"correct {guidance.get('correct_ok', 'n/a')}/{guidance.get('rows', 'n/a')}, "
            + f"self_check {guidance.get('self_check_ok', 'n/a')}/{guidance.get('rows', 'n/a')}, "
            + f"avg_psnr {format_float(perf.get('avg_psnr'), 4)}, "
            + f"avg_ssim {format_float(perf.get('avg_ssim'), 4)}, "
            + f"avg_rse {format_float(perf.get('avg_rse'), 4)}"
        )

    lines.extend(
        [
            "",
            "当前最稳能说什么",
        ]
    )
    for conclusion in FROZEN_CONCLUSIONS:
        lines.append(f"- {conclusion}")

    lines.extend(
        [
            "",
            "题库与扩展材料",
        ]
    )
    for path in scenario["task_bank_files"]:
        lines.append(f"- {path}")
    for note in scenario["demo_notes"]:
        lines.append(f"- {note}")

    lines.extend(
        [
            "",
            "推荐演示命令",
        ]
    )
    for command in scenario["recommended_commands"]:
        lines.append(f"- {command}")
    return "\n".join(lines)


def print_combinations() -> None:
    print("Supported combinations")
    for case_id, case_cfg in CATALOG.items():
        print(f"- {case_id}:")
        for track, track_cfg in case_cfg["tracks"].items():
            modes = ", ".join(track_cfg["run_ids"].keys())
            print(f"  - {track}: {modes}")


def print_demo_scenarios() -> None:
    print("Supported demo scenarios")
    for name, scenario in sorted(DEMO_SCENARIOS.items()):
        print(f"- {name}: {scenario['summary']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Minimal CLI prototype for selecting existing A1/A2 research assets.")
    parser.add_argument("--case", dest="case_id", help="A1 or A2")
    parser.add_argument("--mode", help="direct_answer, plain_guidance, or coe_guided")
    parser.add_argument("--track", help="baseline, bug-repair, expanded-scope, or fresh-generation")
    parser.add_argument("--demo", help="Run a curated demo scenario, for example: advisor")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--list", action="store_true", help="Show supported case/mode/track combinations and exit.")
    return parser.parse_args()


def main() -> None:
    try:
        args = parse_args()
        if args.list:
            print_combinations()
            print("")
            print_demo_scenarios()
            return

        if args.demo:
            if args.demo == "list":
                print_demo_scenarios()
                return
            if args.format != "text":
                raise ValueError("Demo mode currently supports only --format text.")
            print(render_demo_text(build_demo_result(args.demo)))
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
