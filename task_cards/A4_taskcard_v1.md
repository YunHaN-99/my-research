# A4 Task Card v1

## 1. 题目一句话目标
实现 Poisson 图像融合：在给定 `source / target / mask` 的情况下，生成边界过渡更自然的融合结果。

## 2. 当前冻结条目
- family：A4
- 首发条目：`Poisson image blending`
- 当前定位：扩展家族的首个正式条目，已完成 requirement + taskcard_v1，但尚未进入完整实验闭环
- 后续备选：微分方程模型

## 3. 输入 / 输出
输入：
- `source`：源图像
- `target`：目标图像
- `mask`：融合区域掩码
- 可选超参数：`offset / solver / channel_mode`

输出：
- `blended`：融合后的图像
- `debug_info`：最小可复查的求解状态信息
- 实验产物：融合对比图、run 文档与结果摘要

## 4. 核心模型
- 在 `mask` 区域内部求解 Poisson 方程
- 用源图梯度作为 guidance field
- 用目标图边界条件保证融合边界自然过渡
- 典型实现会用稀疏线性系统求解

## 5. 最小算法流程
1. 读取 `source / target / mask`。
2. 计算 `source` 的梯度或 guidance field。
3. 在 `mask` 区域内组装 Poisson 线性系统。
4. 使用稀疏求解器得到区域内像素值。
5. 将解写回 `target`，得到 `blended`。
6. 输出对比图和求解摘要。

## 6. 常见错误与自检
- 错误 1：mask 边界像素索引错位。
  - 自检：先用小尺寸 mask 做单通道调试。
- 错误 2：源图和目标图尺寸或通道数不一致。
  - 自检：进入求解前检查 shape 和通道模式。
- 错误 3：求解后像素值未 clip，出现明显溢出。
  - 自检：输出前检查数值范围。
- 错误 4：只保留融合结果，不保留 source / target / mask 对照。
  - 自检：每次至少输出 1 组四联图。

## 7. 评估指标与实验设计
- 当前更适合的指标：
  - `output_ok`
  - 边界自然度的定性说明
  - 求解时间
- 最小展示：
  - `source`
  - `target`
  - `mask`
  - `blended`
- 最小实验建议：
  - 1 组边界简单的融合 case
  - 1 组纹理或亮度差异明显的融合 case

## 8. 中期阶段可诚实表述的状态
- A4 已从 placeholder 推进为首发条目已冻结的正式任务卡。
- 当前还不能把 A4 写成“已完成主案例闭环”。
- 当前最适合把 A4 写成“已完成 requirement + taskcard_v1，等待协议、评测和实验链路接入”。
