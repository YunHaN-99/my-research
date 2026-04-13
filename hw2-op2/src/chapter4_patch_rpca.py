"""
chapter4_patch_rpca.py - 第四章：Patch-based 低秩 + RPCA 应用
"""

import os
import sys
import time

import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from utils import (
    apply_mask,
    compute_metrics,
    fill_missing_with_mean,
    find_similar_patches,
    get_core_image_names,
    get_default_video_path,
    generate_mask,
    get_results_dir,
    get_test_image,
    get_test_images,
    insert_patch,
    iter_patch_positions,
    overlay_scratch_corruption,
    overlay_text_corruption,
    plot_comparison,
    save_latex_table,
    stack_patches,
    tv_refine,
    unstack_patches,
)
from chapter2_nuclear_norm import nuclear_norm_admm
from chapter3_nonconvex import generalized_shrinkage, weighted_nn_admm


def low_rank_patch_group(group_matrix, shrinkage='wnn', p=0.5, tau=0.05, c=0.15, eps=1e-3):
    group_mean = group_matrix.mean(axis=0, keepdims=True)
    centered = group_matrix - group_mean
    u, sigma, vt = np.linalg.svd(centered, full_matrices=False)

    if shrinkage == 'soft':
        sigma_new = np.maximum(sigma - tau, 0.0)
    elif shrinkage == 'schatten':
        sigma_new = generalized_shrinkage(sigma, mu=1.0 / max(tau, 1e-6), p=p)
    elif shrinkage == 'wnn':
        weights = c / (sigma + eps)
        sigma_new = np.maximum(sigma - weights, 0.0)
    else:
        raise ValueError(f'Unknown shrinkage: {shrinkage}')

    recovered = (u * sigma_new) @ vt + group_mean
    return recovered, int(np.sum(sigma_new > 1e-10))


def patch_based_inpainting(
    observed,
    mask,
    patch_size=8,
    search_window=20,
    num_similar=15,
    shrinkage='wnn',
    outer_iter=6,
    stride=4,
    candidate_step=4,
    p=0.5,
    tau=0.05,
    c=0.15,
    eps=1e-3,
    tv_weight=0.0,
    tv_decay=False,
    initial=None,
    true_image=None,
):
    mask_bool = mask > 0.5
    current = fill_missing_with_mean(observed, mask) if initial is None else initial.copy()
    current[mask_bool] = observed[mask_bool]
    positions = list(iter_patch_positions(current.shape, patch_size=patch_size, stride=stride))

    history = {'rse': [], 'psnr': [], 'rank': []}

    for outer in range(outer_iter):
        accumulator = np.zeros_like(current)
        weight_map = np.zeros_like(current)
        ranks = []

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
            recovered_matrix, rank = low_rank_patch_group(
                group_matrix,
                shrinkage=shrinkage,
                p=p,
                tau=tau,
                c=c,
                eps=eps,
            )
            recovered_patches = unstack_patches(recovered_matrix, patches[0].shape)
            ranks.append(rank)

            patch_weights = 1.0 / (np.asarray(distances) + 1e-3)
            patch_weights = 0.2 + 0.8 * patch_weights / max(np.max(patch_weights), 1e-12)

            for patch, patch_position, patch_weight in zip(recovered_patches, group_positions, patch_weights):
                insert_patch(accumulator, weight_map, patch, patch_position, patch_weight=patch_weight)

        current = accumulator / np.maximum(weight_map, 1e-12)
        current[mask_bool] = observed[mask_bool]

        if tv_weight > 0:
            weight_now = tv_weight / (outer + 1) if tv_decay else tv_weight
            current = tv_refine(current, mask, observed, weight=weight_now)

        if true_image is not None:
            metrics = compute_metrics(true_image, current)
            history['rse'].append(metrics['RSE'])
            history['psnr'].append(metrics['PSNR'])
        history['rank'].append(float(np.mean(ranks) if ranks else 0.0))

    return np.clip(current, 0, 1), history


def rpca_ialm(data_matrix, lam=None, max_iter=100, tol=1e-7, rho=1.5, verbose=False):
    m, n = data_matrix.shape
    if lam is None:
        lam = 1.0 / np.sqrt(max(m, n))

    norm_data = max(np.linalg.norm(data_matrix, 'fro'), 1e-12)
    spectral_norm = max(np.linalg.svd(data_matrix, compute_uv=False)[0], 1e-12)
    mu = 1.25 / spectral_norm
    mu_max = mu * 1e7

    sparse = np.zeros_like(data_matrix)
    dual = np.zeros_like(data_matrix)
    low_rank = np.zeros_like(data_matrix)
    errors = []

    for iteration in range(max_iter):
        temp = data_matrix - sparse + dual / mu
        u, sigma, vt = np.linalg.svd(temp, full_matrices=False)
        sigma = np.maximum(sigma - 1.0 / mu, 0.0)
        low_rank = (u * sigma) @ vt

        sparse = np.sign(data_matrix - low_rank + dual / mu) * np.maximum(
            np.abs(data_matrix - low_rank + dual / mu) - lam / mu,
            0.0,
        )

        residual = data_matrix - low_rank - sparse
        dual = dual + mu * residual
        error = np.linalg.norm(residual, 'fro') / norm_data
        errors.append(error)

        if verbose and iteration % 10 == 0:
            print(f'  RPCA iter {iteration:3d}: err={error:.6e}')

        mu = min(mu * rho, mu_max)
        if error < tol:
            break

    return low_rank, sparse, errors


def rpca_completion_attempt(observed, mask, outer_iter=6, inner_iter=50):
    current = fill_missing_with_mean(observed, mask)
    history = {'change': []}
    missing = mask < 0.5

    for _ in range(outer_iter):
        previous = current.copy()
        low_rank, _, _ = rpca_ialm(current, max_iter=inner_iter, verbose=False)
        current = low_rank
        current[mask > 0.5] = observed[mask > 0.5]
        change = np.linalg.norm((current - previous)[missing]) / max(np.linalg.norm(previous[missing]), 1e-12)
        history['change'].append(change)
        if change < 1e-5:
            break

    return np.clip(current, 0, 1), history


def compare_whole_vs_patch(size=(256, 256), quick=False):
    save_dir = get_results_dir('chapter4')
    image_names = ['lena'] if quick else get_core_image_names(quick=False)
    images = get_test_images(image_names, size=size, gray=True)
    table_rows = []

    for image_name, image in images.items():
        mask = generate_mask(image.shape, mode='random_pixel', ratio=0.5, seed=51)
        observed = apply_mask(image, mask)

        methods = [
            ('Whole-NNM', lambda: nuclear_norm_admm(observed, mask, lam=8.0, mu=0.4, rho=1.05, max_iter=80 if quick else 200, tol=1e-5, true_image=image)[0]),
            ('Whole-WNN', lambda: weighted_nn_admm(observed, mask, c=1.0, eps=1e-3, lam=8.0, mu=0.5, rho=1.03, max_iter=80 if quick else 200, tol=1e-5, true_image=image)[0]),
            ('Patch-soft', lambda: patch_based_inpainting(observed, mask, patch_size=8, search_window=16 if quick else 20, num_similar=10 if quick else 15, shrinkage='soft', outer_iter=3 if quick else 6, stride=6 if quick else 4, candidate_step=4, tau=0.15, true_image=image)[0]),
            ('Patch-WNN', lambda: patch_based_inpainting(observed, mask, patch_size=8, search_window=16 if quick else 20, num_similar=10 if quick else 15, shrinkage='wnn', outer_iter=3 if quick else 6, stride=6 if quick else 4, candidate_step=4, c=0.15, tv_weight=0.05, tv_decay=True, true_image=image)[0]),
        ]

        results = {}
        for method_name, runner in methods:
            start = time.time()
            recovered = runner()
            elapsed = time.time() - start
            metrics = compute_metrics(image, recovered)
            results[method_name] = (recovered, metrics, elapsed)
            table_rows.append([image_name, method_name, f'{metrics["PSNR"]:.2f}', f'{metrics["SSIM"]:.3f}', f'{elapsed:.2f}s'])

        images_to_show = [image, observed] + [result[0] for result in results.values()]
        titles = ['原图', '缺失图'] + [f'{name}\nPSNR={metrics["PSNR"]:.2f}' for name, (_, metrics, _) in results.items()]
        figure, axes = plt.subplots(1, len(images_to_show), figsize=(4 * len(images_to_show), 4))
        for axis, img, title in zip(axes, images_to_show, titles):
            axis.imshow(np.clip(img, 0, 1), cmap='gray')
            axis.set_title(title)
            axis.axis('off')
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, f'whole_vs_patch_{image_name}.png'), dpi=150, bbox_inches='tight')
        plt.close(figure)

    save_latex_table(
        ['Image', 'Method', 'PSNR', 'SSIM', 'Time'],
        table_rows,
        os.path.join(save_dir, 'whole_vs_patch_table.tex'),
        caption='整图方法与 Patch-based 方法对比',
        label='tab:chapter4_whole_patch',
    )
    return table_rows


def run_text_removal(size=(256, 256)):
    save_dir = get_results_dir('chapter4')
    image = get_test_image('lena', gray=True, size=size)
    corrupted, _ = overlay_text_corruption(image, text='LOW RANK', repeats=4, seed=53)
    low_rank, sparse, _ = rpca_ialm(corrupted, max_iter=80, verbose=False)

    figure, axes = plt.subplots(1, 4, figsize=(16, 4))
    for axis, img, title in zip(
        axes,
        [image, corrupted, np.clip(low_rank, 0, 1), np.clip(np.abs(sparse), 0, 1)],
        ['原图', '文字污染', '低秩部分 L', '稀疏部分 S'],
    ):
        axis.imshow(np.clip(img, 0, 1), cmap='gray')
        axis.set_title(title)
        axis.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'rpca_text_removal.png'), dpi=150, bbox_inches='tight')
    plt.close(figure)
    return compute_metrics(image, np.clip(low_rank, 0, 1))


def generate_synthetic_video(num_frames=80, frame_size=(120, 160)):
    height, width = frame_size
    x = np.linspace(0, 1, width)
    y = np.linspace(0, 1, height)
    grid_x, grid_y = np.meshgrid(x, y)
    background = 0.3 + 0.2 * np.sin(2 * np.pi * grid_x) * np.cos(2 * np.pi * grid_y)

    frames = []
    for frame_idx in range(num_frames):
        frame = background.copy()
        left = int(10 + frame_idx * 1.2) % max(1, width - 20)
        top = height // 3
        frame[top:top + 14, left:left + 20] = 0.95
        top2 = int(8 + frame_idx * 0.9) % max(1, height - 12)
        left2 = width * 2 // 3
        frame[top2:top2 + 10, left2:left2 + 10] = 0.7
        frames.append(frame)
    return np.array(frames), background


def _load_video_frames(video_path, num_frames=80, frame_size=(120, 160)):
    if video_path is None or not os.path.exists(video_path):
        return None, None
    capture = cv2.VideoCapture(video_path)
    frames = []
    height, width = frame_size
    while len(frames) < num_frames:
        success, frame = capture.read()
        if not success:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (width, height), interpolation=cv2.INTER_AREA)
        frames.append(gray.astype(np.float64) / 255.0)
    capture.release()
    if not frames:
        return None, None
    return np.array(frames), None


def run_video_background_separation(num_frames=80, frame_size=(120, 160), quick=False):
    save_dir = get_results_dir('chapter4')
    video_path = get_default_video_path()

    frames, true_background = _load_video_frames(video_path, num_frames=num_frames, frame_size=frame_size)
    if frames is None:
        frames, true_background = generate_synthetic_video(num_frames=num_frames, frame_size=frame_size)

    frame_matrix = frames.reshape(frames.shape[0], -1).T
    low_rank, sparse, errors = rpca_ialm(frame_matrix, max_iter=60 if quick else 100, verbose=False)

    low_rank_frames = low_rank.T.reshape(frames.shape)
    sparse_frames = np.abs(sparse.T.reshape(frames.shape))
    indices = np.linspace(0, len(frames) - 1, 6, dtype=int)

    figure, axes = plt.subplots(3, len(indices), figsize=(4 * len(indices), 10))
    for col, index in enumerate(indices):
        axes[0, col].imshow(frames[index], cmap='gray')
        axes[0, col].set_title(f'原始 {index}')
        axes[1, col].imshow(np.clip(low_rank_frames[index], 0, 1), cmap='gray')
        axes[1, col].set_title('背景 L')
        axes[2, col].imshow(np.clip(sparse_frames[index], 0, 1), cmap='hot')
        axes[2, col].set_title('前景 S')
        for row in range(3):
            axes[row, col].axis('off')
    axes[0, 0].set_ylabel('Original')
    axes[1, 0].set_ylabel('Background')
    axes[2, 0].set_ylabel('Foreground')
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'video_background_separation.png'), dpi=150, bbox_inches='tight')
    plt.close(figure)

    return {
        'errors': errors,
        'background_psnr': None if true_background is None else compute_metrics(true_background, np.mean(low_rank_frames, axis=0))['PSNR'],
    }


def rpca_applicability_test(size=(256, 256), quick=False):
    save_dir = get_results_dir('chapter4')
    image = get_test_image('lena', gray=True, size=size)
    results = []

    text_corrupted, _ = overlay_text_corruption(image, text='LOW RANK', repeats=4, seed=57)
    text_recovered, _, _ = rpca_ialm(text_corrupted, max_iter=80 if quick else 120, verbose=False)
    results.append(('text', text_corrupted, np.clip(text_recovered, 0, 1), compute_metrics(image, np.clip(text_recovered, 0, 1))))

    scratch_corrupted, _ = overlay_scratch_corruption(image, num_lines=10 if quick else 14, seed=59)
    scratch_recovered, _, _ = rpca_ialm(scratch_corrupted, max_iter=80 if quick else 120, verbose=False)
    results.append(('scratch', scratch_corrupted, np.clip(scratch_recovered, 0, 1), compute_metrics(image, np.clip(scratch_recovered, 0, 1))))

    for mode in ['random_pixel', 'center_block']:
        mask = generate_mask(image.shape, mode=mode, ratio=0.5 if mode == 'random_pixel' else 0.35, seed=61)
        observed = apply_mask(image, mask)
        recovered, _ = rpca_completion_attempt(observed, mask, outer_iter=4 if quick else 6, inner_iter=30 if quick else 50)
        results.append((mode, observed, recovered, compute_metrics(image, recovered)))

    figure, axes = plt.subplots(len(results), 3, figsize=(12, 4 * len(results)))
    axes = np.atleast_2d(axes)
    table_rows = []
    for row, (mode, corrupted, recovered, metrics) in enumerate(results):
        axes[row, 0].imshow(image, cmap='gray')
        axes[row, 0].set_title('原图')
        axes[row, 1].imshow(np.clip(corrupted, 0, 1), cmap='gray')
        axes[row, 1].set_title(f'{mode} 污染/缺失')
        axes[row, 2].imshow(np.clip(recovered, 0, 1), cmap='gray')
        axes[row, 2].set_title(f'RPCA\nPSNR={metrics["PSNR"]:.2f}')
        for col in range(3):
            axes[row, col].axis('off')
        table_rows.append([mode, f'{metrics["PSNR"]:.2f}', f'{metrics["SSIM"]:.3f}'])

    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'rpca_applicability.png'), dpi=150, bbox_inches='tight')
    plt.close(figure)

    save_latex_table(
        ['Mode', 'PSNR', 'SSIM'],
        table_rows,
        os.path.join(save_dir, 'rpca_applicability_table.tex'),
        caption='RPCA 适用范围测试',
        label='tab:chapter4_rpca',
    )
    return table_rows


def run_chapter4(size=(256, 256), quick=False):
    compare_whole_vs_patch(size=size, quick=quick)
    run_text_removal(size=size)
    run_video_background_separation(
        num_frames=24 if quick else 80,
        frame_size=(64, 96) if quick else (120, 160),
        quick=quick,
    )
    rpca_applicability_test(size=size, quick=quick)
    print(f'[Chapter4] 已保存结果到 {get_results_dir("chapter4")}')


if __name__ == '__main__':
    run_chapter4()
