# A4 requirement

目标：把 A4 的首发条目冻结为“Poisson 图像融合”，作为中期后续扩展家族的第一个正式任务，而不是继续停留在 placeholder。

## 任务定义
- 主任务：在给定 `source / target / mask` 的情况下，使用 Poisson blending 生成边界过渡更自然的融合图像。
- 当前冻结条目：`Poisson image blending`
- 问题边界：输入是源图、目标图和融合掩码，输出是融合结果图像。

## 输入
1. `source`：待贴入内容的图像
2. `target`：背景图像
3. `mask`：融合区域掩码
4. 可选超参数：`offset / solver / channel_mode`

## 输出
1. `blended`：融合后的图像
2. `debug_info`：最小可复查的求解信息，如方程规模或求解状态
3. 实验产物：融合对比图、run 记录、metrics 或质检记录

## 报告必须包含
1. Poisson blending 的目标函数与边界条件说明
2. `source / target / mask / blended` 的对比图
3. 边界自然度与融合痕迹的观察说明
4. 稀疏线性系统求解流程简介
5. failure case 与边界条件错误说明

## 本轮暂不做
1. A4 的“微分方程模型”分支
2. 交互式 GUI 编辑器
3. 大规模图像素材库扩充
4. 复杂混合梯度变体的系统比较

## 补充说明
- A4 当前只冻结 1 个首发条目，目标是把扩展家族从 placeholder 推进到“已有 requirement + taskcard_v1”。
- 微分方程模型保留为 A4 的下一批候选条目。
- 这一步的重点仍然是补齐中期题库结构，而不是立即做完 A4 的正式实验闭环。
