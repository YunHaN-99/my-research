# Prototype Outline v0

## 目的
说明当前仓库已经具备的自动化链路，以及后续教学原型应如何从现有脚本演化出来。

## 1. 当前已经存在的“原型雏形”
当前仓库已经补出一个最小 CLI 入口 `run_research_case.py`，并且在此之前就已经具备一条可复用的 headless 自动化链路：

1. 读取题目要求、Task Card、protocol 和 prompt。
2. 生成或收集代码 artifact。
3. 按固定协议执行评测或 bug-repair benchmark。
4. 产出：
   - `runs/*.md`
   - `outputs/*`
   - `metrics/*.csv`
   - `report/*.md`

这意味着当前并非“没有原型”，而是“原型能力先以脚本链路存在，现已补成一个最小统一 CLI 入口”。

## 2. 当前可复用的脚本链路

### A1
- 主比较脚本：`solutions/hw1_op1/src/run_step6_comparisons.py`
- 首轮可运行入口：`solutions/hw1_op1/src/run_first_working_width_only.py`

### A2
- bug-repair benchmark：`solutions/hw2_op2/run_a2_bug_repair_benchmark.py`
- expanded-scope validation：`solutions/hw2_op2/run_a2_expanded_scope_validation.py`
- fresh-generation replication：`solutions/hw2_op2/run_a2_fresh_generation_replication.py`

## 3. 当前原型能力已经能演示什么
- 固定输入材料如何进入任务链路。
- 三种 prompt 模式如何形成不同的过程痕迹。
- 如何把结果稳定落到 run 文档、metrics 表和输出目录。
- 如何用固定协议与 failure-case benchmark 做可复查评估。

## 4. 当前还缺什么，才算“可展示原型”

### 缺 1：更完整的用户导向流程
- 现在已有最小 CLI 入口，但还不是“输入新题目后自动走完整链路”的统一执行器。

### 缺 2：用户导向说明
- 现在已经有 CLI，但仍更像研究者工作流，不是教学演示工作流。

### 缺 3：过程串联
- 还缺一个显式入口把“输入题目 -> 结构化表示 -> 代码骨架 -> 自检 -> 结果记录”串成一个面向外部读者的连续体验。

## 5. 推荐的最小原型 v0
当前已落地的最小原型 v0 是 CLI，而不是 GUI：

### CLI 最小功能
- 选择主案例：A1 / A2
- 选择模式：direct_answer / plain_guidance / coe_guided
- 选择轨道：baseline / bug-repair / expanded-scope / fresh-generation
- 自动输出：
  - 使用的 prompt
  - 使用的 protocol
  - 对应 run 文档
  - 对应 metrics 摘要

### 当前实现
- 统一入口：`run_research_case.py`
- 说明文档：`report/prototype_cli_v0.md`
- 当前原型定位：选择并展示已有研究资产，不重新发起同类 rerun

### 为什么先做 CLI
- 当前仓库本身已经以脚本和指标表为核心。
- CLI 成本低，最容易把现有自动化链路包装成演示原型。
- 后续若需要，再把 CLI 外包一层 Notebook 或页面。

## 6. 中期材料建议写法
建议中期阶段把原型写成：

> 当前已具备可复用的脚本化研究原型：能够从 prompt / task card / protocol 出发，生成代码 artifact、执行固定协议评测、输出 run 文档与 metrics 表。下一阶段计划将其封装为统一 CLI / Notebook 入口，转化为更适合教学展示的原型形式。

## 7. 下一步最小动作
1. 先用 `run_research_case.py` 作为中期展示入口。
2. 再决定是否需要把当前只读型 CLI 扩成真正可执行新题目的统一入口。
3. 中期前不必强行做 GUI，只要把“现有自动化链路 + 最小 CLI 封装 = 原型雏形”讲清楚即可。
