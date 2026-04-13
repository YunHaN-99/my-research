## Role 1 Reader

- Symptom restatement: seam carving often breaks after the second seam with shape mismatch or invalid seam indices.
- Target behavior: every seam search must operate on the current image state after previous seams were removed.
- Current interface: `carve_width_buggy(im, target_w, compute_energy, find_vertical_seam, remove_vertical_seam)`.

## Role 2 Diagnoser

- Main error: the code computes `energy` once and reuses it across all seam-removal iterations.
- Root cause: the loop updates `out` but never updates the energy map that is supposed to describe `out`.
- Broken invariant: `energy.shape` must stay identical to `out.shape[:2]` on every iteration.

## Role 3 Patcher

- Minimal patch: move `compute_energy(out)` into the loop and add an invariant check before seam search.
- No rewrite is needed because the seam finder and seam remover contracts are already correct.

```python
import numpy as np


def carve_width_buggy(im, target_w, compute_energy, find_vertical_seam, remove_vertical_seam):
    """Patched: recompute the energy map from the current image each round."""
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

## Role 4 Reviewer

- Interface check: function name, parameters, and return value are unchanged.
- Root-cause check: the patch targets the stale-energy bug directly.
- Regression check: energy and image shape remain aligned on every iteration.
- Anti-hack check: there is no fixed seam count, hard-coded size, or bypass of seam search.

## Role 5 Regressor

- Minimal regression check:
  - verify `compute_energy` is called inside the seam-removal loop
  - verify `energy.shape == out.shape[:2]` before seam search
  - verify the loop still removes `w - target_w` seams and returns the resized image
- Delivery recommendation: yes, this is a minimal contract-preserving fix.
