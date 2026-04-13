# A2 Direct Answer Response

Below is a direct implementation of the A2 chapter5 task. The code keeps the scope narrow: patch-group RPCA for grayscale masked inpainting under the fixed protocol.

```python
import os
import sys
import numpy as np

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(THIS_DIR, '..', '..', '..', '..', '..'))
GOLD_SRC = os.path.join(ROOT_DIR, 'hw2-op2', 'src')

if THIS_DIR not in sys.path:
    sys.path.insert(0, THIS_DIR)
if GOLD_SRC not in sys.path:
    sys.path.insert(1, GOLD_SRC)

from utils import (
    compute_metrics,
    fill_missing_with_mean,
    find_similar_patches,
    insert_patch,
    iter_patch_positions,
    stack_patches,
    unstack_patches,
)
from chapter4_patch_rpca import rpca_ialm


def rslt_patch_rpca(group_matrix, lam=None, max_iter=50, tol=1e-7):
    group_mean = group_matrix.mean(axis=0, keepdims=True)
    centered = group_matrix - group_mean
    low_rank, sparse, _ = rpca_ialm(centered, lam=lam, max_iter=max_iter, tol=tol)
    return low_rank + group_mean, sparse


def rslt_inpainting(
    observed,
    mask,
    patch_size=8,
    stride=6,
    search_window=16,
    num_similar=10,
    candidate_step=4,
    rpca_lam=None,
    rpca_max_iter=30,
    outer_iter=2,
    true_image=None,
):
    observed = np.asarray(observed, dtype=np.float64)
    mask = np.asarray(mask, dtype=np.float64)
    if observed.shape != mask.shape:
        raise ValueError('observed and mask must have the same shape')

    mask_bool = mask > 0.5
    current = fill_missing_with_mean(observed, mask)
    current[mask_bool] = observed[mask_bool]
    positions = list(iter_patch_positions(current.shape, patch_size=patch_size, stride=stride))
    history = {'psnr': [], 'sparse_energy': []}

    for _ in range(outer_iter):
        accumulator = np.zeros_like(current)
        weight_map = np.zeros_like(current)
        total_sparse_energy = 0.0

        for position in positions:
            patches, _, group_positions, distances = find_similar_patches(
                current,
                mask,
                position,
                patch_size=patch_size,
                search_window=search_window,
                num_similar=num_similar,
                candidate_step=candidate_step,
                min_overlap_ratio=0.35,
            )
            group_matrix = stack_patches(patches)
            low_rank, sparse = rslt_patch_rpca(
                group_matrix,
                lam=rpca_lam,
                max_iter=rpca_max_iter,
            )
            recovered_patches = unstack_patches(low_rank, patches[0].shape)
            total_sparse_energy += float(np.sum(np.abs(sparse)))

            patch_weights = 1.0 / (np.asarray(distances) + 1e-3)
            patch_weights = 0.2 + 0.8 * patch_weights / max(np.max(patch_weights), 1e-12)

            for patch, patch_position, patch_weight in zip(recovered_patches, group_positions, patch_weights):
                insert_patch(accumulator, weight_map, patch, patch_position, patch_weight=patch_weight)

        current = accumulator / np.maximum(weight_map, 1e-12)
        current[mask_bool] = observed[mask_bool]
        current = np.clip(current, 0.0, 1.0)
        history['sparse_energy'].append(total_sparse_energy)

        if true_image is not None:
            history['psnr'].append(compute_metrics(true_image, current)['PSNR'])

    return np.clip(current, 0.0, 1.0), history
```

This version keeps the known-pixel mask constraint, patch-group RPCA, weighted patch aggregation, and fixed-protocol output path.
