# a2 expanded scope perf codebook v0

适用范围：
- `metrics/a2_expanded_scope_perf_v0.csv`

目标：
- 记录 expanded-scope case 级别的恢复表现。

## 字段定义

### run_id
- 格式：`YYYY-MM-DD_run_xxx`

### image_name
- 当前固定为：
  - `lena`
  - `barbara`
  - `peppers`
  - `cameraman`

### corruption_mode
- 当前固定为：
  - `random_pixel`
  - `center_block`
  - `text`

### corruption_ratio
- 允许值：
  - `0.3`
  - `0.35`
  - `0.7`

### mode
- 这里固定解释为 guidance mode：
  - `direct_answer`
  - `plain_guidance`
  - `coe_guided`

### psnr / ssim / rse
- 固定用 `hw2-op2/src/utils.py::compute_metrics` 口径

### runtime_s
- 单个 expanded case 从输入到恢复输出的总耗时（秒）

### output_ok
- `0` = 输出缺失、shape 不对、含明显无效值，或结果不可检查
- `1` = 输出完整、可检查

### notes
- 记录图像来源与协议偏离
