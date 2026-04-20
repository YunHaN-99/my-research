# A1 Bug Repair Task Card v0

## 1. 题目一句话目标
给定 A1 Seam Carving 的失败样例，先定位主错误，再在不破坏原接口的前提下做最小可运行修补。

## 2. 输入 / 输出
输入：
- symptom.md：外部现象与触发条件
- buggy_code.py：带缺陷的最小代码片段
- 原任务上下文：A1 seam carving 的目标与接口约束

输出：
- diagnosis：一句话主错误定位 + 2 到 4 行原因说明
- patched code：最小修补版本
- regression notes：说明为什么修补后不会复发同类问题
- 实验产物：run 记录 + metrics 条目

## 3. 修补约束
- 保持原函数名、参数列表和返回约定，除非 symptom 明确表明接口本身错误。
- 优先修根因，不要只压掉报错。
- patch 应尽量最小，避免顺手重写整段逻辑。
- 不允许把 diagnosis.md 或 fixed_code.py 当作给模型的输入材料。

## 4. 推荐工作流
1. 先重述 symptom，明确“理想行为”是什么。
2. 找到被破坏的核心不变量。
3. 只修改与主错误直接相关的代码。
4. 做一次最小回归检查，确认没有引入新的 shape / 边界 / 转置问题。

## 5. 典型不变量
- bug_01_dp_boundary：
  - DP 父节点索引必须始终处于合法列范围内。
- bug_02_no_energy_recompute：
  - 每删一条 seam 后，energy.shape 必须与当前图像尺寸一致。
- bug_03_height_transpose：
  - 高度缩放转置时只能交换 H/W 轴，不能把通道轴换进来。

## 6. 常见失败方式
- 只修 symptom，不修主错误来源。
- 改了函数签名，导致补丁无法替换原位置。
- 为了通过当前 case 写死常数或 shape。
- 修补 width 逻辑时引入新的 transpose / dtype 问题。
- 没有给出最小回归说明，导致 patch 可解释性差。
