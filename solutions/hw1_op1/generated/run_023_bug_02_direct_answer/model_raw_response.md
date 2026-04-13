# Diagnosis

- The main bug is that the energy map is computed once before the seam-removal loop and then reused after the image shape changes.
- After the first seam is removed, `out.shape[:2]` no longer matches the stale energy map, so later seams are computed on invalid geometry.
- That causes shape mismatch, invalid seam indices, or visibly distorted outputs.

# Patched Code

```python
import numpy as np


def carve_width_buggy(im, target_w, compute_energy, find_vertical_seam, remove_vertical_seam):
    """Patched: recompute the energy map after every seam removal step."""
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

# Regression Notes

- The energy map is now recomputed from the current image on every iteration.
- The shape assertion guards the core invariant `energy.shape == out.shape[:2]`.
- The patch keeps the original interface and only touches the faulty loop logic.
