# Pilot Scoring Sheet v0

## 目的
给研究者在试用后统一打分，避免不同 session 用不同口径评价结果。

## 1. 基本信息
- `session_id`：
- `participant_id`：
- `task_id`：
- `condition`：`baseline_workflow / process_guided_workflow`
- `session_stage`：`internal_dry_run / formal_pilot`
- `scorer_id`：

## 2. 评分项

### completion_status
- `0` = 未完成核心任务
- `1` = 完成了一部分，但关键接口 / 关键修补未闭合
- `2` = 完成了本次试用要求的核心任务

### runnable
- `0` = 不能运行或关键步骤无法执行
- `1` = 能运行或能完成关键修补验证

### outcome_quality
- `0` = 结果明显不满足任务要求
- `1` = 结果部分满足，但仍缺关键正确性或回归通过
- `2` = 结果满足本次任务要求

### self_check_coverage
- `0` = 没有显式自检
- `1` = 口头提到要检查，但没有落实成明确检查动作
- `2` = 有明确的检查点、断言、回归或验证步骤

### root_cause_explanation
- `0` = 没有解释，或解释与问题不对应
- `1` = 提到了一部分原因，但不够清楚或不够最小
- `2` = 能清楚说明关键原因，并与修补动作对应
- 若任务不适用，可填 `NA`

### regression_plan_quality
- `0` = 没有回归计划
- `1` = 提到“需要再测”，但没有明确测什么
- `2` = 明确写出至少一个回归检查点或验证样例

### artifact_completeness
- `0` = 核心产物缺失
- `1` = 有部分产物，但记录不完整
- `2` = 代码 / 说明 / 记录三者基本齐全

## 3. 汇总表

| 字段 | 分值 |
|---|---|
| completion_status |  |
| runnable |  |
| outcome_quality |  |
| self_check_coverage |  |
| root_cause_explanation |  |
| regression_plan_quality |  |
| artifact_completeness |  |

总评备注：
- 本次最明显的优点：
- 本次最明显的缺口：
- 是否更像 `baseline_workflow` 或 `process_guided_workflow` 的典型表现：
