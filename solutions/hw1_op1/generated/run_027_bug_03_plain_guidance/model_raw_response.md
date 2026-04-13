# Diagnosis

- Main error: the transpose order for height carving is wrong.
- Root cause: the code uses `(2, 0, 1)` on a color image, which moves the channel axis into the width-carving path instead of preserving `(H, W, C)` semantics.
- Broken invariant: height-carving reuse should only swap the height and width axes; the channel axis must stay in place.

# Patch Plan

- Replace the color-image transpose pair with `(1, 0, 2)` both ways.
- Add a grayscale branch so non-RGB inputs still follow a valid transpose path.
- Keep the function name, parameters, and return behavior unchanged.

# Patched Code

```python
import numpy as np


def carve_height_buggy(im, target_h, carve_width_only):
    """Patched: reuse width carving by swapping only H/W axes."""
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

# Regression Checklist

- Color inputs keep the channel axis in the third position before and after carving.
- Grayscale inputs transpose with two axes only.
- Two transposes restore the original axis semantics.
- The patch does not alter the helper contract or introduce unrelated logic.
