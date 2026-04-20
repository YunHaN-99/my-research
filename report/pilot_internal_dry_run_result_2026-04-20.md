# Pilot Internal Dry Run Result 2026-04-20

## 基本信息
- 日期：`2026-04-20`
- `session_id`：`PILOT_20260420_000`
- `participant_id`：`SELF`
- `task_id`：`T2_A1_bug_01`
- `condition`：`process_guided_workflow`
- `session_stage`：`internal_dry_run`

## 本次做了什么
- 按参与者视角填写了 participant form。
- 用 `symptom.md + buggy_code.py + task cards + checklist + notes template` 完成了一次 bug repair。
- 产出了 notes、diagnosis、patched code 和最小回归说明。
- 再按研究者视角补了 session record、scoring sheet 和 CSV 回填。
- 最后用 `llmft` 环境对 patched code 与 scorer-only `fixed_code.py` 做了最小一致性验证。

## 结论
- dry run 已经把 `participant_form -> notes -> patch -> scoring_sheet -> CSV` 链路完整跑通。
- 这次没有暴露必须新增到 CSV 的核心字段缺口。
- 真正别扭的地方主要在模板操作性，不在评分口径本身。

## 本次确认并已落地的模板修补
1. `pilot/pilot_bug_repair_notes_template_v0.md` 增加了 `session_id`。
2. `pilot/pilot_bug_repair_notes_template_v0.md` 增加了“最终提交代码路径 / 文件名”。
3. `pilot/pilot_participant_form_v0.md` 增加了前测 / 后测填写时机提示。

## 产物位置
- participant form：
  `pilot/dry_run_records/PILOT_20260420_000/participant_form_filled.md`
- participant notes：
  `pilot/dry_run_records/PILOT_20260420_000/participant_notes_filled.md`
- participant submission：
  `pilot/dry_run_records/PILOT_20260420_000/participant_submission.md`
- patched code：
  `pilot/dry_run_records/PILOT_20260420_000/src/patched_code.py`
- verification script：
  `pilot/dry_run_records/PILOT_20260420_000/src/verify_patch.py`
- session record：
  `pilot/dry_run_records/PILOT_20260420_000/session_record_filled.md`
- scoring sheet：
  `pilot/dry_run_records/PILOT_20260420_000/scoring_sheet_filled.md`
- dry run findings：
  `pilot/dry_run_records/PILOT_20260420_000/dry_run_findings.md`
- CSV：
  `metrics/pilot_session_log_dry_run_v0.csv`

## 下一步
1. 用修过的模板准备首轮 `4` 人 formal pilot 的任务包。
2. 正式样本仍按 `T2_A1_bug_01 / T3_A2_bug_01` 在 `baseline_workflow / process_guided_workflow` 下各跑 `1` 次。
3. formal pilot 开始后，把每个 session 继续按同样目录结构落成记录包，避免回头补写。
