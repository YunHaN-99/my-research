# diagnosis

问题原因：
- 代码把 `mask == 0` 当成观测像素，把 `mask == 1` 当成缺失像素，掩码语义整体反了。
- A2 的固定语义是：`1 = observed`, `0 = missing / corrupted`。一旦反过来，初始化与约束都会施加到错误位置。

定位方法：
1. 检查 `mask_bool` 的定义是否为 `mask > 0.5`。
2. 对照 symptom，会发现“被锁住不更新”的区域正好是缺失区，而不是真正的观测区。

修复要点：
- 统一使用 `mask > 0.5` 表示观测像素。
- 初始化和每轮 outer iteration 后的约束都必须使用同一套 mask 语义。
