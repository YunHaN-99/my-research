# Phase 2 Progress Report

date: 2026-04-12
repo_latest_commit: 2026-04-07 7eac855 + working tree updates on 2026-04-12
stage_judgment: A1/A2 main-case closure complete under current frozen scope; midterm-package consolidation in progress

## 一句话判断
项目已经完成 A1 / A2 首轮主案例闭环。A2 当前统一表述为：低秩图像任务族下、已完成范围收束并完成主案例闭环的 `hw2-op2/src/chapter5_rslt.py::rslt_inpainting(...)` 灰度图像修复主案例。当前中期重点不是继续追加同类 rerun，而是收束模板库、检查清单、错误分类、题库页和原型入口，并明确 P2 / P3 的未完成项。

## 统一口径摘要

### 已经完成什么
- 主线位置：A1 / A2 main-case closure completed
- 完成度判断：
  - A1 main experiment: completed
  - A1 fixed-protocol replication: completed
  - A1 bug-repair benchmark: completed
  - A1 v1 stage summary: completed
  - A2 baseline: completed
  - A2 fixed-protocol replication: completed
  - A2 failure-case design: completed
  - A2 bug-repair benchmark: completed
  - A2 expanded-scope validation: completed
  - A2 fresh-generation replication: completed
  - task-bank midterm version: completed (`16` formal entries)
  - A3 / A4 first-entry freeze: completed (`requirement + taskcard_v1`)
  - minimal CLI prototype: completed

### 现在最稳能说什么
- A1 / A2 两个主案例都已经闭环，当前仓库的主线判断不是“还在试跑”，而是“已形成可复查的中期主干”。
- 当前冻结的第一条研究结论是：`plain_guidance` / `coe_guided` 的核心优势，是提升自检覆盖、根因说明和回归说明的可复查性。
- 当前冻结的第二条研究结论是：在 A2 这类冻结协议任务上，结构化 guidance 未必显著改变最终恢复指标，但确实改善了过程质量与可解释性。
- 对 A2 来说，当前最强证据来自 fixed-protocol、expanded-scope 与 fresh-generation 三层一致性，而不是继续追加同协议 rerun。

### 还没做什么
- 当前仍需要在所有对外材料中持续坚持同一 A2 口径，不再混写成早期宽标签 “SVD 图像压缩”。
- 模板库 / 结构化检查清单 / 错误分类规则的 `v1` 文档已经补出，但还需要在中期附件包里继续统一命名和引用。
- A3 / A4 已各冻结 `1` 个首发条目并补齐 `requirement + taskcard_v1`；更完整的固定协议、正式实验、统一原型封装和试用数据仍未启动。

## 已完成工作

### 1. A1 主线闭环已完成
- A1 主实验、fixed-protocol replication、bug-repair benchmark 全部完成。
- 当前指标表：
  - `metrics/a1_guidance_eval_v0.csv` = 12 rows
  - `metrics/a1_codegen_perf_v0.csv` = 18 rows
  - `metrics/a1_failure_repair_eval_v0.csv` = 9 rows

| mode | runs | runnable success | correct=2 | self_check=2 | average time_to_first_working_min |
|---|---:|---:|---:|---:|---:|
| direct_answer | 4 | 4/4 | 4/4 | 0/4 | 2.40 |
| plain_guidance | 4 | 4/4 | 4/4 | 4/4 | 4.50 |
| coe_guided | 4 | 4/4 | 4/4 | 4/4 | 2.08 |

| mode | bug-repair runs | diagnosis_correct | patch_runnable | regression_pass | average time_to_fix_min |
|---|---:|---:|---:|---:|---:|
| direct_answer | 3 | 3/3 | 3/3 | 3/3 | 0.57 |
| plain_guidance | 3 | 3/3 | 3/3 | 3/3 | 0.83 |
| coe_guided | 3 | 3/3 | 3/3 | 3/3 | 1.03 |

当前可支持的判断：
- 在 A1 固定协议下，三种模式都能稳定达到 runnable 与 correct。
- plain_guidance / coe_guided 的优势主要体现在 `self_check`、Reviewer/Regressor 痕迹和回归说明的可复查性。
- A1 的 3 个 curated failure cases 已能稳定支撑 bug-repair benchmark。

### 2. A2 fixed-protocol package 已完成并扩展到 fresh-generation
- A2 当前主案例：
  - target project: `hw2-op2`
  - target function: `hw2-op2/src/chapter5_rslt.py::rslt_inpainting(...)`
  - fixed protocol: `lena`, `barbara` + `random_pixel@50%`, `text@50%` + grayscale `256x256`
- completed runs:
  - baseline: `run_030` to `run_032`
  - replication: `run_033` to `run_041`
  - fresh-generation: `run_055` to `run_057`
- current result tables:
  - `metrics/a2_guidance_eval_v0.csv` = 15 rows
  - `metrics/a2_recovery_perf_v0.csv` = 60 rows

| mode | runs | runnable success | correct=2 | self_check=2 | median time_to_first_working_min | avg case runtime_s |
|---|---:|---:|---:|---:|---:|---:|
| direct_answer | 5 | 5/5 | 5/5 | 0/5 | 1.2 | 17.0855 |
| plain_guidance | 5 | 5/5 | 5/5 | 5/5 | 1.3 | 18.2274 |
| coe_guided | 5 | 5/5 | 5/5 | 5/5 | 1.2 | 17.4860 |

当前可支持的判断：
- 15/15 A2 fixed-protocol runs 都是一轮 runnable 且 correct。
- 四个固定 case 在全部 15 runs 上仍只出现 1 组 `(PSNR, SSIM, RSE)` 指标：
  - `lena / random_pixel@50%`: `15.1519 / 0.3766 / 0.3245`
  - `lena / text@50%`: `27.2597 / 0.9483 / 0.0805`
  - `barbara / random_pixel@50%`: `24.2780 / 0.7244 / 0.1358`
  - `barbara / text@50%`: `34.9722 / 0.9762 / 0.0397`
- 因此当前最强证据仍然是“结构化指导提升可检查性”，而不是“在该任务上显著改变最终恢复质量”。
 - 更准确地说，当前优势主要体现在自检覆盖、根因说明和回归说明的可复查性。

### 3. A2 bug-repair benchmark 已完成
- completed bug-repair runs: `run_043` to `run_051`
- current data source: `metrics/a2_failure_repair_eval_v0.csv` = 9 rows

| mode | runs | diagnosis_correct | patch_runnable | regression_pass | average time_to_fix_min |
|---|---:|---:|---:|---:|---:|
| direct_answer | 3 | 3/3 | 3/3 | 3/3 | 0.10 |
| plain_guidance | 3 | 3/3 | 3/3 | 3/3 | 0.10 |
| coe_guided | 3 | 3/3 | 3/3 | 3/3 | 0.10 |

当前可支持的判断：
- 在 3 个 curated A2 failure cases 上，三种模式都能完成根因定位、最小修补与回归通过。
- 当前 3 个 bug 已覆盖 A2 当前最关键的三个实现语义：mask 约束、mask 语义、RPCA 分量语义。

### 4. A2 expanded-scope validation 已完成
- validation runs: `run_052` to `run_054`
- source artifacts: `run_030` / `run_031` / `run_032`
- expanded setup: `4 images x 4 corruption = 16 cases per mode`
- result tables:
  - `metrics/a2_expanded_scope_eval_v0.csv` = 3 rows
  - `metrics/a2_expanded_scope_perf_v0.csv` = 48 rows

| mode | runs | case_count per run | output_ok_count | avg case runtime_s |
|---|---:|---:|---:|---:|
| direct_answer | 1 | 16 | 16 | 15.1708 |
| plain_guidance | 1 | 16 | 16 | 14.9153 |
| coe_guided | 1 | 16 | 16 | 15.0344 |

当前可支持的判断：
- 48/48 expanded-scope cases 都是 `output_ok = 1`。
- 全部 16 个 image/corruption cases 在三种 mode 下仍只出现 1 组 `(PSNR, SSIM, RSE)`，说明当前差异仍主要在过程痕迹而非最终质量。

### 5. A2 范围收束说明
- `Timeline.docx` 原始文案把 A2 写成 “SVD 图像压缩”。
- 仓库当前实际主线已收束为“低秩图像任务族下、已完成范围收束并完成主案例闭环的 `hw2-op2/src/chapter5_rslt.py::rslt_inpainting(...)` 灰度图像修复主案例”。
- 这次收束的含义是：
  - 没有脱离原始低秩 / SVD 研究方向。
  - 也没有宣称整个低秩图像方向都已完成。
  - 当前已经完成的是：在冻结口径下完成 A2 主案例闭环。
- 因此，中期材料中应把 A2 写成“已完成范围收束并完成主案例闭环”，而不是简单写成“原计划 A2 未做”。

## 当前未完成项

### 1. 中期口径收口尚未完成
- Timeline 原始 A2 文案需要与当前主案例说明同步。
- A1 / A2 现有 prompt、task card、bug-repair 资产已经整理为模板库 / 检查清单 / 错误分类文档，但还需继续统一到中期附件包目录。

### 2. Timeline 中期后的扩展项尚未完成
- A3 / A4 已补出首发条目的 `requirement + taskcard_v1`，但尚未进入固定协议 / 正式实验阶段。
- `run_research_case.py` 最小 CLI 原型已经建立，但更完整的统一演示入口尚未形成。
- 小范围试用、学生反馈与量化对照数据尚未启动。

## 风险与边界
- 当前 strongest evidence 仍主要覆盖 A1 单任务、固定图片、固定 `max_side=420`、固定 shrink-only 协议，以及 3 个 curated bug。
- A2 strongest evidence 覆盖 fixed protocol 的 `2 images x 2 corruption x grayscale 256x256`、expanded-scope 的 `4 images x 4 corruption`，以及同协议下 fresh-generation 复现。
- 当前仍不能据此得出“结构化指导显著提升最终正确率”的强结论；更稳妥的结论是“结构化指导提升了可检查性、回归说明与过程可复查性”。
- 若用教育研究语言表述，应优先写成“结构化 guidance 改善了过程质量与可解释性”，而不是“显著抬高最终恢复指标”。
- A2 fresh-generation 已经做完，因此继续追加相同协议的 rerun 边际收益较低。

## 建议的下一步顺序
1. 统一 Timeline / 中期材料中的 A2 定义与阶段口径。
2. 收束 Prompt 模板库 v1、结构化检查清单 v1、错误分类与反馈规则 v1。
3. 形成中期阶段小结、附件清单和可直接提交的材料包。
4. 若时间允许，再把 A3 / A4 首发条目推进到协议与实验链路，并继续整理统一原型与小范围试用计划。

## 可直接引用的依据文件
- `README.md`
- `report/timeline_scope_alignment_2026-04-12.md`
- `report/midterm_stage_summary_v0.md`
- `report/a1_replication_summary_v0.md`
- `report/a1_bug_repair_summary_v0.md`
- `report/a1_v1_stage_summary.md`
- `report/a2_eval_protocol_v0.md`
- `report/a2_baseline_summary_v0.md`
- `report/a2_replication_summary_v0.md`
- `report/a2_bug_repair_protocol_v0.md`
- `report/a2_failure_case_design_v0.md`
- `report/a2_bug_repair_summary_v0.md`
- `report/a2_expanded_scope_protocol_v0.md`
- `report/a2_expanded_scope_summary_v0.md`
- `metrics/a1_guidance_eval_v0.csv`
- `metrics/a1_codegen_perf_v0.csv`
- `metrics/a1_failure_repair_eval_v0.csv`
- `metrics/a2_guidance_eval_v0.csv`
- `metrics/a2_recovery_perf_v0.csv`
- `metrics/a2_failure_repair_eval_v0.csv`
- `metrics/a2_expanded_scope_eval_v0.csv`
- `metrics/a2_expanded_scope_perf_v0.csv`
