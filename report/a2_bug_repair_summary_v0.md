# A2 bug-repair summary v0

## Scope
- target runs: run_043 to run_051
- bugs:
  - `bug_01_missing_mask_constraint`
  - `bug_02_mask_polarity_inverted`
  - `bug_03_sparse_component_written_back`
- modes:
  - `direct_answer`
  - `plain_guidance`
  - `coe_guided`
- protocol_file: `report/a2_bug_repair_protocol_v0.md`
- regression environment: conda `llmft`

## 已完成
- completed bug-repair runs:
  - run_043
  - run_044
  - run_045
  - run_046
  - run_047
  - run_048
  - run_049
  - run_050
  - run_051
- current data source: `metrics/a2_failure_repair_eval_v0.csv` (9 rows total)

## 当前统计

| mode | runs | diagnosis_correct | patch_runnable | regression_pass | median fix_rounds | rough median time_to_fix_min |
|---|---:|---:|---:|---:|---:|---:|
| direct_answer | 3 | 3/3 | 3/3 | 3/3 | 0 | 0.1 |
| plain_guidance | 3 | 3/3 | 3/3 | 3/3 | 0 | 0.1 |
| coe_guided | 3 | 3/3 | 3/3 | 3/3 | 0 | 0.1 |

### By bug
- `bug_01_missing_mask_constraint`: 3/3 diagnosis_correct, 3/3 patch_runnable, 3/3 regression_pass
- `bug_02_mask_polarity_inverted`: 3/3 diagnosis_correct, 3/3 patch_runnable, 3/3 regression_pass
- `bug_03_sparse_component_written_back`: 3/3 diagnosis_correct, 3/3 patch_runnable, 3/3 regression_pass

## 初步观察
- 在这 3 个 A2 curated failure cases 上，三种 guidance 模式都能首轮给出正确诊断与最小可运行补丁。
- 本轮 benchmark 更能支持“结构化输出提升可检查性”的判断，而不是“在该小样本上显著提高修复通过率”。
- plain_guidance 与 coe_guided 在 root-cause 说明、回归清单和接口约束复查上更完整；direct_answer 也能修对，但说明更短。
- 这 3 个 bug 基本覆盖了 A2 当前最关键的实现语义：mask 约束、mask 语义、RPCA 分量语义。

## Measurement boundary
- `time_to_fix_min` 来自本次 scripted benchmark 的 wall-clock，包含 artifact 写入与 `llmft` 回归检查，不建议与 A1 的 same-session 手工记录做强比较。
- regression_pass 通过标准来自 `solutions/hw2_op2/failure_cases/regression_check.py` 下的 stubbed-helper reference match，而不是完整重跑 chapter5 全协议。
- benchmark 仍然只覆盖 3 个 curated bugs、单模型会话、单评分者。
