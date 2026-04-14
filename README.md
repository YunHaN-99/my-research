# AI-for-research
一句话目标：用 A1/A2 主案例做“过程化指导 + 结构化检查 + 纠错评估”的研究仓库。

## Current status
- A1 v1 已收尾：baseline direct_answer / plain_guidance / coe_guided 主实验、固定协议 replication、bug-repair benchmark 均已完成。
- A1 failure cases 已从复查资产扩展为 9 条可评分的 bug-repair benchmark 记录。
- A2 已锁定为 `hw2-op2` chapter5 RSLT inpainting 主案例，baseline direct/plain/CoE 与 fixed-protocol replication 均已完成。
- A2 bug-repair benchmark 已完成，当前已形成 3 个 curated bugs x 3 个 guidance mode 的 9 条可评分记录。
- A2 expanded-scope validation 已完成，当前已补充 4 images x 4 corruption 的扩展稳健性证据。
- A2 fresh-generation replication 已完成，固定协议下累计已形成 15 条 guidance 主记录与 60 条恢复结果记录。
- Timeline 原始文案曾把 A2 写成 “SVD 图像压缩”；当前中期口径需统一为“低秩图像任务族下，最终聚焦 `chapter5 rslt_inpainting` 主案例”。
- 正式 task-bank 页面已建立，当前按“主案例家族 / 固定协议子任务 / failure cases”三层整理题库。
- A3 / A4 已补入占位 task card，当前可诚实表述为“主案例已闭环，题库骨架已成型，扩展条目正在接入”。
- 最小 CLI 原型已建立：`python run_research_case.py --case A2 --mode plain_guidance --track baseline` 可直接输出 prompt、protocol、run 文档和 metrics 摘要。
- 当前阶段：A1/A2 主案例闭环已完成，下一步是题库、原型和中期材料收口，而不是继续追加同类 rerun。

## Quick links
- [task_cards/A1_seam_carving_taskcard_v1.md](task_cards/A1_seam_carving_taskcard_v1.md)
- [task_cards/A1_bug_repair_taskcard_v0.md](task_cards/A1_bug_repair_taskcard_v0.md)
- [task_cards/A2_rslt_inpainting_taskcard_v1.md](task_cards/A2_rslt_inpainting_taskcard_v1.md)
- [task_cards/A2_bug_repair_taskcard_v0.md](task_cards/A2_bug_repair_taskcard_v0.md)
- [task_cards/A3_taskcard_v0.md](task_cards/A3_taskcard_v0.md)
- [task_cards/A4_taskcard_v0.md](task_cards/A4_taskcard_v0.md)
- [report/a1_eval_protocol_v0.md](report/a1_eval_protocol_v0.md)
- [report/a1_replication_summary_v0.md](report/a1_replication_summary_v0.md)
- [report/a1_bug_repair_protocol_v0.md](report/a1_bug_repair_protocol_v0.md)
- [report/a1_bug_repair_summary_v0.md](report/a1_bug_repair_summary_v0.md)
- [report/a1_v1_stage_summary.md](report/a1_v1_stage_summary.md)
- [report/a2_eval_protocol_v0.md](report/a2_eval_protocol_v0.md)
- [report/a2_baseline_summary_v0.md](report/a2_baseline_summary_v0.md)
- [report/a2_replication_summary_v0.md](report/a2_replication_summary_v0.md)
- [report/a2_bug_repair_protocol_v0.md](report/a2_bug_repair_protocol_v0.md)
- [report/a2_failure_case_design_v0.md](report/a2_failure_case_design_v0.md)
- [report/a2_bug_repair_summary_v0.md](report/a2_bug_repair_summary_v0.md)
- [report/a2_expanded_scope_protocol_v0.md](report/a2_expanded_scope_protocol_v0.md)
- [report/a2_expanded_scope_summary_v0.md](report/a2_expanded_scope_summary_v0.md)
- [report/phase2_progress_report_2026-04-12.md](report/phase2_progress_report_2026-04-12.md)
- [report/timeline_scope_alignment_2026-04-12.md](report/timeline_scope_alignment_2026-04-12.md)
- [report/prompt_template_library_v1.md](report/prompt_template_library_v1.md)
- [report/structured_modeling_checklist_v1.md](report/structured_modeling_checklist_v1.md)
- [report/error_taxonomy_and_feedback_rules_v1.md](report/error_taxonomy_and_feedback_rules_v1.md)
- [report/midterm_stage_summary_v0.md](report/midterm_stage_summary_v0.md)
- [report/midterm_attachment_checklist_v0.md](report/midterm_attachment_checklist_v0.md)
- [report/task_bank_index_v1.md](report/task_bank_index_v1.md)
- [report/task_bank_status_v1.md](report/task_bank_status_v1.md)
- [report/prototype_outline_v0.md](report/prototype_outline_v0.md)
- [report/prototype_cli_v0.md](report/prototype_cli_v0.md)
- [report/advisor_confirmation_questions_v0.md](report/advisor_confirmation_questions_v0.md)
- [metrics/a1_guidance_eval_v0.csv](metrics/a1_guidance_eval_v0.csv)
- [metrics/a1_codegen_perf_v0.csv](metrics/a1_codegen_perf_v0.csv)
- [metrics/a1_failure_repair_eval_v0.csv](metrics/a1_failure_repair_eval_v0.csv)
- [metrics/a2_guidance_eval_v0.csv](metrics/a2_guidance_eval_v0.csv)
- [metrics/a2_recovery_perf_v0.csv](metrics/a2_recovery_perf_v0.csv)
- [metrics/a2_failure_repair_eval_v0.csv](metrics/a2_failure_repair_eval_v0.csv)
- [metrics/a2_expanded_scope_eval_v0.csv](metrics/a2_expanded_scope_eval_v0.csv)
- [metrics/a2_expanded_scope_perf_v0.csv](metrics/a2_expanded_scope_perf_v0.csv)

## Repo map
task_cards / prompts / runs / metrics / report / solutions / outputs / run_research_case.py

## Reproduce A1
- 环境基线（统一）：使用 conda 环境 `llmft`，不再把 `.venv` 作为实验主环境。
- 激活命令（PowerShell）：`conda activate llmft`
- 依赖检查：`python -c "import numpy, matplotlib, skimage, scipy; print('deps ok')"`
- 主入口脚本：[solutions/hw1_op1/src/run_step6_comparisons.py](solutions/hw1_op1/src/run_step6_comparisons.py)
- replication 单条评测入口示例：`python solutions/hw1_op1/generated/run_015_plain_guidance_rep3/src/run_protocol_eval.py`
- bug-repair 协议：[report/a1_bug_repair_protocol_v0.md](report/a1_bug_repair_protocol_v0.md)
- failure cases 路径：[solutions/hw1_op1/failure_cases](solutions/hw1_op1/failure_cases)
- 输出位置：[outputs/hw1_op1](outputs/hw1_op1)

## Next milestones
1. 统一 Timeline / 中期材料中的 A2 定义与阶段口径
2. 以 task-bank 页面固定三层结构，并把 A3/A4 从占位推进到首发条目
3. 收束 Prompt 模板库 v1、结构化检查清单 v1、错误分类与反馈规则 v1
4. 形成中期阶段小结、附件清单与原型说明
