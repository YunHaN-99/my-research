import argparse
import importlib.util
import json
from pathlib import Path

import numpy as np


LOW_RANK_VALUE = 0.8
SPARSE_VALUE = 0.1


def load_module(module_path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fill_missing_with_mean(observed, mask):
    filled = observed.copy()
    filled[mask < 0.5] = 0.55
    return filled


def iter_patch_positions(image_shape, patch_size=8, stride=4):
    del image_shape, patch_size, stride
    yield (0, 0)


def find_similar_patches(
    image,
    mask,
    reference_position,
    patch_size=8,
    search_window=20,
    num_similar=15,
    candidate_step=4,
    min_overlap_ratio=0.35,
):
    del mask, reference_position, patch_size, search_window, num_similar, candidate_step, min_overlap_ratio
    patch = np.full_like(image, 0.25)
    return [patch], [np.ones_like(image)], [(0, 0)], [0.0]


def stack_patches(patches):
    return np.vstack([patch.reshape(1, -1) for patch in patches])


def rslt_patch_rpca(group_matrix, lam=None, max_iter=50):
    del lam, max_iter
    low_rank = np.full_like(group_matrix, LOW_RANK_VALUE)
    sparse = np.full_like(group_matrix, SPARSE_VALUE)
    return low_rank, sparse, []


def unstack_patches(matrix, patch_shape):
    return [row.reshape(patch_shape) for row in matrix]


def insert_patch(accumulator, weight_map, patch, position, patch_weight=1.0):
    del position
    accumulator += patch_weight * patch
    weight_map += patch_weight


def compute_metrics(original, recovered):
    return {'PSNR': float(np.mean(recovered - original))}


def install_helpers(module):
    module.fill_missing_with_mean = fill_missing_with_mean
    module.iter_patch_positions = iter_patch_positions
    module.find_similar_patches = find_similar_patches
    module.stack_patches = stack_patches
    module.rslt_patch_rpca = rslt_patch_rpca
    module.unstack_patches = unstack_patches
    module.insert_patch = insert_patch
    module.compute_metrics = compute_metrics


def run_function(module, func_name):
    clean = np.array(
        [
            [0.9, 0.8, 0.7, 0.6],
            [0.5, 0.4, 0.3, 0.2],
            [0.1, 0.9, 0.8, 0.7],
            [0.6, 0.5, 0.4, 0.3],
        ],
        dtype=np.float64,
    )
    mask = np.array(
        [
            [1.0, 1.0, 0.0, 0.0],
            [1.0, 0.0, 0.0, 1.0],
            [0.0, 0.0, 1.0, 1.0],
            [0.0, 1.0, 1.0, 0.0],
        ],
        dtype=np.float64,
    )
    observed = clean * mask

    function = getattr(module, func_name)
    recovered, history = function(
        observed,
        mask,
        patch_size=4,
        stride=4,
        search_window=4,
        num_similar=1,
        candidate_step=4,
        rpca_max_iter=2,
        outer_iter=1,
        true_image=clean,
    )
    return clean, observed, mask, recovered, history


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bug-id', required=True)
    parser.add_argument('--candidate', required=True)
    parser.add_argument('--reference', required=True)
    args = parser.parse_args()

    candidate_path = Path(args.candidate).resolve()
    reference_path = Path(args.reference).resolve()

    candidate = load_module(candidate_path, 'candidate_module')
    reference = load_module(reference_path, 'reference_module')

    install_helpers(candidate)
    install_helpers(reference)

    clean, observed, mask, candidate_recovered, candidate_history = run_function(candidate, 'rslt_inpainting_buggy')
    _, _, _, reference_recovered, reference_history = run_function(reference, 'rslt_inpainting_fixed')

    mask_bool = mask > 0.5
    payload = {
        'bug_id': args.bug_id,
        'candidate_matches_reference': bool(np.allclose(candidate_recovered, reference_recovered)),
        'observed_pixels_preserved': bool(np.allclose(candidate_recovered[mask_bool], observed[mask_bool])),
        'missing_region_changed': bool(
            np.linalg.norm((candidate_recovered - observed)[~mask_bool]) > 1e-8
        ),
        'history_keys_match': sorted(candidate_history.keys()) == sorted(reference_history.keys()),
        'candidate_min': float(np.min(candidate_recovered)),
        'candidate_max': float(np.max(candidate_recovered)),
        'expected_low_rank_value': LOW_RANK_VALUE,
        'expected_sparse_value': SPARSE_VALUE,
    }
    payload['regression_pass'] = all(
        [
            payload['candidate_matches_reference'],
            payload['observed_pixels_preserved'],
            payload['missing_region_changed'],
            payload['history_keys_match'],
        ]
    )

    print(json.dumps(payload, indent=2))
    raise SystemExit(0 if payload['regression_pass'] else 1)


if __name__ == '__main__':
    main()
