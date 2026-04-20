# Pilot Bug Repair Notes Template v0

## 目的
给 `process_guided_workflow` 条件下的参与者一张简短记录纸，用来留下最基本的过程痕迹，便于后续评分和 CSV 回填。

## 基本信息
- `session_id`：
- `participant_id`：
- `task_id`：
- `condition`：`process_guided_workflow`

## 1. Symptom 重述
- 当前看到的问题是：
- 理想行为应该是：

## 2. 关键不变量
- 我认为最关键的不变量是：
- 当前哪里破坏了这个不变量：

## 3. 最小修补计划
- 我准备修改的代码位置：
- 我为什么认为这是根因：
- 我不会去改的部分：

## 4. 自检与回归
- 提交前我会检查：
- 最小回归说明：

## 5. 结果备注
- 当前 patch 是否已能运行：
- 最终提交代码路径 / 文件名：
- 仍不确定的地方：
