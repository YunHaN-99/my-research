# a2 guidance eval codebook v0

适用范围：
- `metrics/a2_guidance_eval_v0.csv`
- 后续 A2 direct / plain / coe guidance 对照实验

目标：
- 固定字段取值，避免不同 run 使用不一致口径。

## 字段定义与取值

### run_id
- 格式：`YYYY-MM-DD_run_xxx`

### case_id
- 当前固定为：`A2`

### mode
- 允许值：`direct_answer / plain_guidance / coe_guided`

### prompt_file
- 对应提示文件路径

### task_card_version
- 允许值：`none / v1`
- direct_answer 通常为 `none`，plain_guidance 与 coe_guided 通常为 `v1`

### artifact_complete
- `0` = 核心产物不全
- `1` = 有代码，但 fixed case 输出图或 run 记录缺项
- `2` = 代码、4 个 fixed case 输出、run 记录、metrics 都齐

### runnable
- `0` = 不能跑
- `1` = 能跑

### correct
- `0` = 不满足 A2 主接口或固定协议
- `1` = 主接口能跑，但 fixed protocol 结果不完整或明显错误
- `2` = 固定 4 个 case 全部完成，输出与 metrics 可检查

### self_check
- `0` = 无
- `1` = 口头提到检查
- `2` = 有明确断言或验证步骤

### error_type
- 允许值：
  - `mask_constraint`
  - `patch_search`
  - `patch_aggregation`
  - `history_logging`
  - `dtype_range`
  - `other`
  - `none`

### fix_rounds
- 非负整数

### time_to_first_working_min
- 单位：分钟
- 若未跑通，填 `NA`

### notes
- 简短备注：
  - 触发条件
  - 关键修复动作
  - 与协议偏差

## 填表规则
- 先在 runs 文档记录事实，再回填 CSV。
- 同一 run 只保留一行主记录。
- 若偏离 `report/a2_eval_protocol_v0.md`，必须在 notes 明确写出原因。
