# Midterm Attachment Checklist v0

## 目的
把当前仓库中已经可以直接作为中期检查附件的材料，与仍待补充的材料分开列出，避免中期提交时临时翻目录。

## 1. 已可直接纳入附件的材料

### 研究范围与阶段说明
- `README.md`
- `report/phase2_progress_report_2026-04-12.md`
- `report/timeline_scope_alignment_2026-04-12.md`
- `report/midterm_stage_summary_v0.md`
- `report/task_bank_status_v1.md`
- `report/prototype_outline_v0.md`

### A1 主案例材料
- `task_cards/A1_seam_carving_taskcard_v1.md`
- `report/a1_eval_protocol_v0.md`
- `report/a1_replication_summary_v0.md`
- `report/a1_bug_repair_protocol_v0.md`
- `report/a1_bug_repair_summary_v0.md`
- `report/a1_v1_stage_summary.md`
- `metrics/a1_guidance_eval_v0.csv`
- `metrics/a1_codegen_perf_v0.csv`
- `metrics/a1_failure_repair_eval_v0.csv`

### A2 主案例材料
- `problems/a2_requirement.md`
- `task_cards/A2_rslt_inpainting_taskcard_v1.md`
- `task_cards/A2_bug_repair_taskcard_v0.md`
- `report/a2_eval_protocol_v0.md`
- `report/a2_baseline_summary_v0.md`
- `report/a2_replication_summary_v0.md`
- `report/a2_bug_repair_protocol_v0.md`
- `report/a2_failure_case_design_v0.md`
- `report/a2_bug_repair_summary_v0.md`
- `report/a2_expanded_scope_protocol_v0.md`
- `report/a2_expanded_scope_summary_v0.md`
- `metrics/a2_guidance_eval_v0.csv`
- `metrics/a2_recovery_perf_v0.csv`
- `metrics/a2_failure_repair_eval_v0.csv`
- `metrics/a2_expanded_scope_eval_v0.csv`
- `metrics/a2_expanded_scope_perf_v0.csv`

### 模板与方法材料
- `report/prompt_template_library_v1.md`
- `report/structured_modeling_checklist_v1.md`
- `report/error_taxonomy_and_feedback_rules_v1.md`
- `prompts/a1/*.md`
- `prompts/a2/*.md`
- `runs/a1_bug_repair_run_template_v0.md`
- `runs/a2_guidance_run_template_v0.md`
- `runs/a2_bug_repair_run_template_v0.md`

## 2. 建议作为“证据样例”附上的材料
- A1 代表性 run：
  - `runs/2026-03-26_run_006_a1_direct_answer_baseline.md`
  - `runs/2026-03-26_run_007_a1_plain_guidance_baseline.md`
  - `runs/2026-03-27_run_008_a1_coe_guided.md`
  - `runs/2026-04-12_run_020_a1_bug_01_direct_answer.md`
- A2 代表性 run：
  - `runs/2026-04-12_run_030_a2_direct_answer_baseline.md`
  - `runs/2026-04-12_run_031_a2_plain_guidance_baseline.md`
  - `runs/2026-04-12_run_032_a2_coe_guided_baseline.md`
  - `runs/2026-04-12_run_052_a2_direct_answer_expanded_scope.md`
  - `runs/2026-04-12_run_055_a2_direct_answer_fresh_generation.md`

## 3. 当前仍待补充的中期材料

### 尚未完成
- 题库 `v1 (>=15 题)` 的实体扩充
- A3 / A4 扩展条目本体
- 可演示的统一原型实现
- 中期提交版附件清单的最终命名与排序

### 建议最小补法
- 先用现有 `task_bank_status_v1.md` 说明当前已有主案例和待扩展案例。
- 先用现有 `prototype_outline_v0.md` 说明当前自动化脚本链路与后续 CLI/Notebook 方向。
- A3 / A4 暂时先写扩展条目，不必立即做完整实验。

## 4. 提交前复核项
- 所有引用的 CSV 都能被打开。
- 所有报告中的 run 编号都能回指到 `runs/` 与 `outputs/`。
- A2 口径统一写成当前主案例，不再混写成 “SVD 图像压缩”。
- 每个结论都能回指至少 1 份 report 和 1 份 metrics 文件。

## 5. 当前判断
- 中期包的主干材料已经够用。
- 现在缺的不是继续跑同类实验，而是把“题库说明 / 原型说明 / 附件排序”补齐。
