## Role 1 Reader

- Symptom restatement: width-shrink DP can crash at boundary columns or produce abnormal seam jumps.
- Target behavior: each DP state should choose the minimum cumulative cost among legal parent columns only.
- Current interface: `build_cumulative_cost_buggy(energy)` returns `(dp, backtrack)`.

## Role 2 Diagnoser

- Main error: the predecessor lookup does not clamp the valid parent range for `j = 0` and `j = w - 1`.
- Root cause: the code assumes all three parents exist and directly reads `j - 1`, `j`, and `j + 1`.
- Broken invariant: predecessor indices stored in `backtrack` must stay within the legal column range.

## Role 3 Patcher

- Minimal patch: compute `left` and `right`, search only `dp[i - 1, left:right + 1]`, then map the local `argmin` back to the absolute predecessor column.
- No unrelated refactor is needed because the bug is confined to the DP transition.

```python
import numpy as np


def build_cumulative_cost_buggy(energy):
    """Patched: clamp parent lookup to legal predecessor columns."""
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

## Role 4 Reviewer

- Interface check: function name, argument list, and return structure are unchanged.
- Root-cause check: the patch fixes illegal predecessor access instead of hiding the resulting error.
- Regression check: edge columns now stay inside bounds and cannot write invalid backtrack indices.
- Anti-hack check: no hard-coded image sizes or path-specific logic was added.

## Role 5 Regressor

- Minimal regression check:
  - verify `j = 0` and `j = w - 1` use only legal predecessor columns
  - verify all recorded `backtrack` values remain in `[0, w - 1]`
  - verify the function still returns `dp` and `backtrack` with shape `(h, w)`
- Delivery recommendation: yes, this is a minimal root-cause patch.
