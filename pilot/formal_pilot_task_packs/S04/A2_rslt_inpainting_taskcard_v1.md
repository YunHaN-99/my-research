# A2 RSLT Inpainting Task Card v1

## 1. 题目一句话目标
实现基于 patch-group RPCA 的灰度图像修复：在已知像素掩码约束下恢复缺失或受污染区域，并尽量保留重复纹理结构。

## 2. 输入 / 输出
输入：
- `observed`，形状为 `H x W` 的灰度图像，已归一化到 `[0, 1]`
- `mask`，形状为 `H x W` 的掩码，`1` 为观测像素，`0` 为缺失 / 被污染像素
- 可选超参数：`patch_size / stride / search_window / num_similar / candidate_step / outer_iter / rpca_max_iter`

输出：
- `recovered`，形状为 `H x W` 的恢复图像
- `history`，至少记录外层迭代中的 `psnr` 或 `sparse_energy`
- 实验产物：对比图、运行记录、指标表与阶段总结

## 3. 核心模型
- patch group：对每个参考 patch 搜索相似 patch，并堆叠成矩阵
- RPCA 分解：`group_matrix = L + S`
  - `L` 捕捉重复纹理与低秩结构
  - `S` 捕捉稀疏污染或异常项
- aggregation：把恢复后的 patch 回写到图像平面，并用权重图归一化
- mask constraint：每轮更新后，观测像素必须保持与输入 `observed` 一致

## 4. 算法流程
1. 用 `mask` 初始化当前图像，对缺失位置做均值或等价初始化。
2. 枚举 patch 位置。
3. 对每个参考 patch 搜索相似 patch，形成 patch group。
4. 对 patch group 做 RPCA，提取低秩部分作为恢复 patch。
5. 将恢复 patch 聚合回整图。
6. 用权重图做归一化，避免重复覆盖导致数值失真。
7. 重新施加 `mask` 约束，确保观测像素不被改写。
8. 重复外层迭代直到达到固定轮数或收敛。

## 5. 代码接口
- 主接口：`rslt_inpainting(observed, mask, ...)`
- 建议保留或拆分的最小函数：
  - `rslt_patch_rpca(group_matrix, ...)`
  - `find_similar_patches(...)`
  - `stack_patches(...) / unstack_patches(...)`
  - `insert_patch(...)`
  - `compute_metrics(...)`
- gold 参考：
  - `hw2-op2/src/chapter5_rslt.py`
  - `hw2-op2/src/utils.py`

## 6. 常见错误与自检
- 错误 1：没有在外层迭代后重新施加 `mask` 约束。
  - 自检：断言 `recovered[mask > 0.5] == observed[mask > 0.5]` 在容差内成立。
- 错误 2：patch group 堆叠 / 反堆叠 shape 错。
  - 自检：每次 `stack -> unstack` 后 patch 数量与 patch 形状保持一致。
- 错误 3：聚合阶段除以 0 或权重图 shape 不对。
  - 自检：使用 `np.maximum(weight_map, 1e-12)`，并检查 `weight_map.shape == observed.shape`。
- 错误 4：输出没有 clip 到 `[0, 1]`。
  - 自检：输出前检查最小值和最大值。
- 错误 5：指标计算图像尺寸不一致。
  - 自检：算 `PSNR / SSIM / RSE` 前检查 `original.shape == recovered.shape`。

## 7. 评估指标与实验设计
- 固定指标：
  - `PSNR`
  - `SSIM`
  - `RSE`
  - `runtime`
- 最小实验集：
  - 图像：`lena`、`barbara`
  - corruption：`random_pixel@50%`、`text@50%`
- 最小展示：
  - 原图 / 退化图 / 恢复图 三联图
  - 每个 case 一行 metrics
  - 与 fixed protocol baseline 的简短比较
