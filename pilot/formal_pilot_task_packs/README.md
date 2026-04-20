# Formal Pilot Task Packs

## 目的
把首轮 `4` 个 formal pilot session 的 participant-visible 材料和 researcher-only 材料提前拆成独立文件夹，避免正式执行时临时拣文件、混发 scorer-only 材料。

## 当前状态
- 已预建 `S01` 到 `S04` 四个独立 task pack 文件夹。
- 已额外整理出可直接发放给参与者的简化目录：
  - `S01/`
  - `S02/`
  - `S03/`
  - `S04/`
- 每个 task pack 都拆成：
  - `participant_pack/`
  - `researcher_pack/`
  - `records/`
- 当前已冻结的是任务顺序和 task pack。
- `session_id`、日期、时间仍待按真实招募结果回填，不在仓库里虚填。

## 目录说明
- `S01/` 到 `S04/`
  - 这是“直接发给参与者”的简化目录。
  - 里面只保留 participant-visible 文件，不含 researcher-only 材料。
- `S01_T2_A1_bug_01_baseline_workflow/`
  - 对应 `P01`
  - 任务：`T2_A1_bug_01`
  - 条件：`baseline_workflow`
- `S02_T2_A1_bug_01_process_guided_workflow/`
  - 对应 `P02`
  - 任务：`T2_A1_bug_01`
  - 条件：`process_guided_workflow`
- `S03_T3_A2_bug_01_baseline_workflow/`
  - 对应 `P03`
  - 任务：`T3_A2_bug_01`
  - 条件：`baseline_workflow`
- `S04_T3_A2_bug_01_process_guided_workflow/`
  - 对应 `P04`
  - 任务：`T3_A2_bug_01`
  - 条件：`process_guided_workflow`

## 使用方式
- 若你只想直接发材料给参与者，就发 `S01/` 到 `S04/` 这四个简化目录。
- 若你还要同时保留研究者侧材料与回收目录，就继续使用长名字目录下的 `participant_pack/`、`researcher_pack/` 和 `records/`。
- `researcher_pack/` 只留给研究者，不向参与者发放。
- 执行结束后，把回收表单、代码、评分和验证产物放回对应 `records/`。
- 若线下执行需要压缩包，可直接按 session 目录打包，不再临时拼材料。

## 严禁混入 participant pack 的材料
- `diagnosis.md`
- `fixed_code.py`
- 既有 `patched_code.py`
- `prompt_used.md`
- `model_raw_response.md`
