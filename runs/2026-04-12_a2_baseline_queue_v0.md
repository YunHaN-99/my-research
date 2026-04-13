# A2 baseline queue v0

固定执行顺序（planned 3）：
1. A2 / direct_answer
2. A2 / plain_guidance
3. A2 / coe_guided

固定协议：
- `report/a2_eval_protocol_v0.md`
- images = `lena`, `barbara`
- corruption = `random_pixel@50%`, `text@50%`
- target function = `rslt_inpainting(observed, mask, ...)`

状态：
- completed:
  - 2026-04-12_run_030 / A2 / direct_answer
  - 2026-04-12_run_031 / A2 / plain_guidance
  - 2026-04-12_run_032 / A2 / coe_guided
- remaining: none

每次 run 结束后立刻回填：
1. `runs/<run_doc>.md`
2. `metrics/a2_guidance_eval_v0.csv` 1 行
3. `metrics/a2_recovery_perf_v0.csv` 4 行
