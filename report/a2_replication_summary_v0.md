# A2 replication summary v0

## Scope
- target runs: run_033 to run_041
- baseline anchors: run_030 to run_032
- case_id: A2
- protocol_file: `report/a2_eval_protocol_v0.md`
- fixed setup:
  - images = `lena`, `barbara`
  - corruption = `random_pixel@50%`, `text@50%`
  - image size = `256 x 256`
  - grayscale only
- replication meaning: copied baseline artifacts were rerun under the same fixed seed and protocol; this is an execution-stability check, not fresh model resampling

## 已完成
- completed replication runs:
  - run_033 direct_answer rep1
  - run_034 plain_guidance rep1
  - run_035 coe_guided rep1
  - run_036 direct_answer rep2
  - run_037 plain_guidance rep2
  - run_038 coe_guided rep2
  - run_039 direct_answer rep3
  - run_040 plain_guidance rep3
  - run_041 coe_guided rep3
- current data sources:
  - `metrics/a2_guidance_eval_v0.csv` (12 rows total)
  - `metrics/a2_recovery_perf_v0.csv` (48 rows total)

## 当前统计

### Guidance eval
- direct_answer: runnable `4/4`, correct=`2` `4/4`, self_check=`2` `0/4`, median `time_to_first_working_min = 1.25`
- plain_guidance: runnable `4/4`, correct=`2` `4/4`, self_check=`2` `4/4`, median `time_to_first_working_min = 1.25`
- coe_guided: runnable `4/4`, correct=`2` `4/4`, self_check=`2` `4/4`, median `time_to_first_working_min = 1.30`

### Recovery results
- all 48 fixed cases are `output_ok = 1`
- each of the 4 fixed image/corruption cases has exactly 1 unique `(PSNR, SSIM, RSE)` tuple across all 12 runs
- representative values:
  - `lena / random_pixel@50%`: PSNR `15.1519`, SSIM `0.3766`, RSE `0.3245`
  - `lena / text@50%`: PSNR `27.2597`, SSIM `0.9483`, RSE `0.0805`
  - `barbara / random_pixel@50%`: PSNR `24.2780`, SSIM `0.7244`, RSE `0.1358`
  - `barbara / text@50%`: PSNR `34.9722`, SSIM `0.9762`, RSE `0.0397`
- average per-case runtime by mode:
  - direct_answer: `16.9590 s`
  - plain_guidance: `17.8435 s`
  - coe_guided: `17.6216 s`

## 初步观察
- 在当前固定协议下，A2 chapter5 inpainting 的 execution path 已经稳定复现，12/12 runs 都是一轮 runnable 且 correct。
- plain_guidance 与 coe_guided 的优势仍主要体现在 `self_check` 和可复查痕迹，而不是在这个 deterministic setup 里拉开最终恢复质量。
- 三种模式的恢复指标在当前 4 个 fixed cases 上完全一致，说明当前 replication 看到的是同一实现链路的稳定执行，而不是算法质量差异。
- runtime 有轻微波动，但样本和硬件上下文都太小，不宜做强 timing 结论。

## Measurement boundary
- `lena` 与 `barbara` 都来自 `hw2-op2/src/utils.py` 的 fallback source：
  - `lena -> skimage:astronaut`
  - `barbara -> skimage:brick`
- 本轮 replication 复用的是复制出来的 baseline artifact，并未重新采样新的模型回答，因此它不能估计 fresh generations 的 sampling variance。
- 当前结论只覆盖 `2 images x 2 mask modes x 50% corruption x grayscale 256x256` 这一固定协议。
