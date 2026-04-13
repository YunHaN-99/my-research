# coe multi role v0

模式：coe_guided
目的：在 A2 主任务上使用固定多角色结构输出，提升可复现性、可检查性与纠错稳定性。

输入材料（必须提供）：
1. A2 题目要求
2. `task_cards/A2_rslt_inpainting_taskcard_v1.md`
3. `report/a2_eval_protocol_v0.md`
4. 当前实现代码与运行日志（如果有）

统一约束：
1. 主接口为 `rslt_inpainting(observed, mask, ...)`
2. 固定协议只做 grayscale masked repair
3. 不进入 GUI / video / TILT / chapter7 扩展
4. 后续所有 A2 CoE run 必须使用以下固定标题

## Role 1 Reader
- 题目重述
- 输入 / 输出
- 验收条件

## Role 2 Planner
- 算法步骤
- 函数拆分
- 核心不变量

## Role 3 Coder
- 代码骨架
- 关键实现
- 需要自检的断言

## Role 4 Reviewer
- 对照 Task Card 的常见错误逐项检查
- 列出最可能失败点
- 给修复建议

Reviewer 检查表：
1. mask 约束丢失
2. patch group shape 错
3. aggregation / weight_map 出错
4. history / metrics 记录缺失
5. dtype / 数值范围异常

## Role 5 Experimenter
- 固定测试图
- 固定 corruption
- 固定记录项
- 结果总结

评估落地：
1. 严格按 `report/a2_eval_protocol_v0.md` 运行。
2. 结果记录到对应 run 文档。
3. 指标写入 `metrics/a2_guidance_eval_v0.csv` 与 `metrics/a2_recovery_perf_v0.csv`。
