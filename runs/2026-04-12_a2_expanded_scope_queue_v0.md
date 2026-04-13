# A2 expanded-scope queue v0

固定执行顺序（planned 3）：
1. run_052 (direct_answer)
2. run_053 (plain_guidance)
3. run_054 (coe_guided)

固定协议：
- `report/a2_expanded_scope_protocol_v0.md`
- images = `lena`, `barbara`, `peppers`, `cameraman`
- corruption = `random_pixel@30%`, `random_pixel@70%`, `center_block@35%`, `text@30%`
- image size = `256x256`
- baseline source artifacts = `run_030` / `run_031` / `run_032`

状态：
- completed:
  - `2026-04-12_run_052` / direct_answer
  - `2026-04-12_run_053` / plain_guidance
  - `2026-04-12_run_054` / coe_guided
- remaining: none

执行纪律：
- 只扩图像与 corruption，不重采样新的模型回答。
- 每个 mode 固定 16 个 case，完成后立刻回填：
  - `runs/<run_doc>.md`
  - `metrics/a2_expanded_scope_eval_v0.csv`
  - `metrics/a2_expanded_scope_perf_v0.csv`
