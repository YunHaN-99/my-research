# a2 recovery perf codebook v0

适用范围：
- `metrics/a2_recovery_perf_v0.csv`

目标：
- 分离“guidance 质量”和“A2 固定 case 的恢复性能”。

## 字段定义

### run_id
- 格式：`YYYY-MM-DD_run_xxx`

### image_name
- 固定为：`lena / barbara`

### corruption_mode
- 固定为：`random_pixel / text`

### corruption_ratio
- 当前固定为：`0.5`

### mode
- 这里固定解释为 guidance mode，只允许：
  - `direct_answer`
  - `plain_guidance`
  - `coe_guided`

### psnr / ssim / rse
- 固定用 `hw2-op2/src/utils.py::compute_metrics` 口径

### runtime_s
- 该 fixed case 从输入到恢复输出的总耗时（秒）

### output_ok
- `0` = 输出缺失、shape 不对、mask 约束明显失效，或结果明显坏图
- `1` = 输出完整、可检查，且结果不是明显坏图

### notes
- 记录异常、协议偏离、特殊说明

## 填表规则
- 每个 run 固定写 4 行：
  - `lena / random_pixel@0.5`
  - `lena / text@0.5`
  - `barbara / random_pixel@0.5`
  - `barbara / text@0.5`
- 若偏离 `report/a2_eval_protocol_v0.md`，必须在 notes 写明。
