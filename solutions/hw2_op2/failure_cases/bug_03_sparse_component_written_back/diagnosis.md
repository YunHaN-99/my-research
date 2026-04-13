# diagnosis

问题原因：
- 代码在 RPCA 分解后，把 `sparse` 分量反堆叠并写回图像，而不是写回 `low_rank` 分量。
- 对于 A2 这个任务，`low_rank` 才是主要恢复信号，`sparse` 只表示污染/异常项。

定位方法：
1. 检查 `recovered_patches = unstack_patches(...)` 用的是哪一个矩阵。
2. 对照输出图，如果结果像残差图而非修复图，通常就是把 `S` 当成了主输出。

修复要点：
- 回写 patch 时使用 `low_rank`。
- `sparse` 只用于 `sparse_energy` 或诊断信息，不作为恢复图主信号。
