# Diagnosis

- The main bug is the wrong transpose order when height carving tries to reuse width-only logic.
- `np.transpose(im, (2, 0, 1))` moves the channel axis into the spatial layout, so the helper no longer receives an image in `(H, W, C)` semantics.
- The inverse transpose is therefore also wrong, which can produce shape errors or color/layout corruption.

# Patched Code

```python
import numpy as np


def carve_height_buggy(im, target_h, carve_width_only):
    """Patched: swap only H/W axes while keeping the channel axis in place."""
    target_h = max(1, int(target_h))
    h, _ = im.shape[:2]
    if target_h >= h:
        return im.copy()

    if im.ndim == 3:
        transposed = np.transpose(im, (1, 0, 2))
        carved = carve_width_only(transposed, target_h)
        out = np.transpose(carved, (1, 0, 2))
    else:
        transposed = np.transpose(im, (1, 0))
        carved = carve_width_only(transposed, target_h)
        out = np.transpose(carved, (1, 0))
    return out
```

# Regression Notes

- Color images now keep the channel axis fixed and only swap height/width.
- Grayscale inputs also use a valid two-axis transpose path.
- The patch preserves the original interface and directly fixes the transpose root cause.
