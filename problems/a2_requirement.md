# A2 requirement

目标：把 `hw2-op2` 的 `chapter5` 收束为研究主案例 A2，围绕基于 patch-group RPCA 的灰度图像修复建立可复现实验管线。

## 任务定义
- 主任务：masked grayscale image repair / inpainting
- gold reference：`hw2-op2/src/chapter5_rslt.py` 中的 `rslt_inpainting(...)`
- 问题边界：输入是已退化图像 `observed` 与同形状掩码 `mask`，输出是恢复图像 `recovered`

## 输入
1. `observed`：灰度图像，形状 `H x W`，数值范围归一化到 `[0, 1]`
2. `mask`：同形状观测掩码，`1` 表示已知像素，`0` 表示缺失 / 被污染像素
3. 可选超参数：`patch_size / stride / search_window / num_similar / outer_iter / rpca_max_iter`

## 输出
1. `recovered`：恢复后的灰度图像，形状 `H x W`
2. `history`：至少保留 `psnr` 或等价的迭代历史信息
3. 实验产物：代表性对比图、run 记录、metrics 条目、阶段总结

## 报告必须包含
1. patch-group + RPCA 的算法原理
2. 固定协议下的恢复结果
3. `PSNR / SSIM / RSE / runtime` 结果表
4. 与 baseline 方法的简短对照
5. 边界与失败模式说明

## 本轮暂不做
1. GUI 交互层复现
2. video / TILT / chapter1~8 全量重跑
3. 大规模超参数搜索
4. 彩色图像扩展

## 补充说明
- A2 不把整个 `hw2-op2` 八章都当成单任务，而是先锁定 `chapter5` 作为主案例。
- `chapter2/3/4/8` 只作为 baseline、协议参考或后续扩展依据。
- 当前目标是先把 A2 的 run / metrics / report 管线搭成与 A1 同风格的主线。
