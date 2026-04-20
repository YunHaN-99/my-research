# Task Bank Index v1

## 目的
把当前题库按“主案例家族 / 固定协议与子任务 / failure cases”三层整理成正式索引页，避免中期材料继续用 run 数量代替题库结构。

## 1. 当前阶段判断
- 当前最准确的表述是：主案例已闭环，题库主干已成型，并已补到中期够用的正式条目规模。
- 若按“中期正式题库条目”计数，当前已可稳定列出 `16` 个条目：
  - A1：`2` 个主任务 + `3` 个 failure cases
  - A2：`2` 个 fixed protocol + `4` 个 expanded-scope 代表案例 + `3` 个 failure cases
  - A3：`1` 个首发条目
  - A4：`1` 个首发条目
- A1 / A2 已经形成可复查的主案例家族。
- A3 / A4 已从 placeholder 推进到“首发条目已冻结”的状态，但尚未进入固定协议和正式实验阶段。
- direct / plain / CoE 的重复 rerun 属于证据材料，不应继续直接计入题库条目数。

## 2. 第 1 层：主案例家族

| family_id | family | 当前状态 | 代表材料 | 说明 |
|---|---|---|---|---|
| A1 | `Seam Carving` | `completed` | `task_cards/A1_seam_carving_taskcard_v1.md`, `report/a1_eval_protocol_v0.md`, `report/a1_bug_repair_summary_v0.md` | 已完成主案例、固定协议复现与 bug-repair benchmark |
| A2 | `hw2-op2/src/chapter5_rslt.py::rslt_inpainting(...)` | `completed` | `problems/a2_requirement.md`, `task_cards/A2_rslt_inpainting_taskcard_v1.md`, `report/a2_eval_protocol_v0.md`, `report/a2_bug_repair_summary_v0.md` | 已完成范围收束，并形成 fixed-protocol / bug-repair / expanded-scope / fresh-generation 证据链 |
| A3 | `curve fitting` 首发条目 | `entry_frozen` | `problems/a3_requirement.md`, `task_cards/A3_taskcard_v1.md` | 已完成首发条目冻结，作为中期扩展家族入口 |
| A4 | `Poisson image blending` 首发条目 | `entry_frozen` | `problems/a4_requirement.md`, `task_cards/A4_taskcard_v1.md` | 已完成首发条目冻结，作为中期扩展家族入口 |

## 3. 第 2 层：固定协议、扩展子任务与首发条目

| entry_id | 所属家族 | 条目 | 当前状态 | 主要依据 |
|---|---|---|---|---|
| A1.width | A1 | width shrink | `completed` | `task_cards/A1_seam_carving_taskcard_v1.md`, `report/a1_eval_protocol_v0.md` |
| A1.height | A1 | height shrink | `completed` | `task_cards/A1_seam_carving_taskcard_v1.md`, `report/a1_eval_protocol_v0.md` |
| A2.random_pixel_50 | A2 | fixed protocol: `random_pixel@50%` | `completed` | `task_cards/A2_rslt_inpainting_taskcard_v1.md`, `report/a2_eval_protocol_v0.md` |
| A2.text_50 | A2 | fixed protocol: `text@50%` | `completed` | `task_cards/A2_rslt_inpainting_taskcard_v1.md`, `report/a2_eval_protocol_v0.md` |
| A2.exp_lena_text_30 | A2 | expanded-scope: `lena + text@30%` | `completed` | `report/a2_expanded_scope_protocol_v0.md`, `report/a2_expanded_scope_selected_entries_v1.md` |
| A2.exp_barbara_center_block_35 | A2 | expanded-scope: `barbara + center_block@35%` | `completed` | `report/a2_expanded_scope_protocol_v0.md`, `report/a2_expanded_scope_selected_entries_v1.md` |
| A2.exp_peppers_random_70 | A2 | expanded-scope: `peppers + random_pixel@70%` | `completed` | `report/a2_expanded_scope_protocol_v0.md`, `report/a2_expanded_scope_selected_entries_v1.md` |
| A2.exp_cameraman_random_30 | A2 | expanded-scope: `cameraman + random_pixel@30%` | `completed` | `report/a2_expanded_scope_protocol_v0.md`, `report/a2_expanded_scope_selected_entries_v1.md` |
| A3.curve_fitting | A3 | 首发条目：带噪一维曲线拟合 | `entry_frozen` | `problems/a3_requirement.md`, `task_cards/A3_taskcard_v1.md` |
| A4.poisson_blending | A4 | 首发条目：Poisson 图像融合 | `entry_frozen` | `problems/a4_requirement.md`, `task_cards/A4_taskcard_v1.md` |

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

> 当前题库已完成 A1 / A2 两个主案例家族的闭环，并整理出固定协议子任务、A2 expanded-scope 代表案例与 curated failure cases 的正式索引页；A3 / A4 也已各冻结 1 个首发条目并补齐 requirement 与 taskcard_v1，因此当前题库已达到中期可展示、层次清晰的版本。

## 7. 下一步最小动作
1. 以这 16 个正式条目作为中期题库展示面，不再用 rerun 数量硬充题目数。
2. 中期后先做 `1` 次内部 dry run，并用当前最贴近主结论的 `T2_A1_bug_01` / `T3_A2_bug_01` 跑首轮 `4` 人小样本。
3. 首轮试用稳定后，再给 A3 / A4 首发条目补固定协议、failure case 和实验链路。
4. 结题前再决定是否把题库从当前中期版扩展到更完整的 `20+` 条与更多任务家族。
