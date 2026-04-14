# Task Bank Status v1

## 目的
说明当前课题题库的实际完成情况、已经闭环的主案例、以及距离 Timeline 中期要求还差什么。

当前正式题库索引页：`report/task_bank_index_v1.md`

## 1. 当前题库骨架

### 已闭环的主案例家族

### A1
- case family: `Seam Carving`
- 当前状态：`completed`
- 已有材料：
  - `task_cards/A1_seam_carving_taskcard_v1.md`
  - `report/a1_eval_protocol_v0.md`
  - A1 baseline / replication / bug-repair 的 run、metrics、summary

### A2
- case family: 低秩图像任务族下的 `chapter5 rslt_inpainting`
- 当前状态：`completed`
- 已有材料：
  - `problems/a2_requirement.md`
  - `task_cards/A2_rslt_inpainting_taskcard_v1.md`
  - A2 baseline / replication / bug-repair / expanded-scope / fresh-generation 的 run、metrics、summary

### 已接入的扩展占位家族

### A3
- case family: 扩展家族占位
- 当前状态：`placeholder`
- 已有材料：
  - `task_cards/A3_taskcard_v0.md`

### A4
- case family: 扩展家族占位
- 当前状态：`placeholder`
- 已有材料：
  - `task_cards/A4_taskcard_v0.md`

## 2. 当前可直接列入正式题库页的条目
- A1 主任务：width shrink
- A1 主任务：height shrink
- A1 failure case：`bug_01_dp_boundary`
- A1 failure case：`bug_02_no_energy_recompute`
- A1 failure case：`bug_03_height_transpose`
- A2 fixed protocol：`random_pixel@50%`
- A2 fixed protocol：`text@50%`
- A2 failure case：`bug_01_missing_mask_constraint`
- A2 failure case：`bug_02_mask_polarity_inverted`
- A2 failure case：`bug_03_sparse_component_written_back`

## 3. 当前还不宜直接写成“题库 v1 >= 15 题”的原因
- 目前仓库最强的是“主案例闭环”和“benchmark 资产完整”，不是“题目数量足够多”。
- 现在已经有正式题库索引页，但当前更适合按三层写：
  - 题目家族
  - 固定协议 case / 子任务
  - curated failure case
- A3 / A4 目前只完成占位接入，还没有进入 requirement / 固定协议 / 正式实验。

## 4. 建议采用的题库计数口径
建议中期材料不要把所有 run 都硬算成“题目数”，而是分三层写：

### 层 1：主案例家族
- A1
- A2

### 层 2：固定协议与 failure-case 子条目
- A1 width / height
- A1 bug_01 / bug_02 / bug_03
- A2 fixed protocol case 1 / case 2
- A2 bug_01 / bug_02 / bug_03

### 层 3：后续待扩展家族
- A3 曲线拟合 / 昆虫分类
- A4 微分方程模型 / Poisson 图像融合

## 5. 中期阶段建议写法
建议中期材料写成：

> 当前题库已完成 A1 / A2 两个主案例家族的闭环实现，并形成固定协议、failure-case benchmark 与正式索引页；A3 / A4 已完成扩展占位 task card，正在接入下一阶段 requirement、协议与评测链路。

## 6. 下一步最小动作
1. 从 A3 / A4 各自候选方向中先冻结 1 个首发条目。
2. 给冻结后的 A3 / A4 条目补 `requirement` 与 `taskcard_v1`。
3. 结题前再把题库从“主案例 + benchmark”扩到更完整的 15 到 20 条。
