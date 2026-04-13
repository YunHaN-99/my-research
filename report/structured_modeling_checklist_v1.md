# Structured Modeling Checklist v1

## 目的
把当前 A1 / A2 主案例中已经证明有效的结构化检查项整理成统一清单，供后续 prompt 设计、run 复核和中期材料引用。

## 1. 通用八步检查

### 1. 题目重述
- 当前任务到底要解决什么问题。
- 哪些内容在本轮 scope 内，哪些明确不做。

### 2. 输入 / 输出
- 输入变量有哪些。
- 每个输入的形状、范围、语义是什么。
- 输出需要返回什么对象，以及最小 artifact 是什么。

### 3. 参数 / 状态变量
- 固定参数有哪些。
- 运行中会被更新的状态变量有哪些。
- 关键 shape 是否会在循环中变化。

### 4. 目标
- 正确性目标是什么。
- 质量目标是什么。
- 本轮是“先保可运行”，还是“追求最优质量”。

### 5. 约束 / 不变量
- 哪些条件在每一轮都必须成立。
- 哪些边界条件一旦破坏就会直接导致错误。
- 哪些约束是协议约束，而不是算法自由选择。

### 6. 算法拆分
- 主接口是什么。
- 最小函数拆分怎么设计。
- 每个子函数的责任边界是什么。

### 7. 评估协议
- 固定测试对象是什么。
- 固定指标是什么。
- 结果落在哪里，哪些 CSV 需要回填。

### 8. 自检与失败模式
- 先列最可能错的 3 到 5 个点。
- 给每个点配一个最小断言或检查规则。
- 区分“代码能跑”和“语义正确”。

## 2. 五元组映射到当前算法任务
Timeline 里提到的“集合 / 参数 / 变量 / 目标 / 约束”，在当前 A1 / A2 这类算法实现任务中，可映射为：

| 五元组 | 算法任务里的对应对象 |
|---|---|
| 集合 | 输入样本、测试图、候选 patch 集、像素位置集合 |
| 参数 | 图像尺寸、target size、patch_size、stride、固定 seed |
| 变量 | seam 路径、当前恢复图像、weight_map、history |
| 目标 | 收缩后保持主体内容 / 修复后提升恢复质量 |
| 约束 | shrink-only、mask 语义、观测像素不变、输出范围和 shape 正确 |

## 3. A1 专项检查

### 题目边界
- 只做 shrink，不做 enlarge。
- 主接口固定为 `seam_carve_image(im, sz)`。

### 输入 / 输出
- 输入图像形状为 `H x W x C`。
- 输出图像必须与目标尺寸严格匹配。

### 核心不变量
- DP 边界不能越界。
- 相邻行 seam 索引差值不能超过 1。
- 每删一条 seam 后，图像宽度或高度必须变化 1。
- 高度缩小时的转置复用必须保持 H / W 语义一致。

### 协议与评估
- 固定测试图：`bing1.png`、`original.png`
- 固定预处理：`max_side = 420`
- 固定任务：width shrink / height shrink
- 固定研究级对照：`direct_answer / plain_guidance / coe_guided`

### 最小自检
- 5x5 或更小矩阵先手推 seam 路径。
- 每轮删 seam 后检查 shape。
- height 模式额外检查 transpose 前后尺寸与通道顺序。

## 4. A2 专项检查

### 题目边界
- 当前主案例固定为 `hw2-op2/src/chapter5_rslt.py::rslt_inpainting(...)`
- 只做 grayscale masked repair。
- 不进入 GUI / video / TILT / chapter7 扩展。

### 输入 / 输出
- `observed` 与 `mask` 都是 `H x W`。
- `mask == 1` 表示 observed，`mask == 0` 表示 missing / corrupted。
- 输出是 `recovered` 与 `history`。

### 核心不变量
- `observed.shape == mask.shape`
- 每轮聚合后都要重新施加 mask 约束。
- `recovered[mask > 0.5]` 必须与 `observed[mask > 0.5]` 一致。
- patch group 的 `stack -> RPCA -> unstack` shape 必须闭合。
- 聚合时 `weight_map` 不能为 0 除。
- RPCA 写回图像的是 `low_rank`，不是 `sparse`。
- 输出要 clip 到 `[0, 1]`，并保持 finite。

### 协议与评估
- 固定测试图：`lena`、`barbara`
- 固定 corruption：`random_pixel@50%`、`text@50%`
- 固定指标：`PSNR / SSIM / RSE / runtime`
- 结果回填：
  - `metrics/a2_guidance_eval_v0.csv`
  - `metrics/a2_recovery_perf_v0.csv`

### 最小自检
- `mask` 语义检查。
- observed 区域不变性检查。
- `weight_map.shape == observed.shape`。
- `np.all(np.isfinite(recovered))`。
- 指标计算前 `original.shape == recovered.shape`。

## 5. 使用方式
- `direct_answer` 至少要过一遍第 1 到第 5 节，避免 scope drift。
- `plain_guidance` 需要把第 6 到第 8 节写进回复结构。
- `coe_guided` 需要把通用八步检查拆进不同角色：
  - Reader：题目重述、输入输出、验收条件
  - Planner：参数、变量、目标、约束、算法拆分
  - Reviewer：失败模式与最小自检
  - Experimenter：评估协议与 artifact 落地

## 6. 当前边界
- 这份 checklist 已能覆盖 A1 / A2 当前主案例。
- 对 A3 / A4 还需要再补“模型假设、数学符号、求解器选择”的检查项。
