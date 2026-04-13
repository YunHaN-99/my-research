# A2 baseline summary v0

## Scope
- target runs: run_030 to run_032
- case_id: A2
- protocol_file: report/a2_eval_protocol_v0.md
- fixed setup:
  - images = `lena`, `barbara`
  - corruption = `random_pixel@50%`, `text@50%`
  - image size = `256 x 256`
  - grayscale only

## 已完成
- completed baseline runs:
  - run_030 direct_answer
  - run_031 plain_guidance
  - run_032 coe_guided
- current data sources:
  - metrics/a2_guidance_eval_v0.csv (3 rows)
  - metrics/a2_recovery_perf_v0.csv (12 rows)

## 当前统计

### Guidance eval
- direct_answer: artifact_complete=2, runnable=1, correct=2, self_check=1
- plain_guidance: artifact_complete=2, runnable=1, correct=2, self_check=2
- coe_guided: artifact_complete=2, runnable=1, correct=2, self_check=2

### Recovery results
- all 12 fixed cases are `output_ok = 1`
- current per-case outputs are numerically identical across the three modes on this first baseline snapshot
- representative values:
  - `lena / random_pixel@50%`: PSNR `15.1519`, SSIM `0.3766`, RSE `0.3245`
  - `lena / text@50%`: PSNR `27.2597`, SSIM `0.9483`, RSE `0.0805`
  - `barbara / random_pixel@50%`: PSNR `24.2780`, SSIM `0.7244`, RSE `0.1358`
  - `barbara / text@50%`: PSNR `34.9722`, SSIM `0.9762`, RSE `0.0397`

## 初步观察
- 在当前 fixed protocol 下，三种模式都能一次性完成 A2 chapter5 主任务。
- plain_guidance 与 coe_guided 的优势首先体现在自检和可复核痕迹，而不是在这个小样本上拉开恢复质量。
- 由于三组实现收敛到相同的核心算法，当前恢复指标没有出现模式间差异，这一轮更像“baseline feasibility check”。

## Measurement boundary
- 本轮 `lena / barbara` 都使用了 `hw2-op2/src/utils.py` 的 fallback source：
  - `lena -> skimage:astronaut`
  - `barbara -> skimage:brick`
- `runtime_s` 是当前机器上的单次执行时间，不宜做强 timing 结论。
- 这只是 baseline snapshot，尚未进入 replication。
