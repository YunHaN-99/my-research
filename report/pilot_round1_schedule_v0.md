# Pilot Round 1 Schedule v0

## 目的
把内部 dry run 和首轮 `4` 人 bug-repair pilot 固定成一张可直接执行的排班表，避免正式开始前还在临时决定任务、条件和顺序。

## 固定原则
- `internal_dry_run` 不计入首轮正式样本。
- 首轮正式样本固定为 `4` 个 session，不纳入 `T1_A1_width`。
- 每位参与者只跑 `1` 个 session，避免学习效应污染条件对照。
- 同一轮尽量由同一位研究者负责发放、记录和评分口径说明。

## 建议 session 顺序

| slot | 建议 session_id | session_stage | task_id | condition | participant_id | 日期 | 时间 | 备注 |
|---|---|---|---|---|---|---|---|---|
| DRY-01 | `PILOT_20260420_000` | `internal_dry_run` | `T2_A1_bug_01` | `process_guided_workflow` | `SELF` | `2026-04-20` | `14:05-14:22` | 已完成；记录见 `report/pilot_internal_dry_run_result_2026-04-20.md` |
| S01 | `PILOT_YYYYMMDD_001` | `formal_pilot` | `T2_A1_bug_01` | `baseline_workflow` | `P01` | 待填 | 待填 | A1 bug_01 的 baseline 对照 |
| S02 | `PILOT_YYYYMMDD_002` | `formal_pilot` | `T2_A1_bug_01` | `process_guided_workflow` | `P02` | 待填 | 待填 | A1 bug_01 的 process-guided 对照 |
| S03 | `PILOT_YYYYMMDD_003` | `formal_pilot` | `T3_A2_bug_01` | `baseline_workflow` | `P03` | 待填 | 待填 | A2 bug_01 的 baseline 对照 |
| S04 | `PILOT_YYYYMMDD_004` | `formal_pilot` | `T3_A2_bug_01` | `process_guided_workflow` | `P04` | 待填 | 待填 | A2 bug_01 的 process-guided 对照 |

补充说明：
- 当前已冻结的是 `S01` 到 `S04` 的任务顺序、条件分配和 task pack。
- `session_id`、日期、时间仍待按真实招募结果回填，不在仓库里虚填。
- 四个 formal pilot 的独立 task pack 已预建在 `pilot/formal_pilot_task_packs/`。

## 每个 session 的时间预算
- `5` 分钟：填写 participant form 的基本信息和背景项
- `3` 分钟：发放任务包并说明条件
- `20` 到 `30` 分钟：完成修补任务
- `5` 分钟：填写试用后主观评价
- `5` 分钟：研究者补 session record、scoring sheet 和 CSV 草稿

## 执行前检查
- dry run 已完成，记录见 `report/pilot_internal_dry_run_result_2026-04-20.md`
- `session_stage` 已按 `internal_dry_run / formal_pilot` 区分
- 每个 session 的任务包已预建在 `pilot/formal_pilot_task_packs/`；若线下发放，再按 session 目录直接打包
- 不向参与者暴露 `diagnosis.md`、`fixed_code.py` 和既有 generated answers

## 首轮完成标准
- `S01` 到 `S04` 四个 session 全部完成
- 每个 session 都有 participant form、session record、scoring sheet
- CSV 至少已有 `4` 行 `formal_pilot` 记录
- 若首轮结束仍发现字段缺口，先修模板，再决定是否开启下一轮
