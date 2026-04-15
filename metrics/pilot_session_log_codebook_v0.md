# pilot session log codebook v0

适用范围：
- `metrics/pilot_session_log_template_v0.csv`
- 后续小样本试用的 session 级结构化记录

目标：
- 先把 baseline vs 过程化流程的小样本试用数据结构固定下来，避免首轮试用后再倒推字段。

## 字段定义与取值

### session_id
- 建议格式：`PILOT_YYYYMMDD_001`

### date
- 建议格式：`YYYY-MM-DD`

### participant_id
- 匿名编号，例如：`P01`

### task_id
- 当前冻结任务池：
  - `T1_A1_width`
  - `T2_A1_bug_01`
  - `T3_A2_bug_01`

### condition
- 允许值：
  - `baseline_workflow`
  - `process_guided_workflow`

### task_type
- 允许值：
  - `implementation`
  - `bug_repair`

### scorer_id
- 评分者或记录者编号

### python_bg / numpy_bg / debugging_bg / image_task_bg
- `1` 到 `5`
- `1` = 非常不熟悉
- `5` = 非常熟悉

### prior_similar_task
- `0` = 没做过类似任务
- `1` = 做过相近任务

### prior_repo_exposure
- `0` = 未提前看过本仓库材料
- `1` = 提前看过

### completion_status
- `0 / 1 / 2`
- 含义见：`pilot/pilot_scoring_sheet_v0.md`

### runnable
- `0 / 1`

### outcome_quality
- `0 / 1 / 2`

### self_check_coverage
- `0 / 1 / 2`

### root_cause_explanation
- `0 / 1 / 2 / NA`
- 对 implementation 任务若不适用，可填 `NA`

### regression_plan_quality
- `0 / 1 / 2`

### artifact_completeness
- `0 / 1 / 2`

### time_to_first_working_min
- 单位：分钟
- 若无可运行结果，可填 `NA`

### total_session_min
- 单位：分钟

### help_request_count
- 非负整数

### task_clarity_rating / process_clarity_rating / confidence_rating / cognitive_load_rating / reuse_intent_rating
- `1` 到 `5`
- `cognitive_load_rating` 取值越高表示主观负担越重

### notes
- 简短补充说明：
  - 卡点
  - 研究者介入
  - 特殊情况

### artifact_paths
- 记录代码、截图、run 文档等相对路径

## 填表规则
- 先保留原始表单和 session record，再回填 CSV。
- 同一 session 只保留一行主记录。
- 如果某个评分项不适用，不要留空，统一填 `NA`。
