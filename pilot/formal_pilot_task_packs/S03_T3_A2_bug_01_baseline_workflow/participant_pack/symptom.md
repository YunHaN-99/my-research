# symptom

现象：
- 函数通常可以正常跑完，不一定抛异常，但恢复图会把本来已经观测到的 clean pixels 也改掉。
- 在 fixed protocol 的 `text@50%` 或 `random_pixel@50%` case 上，检查 `recovered[mask > 0.5]` 与 `observed[mask > 0.5]` 会发现明显偏差。

触发条件：
- 主接口：`rslt_inpainting(observed, mask, ...)`
- 固定协议：`lena / barbara`，grayscale，`256x256`
- corruption：`random_pixel@50%` 或 `text@50%`

归类：
- 代码错误
- mask 约束缺失
