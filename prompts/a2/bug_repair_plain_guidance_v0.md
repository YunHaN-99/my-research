# bug repair plain_guidance v0

模式：`plain_guidance`
目的：给 symptom + buggy code + Bug Repair Task Card，但不使用多角色分工，观察普通结构化指导对诊断与修补的帮助。

输入给模型的信息：
1. failure case 的 `symptom.md`
2. failure case 的 `buggy_code.py`
3. `task_cards/A2_rslt_inpainting_taskcard_v1.md`
4. `task_cards/A2_bug_repair_taskcard_v0.md`

统一交付：
1. diagnosis：主错误定位
2. patch plan：准备如何改
3. patched code：最小修补版本
4. regression checklist：说明为什么补丁不会复发同类错误

统一约束：
- 保持函数名、参数和返回契约不变。
- 只修与当前 bug 直接相关的主错误。
- 不向模型暴露 `diagnosis.md` 或 `fixed_code.py`。

评估执行：
- 按 `report/a2_bug_repair_protocol_v0.md` 固定协议跑。
- 结果填入 `metrics/a2_failure_repair_eval_v0.csv`。
