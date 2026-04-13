"""
chapter1_foundation.py - 第一章：低秩性验证 + 基线方法
"""

import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from utils import (
    aggregate_patches,
    apply_mask,
    compute_metrics,
    compute_singular_profile,
    find_similar_patches,
    generate_mask,
    get_core_image_names,
    get_results_dir,
    get_test_images,
    iterative_truncated_svd_inpainting,
    plot_comparison,
    plot_missing_patterns_demo,
    stack_patches,
)


def analyze_singular_values(images, save_dir):
    figure, axes = plt.subplots(len(images), 3, figsize=(15, 4 * len(images)))
    axes = np.atleast_2d(axes)
    summary = {}

    for row, (name, image) in enumerate(images.items()):
        singular_values, cumulative, k95, k99 = compute_singular_profile(image)
        summary[name] = {'k95': k95, 'k99': k99, 'rank': len(singular_values)}

        axes[row, 0].plot(singular_values[:120], color='steelblue')
        axes[row, 0].set_title(f'{name} - 奇异值衰减')
        axes[row, 0].set_xlabel('序号')
        axes[row, 0].set_ylabel('σ')

        axes[row, 1].semilogy(np.maximum(singular_values[:120], 1e-12), color='darkorange')
        axes[row, 1].set_title(f'{name} - 奇异值(对数)')
        axes[row, 1].set_xlabel('序号')

        axes[row, 2].plot(cumulative, color='seagreen')
        axes[row, 2].axhline(0.95, color='r', linestyle='--', label=f'95% @ {k95}')
        axes[row, 2].axhline(0.99, color='purple', linestyle=':', label=f'99% @ {k99}')
        axes[row, 2].set_ylim(0, 1.02)
        axes[row, 2].set_title(f'{name} - 累积能量')
        axes[row, 2].set_xlabel('序号')
        axes[row, 2].set_ylabel('累计占比')
        axes[row, 2].legend(fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'singular_value_overview.png'), dpi=150, bbox_inches='tight')
    plt.close(figure)
    return summary


def analyze_patch_group_rank(image, save_dir, patch_size=8, num_similar=20):
    height, width = image.shape
    reference_position = (height // 3, width // 3)
    full_mask = np.ones_like(image)
    patches, _, positions, distances = find_similar_patches(
        image,
        full_mask,
        reference_position,
        patch_size=patch_size,
        search_window=48,
        num_similar=num_similar,
        candidate_step=2,
    )
    patch_matrix = stack_patches(patches)
    patch_singular_values, patch_cumulative, patch_k95, patch_k99 = compute_singular_profile(patch_matrix)
    image_singular_values, image_cumulative, image_k95, image_k99 = compute_singular_profile(image)

    figure, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes[0, 0].imshow(image, cmap='gray')
    ref_top, ref_left = reference_position
    axes[0, 0].add_patch(plt.Rectangle((ref_left, ref_top), patch_size, patch_size, fill=False, edgecolor='red', linewidth=2))
    axes[0, 0].set_title('参考 patch 位置')
    axes[0, 0].axis('off')

    patch_grid = aggregate_patches(
        patches,
        [(idx // 5 * patch_size, idx % 5 * patch_size) for idx in range(len(patches))],
        (patch_size * int(np.ceil(len(patches) / 5)), patch_size * 5),
    )
    axes[0, 1].imshow(patch_grid, cmap='gray')
    axes[0, 1].set_title('最相似 patch group')
    axes[0, 1].axis('off')

    axes[1, 0].semilogy(np.maximum(image_singular_values[:80], 1e-12), label=f'整图 95%@{image_k95}')
    axes[1, 0].semilogy(np.maximum(patch_singular_values[:20], 1e-12), label=f'Patch group 95%@{patch_k95}')
    axes[1, 0].set_title('整图 vs Patch group 奇异值衰减')
    axes[1, 0].set_xlabel('序号')
    axes[1, 0].legend()

    axes[1, 1].plot(image_cumulative, label=f'整图 99%@{image_k99}')
    axes[1, 1].plot(np.linspace(0, len(image_cumulative) - 1, len(patch_cumulative)), patch_cumulative, label=f'Patch group 99%@{patch_k99}')
    axes[1, 1].axhline(0.95, color='r', linestyle='--', alpha=0.5)
    axes[1, 1].axhline(0.99, color='g', linestyle=':', alpha=0.5)
    axes[1, 1].set_title('累积能量对比')
    axes[1, 1].set_xlabel('序号')
    axes[1, 1].set_ylabel('累计占比')
    axes[1, 1].legend()

    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'patch_group_rank_analysis.png'), dpi=150, bbox_inches='tight')
    plt.close(figure)
    return {
        'patch_k95': patch_k95,
        'patch_k99': patch_k99,
        'image_k95': image_k95,
        'image_k99': image_k99,
        'distances': distances,
        'positions': positions,
    }


def truncated_svd_baseline(image, save_dir, rank_list=None, ratio=0.5):
    if rank_list is None:
        max_rank = min(image.shape)
        rank_list = [rank for rank in [5, 10, 20, 50, 100, 150, 200] if rank < max_rank]
        if not rank_list:
            rank_list = [max(2, max_rank // 4), max(4, max_rank // 2)]

    mask = generate_mask(image.shape, mode='random_pixel', ratio=ratio, seed=7)
    observed = apply_mask(image, mask)
    results = []
    best = None

    for rank in rank_list:
        recovered, history = iterative_truncated_svd_inpainting(observed, mask, rank=rank, max_iter=20, tol=1e-4)
        metrics = compute_metrics(image, recovered)
        metrics['rank'] = rank
        metrics['iterations'] = len(history['change'])
        results.append(metrics)
        if best is None or metrics['PSNR'] > best['metrics']['PSNR']:
            best = {'metrics': metrics, 'recovered': recovered}

    figure, axis = plt.subplots(figsize=(8, 5))
    axis.plot([item['rank'] for item in results], [item['PSNR'] for item in results], 'o-', color='royalblue')
    axis.set_xlabel('截断秩 k')
    axis.set_ylabel('PSNR (dB)')
    axis.set_title('Truncated SVD baseline: rank vs PSNR')
    axis.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'truncated_svd_rank_vs_psnr.png'), dpi=150, bbox_inches='tight')
    plt.close(figure)

    plot_comparison(
        image,
        observed,
        best['recovered'],
        title=f'Truncated SVD 最优结果 (k={best["metrics"]["rank"]})',
        metrics=best['metrics'],
        save_path=os.path.join(save_dir, 'truncated_svd_best.png'),
    )
    return results


def run_chapter1(size=(256, 256), quick=False):
    save_dir = get_results_dir('chapter1')
    image_names = get_core_image_names(quick=quick)
    images = get_test_images(image_names, size=size, gray=True)

    summary = analyze_singular_values(images, save_dir)
    patch_summary = analyze_patch_group_rank(images['lena'], save_dir, patch_size=8, num_similar=12 if quick else 20)
    plot_missing_patterns_demo(images['lena'], ratio=0.5, save_path=os.path.join(save_dir, 'missing_patterns_grid.png'))
    baseline = truncated_svd_baseline(images['lena'], save_dir, ratio=0.5)

    summary_path = os.path.join(save_dir, 'chapter1_summary.txt')
    with open(summary_path, 'w', encoding='utf-8') as file:
        file.write('Chapter 1 Summary\n')
        file.write('=================\n')
        for name, stats in summary.items():
            file.write(f'{name}: 95% energy @ {stats["k95"]}, 99% energy @ {stats["k99"]}\n')
        file.write(
            f'Patch group: 95% energy @ {patch_summary["patch_k95"]}, '
            f'99% energy @ {patch_summary["patch_k99"]}\n'
        )
        best = max(baseline, key=lambda item: item['PSNR'])
        file.write(f'Best truncated SVD rank: {best["rank"]}, PSNR={best["PSNR"]:.2f} dB\n')

    print(f'[Chapter1] 已保存结果到 {save_dir}')
    return {
        'singular_summary': summary,
        'patch_summary': patch_summary,
        'baseline': baseline,
    }


if __name__ == '__main__':
    run_chapter1()
