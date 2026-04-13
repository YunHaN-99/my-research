# A1 bug-repair queue v0

固定执行顺序（planned 9）：
1. bug_01_dp_boundary / direct_answer
2. bug_01_dp_boundary / plain_guidance
3. bug_01_dp_boundary / coe_guided
4. bug_02_no_energy_recompute / direct_answer
5. bug_02_no_energy_recompute / plain_guidance
6. bug_02_no_energy_recompute / coe_guided
7. bug_03_height_transpose / direct_answer
8. bug_03_height_transpose / plain_guidance
9. bug_03_height_transpose / coe_guided

状态：
- completed:
  - 2026-04-12_run_020 / bug_01_dp_boundary / direct_answer
  - 2026-04-12_run_021 / bug_01_dp_boundary / plain_guidance
  - 2026-04-12_run_022 / bug_01_dp_boundary / coe_guided
  - 2026-04-12_run_023 / bug_02_no_energy_recompute / direct_answer
  - 2026-04-12_run_024 / bug_02_no_energy_recompute / plain_guidance
  - 2026-04-12_run_025 / bug_02_no_energy_recompute / coe_guided
  - 2026-04-12_run_026 / bug_03_height_transpose / direct_answer
  - 2026-04-12_run_027 / bug_03_height_transpose / plain_guidance
  - 2026-04-12_run_028 / bug_03_height_transpose / coe_guided
- remaining: none

执行纪律：
- 只变 guidance mode，不变 bug 材料。
- 同一 bug 的 symptom.md 与 buggy_code.py 在三个 mode 间完全一致。
- diagnosis.md 与 fixed_code.py 只用于评分，不给模型看。
- 完成每次 run 后立刻回填：
  - runs/<run_doc>.md
  - metrics/a1_failure_repair_eval_v0.csv
- 推荐直接从 runs/a1_bug_repair_run_template_v0.md 复制生成单次 run 文档。

run 文档最小记录项：
1. run_id / bug_id / mode / prompt_file
2. symptom 与 buggy_code 路径
3. diagnosis 摘要
4. patch 摘要
5. diagnosis_correct / patch_runnable / regression_pass
6. fix_rounds / time_to_fix_min / notes
