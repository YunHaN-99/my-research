# Prompt Template Library v1

## 目的
把仓库中已经验证过的 prompt 资产整理成可直接引用的模板库，供中期材料、后续扩展任务和统一 run 规范复用。

## 1. A1 主案例模板

### A1 baseline direct answer
- file: `prompts/a1/baseline_direct_answer_v0.md`
- 用途：只给题目要求，不给 Task Card 和错误清单，观察模型直接产出代码时的稳定性。
- 典型输入材料：
  - A1 题目要求
  - 主接口 `seam_carve_image(im, sz)`
  - shrink-only 约束
- 典型输出：
  - 可运行代码
  - 基本对比图
  - run 记录与 guidance 指标

### A1 baseline plain guidance
- file: `prompts/a1/baseline_plain_guidance_v0.md`
- 用途：在 direct-answer 基础上加入 `task_cards/A1_seam_carving_taskcard_v1.md`，提升任务边界和自检可检查性。
- 必要输入：
  - A1 题目要求
  - `task_cards/A1_seam_carving_taskcard_v1.md`
  - shrink-only 约束

### A1 CoE multi-role
- file: `prompts/a1/coe_multi_role_v0.md`
- 用途：固定多角色结构，增强题目重述、算法规划、Reviewer 检查和实验记录的一致性。
- 固定角色：
  - Reader
  - Planner
  - Coder
  - Reviewer
  - Experimenter
- 适用场景：
  - 主实验
  - 需要完整自检轨迹的复现实验

## 2. A1 bug-repair 模板

### A1 bug-repair direct answer
- file: `prompts/a1/bug_repair_direct_answer_v0.md`
- 用途：只给 `symptom + buggy_code`，观察模型能否自行定位根因并给出最小补丁。

### A1 bug-repair plain guidance
- file: `prompts/a1/bug_repair_plain_guidance_v0.md`
- 用途：在 bug-repair 中加入 Task Card / 不变量 / regression checklist。

### A1 bug-repair CoE
- file: `prompts/a1/bug_repair_coe_v0.md`
- 用途：固定 Reader / Diagnoser / Patcher / Reviewer / Regressor 结构，提升 bug-repair 的诊断可追踪性。

## 3. A2 主案例模板

### A2 baseline direct answer
- file: `prompts/a2/baseline_direct_answer_v0.md`
- 用途：只给 A2 题目要求，不给 Task Card 和错误清单，观察模型直接实现 `rslt_inpainting(...)` 的稳定性。
- 当前任务口径：
  - `hw2-op2` chapter5
  - grayscale masked repair
  - 固定协议 `lena / barbara x random_pixel@50% / text@50%`

### A2 baseline plain guidance
- file: `prompts/a2/baseline_plain_guidance_v0.md`
- 用途：给 A2 题目要求 + `task_cards/A2_rslt_inpainting_taskcard_v1.md` + fixed protocol，提升 mask 约束和输出完整性的自检能力。

### A2 CoE multi-role
- file: `prompts/a2/coe_multi_role_v0.md`
- 用途：在 A2 主任务上固定多角色结构，提升可复现性、可检查性与纠错稳定性。
- 固定角色：
  - Reader
  - Planner
  - Coder
  - Reviewer
  - Experimenter
- 固定 Reviewer 检查项：
  - mask 约束丢失
  - patch group shape 错
  - aggregation / weight_map 出错
  - history / metrics 记录缺失
  - dtype / 数值范围异常

## 4. A2 bug-repair 模板

### A2 bug-repair direct answer
- file: `prompts/a2/bug_repair_direct_answer_v0.md`
- 用途：只给 `symptom + buggy_code`，观察模型能否自行定位 A2 核心实现语义错误。

### A2 bug-repair plain guidance
- file: `prompts/a2/bug_repair_plain_guidance_v0.md`
- 用途：在 bug-repair 中显式加入 A2 Task Card、不变量和 regression checklist。

### A2 bug-repair CoE
- file: `prompts/a2/bug_repair_coe_v0.md`
- 用途：固定 Reader / Diagnoser / Patcher / Reviewer / Regressor 结构，增强根因说明与回归说明的可检查性。

## 5. Run 文档模板

### A1 bug-repair run template
- file: `runs/a1_bug_repair_run_template_v0.md`
- 用途：统一记录输入材料、首轮诊断、补丁路径、回归结果和 CSV 回填信息。

### A2 guidance run template
- file: `runs/a2_guidance_run_template_v0.md`
- 用途：统一记录 fixed protocol checklist、prompt 路径、输出产物和 recovery 指标。

### A2 bug-repair run template
- file: `runs/a2_bug_repair_run_template_v0.md`
- 用途：统一记录 bug-repair benchmark 的症状、补丁、回归与指标回填。

## 6. 使用规则
- 同一任务族内不要混用不同口径的 A2 定义；当前统一以 `hw2-op2/src/chapter5_rslt.py::rslt_inpainting(...)` 为主案例。
- `direct_answer / plain_guidance / coe_guided` 应始终作为固定研究级对照出现，避免临时新增模式打乱可比性。
- bug-repair 场景要严格区分：
  - 可以给模型看的材料
  - scorer-only 参考材料
- 所有模板都应落回：
  - run 文档
  - `metrics/*.csv`
  - 对应输出目录

## 7. 当前状态
- 模板资产已经覆盖：
  - A1 主实验
  - A1 bug-repair
  - A2 主实验
  - A2 bug-repair
- 仍待补充：
  - A3 / A4 扩展任务模板
  - 更接近教学演示的 Notebook / CLI 交互模板
