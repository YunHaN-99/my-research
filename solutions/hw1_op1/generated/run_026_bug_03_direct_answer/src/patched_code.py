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
