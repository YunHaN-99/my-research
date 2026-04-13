# Timeline Scope Alignment 2026-04-12

## 目的
这份说明用于把 `Timeline.docx` 的原始阶段表述，与仓库当前已经落地的 A1 / A2 主案例口径对齐，避免中期材料中同时出现两套互相冲突的 A2 定义。

## 原始 Timeline 表述
- `Timeline.docx` 将首轮主案例写为：
  - `A1 接缝裁剪（Seam Carving）`
  - `A2 SVD 图像压缩`
- 同一份 Timeline 对中期前的验收重点写得更偏“主案例跑通、模板库、指标表、完整 run 记录”，而不是强绑定某个具体章节函数名。

## 仓库当前实际主线
- A1 保持不变：`Seam Carving`
- A2 已从早期宽表述收束为：
  - 低秩图像任务族下的主案例
  - 最终固定为 `hw2-op2/src/chapter5_rslt.py::rslt_inpainting(...)`
  - 研究问题是 grayscale masked image repair / inpainting
- A2 当前配套资产已经完整落地：
  - `problems/a2_requirement.md`
  - `task_cards/A2_rslt_inpainting_taskcard_v1.md`
  - `report/a2_eval_protocol_v0.md`
  - `report/a2_bug_repair_protocol_v0.md`
  - `report/a2_failure_case_design_v0.md`
  - `metrics/a2_*.csv`
  - `runs/2026-04-12_run_030` 到 `run_057` 对应的 run 文档与产物

## 为什么这不应被表述为 “A2 未完成”
- 原始 Timeline 中的 “A2 SVD 图像压缩” 更像是一个早期方向标签，而不是已经冻结的最终实验协议。
- 当前仓库并没有偏离“低秩图像教学任务 + 可量化评估”这条研究主线，而是把 A2 从过宽的任务名，收束成了更可执行、可复现、可评分的 `chapter5 rslt_inpainting` 主案例。
- `hw2-op2` 中仍然保留了 SVD / truncated SVD 的理论和 baseline 资产，因此当前 A2 不是完全脱离原始 A2，而是从 “SVD 图像任务” 收束到了 “以低秩方法为背景的图像修复主案例”。

## 建议采用的统一表述
- A1：`Seam Carving` 主案例，用于验证过程化指导、固定协议复现与 bug-repair benchmark。
- A2：低秩图像任务族主案例，最终聚焦 `chapter5 rslt_inpainting` 的灰度图像修复，用于验证固定协议评测、bug-repair、expanded-scope 与 fresh-generation 复现。

## 按当前口径的完成判断

### A1
- 可直接判断为：`completed`
- 理由：
  - baseline / replication / bug-repair 都已完成
  - 协议、指标、run 文档、输出图、阶段总结都已落地

### A2
- 若按当前仓库口径判断：`completed`
- 若按 Timeline 原始字面 “A2 SVD 图像压缩” 判断：`存在名称与边界漂移，不宜直接按字面写 completed`
- 更准确的中期写法应为：
  - “A2 已完成范围收束，并在当前冻结口径下完成主案例闭环。”

## 中期材料推荐写法
建议在中期材料中使用下面这段话：

> 课题早期规划中将 A2 宽表述为 “SVD 图像压缩”。进入仓库实施阶段后，为提高可复现性和可评分性，A2 被收束为同一低秩图像任务族下的 `chapter5 rslt_inpainting` 主案例。该主案例保留了 SVD / 低秩方法背景，同时形成了更稳定的 fixed-protocol、bug-repair、expanded-scope 与 fresh-generation 评测链路。因此，中期阶段应将 A2 视为“已完成范围收束并完成主案例闭环”，而不是简单按早期宽标签判断为未完成。

## 直接可引用的证据
- `README.md`
- `problems/a2_requirement.md`
- `task_cards/A2_rslt_inpainting_taskcard_v1.md`
- `report/a2_eval_protocol_v0.md`
- `report/phase2_progress_report_2026-04-12.md`
- `report/midterm_stage_summary_v0.md`
