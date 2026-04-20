# Internal Dry Run Findings

## 基本结论
- 这次 `internal_dry_run` 已经把 `participant_form -> notes -> patch -> scoring_sheet -> CSV` 整条链路跑通。
- 选用任务：`T2_A1_bug_01`
- 条件：`process_guided_workflow`
- session：`PILOT_20260420_000`

## 过程结果
- 参与者阶段未读取 scorer-only 的 `diagnosis.md` / `fixed_code.py`。
- 提交的 diagnosis 与 scorer-only 参考结论一致。
- patched code 与 scorer-only `fixed_code.py` 在最小矩阵回归上结果一致。
- 评分与 CSV 回填都能在一次 session 内完成，不需要额外再造字段。

## 真正别扭的地方
- 第一次填写时发现 `pilot_bug_repair_notes_template_v0.md` 缺 `session_id`。
  如果同时回收多份 notes，只靠文件名对齐不够稳。
- 第一次填写时发现 `pilot_bug_repair_notes_template_v0.md` 缺“最终提交代码路径 / 文件名”。
  参与者 notes 能解释思路，但不能独立指向最终 patch，研究者回填时还得再翻 session record。
- 第一次填写时发现 `pilot_participant_form_v0.md` 缺显式的前测 / 后测填写时机提示。
  真跑时如果直接整张表一起发给参与者，容易有人把后测部分提前扫一遍。

## 本次已落地的修改
1. notes template 已补 `session_id`。
2. notes template 已补“最终提交代码路径 / 文件名”。
3. participant form 已补填写时机提示。

## 本次验证输出
- `verification=pass`
- `dp`：
  `[[3., 1., 4., 2.], [3., 6., 2., 5.], [9., 4., 4., 3.]]`
- `backtrack`：
  `[[0, 0, 0, 0], [1, 1, 1, 3], [0, 2, 2, 2]]`
