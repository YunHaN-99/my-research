# A1 bug-repair summary v0

## Scope
- target runs: run_020 to run_028
- bugs: bug_01_dp_boundary, bug_02_no_energy_recompute, bug_03_height_transpose
- modes: direct_answer, plain_guidance, coe_guided
- protocol_file: report/a1_bug_repair_protocol_v0.md
- regression environment: conda `llmft`

## 已完成
- completed bug-repair runs:
  - run_020
  - run_021
  - run_022
  - run_023
  - run_024
  - run_025
  - run_026
  - run_027
  - run_028
- current data source: metrics/a1_failure_repair_eval_v0.csv (9 rows total)

## 当前统计

| mode | runs | diagnosis_correct | patch_runnable | regression_pass | median fix_rounds | rough median time_to_fix_min |
|---|---:|---:|---:|---:|---:|---:|
| direct_answer | 3 | 3/3 | 3/3 | 3/3 | 0 | 0.6 |
| plain_guidance | 3 | 3/3 | 3/3 | 3/3 | 0 | 0.8 |
| coe_guided | 3 | 3/3 | 3/3 | 3/3 | 0 | 1.0 |

### By bug
- bug_01_dp_boundary: 3/3 diagnosis_correct, 3/3 patch_runnable, 3/3 regression_pass
- bug_02_no_energy_recompute: 3/3 diagnosis_correct, 3/3 patch_runnable, 3/3 regression_pass
- bug_03_height_transpose: 3/3 diagnosis_correct, 3/3 patch_runnable, 3/3 regression_pass

## 初步观察
- 在这 3 个最小失败样例上，三种 guidance 模式都能首轮给出正确诊断与最小可运行补丁。
- 本轮 benchmark 更能支持“结构化输出提升可检查性”的判断，而不是“在该小样本上显著提高修复通过率”。
- coe_guided 的 reviewer / regressor 段落最完整，plain_guidance 也能稳定给出不变量与回归清单。
- direct_answer 也能修对，但解释与复核轨迹更短。

## Measurement boundary
- `time_to_fix_min` 是本次仓库收尾过程中的 rough same-session wall-clock，不是单独仪器化测量，不建议做强比较。
- regression_pass 通过标准来自 llmft 环境下对 patched_code 与 fixed_code 的行为一致性检查。
- benchmark 仍然只覆盖 3 个 curated bugs、单模型会话、单评分者。
