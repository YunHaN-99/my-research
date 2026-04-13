# bug repair coe v0

模式：`coe_guided`
目的：在 bug-repair 任务上使用固定多角色结构，提升主错误定位的完整度、patch 可检查性与回归说明质量。

输入材料（必须提供）：
1. failure case 的 `symptom.md`
2. failure case 的 `buggy_code.py`
3. `task_cards/A2_rslt_inpainting_taskcard_v1.md`
4. `task_cards/A2_bug_repair_taskcard_v0.md`

统一约束：
1. 只修当前 bug，不扩写无关重构。
2. 保持原函数接口与返回约定。
3. 不允许把 `diagnosis.md` 或 `fixed_code.py` 当作输入。
4. 后续所有 A2 bug-repair CoE run 必须使用以下固定标题。

## Role 1 Reader
- 重述 symptom
- 说明目标行为
- 提取当前代码接口

## Role 2 Diagnoser
- 给出主错误定位
- 区分根因与表象
- 说明被破坏的不变量

## Role 3 Patcher
- 给出最小 patch 方案
- 输出 patched code
- 解释为何不改动无关逻辑

## Role 4 Reviewer
- 检查接口是否保持一致
- 检查 patch 是否真的修到根因
- 检查是否引入新的 mask / patch / RPCA 语义回归
- 检查是否出现写死常数或临时绕过

## Role 5 Regressor
- 给出最小回归检查
- 说明该 bug 的关键通过条件
- 输出最终是否建议交付

评估落地：
1. 严格按 `report/a2_bug_repair_protocol_v0.md` 执行。
2. 结果记录到对应 run 文档。
3. 指标写入 `metrics/a2_failure_repair_eval_v0.csv`。
