# Error Taxonomy And Feedback Rules v1

## 目的
把 A1 / A2 已经真实出现过的错误，整理成可复用的错误分类和反馈规则，用于后续 prompt 设计、bug-repair 评分和中期材料说明。

## 1. 范围漂移类

### 典型症状
- 回答了不在当前协议里的任务。
- 擅自扩大到 GUI / 视频 / 彩图 / 额外章节。
- 生成了能跑但不可比的额外逻辑。

### 当前案例
- A1 若从 shrink 漂到 enlarge。
- A2 若从 `chapter5 rslt_inpainting` 漂到 GUI / video / chapter7。

### 反馈规则
- 先回收 scope，再看代码。
- 明确写出：
  - 本轮主接口
  - 固定测试协议
  - 明确不做的内容

## 2. 接口 / 输入输出类

### 典型症状
- 主函数名不对。
- 输入 shape 假设错。
- 返回值缺字段或 artifact 不完整。

### 当前案例
- A1 主接口不是 `seam_carve_image(im, sz)`。
- A2 `observed` / `mask` shape 不一致，或没有返回 `history`。

### 反馈规则
- 先校验函数签名和最小返回契约。
- 代码审查前必须有一条“接口是否保持不变”的显式检查。

## 3. 核心语义 / 不变量类

### 典型症状
- 代码能跑，但违反任务的核心语义。
- 输出表面正常，实则观测区、边界条件或主要约束已被破坏。

### 当前案例
- A1 `bug_01_dp_boundary`
- A1 `bug_02_no_energy_recompute`
- A1 `bug_03_height_transpose`
- A2 `bug_01_missing_mask_constraint`
- A2 `bug_02_mask_polarity_inverted`
- A2 `bug_03_sparse_component_written_back`

### 反馈规则
- 先用一句话写清楚“被破坏的不变量”。
- 补丁必须直接回到该不变量，而不是绕开算法。
- bug-repair 文档必须同时包含：
  - root cause
  - minimal patch
  - regression point

## 4. 算法逻辑类

### 典型症状
- 主体算法流程顺序错。
- 中间变量复用错。
- 正确的组件被错误地写回最终输出。

### 当前案例
- A1 未在删 seam 后重算能量。
- A2 把 `sparse` 当成恢复主信号写回图像。
- A2 patch group `stack / unstack` 逻辑错时会造成恢复异常。

### 反馈规则
- 强制拆分最小函数责任边界。
- 对“循环更新 -> 聚合 -> 回写 -> 重新施加约束”这类关键链路写出顺序检查。

## 5. Shape / 数值 / 运行时类

### 典型症状
- 维度不对。
- 除 0、NaN、Inf。
- dtype、像素范围异常。

### 当前案例
- A1 删除 seam 后 shape 不对。
- A2 `weight_map` 为 0 除、patch shape 错、输出未 clip 到 `[0, 1]`。

### 反馈规则
- 每个任务都要保留一组最小断言：
  - shape
  - finite
  - range
  - protocol-specific invariant

## 6. 评估 / 产物完整性类

### 典型症状
- 代码能跑，但没有 run 文档。
- CSV 未回填。
- 图和 summary 文件缺失。

### 当前案例
- A1 / A2 都要求 run 文档、metrics 行和固定协议输出。
- A2 还要求 4 个 fixed case 的 recovery 记录。

### 反馈规则
- 把 “artifact_complete” 与 “runnable / correct” 分开记录。
- 任何实验结论都必须能回指：
  - prompt
  - generated artifact
  - output directory
  - metrics row

## 7. 结果解释类

### 典型症状
- 用小样本 timing 得出强性能结论。
- 把 execution stability 误写成质量提升。
- 把 reused artifact 的 rerun 当成 fresh-generation variance。

### 当前案例
- A1 / A2 的 `time_to_fix_min` 都不适合做强 timing 结论。
- A2 fixed-protocol replication 和 expanded-scope validation 不能替代 fresh-generation variance。

### 反馈规则
- 解释时必须显式写：
  - measurement boundary
  - what this evidence supports
  - what this evidence does not support

## 8. 当前最有价值的错误分类结论
- 当前最稳定、最值得继续保留的错误分类，不是按“文件报错信息”分，而是按研究任务语义分：
  - 范围漂移
  - 接口 / I/O
  - 核心不变量
  - 算法逻辑
  - shape / 数值 / runtime
  - 评估 / artifact 完整性
  - 结果解释

## 9. 推荐落地方式
- 在 prompt 中：
  - 直接把核心不变量和回归清单显式化
- 在 bug-repair 中：
  - 先写 root cause，再写最小补丁
- 在报告中：
  - 先报告 “结构化指导提升可检查性”
  - 再谨慎讨论正确率 / 时间差异
