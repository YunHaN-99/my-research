# Pilot Session Record Template v0

## 1. Session 信息
- `session_id`：`PILOT_20260420_000`
- 日期：`2026-04-20`
- `participant_id`：`SELF`
- `task_id`：`T2_A1_bug_01`
- `condition`：`process_guided_workflow`
- `session_stage`：`internal_dry_run`
- 研究者 / 记录者：`SELF`

## 2. 发放材料
- 任务说明：
  `solutions/hw1_op1/failure_cases/bug_01_dp_boundary/symptom.md`
- 提供的文件：
  - `solutions/hw1_op1/failure_cases/bug_01_dp_boundary/buggy_code.py`
  - `pilot/pilot_participant_form_v0.md`
- 若为 `process_guided_workflow`，额外提供：
  - `task_cards/A1_seam_carving_taskcard_v1.md`
  - `task_cards/A1_bug_repair_taskcard_v0.md`
  - `pilot/pilot_bug_repair_checklist_v0.md`
  - `pilot/pilot_bug_repair_notes_template_v0.md`

## 3. 时间记录
- 开始时间：`14:05`
- 首次出现可运行结果时间：`14:13`
- 结束时间：`14:22`
- 总时长（分钟）：`17`

## 4. 过程观察
- 参与者是否先做输入 / 输出澄清：
  是，先把 symptom 重述成“边界列非法父节点被纳入 DP 转移”。
- 是否出现显式自检：
  是，在 notes 里明确写了边界列不越界和 `backtrack` 范围检查。
- 是否主动解释关键原因或关键步骤：
  是，解释了为什么 `j=0` 的负索引和 `j=w-1` 的越界都来自同一个根因。
- 是否写出回归或验证动作：
  是，给了一个 `3x4` 小矩阵验证，并与 `fixed_code.py` 做了一次 scorer-side 对照。
- 求助次数：
  `0`
- 研究者介入说明：
  无。内部 dry run 由同一人完成，但参与者阶段没有读取 scorer-only 参考答案。

## 5. 产物位置
- 代码路径：
  - `pilot/dry_run_records/PILOT_20260420_000/src/patched_code.py`
  - `pilot/dry_run_records/PILOT_20260420_000/src/verify_patch.py`
- 截图 / 输出路径：
  无截图；命令行验证输出已记录在 `dry_run_findings.md`
- run 记录路径：
  - `pilot/dry_run_records/PILOT_20260420_000/participant_submission.md`
  - `pilot/dry_run_records/PILOT_20260420_000/participant_notes_filled.md`
- 其他附件：
  - `pilot/dry_run_records/PILOT_20260420_000/participant_form_filled.md`
  - `pilot/dry_run_records/PILOT_20260420_000/scoring_sheet_filled.md`
  - `pilot/dry_run_records/PILOT_20260420_000/dry_run_findings.md`

## 6. 回填摘要
- `scoring_sheet_path`：
  `pilot/dry_run_records/PILOT_20260420_000/scoring_sheet_filled.md`
- `csv_backfill_status`：`completed`
- `artifact_paths_checked`：`yes`
- 若本次为 `internal_dry_run`，记录本轮暴露出来的问题：
  - 字段是否缺失：
    `pilot_bug_repair_notes_template_v0.md` 缺 `session_id`，实际回收时只能靠文件名或人工补记来对齐。
  - 是否存在重复评分项：
    没有硬性重复打分，但 participant notes 与 session record 都会写“回归检查”，需要靠 scorer 约定只在 scoring sheet 里正式打分。
  - 哪个步骤最难操作：
    从 participant notes 平滑回填到 CSV 最别扭，因为 notes 里没有 artifact path，session record 又要再记一次。
  - 对模板的修改建议：
    给 notes template 增加 `session_id` 和“最终提交代码路径 / 文件名”；给 participant form 增加“前半场 / 后半场”的填写提示。

## 7. 研究者备注
- 本次 session 最值得保留的观察：
  对 bug-repair 小题，`checklist + notes template` 能明显把参与者思路约束在“不变量 + 最小修补”上。
- 本次 session 最值得改进的地方：
  记录链路已经能跑通，但 notes template 和 participant form 仍有两处操作提示不足，第一次真实回收材料时会让人停下来想“这张表现在该谁填到哪一步”。
- 若下一轮继续跑，应调整什么：
  先修模板字段，再按同一目录结构继续累积 `formal_pilot` 的 session 包，避免 dry run 和正式样本混写。
