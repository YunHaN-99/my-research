# bug repair direct_answer v0

模式：`direct_answer`
目的：只给 symptom + buggy code，不给 Task Card 和错误清单，观察模型能否自行定位根因并完成最小修补。

输入给模型的最小信息：
1. failure case 的 `symptom.md`
2. failure case 的 `buggy_code.py`
3. 目标：保留原函数接口，给出 diagnosis + patched code + 简短回归说明

统一约束：
- 不允许重写成无关的新接口。
- patch 以修主错误为准，不以“绕开报错”为准。
- 不向模型暴露 `diagnosis.md` 或 `fixed_code.py`。

评估执行：
- 按 `report/a2_bug_repair_protocol_v0.md` 固定协议跑。
- 结果填入 `metrics/a2_failure_repair_eval_v0.csv`。
