# Midterm Stage Summary v0

## 1. 当前阶段定位
截至 `2026-04-12`，仓库已经完成 A1 与当前口径下 A2 主案例的闭环实验链路。更准确地说，当前阶段不是“项目全部完成”，而是“首轮主案例已经闭环，中期材料收口正在进行”。

本阶段最重要的进展有两点：
- 已把研究从“泛泛讨论大模型辅助做题”收束成可执行、可评分、可复查的 A1 / A2 主案例流水线。
- 已形成从 prompt、task card、run 文档、metrics 到阶段总结的完整证据链，而不是停留在零散实验截图。

## 2. A1 / A2 主案例口径

### A1
- 主案例：`Seam Carving`
- 研究用途：验证过程化讲解、固定协议复现、failure-case bug repair

### A2
- 当前主案例：`hw2-op2/src/chapter5_rslt.py::rslt_inpainting(...)`
- 研究用途：验证低秩图像任务中的 fixed-protocol 评测、bug-repair、expanded-scope 和 fresh-generation 复现

需要说明的是，`Timeline.docx` 早期把 A2 宽表述为 “SVD 图像压缩”。进入仓库实施阶段后，A2 被收束为同一低秩图像任务族下、但更可复现和可评分的 `chapter5 rslt_inpainting` 主案例。因此，中期材料中应写成“已完成范围收束并完成主案例闭环”，而不是把当前 A2 误判为未做。

## 3. 本阶段已形成的核心资产

### 研究资产
- `task_cards/`：A1 / A2 主任务卡与 bug-repair task card
- `prompts/`：A1 / A2 的 direct_answer / plain_guidance / coe_guided 模板
- `runs/`：每次实验的 run 文档
- `metrics/`：可直接汇总的 guidance / perf / bug-repair / expanded-scope 数据表
- `report/`：协议、总结、阶段报告和中期收口文档

### 方法资产
- 多角色协作流程已经在 A1 / A2 两条主线上稳定落地
- 结构化检查清单已能覆盖输入输出、核心不变量、固定协议和最小自检
- bug-repair benchmark 已具备可重复执行的 failure-case 设计与评分口径

## 4. A1 当前结果

### 已完成内容
- baseline direct_answer / plain_guidance / coe_guided
- fixed-protocol replication
- bug-repair benchmark
- A1 阶段总结

### 当前证据
- `metrics/a1_guidance_eval_v0.csv`：12 条 guidance 记录
- `metrics/a1_codegen_perf_v0.csv`：18 条性能记录
- `metrics/a1_failure_repair_eval_v0.csv`：9 条 bug-repair 记录

### 可支持的结论
- 三种模式在 A1 固定协议下都能稳定达到 runnable 与 correct。
- plain_guidance 与 coe_guided 在 `self_check`、回归说明和可复查性上明显更完整。
- 在当前 3 个 curated failure cases 上，结构化 guidance 更能提升“诊断与复核的清晰度”，而不是显著拉开修复通过率。

## 5. A2 当前结果

### 已完成内容
- baseline
- fixed-protocol replication
- bug-repair benchmark
- expanded-scope validation
- fresh-generation replication

### 当前证据
- `metrics/a2_guidance_eval_v0.csv`：15 条 guidance 记录
- `metrics/a2_recovery_perf_v0.csv`：60 条恢复结果记录
- `metrics/a2_failure_repair_eval_v0.csv`：9 条 bug-repair 记录
- `metrics/a2_expanded_scope_eval_v0.csv`：3 条 expanded-scope 主记录
- `metrics/a2_expanded_scope_perf_v0.csv`：48 条 expanded-scope case 记录

### 可支持的结论
- 三种模式在 A2 固定协议下都能一轮 runnable 且 correct。
- fixed-protocol 的 4 个 case 在 15 次运行中保持完全一致的 `(PSNR, SSIM, RSE)`，说明当前主差异仍主要体现在过程化自检与可复查性。
- expanded-scope validation 说明当前执行链路不只在初始 4 个 fixed cases 上稳定。
- fresh-generation replication 说明当前 A2 不只是“复制旧 artifact 复跑”，而是新产物在同协议下也能回到同一固定结果。

## 6. 本阶段最稳妥的研究结论
- 当前最稳妥、最可辩护的结论是：
  - 结构化 guidance 提升了过程可检查性、根因说明质量和回归说明完整性。
- 当前不宜写成强结论的是：
  - 结构化 guidance 在这两个主案例上普遍提升最终正确率
  - 结构化 guidance 在时间上稳定优于 direct_answer

原因很明确：
- 样本量仍小
- 当前很多 run 是固定协议
- A2 的 fixed-protocol、expanded-scope 和 fresh-generation 都显示最终质量高度一致

## 7. 与 Timeline 的对应关系

### 已满足中期前要求的部分
- A1 / A2 主案例已固定并跑通
- Task Card 已从 bootstrap 发展到可用版本
- metrics 表、run 文档、阶段总结都已形成
- baseline、过程化模板、bug-repair benchmark 已具备可展示证据

### 尚未满足的部分
- 题库 `v1 (>=15 题)` 还未形成
- A3 / A4 扩展条目还未接入
- “输入题目 -> 结构化表示 -> 代码骨架 -> 自检 -> 结果记录”的统一原型还未形成可演示版本
- 小范围试用和学生反馈数据尚未开始

## 8. 中期前最该补的材料
当前最优先的不是继续加同类型 run，而是把已有资产变成中期可提交材料：

1. Timeline 口径对齐说明
2. Prompt 模板库 `v1`
3. 结构化检查清单 `v1`
4. 错误分类与反馈规则 `v1`
5. 阶段小结与附件清单

## 9. 下一步执行顺序
建议按下面顺序推进：

1. 统一 Timeline / 中期材料中的 A2 定义。
2. 用当前 A1 / A2 资产收束模板库、检查清单、错误分类文档。
3. 形成中期提交包，把“已完成”和“仍待开展”分开写清楚。
4. 中期之后再补 A3 / A4、原型和小范围试用。

## 10. 当前阶段判断
- 若按当前仓库主线判断：A1 / A2 主案例都已完成。
- 若按整个 12 个月 Timeline 判断：项目远未全部完成，当前只是“首轮主案例闭环完成 + 中期材料收口阶段”。
