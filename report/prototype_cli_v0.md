# Prototype CLI v0

## 目的
给当前仓库补一个最小 CLI 原型，把已经存在的 A1 / A2 研究资产封装成单一入口，方便中期展示时直接选择案例、模式和轨道。

## 1. 当前入口
- 脚本：`run_research_case.py`
- 运行方式：
  - `python run_research_case.py --demo advisor`
  - `python run_research_case.py --case A1 --mode plain_guidance --track baseline`
  - `python run_research_case.py --case A2 --mode coe_guided --track bug-repair`
  - `python run_research_case.py --case A2 --mode direct_answer --track expanded-scope`
  - `python run_research_case.py --list`

## 2. 这个 CLI 做什么
- 提供固定的导师演示模式：`--demo advisor`
- 选择主案例：A1 / A2
- 选择模式：`direct_answer` / `plain_guidance` / `coe_guided`
- 选择轨道：
  - A1：`baseline` / `bug-repair`
  - A2：`baseline` / `bug-repair` / `expanded-scope` / `fresh-generation`
- 自动输出：
  - 使用的 prompt template
  - 对应的 protocol 文件
  - 对应的 run 文档
  - 对应的 metrics 摘要
  - 在 `--demo advisor` 下，按“输入题目 -> 结构化表示 -> prompt 选择 -> run 结果 -> metrics 摘要”输出固定演示链条

## 3. 这个 CLI 不做什么
- 不重新触发 direct / plain / CoE rerun
- 不新生成代码 artifact
- 不替代现有评测脚本

它是一个“已有研究资产选择器和摘要器”，不是新的实验执行器。

## 4. 当前演示价值
- 能把 `prompt / task card / protocol / run / metrics` 串成单一入口。
- 能让导师用一条命令直接看到研究链条，而不用手动在多个文档和 CSV 之间跳转。
- 能让外部读者直接看到不同 case / mode / track 对应的证据面。
- 能把当前仓库说明成“已有 CLI 原型”，而不是“只有零散脚本”。

## 5. 中期建议写法
建议中期材料写成：

> 当前已基于现有 A1 / A2 资产封装出可演示的 CLI 原型 `run_research_case.py`。该原型不重新执行同类 rerun，而是提供固定的导师演示模式，并支持按主案例、模式和轨道检索已有研究资产，自动输出对应的 prompt、protocol、run 文档和 metrics 摘要，用于展示当前研究仓库已经形成的可复查证据链。
