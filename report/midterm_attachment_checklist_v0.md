# Midterm Attachment Checklist v0

## 目的
把当前仓库中已经可以直接作为中期检查附件的材料，与仍待补充的材料分开列出，避免中期提交时临时翻目录。

## 1. 统一口径摘要
这份附件清单服务于同一套阶段判断：A1 / A2 主案例闭环已完成，中期材料收口进行中。A2 在附件包中的统一写法应为：“低秩图像任务族下，已完成范围收束并完成主案例闭环的 `hw2-op2/src/chapter5_rslt.py::rslt_inpainting(...)` 灰度图像修复主案例”。

### 已经完成什么
- A1 主案例闭环材料已经齐备。
- A2 主案例闭环材料已经齐备，覆盖 baseline、fixed-protocol replication、bug-repair benchmark、expanded-scope validation 与 fresh-generation replication。
- 阶段说明、协议、metrics、代表性 run 和模板文档都已经有可提交版本。

### 现在最稳能说什么
- 当前附件包足以支撑“主案例闭环已经完成”的判断。
- 当前附件包足以支撑“结构化 guidance 改善过程可检查性与可复查性”的判断。
- 当前附件包不应用来支持“结构化 guidance 已显著提升最终恢复质量”的强结论。

### 还没做什么
- 题库 `v1` 已整理到中期够用版本，当前正式条目为 `16` 个，但仍不是结题版完整题库。
- A3 / A4 已各冻结 `1` 个首发条目并补齐 `requirement + taskcard_v1`，但尚未进入 fixed protocol / 正式实验主线。
- 最小 CLI 原型已经建立，试用方案与模板也已补出；但更完整的统一演示封装以及小范围试用的实际招募与数据采集尚未进入本次“已完成”附件范围。

## 2. 已可直接纳入附件的主干材料

### 研究范围与阶段说明
- `README.md`
- `report/phase2_progress_report_2026-04-12.md`
- `report/timeline_scope_alignment_2026-04-12.md`
- `report/midterm_stage_summary_v0.md`
- `report/advisor_confirmation_questions_v0.md`
- `report/task_bank_index_v1.md`
- `report/task_bank_status_v1.md`
- `report/a2_expanded_scope_selected_entries_v1.md`
- `report/prototype_outline_v0.md`
- `report/prototype_cli_v0.md`
- `report/advisor_demo_entry_v1.md`
- `report/small_sample_pilot_plan_v0.md`

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

### 扩展条目首发材料
- `problems/a3_requirement.md`
- `task_cards/A3_taskcard_v1.md`
- `problems/a4_requirement.md`
- `task_cards/A4_taskcard_v1.md`

### 模板与方法材料
- `run_research_case.py`
- `report/prompt_template_library_v1.md`
- `report/structured_modeling_checklist_v1.md`
- `report/error_taxonomy_and_feedback_rules_v1.md`
- `prompts/a1/*.md`
- `prompts/a2/*.md`
- `runs/a1_bug_repair_run_template_v0.md`
- `runs/a2_guidance_run_template_v0.md`
- `runs/a2_bug_repair_run_template_v0.md`

### 试用准备材料
- `pilot/pilot_participant_form_v0.md`
- `pilot/pilot_scoring_sheet_v0.md`
- `pilot/pilot_session_record_template_v0.md`
- `metrics/pilot_session_log_template_v0.csv`
- `metrics/pilot_session_log_codebook_v0.md`

## 3. 建议作为“证据样例”附上的材料
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

## 4. 当前仍待补充、但不应写成“已完成”的中期材料

### 尚未完成
- A3 / A4 首发条目的固定协议、failure case 与正式实验本体
- 更完整的统一原型封装与展示包装
- 小范围试用的实际招募、执行与数据采集
- 中期提交版附件清单的最终命名与排序

### 建议最小补法
- 先用现有 `task_bank_index_v1.md` 与 `task_bank_status_v1.md` 说明当前题库骨架。
- 用 `a2_expanded_scope_selected_entries_v1.md` 说明为什么从 16 个 expanded-scope case 中只固化 4 个正式条目。
- 先用现有 `prototype_cli_v0.md` 与 `prototype_outline_v0.md` 说明当前最小 CLI 已落地，以及后续 CLI / Notebook 方向。
- 用 `small_sample_pilot_plan_v0.md` 和 `pilot/`、`metrics/` 里的模板说明试用方案已经定、数据结构已经预埋。
- A3 / A4 当前已补到 requirement + taskcard_v1，不必立即做完整实验。

## 5. 提交前复核项
- 所有引用的 CSV 都能被打开。
- 所有报告中的 run 编号都能回指到 `runs/` 与 `outputs/`。
- A2 口径统一写成“低秩图像任务族下，已完成范围收束并完成主案例闭环的 `hw2-op2/src/chapter5_rslt.py::rslt_inpainting(...)` 灰度图像修复主案例”。
- 每个结论都能回指至少 1 份 report 和 1 份 metrics 文件。
- “已完成”与“后续扩展”必须分开排序，不混放在同一组附件里。

## 6. 当前判断
- 中期包的主干材料已经够用。
- 当前题库正式条目已整理到 `16` 条，足以支撑中期展示。
- 现在缺的不是继续跑同类实验，而是把“题库说明 / 原型说明 / 试用方案 / 附件排序”补齐。
