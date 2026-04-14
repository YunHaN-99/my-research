# Task Bank Index v1

## 目的
把当前题库按“主案例家族 / 固定协议与子任务 / failure cases”三层整理成正式索引页，避免中期材料继续用 run 数量代替题库结构。

## 1. 当前阶段判断
- 当前最准确的表述不是“题库已经凑够 15 题”，而是“主案例已闭环，题库骨架已成型，扩展条目正在接入”。
- A1 / A2 已经形成可复查的主案例家族。
- A3 / A4 已建立占位 task card，但尚未进入 requirement、固定协议和正式实验阶段。
- direct / plain / CoE 的重复 rerun 属于证据材料，不应继续直接计入题库条目数。

## 2. 第 1 层：主案例家族

| family_id | family | 当前状态 | 代表材料 | 说明 |
|---|---|---|---|---|
| A1 | `Seam Carving` | `completed` | `task_cards/A1_seam_carving_taskcard_v1.md`, `report/a1_eval_protocol_v0.md`, `report/a1_bug_repair_summary_v0.md` | 已完成主案例、固定协议复现与 bug-repair benchmark |
| A2 | `hw2-op2/src/chapter5_rslt.py::rslt_inpainting(...)` | `completed` | `problems/a2_requirement.md`, `task_cards/A2_rslt_inpainting_taskcard_v1.md`, `report/a2_eval_protocol_v0.md`, `report/a2_bug_repair_summary_v0.md` | 已完成范围收束，并形成 fixed-protocol / bug-repair / expanded-scope / fresh-generation 证据链 |
| A3 | 扩展家族占位 | `placeholder` | `task_cards/A3_taskcard_v0.md` | 当前只完成题库入口占位，不进入“已完成主案例”判断 |
| A4 | 扩展家族占位 | `placeholder` | `task_cards/A4_taskcard_v0.md` | 当前只完成题库入口占位，不进入“已完成主案例”判断 |

## 3. 第 2 层：固定协议与子任务

| entry_id | 所属家族 | 条目 | 当前状态 | 主要依据 |
|---|---|---|---|---|
| A1.width | A1 | width shrink | `completed` | `task_cards/A1_seam_carving_taskcard_v1.md`, `report/a1_eval_protocol_v0.md` |
| A1.height | A1 | height shrink | `completed` | `task_cards/A1_seam_carving_taskcard_v1.md`, `report/a1_eval_protocol_v0.md` |
| A2.random_pixel_50 | A2 | fixed protocol: `random_pixel@50%` | `completed` | `task_cards/A2_rslt_inpainting_taskcard_v1.md`, `report/a2_eval_protocol_v0.md` |
| A2.text_50 | A2 | fixed protocol: `text@50%` | `completed` | `task_cards/A2_rslt_inpainting_taskcard_v1.md`, `report/a2_eval_protocol_v0.md` |

## 4. 第 3 层：Failure Cases

| entry_id | 所属家族 | failure case | 当前状态 | 主要依据 |
|---|---|---|---|---|
| A1.bug_01 | A1 | `bug_01_dp_boundary` | `completed` | `task_cards/A1_bug_repair_taskcard_v0.md`, `report/a1_bug_repair_protocol_v0.md` |
| A1.bug_02 | A1 | `bug_02_no_energy_recompute` | `completed` | `task_cards/A1_bug_repair_taskcard_v0.md`, `report/a1_bug_repair_protocol_v0.md` |
| A1.bug_03 | A1 | `bug_03_height_transpose` | `completed` | `task_cards/A1_bug_repair_taskcard_v0.md`, `report/a1_bug_repair_protocol_v0.md` |
| A2.bug_01 | A2 | `bug_01_missing_mask_constraint` | `completed` | `task_cards/A2_bug_repair_taskcard_v0.md`, `report/a2_bug_repair_protocol_v0.md` |
| A2.bug_02 | A2 | `bug_02_mask_polarity_inverted` | `completed` | `task_cards/A2_bug_repair_taskcard_v0.md`, `report/a2_bug_repair_protocol_v0.md` |
| A2.bug_03 | A2 | `bug_03_sparse_component_written_back` | `completed` | `task_cards/A2_bug_repair_taskcard_v0.md`, `report/a2_bug_repair_protocol_v0.md` |

## 5. 当前不计入题库条目数的材料
- direct / plain_guidance / coe_guided 的同类 rerun
- expanded-scope validation 的 16-case 扩展稳健性记录
- fresh-generation replication
- run 文档本身

这些内容仍然重要，但它们应被归类为“支撑主案例和子条目的证据链”，而不是额外的题库条目。

## 6. 中期建议写法
建议中期材料使用下面这句：

> 当前题库已完成 A1 / A2 两个主案例家族的闭环，并整理出固定协议子任务与 curated failure cases 的正式索引页；A3 / A4 已建立扩展占位 task card，正在接入下一阶段的 requirement、协议与评测链路。

## 7. 下一步最小动作
1. 从 A3 / A4 各自候选方向中先冻结 1 个首发条目。
2. 给冻结后的 A3 / A4 条目补 `requirement` 与 `taskcard_v1`。
3. 再决定是否把题库从当前骨架扩展到更完整的 `v1 (>=15 题)`。
