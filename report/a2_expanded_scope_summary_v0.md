# A2 expanded-scope summary v0

## Scope
- target runs: `run_052` to `run_054`
- source artifacts:
  - `run_030` direct_answer
  - `run_031` plain_guidance
  - `run_032` coe_guided
- protocol_file: `report/a2_expanded_scope_protocol_v0.md`
- fixed setup:
  - images = `lena`, `barbara`, `peppers`, `cameraman`
  - corruption = `random_pixel@30%`, `random_pixel@70%`, `center_block@35%`, `text@30%`
  - image size = `256 x 256`
  - grayscale only
- evaluation meaning: reuse existing generated artifacts and expand only the evaluation set; this is not fresh-generation replication

## 已完成
- completed expanded-scope runs:
  - `run_052` direct_answer
  - `run_053` plain_guidance
  - `run_054` coe_guided
- current data sources:
  - `metrics/a2_expanded_scope_eval_v0.csv` (3 rows total)
  - `metrics/a2_expanded_scope_perf_v0.csv` (48 rows total)

## 当前统计

### Run-level eval
- direct_answer: `case_count = 16`, `output_ok_count = 16`, average per-case runtime `15.1708 s`
- plain_guidance: `case_count = 16`, `output_ok_count = 16`, average per-case runtime `14.9153 s`
- coe_guided: `case_count = 16`, `output_ok_count = 16`, average per-case runtime `15.0344 s`

### Recovery results
- all 48 expanded-scope cases are `output_ok = 1`
- all 16 image/corruption cases have exactly 1 unique `(PSNR, SSIM, RSE)` tuple across the three modes
- average metrics by corruption:
  - `random_pixel@30%`: PSNR `23.6039`, SSIM `0.6394`, RSE `0.1368`
  - `random_pixel@70%`: PSNR `15.8864`, SSIM `0.3488`, RSE `0.3323`
  - `center_block@35%`: PSNR `15.9697`, SSIM `0.7230`, RSE `0.3184`
  - `text@30%`: PSNR `31.2425`, SSIM `0.9687`, RSE `0.0562`
- representative hard/easy cases by average PSNR:
  - hardest: `lena / random_pixel@70%` = `13.0882`
  - hardest: `cameraman / center_block@35%` = `13.4256`
  - hardest: `cameraman / random_pixel@70%` = `13.4740`
  - easiest: `barbara / text@30%` = `36.5561`
  - easiest: `peppers / text@30%` = `30.3754`
  - easiest: `barbara / random_pixel@30%` = `29.4335`

## 初步观察
- 在 expanded-scope 的 `4 images x 4 corruption` 设置下，三种 mode 复用的现有代码产物仍然全部可运行，说明 A2 的执行链路不只在最初 4 个 fixed cases 上稳定。
- 三种 mode 的恢复指标在全部 16 个 expanded cases 上仍然完全一致，说明当前 direct/plain/CoE 的差异仍主要在可检查性，而不是最终恢复质量。
- `text@30%` 明显比缺失型 case 更容易，`random_pixel@70%` 和 `center_block@35%` 更难，其中 `cameraman` 与 `lena` 的高缺失 case 最脆弱。
- `barbara` 在 `random_pixel@30%` 和 `text@30%` 下表现最好，符合其纹理重复结构更强、patch-group 更容易找到相似块的直觉。

## Measurement boundary
- `lena`、`barbara`、`peppers`、`cameraman` 分别来自 `hw2-op2/src/utils.py` 的 fallback source：
  - `lena -> skimage:astronaut`
  - `barbara -> skimage:brick`
  - `peppers -> skimage:coffee`
  - `cameraman -> skimage:camera`
- 本轮 expanded-scope validation 复用的是已有 baseline generated artifacts，不是 fresh model generations，因此不能估计采样方差。
- 当前结论只覆盖 grayscale `256x256` 与这 16 个 expanded cases，不直接外推到彩图、更大尺寸或全新 corruption 家族。
