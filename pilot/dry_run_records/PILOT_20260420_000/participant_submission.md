# Participant Submission

## diagnosis
主错误是 DP 边界转移没有先截断合法父节点集合，导致 `j=0` / `j=w-1` 时仍会读取非法列索引。

原因说明：
1. 当前实现把 `j-1`、`j`、`j+1` 固定打包成三项列表。
2. `j=0` 时会把 `-1` 误当成合法列，`j=w-1` 时会直接读到越界的 `j+1`。
3. 这会导致边界列报错，或者在未崩溃时产生错误的 seam 回溯路径。

## patched code
- 代码文件：`pilot/dry_run_records/PILOT_20260420_000/src/patched_code.py`

## regression notes
最小回归检查：
1. 用 `3x4` 的手工能量矩阵调用 patched function。
2. 确认函数不抛异常。
3. 确认 `backtrack.min() >= 0` 且 `backtrack.max() < w`。
4. 与 scorer-only 的 `fixed_code.py` 对照时，`dp` 和 `backtrack` 一致。
