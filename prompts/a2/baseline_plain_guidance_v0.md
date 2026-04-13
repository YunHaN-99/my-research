# baseline plain_guidance v0

模式：plain_guidance
目的：给 A2 题目要求 + Task Card v1，但不使用多角色分工，观察普通结构化指导对实现与自检的帮助。

输入给模型的信息：
1. A2 题目要求
2. `task_cards/A2_rslt_inpainting_taskcard_v1.md`
3. `report/a2_eval_protocol_v0.md`
4. 约束：优先保证可运行、mask 约束正确、固定 4 个 case 可复现

交付要求：
1. 代码
2. 关键自检点
3. 固定协议结果
4. run 记录与 metrics 条目

评估执行：
- 按 `report/a2_eval_protocol_v0.md` 固定协议跑。
- 结果填入 `metrics/a2_guidance_eval_v0.csv` 与 `metrics/a2_recovery_perf_v0.csv`。
