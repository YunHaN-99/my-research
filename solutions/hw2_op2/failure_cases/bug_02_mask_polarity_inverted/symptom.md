# symptom

现象：
- 代码能跑，但缺失/污染区域经常几乎不被修复，反而本来观测到的 clean 区域被反复改写。
- 在 `text@50%` case 上，文字遮挡区域可能被原样保留；在 `random_pixel@50%` case 上，known pixels 会出现不必要漂移。

触发条件：
- 主接口：`rslt_inpainting(observed, mask, ...)`
- 固定协议：`lena / barbara`，grayscale，`256x256`
- corruption：`random_pixel@50%` 或 `text@50%`

归类：
- 代码错误
- 掩码语义错误
