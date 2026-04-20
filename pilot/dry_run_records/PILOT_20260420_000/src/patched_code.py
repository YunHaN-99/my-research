import numpy as np


def build_cumulative_cost_patched(energy):
    """Clamp parent candidates at the left/right boundary before DP transition."""
    h, w = energy.shape
    dp = np.zeros((h, w), dtype=np.float64)
    backtrack = np.zeros((h, w), dtype=np.int32)
    dp[0] = energy[0]

    for i in range(1, h):
        for j in range(w):
            left = max(0, j - 1)
            right = min(w, j + 2)
            prev = dp[i - 1, left:right]
            best_prev_col = left + int(np.argmin(prev))
            backtrack[i, j] = best_prev_col
            dp[i, j] = energy[i, j] + dp[i - 1, best_prev_col]

    return dp, backtrack
