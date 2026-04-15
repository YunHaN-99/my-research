# Advisor Demo Entry v1

## 目的
把当前 CLI 原型补成一个更适合给导师演示的入口，避免展示时还要在 requirement、task card、run、metrics 和阶段总结之间来回切换。

## 1. 推荐命令
- `python run_research_case.py --demo advisor`

这条命令会固定输出下面这条研究链：

1. 输入题目
2. 结构化表示
3. prompt 选择
4. run 结果
5. metrics 摘要
6. 当前最稳能说什么
7. 可继续展开的题库 / bug-repair / expanded-scope 入口

## 2. 当前默认展示内容
- 主案例：A2
- 展示模式：`plain_guidance`
- 展示轨道：`baseline`
- 同轨道模式对比：`direct_answer / plain_guidance / coe_guided`
- 补充证据入口：
  - A2 `bug-repair`
  - A2 `expanded-scope`
  - A2 `fresh-generation`
  - A1 `baseline`

## 3. 为什么默认用这条链
- A2 当前证据最完整，最适合展示“范围收束后的主案例闭环”。
- `plain_guidance` 最容易把结构化 guidance 的过程痕迹讲清楚。
- baseline 轨道最适合先讲固定协议、再讲 bug-repair 和 expanded-scope 的扩展证据。

## 4. 演示时建议怎么讲
- 第一句先讲阶段判断：
  - `A1 / A2` 首轮主案例闭环已完成；当前中期重点是收束模板库、检查清单、错误分类、题库页和原型入口。
- 然后讲 A2 已经从早期宽标签收束到：
  - `hw2-op2/src/chapter5_rslt.py::rslt_inpainting(...)`
- 接着顺着命令输出往下讲：
  - 题目 requirement 说明研究对象是什么
  - task card 说明结构化表示如何固定输入、输出、接口和评测
  - prompt template 说明三种 mode 如何进入同一固定协议
  - run 文档说明当前不是口头结论，而是有回指材料
  - metrics 摘要说明当前最强结论来自过程质量，而不是最终指标显著抬升

## 5. 导师继续追问时的展开命令
- 看 A2 bug-repair：
  - `python run_research_case.py --case A2 --mode plain_guidance --track bug-repair`
- 看 A2 expanded-scope：
  - `python run_research_case.py --case A2 --mode plain_guidance --track expanded-scope`
- 看 A2 fresh-generation：
  - `python run_research_case.py --case A2 --mode plain_guidance --track fresh-generation`
- 看 A1 对照：
  - `python run_research_case.py --case A1 --mode plain_guidance --track baseline`

## 6. 当前边界
- 这仍然是“演示型入口”，不是新实验执行器。
- 它不会重新跑 direct / plain / CoE。
- 它的目标是把已有研究资产整理成导师能一眼看懂的链条，而不是替代完整教学系统。
