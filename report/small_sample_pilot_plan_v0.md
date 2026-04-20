# Small Sample Pilot Plan v0

## 目的
把 Timeline 后续要做的“小范围试用”先冻结成一套可执行的 `v0` 方案，重点不是马上开始招募，而是先把试用问题、任务池、表单、评分表、记录模板和数据结构定下来。

## 1. 当前定位
- 当前还没有开始实际招募、正式试用和数据采集。
- 这份文档的作用是先把“baseline vs 过程化流程”的试用方案定住。
- 首轮正式试用的顺序已经收束为“先 bug-repair，后 implementation”。
- 在正式首轮之前，先做 `1` 次内部 dry run，验证表单、评分表、session record 和 CSV 回填链路是否顺手。
- 中期阶段最稳的说法应是：
  - 小样本试用方案已定，表单、评分表、记录模板和 CSV 数据结构已预埋；实际招募与数据采集放到中期后执行。

## 2. 试用要回答什么
当前小样本试用不追求证明“过程化流程显著提高最终算法指标”，而是优先观察下面这些更贴近当前证据的结果：

1. 相比 `baseline workflow`，`process-guided workflow` 是否更容易让参与者留下可复查的过程痕迹。
2. 过程化流程是否提升自检覆盖、关键说明质量和回归说明质量。
3. 在小样本教学场景中，参与者是否主观感到过程化流程更清楚、更可复用。

## 3. 两个对照条件

### baseline_workflow
- 给任务说明、输入输出和最小完成目标。
- 不额外提供结构化 task card、检查清单、过程模板。
- 允许参与者自由组织自己的解题过程。

### process_guided_workflow
- 给任务说明、task card 摘要、最小检查清单、过程记录模板。
- 强调“先结构化表示，再做实现 / 修补，再写自检和回归说明”。
- 不强制使用 GUI 或复杂工具，仍以当前 CLI / 文档工作流为主。
- 当前 participant-facing 材料固定为：
  - `pilot/pilot_bug_repair_checklist_v0.md`
  - `pilot/pilot_bug_repair_notes_template_v0.md`

## 4. 试用对象与首轮样本规模
- `v0` 首轮目标样本：`4` 人。
- 首轮固定覆盖 `2` 个 bug-repair 任务在 `2` 个条件下的 `4` 个 session。
- 若首轮顺利，再考虑扩到 `6+` 人，并把 `T1_A1_width` 作为下一轮补充任务。
- 候选对象：
  - 具备基础 Python 能力的同学 / 同行
  - 对 numpy、图像处理或算法课题有入门理解
  - 未深度参与本仓库当前实验链路的人
- 当前不做大规模招募，只做 feasibility-style 的小样本试用。

## 5. 冻结的任务池
为了避免试用时临时挑题，当前先冻结一组 bounded task pool：

| task_id | 来源 | 任务类型 | 试用定位 | 主要依据 |
|---|---|---|---|---|
| `T1_A1_width` | A1 width shrink | implementation | 看参与者能否把输入 / 输出 /检查点组织清楚 | `task_cards/A1_seam_carving_taskcard_v1.md` |
| `T2_A1_bug_01` | `bug_01_dp_boundary` | bug_repair | 看根因定位、自检和回归说明是否清楚 | `task_cards/A1_bug_repair_taskcard_v0.md` |
| `T3_A2_bug_01` | `bug_01_missing_mask_constraint` | bug_repair | 看过程化流程是否更利于解释语义约束和回归 | `task_cards/A2_bug_repair_taskcard_v0.md` |

说明：
- `v0` 首轮更推荐优先跑 `T2_A1_bug_01` 和 `T3_A2_bug_01`，因为它们更贴近当前最强研究结论。
- 若试用节奏顺利，再把 `T1_A1_width` 纳入同一轮或下一轮小样本补充。

## 6. 首轮分配方式
当前推荐最省力、也最贴合当前研究结论的做法是：

1. 以 `task_id x condition` 为最小试用单元。
2. 首轮固定为 `4` 个 session：
   - `T2_A1_bug_01` + `baseline_workflow`
   - `T2_A1_bug_01` + `process_guided_workflow`
   - `T3_A2_bug_01` + `baseline_workflow`
   - `T3_A2_bug_01` + `process_guided_workflow`
3. `T1_A1_width` 不进入首轮；只在首轮顺利后作为第二轮补充。

## 7. 正式首轮前的内部 dry run
- 内部 dry run 不算正式招募，不计入首轮 `4` 人样本。
- 执行者可为自己，或 `1` 位熟悉 Python 的同学。
- 建议先选 `T2_A1_bug_01` 或 `T3_A2_bug_01` 之一，完整走一遍记录链路。
- 必须走完的链路：
  - `pilot/pilot_participant_form_v0.md`
  - `pilot/pilot_session_record_template_v0.md`
  - `pilot/pilot_scoring_sheet_v0.md`
  - `metrics/pilot_session_log_template_v0.csv`
- 本次 dry run 重点检查：
  - 字段是否够用
  - 是否存在重复评分项
  - 哪些步骤最难操作
  - 回填 CSV 时是否需要反复翻原始记录
  - `internal_dry_run / formal_pilot` 的区分是否清楚

## 8. 单次试用流程
每次 session 建议控制在 `35` 到 `50` 分钟内：

1. `5` 分钟：填写参与者表单中的基本信息与背景项。
2. `3` 分钟：发放任务包，说明当前条件是 `baseline_workflow` 还是 `process_guided_workflow`。
3. `20` 到 `30` 分钟：完成任务。
4. `5` 分钟：填写试用后主观评价。
5. `5` 分钟：研究者补评分表和 session record。

## 9. 记录哪些数据

### 客观记录
- `completion_status`
- `runnable`
- `outcome_quality`
- `self_check_coverage`
- `root_cause_explanation`
- `regression_plan_quality`
- `artifact_completeness`
- `time_to_first_working_min`
- `total_session_min`
- `help_request_count`

### 主观记录
- `task_clarity_rating`
- `process_clarity_rating`
- `confidence_rating`
- `cognitive_load_rating`
- `reuse_intent_rating`
- `notes`

## 10. 当前已经落地的试用材料
- 方案文档：`report/small_sample_pilot_plan_v0.md`
- 内部 dry run 说明：`report/pilot_internal_dry_run_v0.md`
- 首轮排班表：`report/pilot_round1_schedule_v0.md`
- 首轮任务包清单：`report/pilot_round1_task_pack_checklist_v0.md`
- 参与者表单：`pilot/pilot_participant_form_v0.md`
- process-guided checklist：`pilot/pilot_bug_repair_checklist_v0.md`
- process-guided notes template：`pilot/pilot_bug_repair_notes_template_v0.md`
- 评分表：`pilot/pilot_scoring_sheet_v0.md`
- 记录模板：`pilot/pilot_session_record_template_v0.md`
- CSV 数据骨架：`metrics/pilot_session_log_template_v0.csv`
- CSV codebook：`metrics/pilot_session_log_codebook_v0.md`

## 11. 中期推荐写法
建议中期材料写成：

> Timeline 后续要求的小样本试用目前尚未开始实际招募，但 baseline vs 过程化流程的 `v0` 试用方案已经冻结，任务池、参与者表单、评分表、记录模板与 CSV 数据结构均已预埋，因此中期之后可以直接进入小范围试用执行。

## 12. 下一步最小动作
1. 正式首轮前先做 `1` 次内部 dry run，完整走通 `participant_form -> session_record -> scoring_sheet -> CSV`。
2. 中期后先用 `T2_A1_bug_01` 和 `T3_A2_bug_01` 跑首轮 `4` 人试用。
3. 试用结束后先回填 `metrics/pilot_session_log_template_v0.csv` 的正式版本，并记录模板是否还需微调。
4. 若首轮可行，再补 `T1_A1_width` 并完善对照说明。
