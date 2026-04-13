# A2 failure-case design v0

## Scope
- target task: `hw2-op2/src/chapter5_rslt.py::rslt_inpainting(...)`
- target phase: A2 bug-repair benchmark preparation
- design goal: 用 3 个最小失败样例覆盖 A2 最关键、最容易被模型写错的不变量

## 选题原则
1. bug 必须贴着 `rslt_inpainting` 主循环，而不是外围展示代码。
2. bug 要能在固定协议 `lena / barbara x random_pixel@50% / text@50%` 下解释清楚。
3. 每个 bug 都要有明确的根因、不变量和最小修补点。
4. 三个 bug 尽量覆盖不同层面：mask 约束、mask 语义、RPCA 分量语义。

## Curated bugs

### 1. bug_01_missing_mask_constraint
- 主错误：聚合后忘记重新施加观测像素约束。
- 破坏的不变量：`mask > 0.5` 区域必须始终与 `observed` 一致。
- 典型 symptom：代码能跑，但 clean pixels 被 patch 聚合结果改写。

### 2. bug_02_mask_polarity_inverted
- 主错误：把 `mask == 0` 当成观测像素。
- 破坏的不变量：A2 里 `1 = observed`, `0 = missing/corrupted` 的语义必须全流程一致。
- 典型 symptom：缺失区几乎不被修复，反而观测区被不断改写。

### 3. bug_03_sparse_component_written_back
- 主错误：把 RPCA 的 `sparse` 分量写回图像，而不是 `low_rank`。
- 破坏的不变量：低秩分量是恢复主信号，稀疏分量只表示异常/污染。
- 典型 symptom：函数能跑，但输出像残差图，恢复指标显著劣化。

## 当前结论
- A2 bug-repair benchmark 已具备最小材料：
  - `task_cards/A2_bug_repair_taskcard_v0.md`
  - `report/a2_bug_repair_protocol_v0.md`
  - `solutions/hw2_op2/failure_cases/`
  - `prompts/a2/bug_repair_*.md`
  - `runs/2026-04-12_a2_bug_repair_queue_v0.md`
- 下一步应执行 9 个固定 bug-repair runs，而不是继续增加新的 failure case 数量。

## Boundary
- 当前 failure cases 是 curated benchmark，不代表 A2 全部可能错误类型。
- 本轮只覆盖 `rslt_inpainting` 的核心实现，不覆盖 GUI、彩图、多章节比较或视频分支。
