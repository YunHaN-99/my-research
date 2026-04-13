# a2 failure repair eval codebook v0

适用范围：
- `metrics/a2_failure_repair_eval_v0.csv`

目标：
- 固定 A2 bug-repair benchmark 的评分字段与填表口径。

## 字段定义

### run_id
- 格式：`YYYY-MM-DD_run_xxx`

### bug_id
- 当前固定为：
  - `bug_01_missing_mask_constraint`
  - `bug_02_mask_polarity_inverted`
  - `bug_03_sparse_component_written_back`

### mode
- 允许值：
  - `direct_answer`
  - `plain_guidance`
  - `coe_guided`

### diagnosis_correct
- `1` = 命中根因
- `0` = 只描述表象，或定位偏题

### patch_runnable
- `1` = patch 可替换、无显式语法错误、接口契约保持一致
- `0` = patch 本身不可用，或破坏接口

### regression_pass
- `1` = 原主错误消失，且该 bug 的关键不变量恢复
- `0` = 原问题仍在，或引入新的关键回归

### fix_rounds
- 非负整数

### time_to_fix_min
- 单位：分钟
- 若未修到可用版本，填 `NA`
- 本字段默认是 rough same-session wall-clock，不建议做强 timing 结论

### notes
- 记录：
  - 首轮表现
  - 关键修复动作
  - 与协议的偏离
  - 特殊评分说明

## 填表规则
- 先在对应 run 文档中记录事实，再回填 CSV。
- 每个 bug x mode 只保留 1 行最终记录。
- 若偏离 `report/a2_bug_repair_protocol_v0.md`，必须在 `notes` 中写明。
