# diagnosis

问题原因：
- patch 聚合后直接用 `accumulator / weight_map` 覆盖了整张 `current`，但没有把观测像素位置重新锁回 `observed`。
- 这样会导致本来已知的 clean pixels 被邻域 patch 的平均结果改写，违反 A2 的 mask constraint。

定位方法：
1. 在每轮 outer iteration 后检查 `np.max(np.abs(current[mask > 0.5] - observed[mask > 0.5]))`。
2. 对比 gold 参考，会发现正确实现会在每轮聚合后执行 `current[mask_bool] = observed[mask_bool]`。

修复要点：
- 聚合归一化后立刻重新施加 `mask > 0.5` 的观测像素约束。
- 该约束应在每轮 outer iteration 都执行，而不是只在初始化时执行一次。
