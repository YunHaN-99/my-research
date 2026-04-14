# AI-for-research
一句话目标：用 A1/A2 主案例做“过程化指导 + 结构化检查 + 纠错评估”的研究仓库。

## 当前状态
- A1 v1 已收尾：`direct_answer` / `plain_guidance` / `coe_guided` 主实验、固定协议复现、bug-repair benchmark 均已完成。
- A1 failure cases 已从复查资产扩展为 9 条可评分的 bug-repair benchmark 记录。
- A2 已锁定为 `hw2-op2` chapter5 RSLT inpainting 主案例，baseline、fixed-protocol replication、bug-repair benchmark、expanded-scope validation、fresh-generation replication 均已完成。
- A2 当前已形成 15 条 guidance 主记录、60 条恢复结果记录、9 条 bug-repair 记录，以及 48 条 expanded-scope case 记录。
- Timeline 原始文案曾把 A2 写成 “SVD 图像压缩”；当前中期口径需统一为“低秩图像任务族下，最终聚焦 `chapter5 rslt_inpainting` 主案例”。
- 正式 task-bank 页面已建立，当前按“主案例家族 / 固定协议子任务 / failure cases”三层整理题库。
- A3 / A4 已补入占位 task card，当前可诚实表述为“主案例已闭环，题库骨架已成型，扩展条目正在接入”。
- 最小 CLI 原型已建立：`python run_research_case.py --case A2 --mode plain_guidance --track baseline` 可直接输出 prompt、protocol、run 文档和 metrics 摘要。
- 当前阶段：A1/A2 主案例闭环已完成，下一步是题库、原型和中期材料收口，而不是继续追加同类 rerun。

## 快速入口
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

## 仓库结构
task_cards / prompts / runs / metrics / report / solutions / outputs / run_research_case.py

## CLI 原型入口
- 列出支持的 case / mode / track 组合：`python run_research_case.py --list`
- 查看 A1 baseline 摘要：`python run_research_case.py --case A1 --mode plain_guidance --track baseline`
- 查看 A2 bug-repair 摘要：`python run_research_case.py --case A2 --mode coe_guided --track bug-repair`
- 查看 A2 expanded-scope 摘要：`python run_research_case.py --case A2 --mode direct_answer --track expanded-scope`
- 说明文档：[report/prototype_cli_v0.md](report/prototype_cli_v0.md)

## A1 复现入口
- 环境基线（统一）：使用 conda 环境 `llmft`，不再把 `.venv` 作为实验主环境。
- 激活命令（PowerShell）：`conda activate llmft`
- 依赖检查：`python -c "import numpy, matplotlib, skimage, scipy; print('deps ok')"`
- 主入口脚本：[solutions/hw1_op1/src/run_step6_comparisons.py](solutions/hw1_op1/src/run_step6_comparisons.py)
- 单条 replication 评测入口示例：`python solutions/hw1_op1/generated/run_015_plain_guidance_rep3/src/run_protocol_eval.py`
- bug-repair 协议：[report/a1_bug_repair_protocol_v0.md](report/a1_bug_repair_protocol_v0.md)
- failure cases 路径：[solutions/hw1_op1/failure_cases](solutions/hw1_op1/failure_cases)
- 输出位置：[outputs/hw1_op1](outputs/hw1_op1)

## 下一步
1. 把导师确认的三问发出去，尽快锁定 A2 口径、中期主轴和中期后优先级。
2. 从 A3 / A4 候选方向中各冻结 1 个首发条目，把占位 task card 往 `requirement` 和 `taskcard_v1` 推进。
3. 继续收束 Prompt 模板库、结构化检查清单、错误分类规则和中期附件包。
4. 在不追加同类 rerun 的前提下，把现有 CLI 原型继续整理成更适合展示的中期入口。
