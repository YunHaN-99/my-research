# A2 bug-repair queue v0

固定执行顺序（planned 9）：
1. bug_01_missing_mask_constraint / direct_answer
2. bug_01_missing_mask_constraint / plain_guidance
3. bug_01_missing_mask_constraint / coe_guided
4. bug_02_mask_polarity_inverted / direct_answer
5. bug_02_mask_polarity_inverted / plain_guidance
6. bug_02_mask_polarity_inverted / coe_guided
7. bug_03_sparse_component_written_back / direct_answer
8. bug_03_sparse_component_written_back / plain_guidance
9. bug_03_sparse_component_written_back / coe_guided

状态：
- completed:
  - 2026-04-12_run_043 / bug_01_missing_mask_constraint / direct_answer
  - 2026-04-12_run_044 / bug_01_missing_mask_constraint / plain_guidance
  - 2026-04-12_run_045 / bug_01_missing_mask_constraint / coe_guided
  - 2026-04-12_run_046 / bug_02_mask_polarity_inverted / direct_answer
  - 2026-04-12_run_047 / bug_02_mask_polarity_inverted / plain_guidance
  - 2026-04-12_run_048 / bug_02_mask_polarity_inverted / coe_guided
  - 2026-04-12_run_049 / bug_03_sparse_component_written_back / direct_answer
  - 2026-04-12_run_050 / bug_03_sparse_component_written_back / plain_guidance
  - 2026-04-12_run_051 / bug_03_sparse_component_written_back / coe_guided
- remaining: none

执行纪律：
- 只变 guidance mode，不变 bug 材料。
- 同一 bug 的 `symptom.md` 与 `buggy_code.py` 在三个 mode 间完全一致。
- `diagnosis.md` 与 `fixed_code.py` 只用于评分，不给模型看。
- 完成每次 run 后立刻回填：
  - `runs/<run_doc>.md`
  - `metrics/a2_failure_repair_eval_v0.csv`
- 推荐直接从 `runs/a2_bug_repair_run_template_v0.md` 复制生成单次 run 文档。

run 文档最小记录项：
1. `run_id / bug_id / mode / prompt_file`
2. `symptom` 与 `buggy_code` 路径
3. diagnosis 摘要
4. patch 摘要
5. `diagnosis_correct / patch_runnable / regression_pass`
6. `fix_rounds / time_to_fix_min / notes`
