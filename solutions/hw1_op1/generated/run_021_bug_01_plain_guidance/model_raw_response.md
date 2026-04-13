# Diagnosis

- Main error: the DP step does not clamp the legal parent-column range at the left and right image boundaries.
- Root cause: `dp[i - 1, j - 1]` and `dp[i - 1, j + 1]` are accessed unconditionally, so the parent set is invalid when `j` is on an edge.
- Broken invariant: for every `(i, j)`, the chosen predecessor column must stay inside `[0, w - 1]`.

# Patch Plan

- Replace the fixed three-parent list with a boundary-aware slice.
- Convert the local `argmin` result back to the absolute predecessor column.
- Keep the function name, parameters, and return value unchanged.

# Patched Code

```python
import numpy as np


def build_cumulative_cost_buggy(energy):
    """Patched: clamp parent lookup to the legal predecessor range."""
    h, w = energy.shape
    dp = np.zeros((h, w), dtype=np.float64)
    backtrack = np.zeros((h, w), dtype=np.int32)
    dp[0] = energy[0]

    for i in range(1, h):
        for j in range(w):
            left = max(j - 1, 0)
            right = min(j + 1, w - 1)
            prev_slice = dp[i - 1, left:right + 1]
            best_offset = int(np.argmin(prev_slice))
            best_prev = left + best_offset
            backtrack[i, j] = best_prev
            dp[i, j] = energy[i, j] + dp[i - 1, best_prev]

    return dp, backtrack
```

# Regression Checklist

- `j = 0` only considers columns `0` and `1` when available.
- `j = w - 1` only considers columns `w - 2` and `w - 1` when available.
- `backtrack` never records an out-of-range predecessor.
- The patch is local to the DP transition and does not alter the interface.
