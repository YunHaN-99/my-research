## Role 1 Reader

- Task: implement A2 chapter5 grayscale masked inpainting as a fresh artifact.
- Required interface: `rslt_inpainting(observed, mask, ...)`.
- Acceptance: all 4 fixed protocol cases must run and emit metrics and output figures.

## Role 2 Planner

- Core stages: initialize missing pixels, search similar patches, run RPCA per patch group, aggregate, re-apply mask, record history.
- Main invariants:
  - `observed.shape == mask.shape`
  - observed pixels stay unchanged
  - aggregation never divides by zero

## Role 3 Coder

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


def _prepare_inputs(observed, mask):
    observed = np.asarray(observed, dtype=np.float64)
    mask = np.asarray(mask, dtype=np.float64)
    if observed.shape != mask.shape:
        raise ValueError('observed and mask must have the same shape')
    return observed, mask, mask > 0.5


def _distance_to_weights(distances):
    raw = np.asarray(distances, dtype=np.float64)
    weights = 1.0 / np.maximum(raw + 1e-3, 1e-12)
    return 0.2 + 0.8 * weights / max(float(np.max(weights)), 1e-12)


def rslt_patch_rpca(group_matrix, lam=None, max_iter=50, tol=1e-7):
    group_mean = group_matrix.mean(axis=0, keepdims=True)
    centered = group_matrix - group_mean
    low_rank, sparse, _ = rpca_ialm(centered, lam=lam, max_iter=max_iter, tol=tol)
    return low_rank + group_mean, sparse


def _validate_state(observed, mask_bool, current, weight_map):
    if current.shape != observed.shape:
        raise ValueError('current shape drifted from observed shape')
    if weight_map.shape != observed.shape:
        raise ValueError('weight_map shape drifted from observed shape')
    if not np.all(np.isfinite(current)):
        raise ValueError('current image contains non-finite values')
    assert np.allclose(current[mask_bool], observed[mask_bool])


def _merge_estimate(accumulator, weight_map, observed, mask_bool):
    updated = accumulator / np.maximum(weight_map, 1e-12)
    updated[mask_bool] = observed[mask_bool]
    updated = np.clip(updated, 0.0, 1.0)
    _validate_state(observed, mask_bool, updated, weight_map)
    return updated


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
    observed, mask, mask_bool = _prepare_inputs(observed, mask)
    current = fill_missing_with_mean(observed, mask)
    current[mask_bool] = observed[mask_bool]
    positions = tuple(iter_patch_positions(current.shape, patch_size=patch_size, stride=stride))
    history = {'psnr': [], 'sparse_energy': []}

    for _ in range(int(outer_iter)):
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
            low_rank, sparse = rslt_patch_rpca(group_matrix, lam=rpca_lam, max_iter=rpca_max_iter)
            recovered_patches = unstack_patches(low_rank, patches[0].shape)
            total_sparse_energy += float(np.sum(np.abs(sparse)))

            for patch, patch_position, patch_weight in zip(recovered_patches, group_positions, _distance_to_weights(distances)):
                insert_patch(accumulator, weight_map, patch, patch_position, patch_weight=patch_weight)

        current = _merge_estimate(accumulator, weight_map, observed, mask_bool)
        history['sparse_energy'].append(total_sparse_energy)

        if true_image is not None:
            history['psnr'].append(compute_metrics(true_image, current)['PSNR'])

    return current, history
```

## Role 4 Reviewer

- Interface check: preserved.
- Root-cause risk check:
  - mask constraint handled explicitly
  - weight-map zero division guarded
  - shape drift checked
- Scope check: no GUI / video / chapter7 expansion leaked into the implementation.

## Role 5 Experimenter

- Fixed protocol:
  - images = `lena`, `barbara`
  - corruptions = `random_pixel@50%`, `text@50%`
  - metrics = `PSNR / SSIM / RSE / runtime`
- Delivery requirement: code + 4 fixed outputs + run log + metrics rows.
