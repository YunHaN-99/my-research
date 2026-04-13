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
