# Prototype Outline v0

## 目的
说明当前仓库已经具备的自动化链路，以及后续教学原型应如何从现有脚本演化出来。

## 1. 当前已经存在的“原型雏形”
当前仓库还没有统一的 Notebook / CLI 交互入口，但已经具备一条可复用的 headless 自动化链路：

1. 读取题目要求、Task Card、protocol 和 prompt。
2. 生成或收集代码 artifact。
3. 按固定协议执行评测或 bug-repair benchmark。
4. 产出：
   - `runs/*.md`
   - `outputs/*`
   - `metrics/*.csv`
   - `report/*.md`

这意味着当前并非“没有原型”，而是“原型能力已经存在，但尚未封装成单一入口”。

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

### 缺 1：统一入口
- 现在是分散脚本，不是单一命令或页面。

### 缺 2：用户导向说明
- 现在更像研究者工作流，不是教学演示工作流。

### 缺 3：过程串联
- 还缺一个显式入口把“输入题目 -> 结构化表示 -> 代码骨架 -> 自检 -> 结果记录”串成一个面向外部读者的连续体验。

## 5. 推荐的最小原型 v0
建议先做一个 CLI 原型，而不是直接上 GUI：

### CLI 最小功能
- 选择主案例：A1 / A2
- 选择模式：direct_answer / plain_guidance / coe_guided
- 选择轨道：baseline / bug-repair / expanded-scope / fresh-generation
- 自动输出：
  - 使用的 prompt
  - 使用的 protocol
  - 对应 run 文档
  - 对应 metrics 摘要

### 为什么先做 CLI
- 当前仓库本身已经以脚本和指标表为核心。
- CLI 成本低，最容易把现有自动化链路包装成演示原型。
- 后续若需要，再把 CLI 外包一层 Notebook 或页面。

## 6. 中期材料建议写法
建议中期阶段把原型写成：

> 当前已具备可复用的脚本化研究原型：能够从 prompt / task card / protocol 出发，生成代码 artifact、执行固定协议评测、输出 run 文档与 metrics 表。下一阶段计划将其封装为统一 CLI / Notebook 入口，转化为更适合教学展示的原型形式。

## 7. 下一步最小动作
1. 先补 1 份 CLI 原型设计页。
2. 再决定是否需要真正实现 `python run_research_case.py --case A1 --mode coe_guided` 这类统一入口。
3. 中期前不必强行做 GUI，只要把“现有自动化链路 = 原型雏形”讲清楚即可。
