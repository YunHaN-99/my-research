# Diagnosis

- Main error: the seam-removal loop uses an energy map computed from the pre-removal image and never refreshes it.
- Root cause: `energy = compute_energy(out)` sits outside the loop, so the next seam is solved against stale pixel layout.
- Broken invariant: after each seam deletion, `energy.shape` must match `out.shape[:2]`.

# Patch Plan

- Move `compute_energy(out)` inside the loop so each iteration uses the current image.
- Add a shape assertion to guard the invariant explicitly.
- Leave the function name, arguments, and return contract unchanged.

# Patched Code

```python
import numpy as np


def carve_width_buggy(im, target_w, compute_energy, find_vertical_seam, remove_vertical_seam):
    """Patched: recompute energy from the current image every round."""
    h, w = im.shape[:2]
    if target_w >= w:
        return im.copy()

    out = im.copy()
    for _ in range(w - target_w):
        energy = compute_energy(out)
        assert energy.shape == out.shape[:2]
        seam = find_vertical_seam(energy)
        out = remove_vertical_seam(out, seam)
    return out
```

# Regression Checklist

- After each seam removal, the next energy map is recomputed from the updated `out`.
- `energy.shape == out.shape[:2]` holds at each iteration.
- The loop still removes exactly `w - target_w` seams.
- No interface or unrelated control flow changes were introduced.
