# A2 evaluation protocol v0

固定测试图：
1. `lena`
2. `barbara`

固定预处理：
- grayscale only
- normalize to `[0, 1]`
- image size = `(256, 256)`

固定 corruption：
1. `random_pixel@50%`
2. `text@50%`

固定目标任务：
1. 实现 `rslt_inpainting(observed, mask, ...)`
2. 在固定 4 个 case 上输出恢复结果与 `PSNR / SSIM / RSE / runtime`

固定 gold 参考：
1. `hw2-op2/src/chapter5_rslt.py::rslt_inpainting`
2. `hw2-op2/src/utils.py::generate_mask / compute_metrics`

固定研究级对照：
1. `direct_answer`
2. `plain_guidance`
3. `coe_guided`

固定 artifact 要求：
1. 代码
2. 4 个 fixed case 的恢复输出
3. run 文档
4. `metrics/a2_guidance_eval_v0.csv` 中 1 行主记录
5. `metrics/a2_recovery_perf_v0.csv` 中 4 行 case 记录

执行约束：
- 后续 A2 run 默认沿用本协议，不随意更换测试图、corruption、尺寸和指标口径。
- 若有偏离，必须在对应 run 文档与 metrics 中显式标注原因与影响。
