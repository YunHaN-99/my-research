# A2 expanded-scope protocol v0

## 目标
- 在不重新采样新的模型回答的前提下，复用 A2 baseline 已生成的 direct/plain/CoE 代码产物，
  检查它们在更宽的图像与 corruption 集上的执行稳定性与恢复表现。

## source artifacts
1. `2026-04-12_run_030` direct_answer
2. `2026-04-12_run_031` plain_guidance
3. `2026-04-12_run_032` coe_guided

## 固定预处理
- grayscale only
- normalize to `[0, 1]`
- image size = `(256, 256)`

## expanded 图像集
1. `lena`
2. `barbara`
3. `peppers`
4. `cameraman`

## expanded corruption 集
1. `random_pixel@30%`
2. `random_pixel@70%`
3. `center_block@35%`
4. `text@30%`

## 固定目标任务
1. 复用已生成的 `rslt_inpainting(observed, mask, ...)`
2. 对每个 mode 在固定 `4 images x 4 corruption = 16 cases` 上输出恢复结果与 `PSNR / SSIM / RSE / runtime`

## 固定 gold 参考
1. `hw2-op2/src/chapter5_rslt.py::rslt_inpainting`
2. `hw2-op2/src/utils.py::generate_mask / compute_metrics`

## artifact 要求
1. expanded-scope 输出目录
2. 每个 case 的 `compare.png` 与 `summary.json`
3. 每个 run 的 `eval_summary.json`
4. run 文档
5. `metrics/a2_expanded_scope_eval_v0.csv` 中 1 行主记录
6. `metrics/a2_expanded_scope_perf_v0.csv` 中 16 行 case 记录

## 执行约束
- 本轮 expanded-scope validation 只扩图像与 corruption，不重采样 fresh generations。
- 若后续需要估计采样方差，应单列为 `fresh-generation replication`，不与本协议混合。
- 若有协议偏离，必须在对应 run 文档与 metrics 中显式标注原因与影响。
