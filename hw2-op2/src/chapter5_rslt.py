"""
chapter5_rslt.py - 第五章：RSLT 稀疏低秩纹理修复

核心思想：对纹理图像提取相似 patch group，将其堆叠为矩阵后
使用 RPCA (L+S 分解) 而非简单 SVD 阈值化来恢复纹理。
低秩分量 L 保留重复纹理结构，稀疏分量 S 剥离污染/噪声。
"""

import os
import sys
import time

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
    generate_mask,
    get_core_image_names,
    get_results_dir,
    get_test_image,
    get_test_images,
    insert_patch,
    iter_patch_positions,
    overlay_scratch_corruption,
    overlay_text_corruption,
    plot_comparison,
    plot_image_grid,
    save_latex_table,
    stack_patches,
    unstack_patches,
)
from chapter4_patch_rpca import rpca_ialm, patch_based_inpainting


def rslt_patch_rpca(group_matrix, lam=None, max_iter=50, tol=1e-7):
    """对 patch group 矩阵做 RPCA 分解，返回低秩部分和稀疏部分。"""
    group_mean = group_matrix.mean(axis=0, keepdims=True)
    centered = group_matrix - group_mean
    low_rank, sparse, errors = rpca_ialm(centered, lam=lam, max_iter=max_iter, tol=tol)
    return low_rank + group_mean, sparse, errors


def rslt_texture_repair(
    corrupted,
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
    """RSLT：通过 patch 级别 RPCA 修复稀疏污染纹理。

    与 chapter4 的 patch_based_inpainting (SVD shrinkage) 不同，
    本方法对每个 patch group 执行完整的 RPCA 分解 (L+S)，
    使低秩部分自动恢复纹理、稀疏部分捕获污染。
    """
    current = corrupted.copy()
    positions = list(iter_patch_positions(current.shape, patch_size=patch_size, stride=stride))
    history = {'psnr': [], 'sparse_energy': []}

    for outer in range(outer_iter):
        accumulator = np.zeros_like(current)
        weight_map = np.zeros_like(current)
        total_sparse_energy = 0.0

        for position in positions:
            patches, _, group_positions, distances = find_similar_patches(
                current,
                np.ones_like(current),
                position,
                patch_size=patch_size,
                search_window=search_window,
                num_similar=num_similar,
                candidate_step=candidate_step,
                min_overlap_ratio=0.35,
            )
            group_matrix = stack_patches(patches)
            low_rank, sparse, _ = rslt_patch_rpca(
                group_matrix, lam=rpca_lam, max_iter=rpca_max_iter,
            )
            recovered_patches = unstack_patches(low_rank, patches[0].shape)
            total_sparse_energy += np.sum(np.abs(sparse))

            patch_weights = 1.0 / (np.asarray(distances) + 1e-3)
            patch_weights = 0.2 + 0.8 * patch_weights / max(np.max(patch_weights), 1e-12)

            for patch, patch_position, patch_weight in zip(recovered_patches, group_positions, patch_weights):
                insert_patch(accumulator, weight_map, patch, patch_position, patch_weight=patch_weight)

        current = accumulator / np.maximum(weight_map, 1e-12)
        history['sparse_energy'].append(total_sparse_energy)

        if true_image is not None:
            metrics = compute_metrics(true_image, current)
            history['psnr'].append(metrics['PSNR'])

    return np.clip(current, 0, 1), history


def rslt_inpainting(
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
    """RSLT 用于缺失像素补全（带 mask 约束版本）。"""
    mask_bool = mask > 0.5
    current = fill_missing_with_mean(observed, mask)
    current[mask_bool] = observed[mask_bool]
    positions = list(iter_patch_positions(current.shape, patch_size=patch_size, stride=stride))
    history = {'psnr': [], 'sparse_energy': []}

    for outer in range(outer_iter):
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
            low_rank, sparse, _ = rslt_patch_rpca(
                group_matrix, lam=rpca_lam, max_iter=rpca_max_iter,
            )
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


def demo_rslt_texture_repair(size=(256, 256), quick=False):
    """演示 RSLT 去除文字和划痕污染。"""
    save_dir = get_results_dir('chapter5')
    image = get_test_image('barbara', gray=True, size=size)

    text_corrupted, text_sparse_mask = overlay_text_corruption(image, text='LOW RANK', repeats=4, seed=53)
    text_clean_mask = 1.0 - text_sparse_mask
    text_recovered, text_history = rslt_inpainting(
        text_corrupted, text_clean_mask,
        patch_size=8,
        search_window=16 if quick else 20,
        num_similar=10 if quick else 15,
        stride=6 if quick else 4,
        candidate_step=4,
        rpca_max_iter=30 if quick else 60,
        outer_iter=2 if quick else 4,
        true_image=image,
    )

    scratch_corrupted, scratch_sparse_mask = overlay_scratch_corruption(image, num_lines=10, seed=59)
    scratch_clean_mask = 1.0 - scratch_sparse_mask
    scratch_recovered, scratch_history = rslt_inpainting(
        scratch_corrupted, scratch_clean_mask,
        patch_size=8,
        search_window=16 if quick else 20,
        num_similar=10 if quick else 15,
        stride=6 if quick else 4,
        candidate_step=4,
        rpca_max_iter=30 if quick else 60,
        outer_iter=2 if quick else 4,
        true_image=image,
    )

    plot_comparison(
        image, text_corrupted, text_recovered,
        title='RSLT 文字去除 (Barbara)',
        metrics=compute_metrics(image, text_recovered),
        save_path=os.path.join(save_dir, 'rslt_text_removal.png'),
    )
    plot_comparison(
        image, scratch_corrupted, scratch_recovered,
        title='RSLT 划痕去除 (Barbara)',
        metrics=compute_metrics(image, scratch_recovered),
        save_path=os.path.join(save_dir, 'rslt_scratch_removal.png'),
    )

    return {
        'text': compute_metrics(image, text_recovered),
        'scratch': compute_metrics(image, scratch_recovered),
    }


def compare_rslt_vs_patch_shrinkage(size=(256, 256), quick=False):
    """对比 RSLT-RPCA vs SVD-shrinkage patch 方法。"""
    save_dir = get_results_dir('chapter5')
    image_names = ['barbara'] if quick else ['barbara', 'lena']
    images = get_test_images(image_names, size=size, gray=True)
    table_rows = []

    for image_name, image in images.items():
        # 文字污染区域作为已知 mask，让 patch 方法可以做带约束修复
        corrupted, sparse_mask = overlay_text_corruption(image, text='NOISE', repeats=5, seed=67)
        clean_mask = 1.0 - sparse_mask  # 1 = clean, 0 = corrupted

        methods = {
            'Patch-Soft': lambda: patch_based_inpainting(
                corrupted, clean_mask,
                shrinkage='soft', outer_iter=3 if quick else 6,
                stride=6 if quick else 4, candidate_step=4,
                search_window=16 if quick else 20,
                num_similar=10 if quick else 15,
                tau=0.05,
                true_image=image,
            )[0],
            'Patch-WNN': lambda: patch_based_inpainting(
                corrupted, clean_mask,
                shrinkage='wnn', outer_iter=3 if quick else 6,
                stride=6 if quick else 4, candidate_step=4,
                search_window=16 if quick else 20,
                num_similar=10 if quick else 15,
                c=0.15,
                true_image=image,
            )[0],
            'RSLT-RPCA': lambda: rslt_inpainting(
                corrupted, clean_mask,
                stride=6 if quick else 4, candidate_step=4,
                search_window=16 if quick else 20,
                num_similar=10 if quick else 15,
                rpca_max_iter=30 if quick else 60,
                outer_iter=2 if quick else 4,
                true_image=image,
            )[0],
        }

        results = {}
        for method_name, runner in methods.items():
            start = time.time()
            recovered = runner()
            elapsed = time.time() - start
            metrics = compute_metrics(image, recovered)
            results[method_name] = (recovered, metrics, elapsed)
            table_rows.append([image_name, method_name, f'{metrics["PSNR"]:.2f}', f'{metrics["SSIM"]:.3f}', f'{elapsed:.1f}s'])

        imgs = [image, corrupted] + [r[0] for r in results.values()]
        titles = ['原图', '污染图'] + [f'{n}\nPSNR={m["PSNR"]:.2f}' for n, (_, m, _) in results.items()]
        figure, axes = plt.subplots(1, len(imgs), figsize=(4 * len(imgs), 4))
        for axis, img, title in zip(axes, imgs, titles):
            axis.imshow(np.clip(img, 0, 1), cmap='gray')
            axis.set_title(title)
            axis.axis('off')
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, f'rslt_vs_patch_{image_name}.png'), dpi=150, bbox_inches='tight')
        plt.close(figure)

    save_latex_table(
        ['Image', 'Method', 'PSNR', 'SSIM', 'Time'],
        table_rows,
        os.path.join(save_dir, 'rslt_comparison_table.tex'),
        caption='RSLT vs Patch-Shrinkage 纹理修复对比',
        label='tab:chapter5_rslt_compare',
    )
    return table_rows


def visualize_sparse_component(size=(256, 256), quick=False):
    """可视化 RSLT 提取的稀疏分量 S。"""
    save_dir = get_results_dir('chapter5')
    image = get_test_image('barbara', gray=True, size=size)
    corrupted, true_sparse_mask = overlay_text_corruption(image, text='DEMO', repeats=5, seed=73)

    current = corrupted.copy()
    positions = list(iter_patch_positions(current.shape, patch_size=8, stride=6 if quick else 4))

    sparse_accumulator = np.zeros_like(current)
    sparse_weight_map = np.zeros_like(current)
    low_rank_accumulator = np.zeros_like(current)
    low_rank_weight_map = np.zeros_like(current)

    for position in positions:
        patches, _, group_positions, distances = find_similar_patches(
            current, np.ones_like(current), position,
            patch_size=8, search_window=16 if quick else 20,
            num_similar=10 if quick else 15, candidate_step=4,
        )
        group_matrix = stack_patches(patches)
        low_rank, sparse, _ = rslt_patch_rpca(group_matrix, max_iter=30 if quick else 50)

        lr_patches = unstack_patches(low_rank, patches[0].shape)
        sp_patches = unstack_patches(sparse, patches[0].shape)
        for lr_p, sp_p, pos in zip(lr_patches, sp_patches, group_positions):
            insert_patch(low_rank_accumulator, low_rank_weight_map, lr_p, pos, 1.0)
            insert_patch(sparse_accumulator, sparse_weight_map, np.abs(sp_p), pos, 1.0)

    low_rank_result = low_rank_accumulator / np.maximum(low_rank_weight_map, 1e-12)
    sparse_result = sparse_accumulator / np.maximum(sparse_weight_map, 1e-12)
    sparse_display = sparse_result / max(sparse_result.max(), 1e-12)

    figure, axes = plt.subplots(1, 4, figsize=(18, 4))
    for axis, img, title, cmap in zip(
        axes,
        [image, corrupted, np.clip(low_rank_result, 0, 1), sparse_display],
        ['原图', '污染图', '低秩分量 L', '稀疏分量 |S|'],
        ['gray', 'gray', 'gray', 'hot'],
    ):
        axis.imshow(np.clip(img, 0, 1), cmap=cmap)
        axis.set_title(title)
        axis.axis('off')
    figure.suptitle('RSLT Patch-level L+S 分解可视化', fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'rslt_sparse_visualization.png'), dpi=150, bbox_inches='tight')
    plt.close(figure)

    return compute_metrics(image, np.clip(low_rank_result, 0, 1))


def rslt_missing_rate_experiment(size=(256, 256), quick=False):
    """RSLT 在不同缺失率下的补全表现。"""
    save_dir = get_results_dir('chapter5')
    image = get_test_image('barbara', gray=True, size=size)
    ratios = [0.3, 0.5, 0.7] if quick else [0.1, 0.3, 0.5, 0.7, 0.9]
    records = []

    for ratio in ratios:
        mask = generate_mask(image.shape, mode='random_pixel', ratio=ratio, seed=77)
        observed = apply_mask(image, mask)
        recovered, history = rslt_inpainting(
            observed, mask,
            stride=6 if quick else 4, candidate_step=4,
            search_window=16 if quick else 20,
            num_similar=10 if quick else 15,
            rpca_max_iter=30 if quick else 50,
            outer_iter=2 if quick else 3,
            true_image=image,
        )
        metrics = compute_metrics(image, recovered)
        records.append({'ratio': ratio, **metrics})

        if abs(ratio - 0.5) < 1e-9:
            plot_comparison(
                image, observed, recovered,
                title=f'RSLT inpainting @ {ratio:.0%}',
                metrics=metrics,
                save_path=os.path.join(save_dir, 'rslt_inpainting_50.png'),
            )

    figure, axis = plt.subplots(figsize=(8, 5))
    axis.plot([r['ratio'] for r in records], [r['PSNR'] for r in records], 'o-', color='crimson')
    axis.set_xlabel('缺失率')
    axis.set_ylabel('PSNR (dB)')
    axis.set_title('RSLT inpainting: 缺失率 vs PSNR')
    axis.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'rslt_missing_rate.png'), dpi=150, bbox_inches='tight')
    plt.close(figure)

    return records


def run_chapter5(size=(256, 256), quick=False):
    demo_rslt_texture_repair(size=size, quick=quick)
    compare_rslt_vs_patch_shrinkage(size=size, quick=quick)
    visualize_sparse_component(size=size, quick=quick)
    rslt_missing_rate_experiment(size=size, quick=quick)
    print(f'[Chapter5] 已保存结果到 {get_results_dir("chapter5")}')


if __name__ == '__main__':
    run_chapter5()
