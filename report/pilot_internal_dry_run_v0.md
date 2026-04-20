# Pilot Internal Dry Run v0

## 目的
在正式首轮 `4` 人小样本之前，先用自己或 `1` 位熟悉 Python 的同学完整走一遍 `participant_form -> session_record -> scoring_sheet -> CSV` 回填链路，优先暴露模板字段、评分口径和操作顺序上的问题。

## 当前定位
- 这一步不是正式招募，不计入首轮 `4` 人样本。
- 这一步的目标不是得出教学结论，而是检查模板链路是否够用。
- 正式首轮仍然固定为：`T2_A1_bug_01` 和 `T3_A2_bug_01`，在 `baseline_workflow / process_guided_workflow` 下各 `1` 次。

## 建议执行方式
- 执行者：自己，或 `1` 位熟悉 Python 的同学。
- 推荐任务：先选 `T2_A1_bug_01` 或 `T3_A2_bug_01` 之一。
- 推荐条件：优先先走 `process_guided_workflow`，因为它涉及的材料更多，更容易提前暴露字段缺口。
- `session_stage` 统一记为：`internal_dry_run`。
- 若走 `process_guided_workflow`，同步发放：
  - `pilot/pilot_bug_repair_checklist_v0.md`
  - `pilot/pilot_bug_repair_notes_template_v0.md`

## 必走链路
1. 填写 [pilot_participant_form_v0.md](C:/Users/ydyz0/Desktop/AIforResearch/pilot/pilot_participant_form_v0.md) 的基本信息、背景项和主观评价。
2. 用 [pilot_session_record_template_v0.md](C:/Users/ydyz0/Desktop/AIforResearch/pilot/pilot_session_record_template_v0.md) 记录发放材料、过程观察、求助和产物位置。
3. 用 [pilot_scoring_sheet_v0.md](C:/Users/ydyz0/Desktop/AIforResearch/pilot/pilot_scoring_sheet_v0.md) 按统一口径打分。
4. 把上述信息回填到 [pilot_session_log_template_v0.csv](C:/Users/ydyz0/Desktop/AIforResearch/metrics/pilot_session_log_template_v0.csv)。
5. 对照 [pilot_session_log_codebook_v0.md](C:/Users/ydyz0/Desktop/AIforResearch/metrics/pilot_session_log_codebook_v0.md) 检查字段定义是否能支撑无歧义回填。

## 必查问题
- 是否存在必须记录但当前没有字段承接的信息。
- 是否存在重复评分项，导致同一信息要在两个模板里重复判断。
- 研究者是否能不反复翻文档就完成 CSV 回填。
- `notes` 和 `artifact_paths` 是否足够承接开放问题与附件路径。
- `internal_dry_run / formal_pilot` 的区分是否清楚。
- 任务说明、过程记录和评分动作的顺序是否自然。

## 通过标准
- 不新增必须字段也能完整回填一条 CSV。
- 评分项只在评分表中做一次正式判断，不在其他模板里重复打分。
- 研究者能在 session 结束后较快完成回填。
- 任何不适用项都能明确写成 `NA`，而不是留空。
- 若发现问题，能够直接落成模板修改项，而不是停留在口头提醒。

## 输出物
- `1` 份填写后的 participant form
- `1` 份填写后的 session record
- `1` 份填写后的 scoring sheet
- `1` 行测试用 CSV
- `1` 份 dry run 发现与修改记录

## 最近一次执行
- 已于 `2026-04-20` 完成 `1` 次实际 dry run：
  - `session_id`：`PILOT_20260420_000`
  - `task_id`：`T2_A1_bug_01`
  - `condition`：`process_guided_workflow`
- 汇总结果见：`report/pilot_internal_dry_run_result_2026-04-20.md`
- 记录包见：`pilot/dry_run_records/PILOT_20260420_000/`
- CSV 记录见：`metrics/pilot_session_log_dry_run_v0.csv`
- 本次 dry run 暴露并已修复的模板问题：
  - notes template 补上了 `session_id`
  - notes template 补上了“最终提交代码路径 / 文件名”
  - participant form 补上了前测 / 后测填写时机提示

## 若暴露问题，优先处理顺序
1. 先修字段缺失和重复评分。
2. 再修填写顺序和命名歧义。
3. 最后再考虑是否需要扩展更多开放问题或额外统计项。
