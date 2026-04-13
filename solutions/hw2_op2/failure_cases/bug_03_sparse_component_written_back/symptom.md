# symptom

现象：
- 函数通常不会报错，`history` 也能正常生成，但恢复图看起来更像残差/噪声图，而不是修复结果。
- 在 fixed protocol 的 `text@50%` case 上，字符边缘往往被保留或放大；在 `random_pixel@50%` case 上，指标会明显偏低。

触发条件：
- 主接口：`rslt_inpainting(observed, mask, ...)`
- 固定协议：`lena / barbara`，grayscale，`256x256`
- 尤其在纹理更强的 `barbara` case 上更容易看出异常

归类：
- 代码错误
- RPCA 分量语义错误
