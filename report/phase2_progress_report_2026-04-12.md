# Phase 2 Progress Report

date: 2026-04-12
repo_latest_commit: 2026-04-07 7eac855 + working tree updates on 2026-04-12
stage_judgment: Phase 2 closure plus fresh-generation replication complete; midterm-package consolidation in progress

## 一句话判断
项目已经完成 A1 闭环包，以及当前口径下 A2 `chapter5 rslt_inpainting` 主案例的 baseline、fixed-protocol replication、bug-repair benchmark、expanded-scope validation 与 fresh-generation replication。当前更合理的下一步不是继续追加同类 rerun，而是统一 Timeline 口径、收束中期材料，并明确 P2/P3 的未完成项。

## 当前阶段判断
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
- 当前主要缺口：
  - Timeline 原始 A2 文案与仓库当前 A2 定义尚未在中期材料里彻底统一
  - 模板库 / 结构化检查清单 / 错误分类规则仍缺少集中版文档
  - A3 / A4 扩展条目、统一原型、试用数据仍未启动

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

### 5. A2 scope 与 Timeline 原始文案存在偏差，但当前主案例已形成稳定闭环
- `Timeline.docx` 原始文案把 A2 写成 “SVD 图像压缩”。
- 仓库当前实际主线已收束为“低秩图像任务族下，最终聚焦 `chapter5 rslt_inpainting` 的灰度图像修复主案例”。
- 这意味着：
  - 按当前仓库口径，A2 主案例已完成。
  - 按 Timeline 原始字面，A2 存在名称和任务边界漂移，应该在中期材料中明确解释为“范围收束”，而不是简单写成“原计划 A2 未做”。

## 当前未完成项

### 1. 中期口径收口尚未完成
- Timeline 原始 A2 文案需要与当前主案例说明同步。
- A1/A2 现有 prompt、task card、bug-repair 资产需要整理为模板库 / 检查清单 / 错误分类文档。

### 2. Timeline 中期后的内容尚未启动
- A3 / A4 扩展条目尚未补入题库。
- “输入题目 -> 结构化表示 -> 代码骨架 -> 自检 -> 结果记录”的统一原型尚未形成用户可演示版本。
- 小范围试用、学生反馈与量化对照数据尚未启动。

## 风险与边界
- 当前 strongest evidence 仍主要覆盖 A1 单任务、固定图片、固定 `max_side=420`、固定 shrink-only 协议，以及 3 个 curated bug。
- A2 strongest evidence 覆盖 fixed protocol 的 `2 images x 2 corruption x grayscale 256x256`、expanded-scope 的 `4 images x 4 corruption`，以及同协议下 fresh-generation 复现。
- 当前仍不能据此得出“结构化指导显著提升最终正确率”的强结论；更稳妥的结论是“结构化指导提升了可检查性、回归说明与过程可复查性”。
- A2 fresh-generation 已经做完，因此继续追加相同协议的 rerun 边际收益较低。

## 建议的下一步顺序
1. 统一 Timeline / 中期材料中的 A2 定义与阶段口径。
2. 收束 Prompt 模板库 v1、结构化检查清单 v1、错误分类与反馈规则 v1。
3. 形成中期阶段小结、附件清单和可直接提交的材料包。
4. 若时间允许，再补 A3 / A4 扩展条目、统一原型与小范围试用计划。

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
