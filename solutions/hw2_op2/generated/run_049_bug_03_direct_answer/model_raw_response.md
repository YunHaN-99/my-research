# Diagnosis

- The main bug is that the code wrote back sparse residual patches instead of low-rank reconstruction.
- This breaks the core A2 invariant for the masked RPCA inpainting loop.
- The fix should keep the original interface and patch only the root-cause line(s).

# Patched Code

```python
import numpy as np


def rslt_inpainting_buggy(
    observed,
    mask,
    patch_size=8,
    stride=4,
    search_window=20,
    num_similar=15,
    candidate_step=4,
    rpca_lam=None,
    rpca_max_iter=50,
    outer_iter=3,
    true_image=None,
):
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
            low_rank, sparse, _ = rslt_patch_rpca(group_matrix, lam=rpca_lam, max_iter=rpca_max_iter)
            recovered_patches = unstack_patches(low_rank, patches[0].shape)
            total_sparse_energy += np.sum(np.abs(sparse))

            patch_weights = 1.0 / (np.asarray(distances) + 1e-3)
            patch_weights = 0.2 + 0.8 * patch_weights / max(np.max(patch_weights), 1e-12)

            for patch, patch_position, patch_weight in zip(recovered_patches, group_positions, patch_weights):
                insert_patch(accumulator, weight_map, patch, patch_position, patch_weight=patch_weight)

        current = accumulator / np.maximum(weight_map, 1e-12)
        current[mask_bool] = observed[mask_bool]
        history['sparse_energy'].append(total_sparse_energy)

        if true_image is not None:
            metrics = compute_metrics(true_image, current)
            history['psnr'].append(metrics['PSNR'])

    return np.clip(current, 0, 1), history
```

# Regression Notes

- The patch preserves the original function signature and return contract.
- The repaired implementation restores the A2 invariant that was broken in the failure case.
- The change is local to the bug and does not rewrite unrelated patch-group logic.
