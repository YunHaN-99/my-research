# Timeline Scope Alignment 2026-04-12

## 一句话口径
截至 `2026-04-12`，A2 应统一表述为“低秩图像任务族下，已完成范围收束并完成主案例闭环的 `hw2-op2/src/chapter5_rslt.py::rslt_inpainting(...)` 灰度图像修复案例”，而不是继续沿用早期宽标签 “SVD 图像压缩”。

## 1. 这份说明要解决什么
- 对齐 `Timeline.docx` 早期宽标签与仓库当前冻结口径。
- 避免中期材料里同时出现 “A2 已完成” 和 “A2 未做” 两套互相冲突的判断。
- 把“已经完成什么、现在最稳能说什么、还没做什么”固定成同一套表述。

## 2. A2 范围收束说明

### 原始 Timeline 标签
- `Timeline.docx` 早期把首轮主案例写为：
  - A1：`Seam Carving`
  - A2：`SVD 图像压缩`
- 这个写法更像方向标签，用来描述低秩 / SVD 图像任务方向，而不是已经冻结的最终实验协议。

### 当前冻结口径
- case family：低秩图像任务族
- target project：`hw2-op2`
- target function：`hw2-op2/src/chapter5_rslt.py::rslt_inpainting(...)`
- research question：grayscale masked image repair / inpainting
- evaluation package：
  - baseline
  - fixed-protocol replication
  - bug-repair benchmark
  - expanded-scope validation
  - fresh-generation replication

### 这次收束意味着什么
- 不是脱离原始 A2，而是把早期宽标签收束成可执行、可复现、可评分的单一主案例。
- 不是宣称“整个低秩图像方向都已完成”，而是明确“当前 A2 的主案例闭环已完成”。
- 中期阶段判断对象应是“当前冻结口径下的 A2 主案例”，不是早期尚未细化的宽标签。

### 为什么这样收束是合理的
- `hw2-op2` 中仍保留了 SVD / truncated SVD 的理论和 baseline 背景。
- 当前 A2 已形成任务卡、协议、run 文档、metrics 与阶段总结的完整证据链。
- 继续沿用 “SVD 图像压缩” 宽标签会把“方向”与“主案例”混写，直接导致完成判断失真。

## 3. 统一阶段判断

### 已经完成什么
- A1：`Seam Carving` 主案例闭环已完成。
- A2：`chapter5 rslt_inpainting` 主案例闭环已完成。
- 配套资产：prompt、task card、run 文档、metrics、bug-repair、expanded-scope、fresh-generation 证据链已落地。

### 现在最稳能说什么
- 当前仓库已经完成 A1 / A2 两个主案例的闭环，不再是零散试验。
- 当前最稳妥的研究结论是：结构化 guidance 主要提升过程可检查性、根因说明质量和回归说明完整性。
- 对 A2 来说，当前最强证据不是“最终恢复质量被显著拉开”，而是“在最终指标高度一致时，结构化 guidance 仍能提供更好的可复查过程”。

### 还没做什么
- 题库 `v1 (>=15 题)` 还未整理完成。
- A3 / A4 已接入占位条目，但尚未进入 requirement / 固定协议 / 正式实验主线。
- 统一原型尚未形成可演示版本。
- 小范围试用、学生反馈和后续量化对照尚未启动。

## 4. 中期材料推荐写法
建议统一使用下面这段话：

> 截至 `2026-04-12`，A1 `Seam Carving` 主案例已完成闭环。A2 在早期 Timeline 中曾被宽表述为 “SVD 图像压缩”，但进入仓库实施阶段后，为提高可复现性和可评分性，已收束为低秩图像任务族下的 `hw2-op2/src/chapter5_rslt.py::rslt_inpainting(...)` 灰度图像修复主案例。当前 A2 已完成 baseline、fixed-protocol replication、bug-repair benchmark、expanded-scope validation 与 fresh-generation replication，因此中期阶段应将其表述为“已完成范围收束并完成主案例闭环”，而不是简单按早期宽标签判断为未完成。

## 5. 中期材料中不宜再出现的写法
- “A2 原计划未做。”
- “A2 仍然等同于 SVD 图像压缩全部范围。”
- “当前证据已经足以证明结构化 guidance 显著提升最终恢复质量。”

## 6. 直接可引用的证据
- `README.md`
- `problems/a2_requirement.md`
- `task_cards/A2_rslt_inpainting_taskcard_v1.md`
- `report/a2_eval_protocol_v0.md`
- `report/phase2_progress_report_2026-04-12.md`
- `report/midterm_stage_summary_v0.md`
