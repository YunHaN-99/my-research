# Task Bank Status v1

## 目的
说明当前课题题库的实际完成情况、已经闭环的主案例、以及距离 Timeline 中期要求还差什么。

当前正式题库索引页：`report/task_bank_index_v1.md`

## 1. 当前题库骨架

当前按“正式条目”计数，已可稳定列入中期题库的条目数为 `16`：
- A1：`2` 个主任务 + `3` 个 failure cases
- A2：`2` 个 fixed protocol + `4` 个 expanded-scope 代表案例 + `3` 个 failure cases
- A3：`1` 个首发条目
- A4：`1` 个首发条目

### 已闭环的主案例家族

### A1
- case family: `Seam Carving`
- 当前状态：`completed`
- 已有材料：
  - `task_cards/A1_seam_carving_taskcard_v1.md`
  - `report/a1_eval_protocol_v0.md`
  - A1 baseline / replication / bug-repair 的 run、metrics、summary

### A2
- case family: 低秩图像任务族下的 `hw2-op2/src/chapter5_rslt.py::rslt_inpainting(...)`
- 当前状态：`completed`
- 已有材料：
  - `problems/a2_requirement.md`
  - `task_cards/A2_rslt_inpainting_taskcard_v1.md`
  - A2 baseline / replication / bug-repair / expanded-scope / fresh-generation 的 run、metrics、summary

### 已接入的扩展首发家族

### A3
- case family: `curve fitting` 首发条目
- 当前状态：`entry_frozen`
- 已有材料：
  - `problems/a3_requirement.md`
  - `task_cards/A3_taskcard_v1.md`

### A4
- case family: `Poisson image blending` 首发条目
- 当前状态：`entry_frozen`
- 已有材料：
  - `problems/a4_requirement.md`
  - `task_cards/A4_taskcard_v1.md`

## 2. 当前可直接列入正式题库页的条目
- A1 主任务：width shrink
- A1 主任务：height shrink
- A1 failure case：`bug_01_dp_boundary`
- A1 failure case：`bug_02_no_energy_recompute`
- A1 failure case：`bug_03_height_transpose`
- A2 fixed protocol：`random_pixel@50%`
- A2 fixed protocol：`text@50%`
- A2 expanded-scope：`lena + text@30%`
- A2 expanded-scope：`barbara + center_block@35%`
- A2 expanded-scope：`peppers + random_pixel@70%`
- A2 expanded-scope：`cameraman + random_pixel@30%`
- A2 failure case：`bug_01_missing_mask_constraint`
- A2 failure case：`bug_02_mask_polarity_inverted`
- A2 failure case：`bug_03_sparse_component_written_back`
- A3 首发条目：带噪一维曲线拟合
- A4 首发条目：Poisson 图像融合

## 3. 当前不建议把亮点简化成“题库已经凑到 15 题以上”
- 当前已经整理出 `16` 个正式条目，数量上已达到中期够用版本。
- 但目前仓库最强的地方仍然是“主案例闭环”和“benchmark 资产完整”，不是单纯“题目数量变多”。
- 因此更适合按三层来写题库，而不是只报一个总数：
  - 题目家族
  - 固定协议 case / 子任务
  - curated failure case
- A3 / A4 现在已经完成首发条目冻结，但还没有进入固定协议 / 正式实验。

## 4. 建议采用的题库计数口径
建议中期材料不要把所有 run 都硬算成“题目数”，而是分三层写：

### 层 1：主案例家族
- A1
- A2

### 层 2：固定协议与 failure-case 子条目
- A1 width / height
- A1 bug_01 / bug_02 / bug_03
- A2 fixed protocol case 1 / case 2
- A2 expanded-scope representative case 1 / 2 / 3 / 4
- A2 bug_01 / bug_02 / bug_03
- A3 首发条目
- A4 首发条目

### 层 3：后续待扩展方向
- A3 后续候选：昆虫分类
- A4 后续候选：微分方程模型

## 5. 中期阶段建议写法
建议中期材料写成：

> 当前题库已完成 A1 / A2 两个主案例家族的闭环实现，并形成固定协议、A2 expanded-scope 代表案例、failure-case benchmark 与正式索引页；A3 / A4 也已各冻结 1 个首发条目并补齐 requirement 与 taskcard_v1，因此当前题库已经达到中期够用的版本。

## 6. 下一步最小动作
1. 中期阶段先用这 16 个正式条目稳定展示题库层次，不再继续靠 rerun 扩条目数。
2. 中期后再给 A3 / A4 首发条目补固定协议、failure case 与实验链路。
3. 结题前再把题库从“主案例 + benchmark + 首发扩展条目”扩到更完整的 `20+` 条与更多任务家族。
