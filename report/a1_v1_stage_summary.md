# A1 v1 stage summary

## Final judgment
A1 的 v1 阶段已经闭环：主实验完成、固定协议 replication 完成、bug-repair benchmark 完成。

## Evidence chain

### 1. Main experiment
- baseline runs: run_006, run_007, run_008
- 结论：direct_answer / plain_guidance / coe_guided 三种模式都已跑通 A1 seam carving 主任务。

### 2. Fixed-protocol replication
- replication runs: run_010 to run_018
- metrics:
  - guidance eval: 12 rows
  - codegen perf: 18 rows
- 结论：在固定图片、固定 `max_side=420`、固定 shrink-only 协议下，三种模式都稳定达到 runnable 和 correct；plain_guidance 与 coe_guided 的 self-check 记录更完整。

### 3. Bug-repair benchmark
- bug-repair runs: run_020 to run_028
- metrics:
  - failure repair eval: 9 rows
- 结论：在 3 个 curated A1 failure cases 上，三种模式都能完成正确诊断、最小修补和回归通过；结构化 guidance 的优势主要体现在诊断与回归说明的可检查性。

## What A1 supports now
- 可以支持的最强表述：
  - 在固定协议下，结构化指导不会削弱 A1 主任务的可运行性与正确性。
  - plain_guidance / coe_guided 在自检和可复查性上优于 direct_answer。
  - 在最小失败样例上，三种模式都能完成根因定位与最小修补。
- 不应过度外推的部分：
  - 还不能据此宣称结构化指导在更大范围内普遍提高最终正确率。
  - bug-repair benchmark 目前仍是 3 bug 的小样本。

## Repo decision
- A1 不再阻塞仓库主线。
- 下一条实现里程碑应当是 A2 minimal implementation。
