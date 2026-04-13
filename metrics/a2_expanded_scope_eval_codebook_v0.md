# a2 expanded scope eval codebook v0

适用范围：
- `metrics/a2_expanded_scope_eval_v0.csv`

目标：
- 固定 expanded-scope run 级别的记录口径。

## 字段定义

### run_id
- 格式：`YYYY-MM-DD_run_xxx`

### mode
- 允许值：
  - `direct_answer`
  - `plain_guidance`
  - `coe_guided`

### source_artifact_run_id
- 本轮 expanded-scope 复用的 baseline 生成代码来源：
  - `2026-04-12_run_030`
  - `2026-04-12_run_031`
  - `2026-04-12_run_032`

### scope_id
- 当前固定为：`a2_expanded_scope_v0`

### image_count
- 当前固定为：`4`

### case_count
- 当前固定为：`16`

### artifact_complete
- `0` = 关键产物缺失
- `1` = 有部分输出，但 run 文档或 metrics 不完整
- `2` = 输出、run 文档与 metrics 全齐

### runnable
- `0` = run 中断或核心输出缺失
- `1` = run 完整执行

### output_ok_count
- 通过最小完整性检查的 case 数量

### notes
- 记录协议边界、复用来源与异常说明
