# Diagnosis

- The main bug is the DP transition reading `j - 1` and `j + 1` without clamping the valid parent range.
- At `j = 0` or `j = w - 1`, this can either raise an `IndexError` or silently read the wrong parent through Python negative indexing.
- That breaks the seam-path invariant because backtracking can record an invalid predecessor column.

# Patched Code

```python
import numpy as np


def build_cumulative_cost_buggy(energy):
    """Patched: only search legal parent columns for each DP state."""
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

# Regression Notes

- Boundary columns now read only legal parent candidates.
- `backtrack[i, j]` is always written with a valid previous-column index.
- This fixes the root cause instead of suppressing the exception.
