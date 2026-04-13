# baseline direct_answer v0

模式：direct_answer
目的：只给 A2 的题目要求，不给 Task Card，不给错误清单，观察模型直接产出 `rslt_inpainting(...)` 代码时的稳定性。

输入给模型的最小信息：
1. A2 主任务：基于 patch-group RPCA 的灰度图像修复
2. 目标函数：`rslt_inpainting(observed, mask, ...)`
3. 输出要求：可运行代码 + 固定协议下的恢复结果 + metrics 记录
4. 限制：当前阶段只做 grayscale masked repair，不进入 GUI / video / 其他 chapter

评估执行：
- 按 `report/a2_eval_protocol_v0.md` 固定协议跑。
- 结果填入 `metrics/a2_guidance_eval_v0.csv` 与 `metrics/a2_recovery_perf_v0.csv`。
