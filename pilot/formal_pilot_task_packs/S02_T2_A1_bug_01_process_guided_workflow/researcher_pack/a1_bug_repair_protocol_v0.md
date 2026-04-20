# A1 Bug Repair Protocol v0

## 固定 benchmark 对象
1. bug_01_dp_boundary
2. bug_02_no_energy_recompute
3. bug_03_height_transpose

## 固定 guidance mode
1. direct_answer
2. plain_guidance
3. coe_guided

## 固定总规模
- 3 bugs x 3 modes = 9 runs

## 每次 run 允许给模型的材料

### direct_answer
1. 对应 bug 的 symptom.md
2. 对应 bug 的 buggy_code.py

### plain_guidance
1. 对应 bug 的 symptom.md
2. 对应 bug 的 buggy_code.py
3. task_cards/A1_seam_carving_taskcard_v1.md
4. task_cards/A1_bug_repair_taskcard_v0.md

### coe_guided
1. 对应 bug 的 symptom.md
2. 对应 bug 的 buggy_code.py
3. task_cards/A1_seam_carving_taskcard_v1.md
4. task_cards/A1_bug_repair_taskcard_v0.md
5. prompts/a1/bug_repair_coe_v0.md 规定的固定角色结构

## scorer-only 材料
以下材料只用于人工评分与复核，不允许在生成阶段暴露给模型：
1. diagnosis.md
2. fixed_code.py

## 固定交付物
每次 run 至少保留以下内容：
1. diagnosis：主错误定位
2. patched code：修补后的代码
3. regression notes：最小回归说明
4. run 文档：记录首轮表现、修补轮次、耗时和结论
5. metrics/a1_failure_repair_eval_v0.csv 中 1 行结果

## 评分口径

### diagnosis_correct
- 1：主错误定位与 diagnosis.md 一致，至少命中根因层面
- 0：只描述表象，或定位到次要问题

### patch_runnable
- 1：patch 后代码能保持原接口导入/替换，不存在显式语法错误或明显契约破坏
- 0：patch 代码本身不可用，或无法替换到原调用位置

### regression_pass
- 1：修补后不再触发原主错误，且满足该 bug 的关键不变量
- 0：原问题仍在，或修补引入新的关键回归

## bug-specific 回归检查

### bug_01_dp_boundary
- j=0 与 j=w-1 时只读取合法父节点
- backtrack 记录不越界

### bug_02_no_energy_recompute
- seam 删除循环中每轮都重算 energy
- energy.shape 始终与当前 out.shape[:2] 一致

### bug_03_height_transpose
- 彩色图像只交换 H/W 轴，不改变通道轴位置
- 两次转置后语义仍回到 (H, W, C)

## 执行纪律
- 所有 bug-repair run 使用同一批 failure case 材料，不换题、不扩题。
- 同一 bug 的三个 mode 必须使用同样的 symptom.md 和 buggy_code.py。
- 如果某次 run 偏离本协议，必须在对应 run 文档和 metrics notes 中显式记录。
- 每完成一次 run，立刻补 run 文档与 metrics 行，不留待事后回忆。
