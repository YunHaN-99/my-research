# Pilot Scoring Sheet v0

## 1. 基本信息
- `session_id`：`PILOT_20260420_000`
- `participant_id`：`SELF`
- `task_id`：`T2_A1_bug_01`
- `condition`：`process_guided_workflow`
- `session_stage`：`internal_dry_run`
- `scorer_id`：`SELF`

## 2. 汇总表

| 字段 | 分值 |
|---|---|
| completion_status | 2 |
| runnable | 1 |
| outcome_quality | 2 |
| self_check_coverage | 2 |
| root_cause_explanation | 2 |
| regression_plan_quality | 2 |
| artifact_completeness | 2 |

总评备注：
- 本次最明显的优点：
  诊断和 patch 都很小，说明 `process_guided_workflow` 对边界类 bug 足够收束，没有把任务带偏成“大改代码”。
- 本次最明显的缺口：
  参与者 notes 缺少 `session_id` 和最终代码路径，研究者回填时还得额外翻 session record。
- 是否更像 `baseline_workflow` 或 `process_guided_workflow` 的典型表现：
  明显更像 `process_guided_workflow`，因为整个过程都围绕 symptom、关键不变量、最小修补和回归说明来组织。

评分依据补充：
- `completion_status=2`：核心修补已完成。
- `runnable=1`：patched code 在 `llmft` 环境下验证通过。
- `outcome_quality=2`：与 scorer-only `fixed_code.py` 的行为一致。
- `self_check_coverage=2`：有明确边界与 backtrack 范围检查。
- `root_cause_explanation=2`：主错误定位与 `diagnosis.md` 一致。
- `regression_plan_quality=2`：给出了可直接执行的最小矩阵回归。
- `artifact_completeness=2`：表单、notes、patch、评分和 CSV 均已落盘。
