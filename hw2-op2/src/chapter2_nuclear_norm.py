"""
chapter2_nuclear_norm.py - 第二章：核范数补全 + 偏差分析
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
    compute_rse,
    compute_singular_profile,
    generate_mask,
    get_core_image_names,
    get_results_dir,
    get_test_image,
    get_test_images,
    plot_comparison,
    save_latex_table,
)


def nuclear_norm_admm(
    observed,
    mask,
    lam=5.0,
    mu=0.4,
    rho=1.05,
    mu_max=80.0,
    max_iter=200,
    tol=1e-5,
    true_image=None,
    snapshot_iters=None,
):
    mask_bool = mask > 0.5
    x = observed.copy()
    z = x.copy()
    y = np.zeros_like(x)
    norm_obs = max(np.linalg.norm(observed.ravel()), 1e-12)

    if snapshot_iters is None:
        snapshot_iters = [0, 9, 49, max_iter - 1]

    history = {
        'rse': [],
        'primal_res': [],
        'dual_res': [],
        'rank': [],
        'snapshots': [],
        'snapshot_iters': [],
    }

    for iteration in range(max_iter):
        w = z - y / mu
        x = np.where(mask_bool, (lam * observed + mu * w) / (lam + mu), w)

        u, sigma, vt = np.linalg.svd(x + y / mu, full_matrices=False)
        sigma_threshold = np.maximum(sigma - 1.0 / mu, 0.0)
        z_new = (u * sigma_threshold) @ vt
        dual_res = mu * np.linalg.norm(z_new - z)
        z = z_new

        primal_vector = x - z
        y = y + mu * primal_vector
        primal_res = np.linalg.norm(primal_vector)

        history['primal_res'].append(primal_res)
        history['dual_res'].append(dual_res)
        history['rank'].append(int(np.sum(sigma_threshold > 1e-10)))
        if true_image is not None:
            history['rse'].append(compute_rse(true_image, z))
        if iteration in snapshot_iters or iteration == max_iter - 1:
            history['snapshots'].append(np.clip(z, 0, 1).copy())
            history['snapshot_iters'].append(iteration + 1)

        mu = min(mu * rho, mu_max)
        if primal_res / norm_obs < tol and dual_res / norm_obs < 5 * tol:
            break

    return np.clip(z, 0, 1), history


def _format_metric(psnr, ssim, highlight=False):
    content = f'{psnr:.2f}/{ssim:.3f}'
    return f'\\textbf{{{content}}}' if highlight else content


def run_missing_rate_experiment(size=(256, 256), quick=False):
    save_dir = get_results_dir('chapter2')
    image_names = get_core_image_names(quick=quick)
    ratios = [0.3, 0.5, 0.7] if quick else [0.1, 0.3, 0.5, 0.7, 0.9]

    images = get_test_images(image_names, size=size, gray=True)
    table_rows = []
    raw_records = []

    for image_name, image in images.items():
        for ratio in ratios:
            mask = generate_mask(image.shape, mode='random_pixel', ratio=ratio, seed=11)
            observed = apply_mask(image, mask)
            start = time.time()
            recovered, history = nuclear_norm_admm(
                observed,
                mask,
                lam=8.0,
                mu=0.4,
                rho=1.05,
                max_iter=80 if quick else 140,
                tol=1e-5,
                true_image=image,
            )
            elapsed = time.time() - start
            metrics = compute_metrics(image, recovered)
            metrics['time'] = elapsed
            raw_records.append({'image': image_name, 'ratio': ratio, **metrics})

    headers = ['Image', 'Ratio', 'PSNR/SSIM']
    rows = []
    for image_name in image_names:
        image_rows = [item for item in raw_records if item['image'] == image_name]
        for record in image_rows:
            rows.append([record['image'], f'{record["ratio"]:.0%}', f'{record["PSNR"]:.2f}/{record["SSIM"]:.3f}'])
    save_latex_table(
        headers,
        rows,
        os.path.join(save_dir, 'missing_rate_table.tex'),
        caption='核范数 ADMM 在不同缺失率下的 PSNR/SSIM',
        label='tab:chapter2_missing',
    )
    return raw_records


def plot_convergence_diagnostics(size=(256, 256), quick=False):
    save_dir = get_results_dir('chapter2')
    image = get_test_image('lena', gray=True, size=size)
    mask = generate_mask(image.shape, mode='random_pixel', ratio=0.5, seed=17)
    observed = apply_mask(image, mask)
    recovered, history = nuclear_norm_admm(
        observed,
        mask,
        lam=5.0,
        mu=1.0,
        rho=1.1,
        max_iter=80 if quick else 150,
        tol=1e-5,
        true_image=image,
        snapshot_iters=[0, 9, 49, 119],
    )

    figure, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes[0, 0].semilogy(np.maximum(history['rse'], 1e-12), color='royalblue')
    axes[0, 0].set_title('RSE vs Iteration')
    axes[0, 0].set_xlabel('Iteration')
    axes[0, 0].set_ylabel('RSE')
    axes[0, 0].grid(True, alpha=0.3)

    axes[0, 1].semilogy(np.maximum(history['primal_res'], 1e-12), label='Primal')
    axes[0, 1].semilogy(np.maximum(history['dual_res'], 1e-12), label='Dual')
    axes[0, 1].set_title('ADMM 残差')
    axes[0, 1].set_xlabel('Iteration')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    axes[1, 0].plot(history['rank'], color='darkorange')
    axes[1, 0].set_title('恢复矩阵秩变化')
    axes[1, 0].set_xlabel('Iteration')
    axes[1, 0].set_ylabel('Rank')
    axes[1, 0].grid(True, alpha=0.3)

    snapshots = history['snapshots'][:4]
    iterations = history['snapshot_iters'][:4]
    snapshot_strip = np.concatenate([np.clip(item, 0, 1) for item in snapshots], axis=1)
    axes[1, 1].imshow(snapshot_strip, cmap='gray')
    axes[1, 1].set_title('第1/10/50/最终次迭代')
    axes[1, 1].axis('off')
    if iterations:
        width = snapshot_strip.shape[1] / len(iterations)
        for idx, iteration in enumerate(iterations):
            axes[1, 1].text(idx * width + 4, 12, f'Iter {iteration}', color='yellow', fontsize=9, bbox={'facecolor': 'black', 'alpha': 0.4})

    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'convergence_diagnostics.png'), dpi=150, bbox_inches='tight')
    plt.close(figure)

    plot_comparison(
        image,
        observed,
        recovered,
        title='Lena @ 50% random pixel',
        metrics=compute_metrics(image, recovered),
        save_path=os.path.join(save_dir, 'lena_50_recovery.png'),
    )
    return recovered, history


def parameter_sensitivity_experiment(size=(256, 256), quick=False):
    save_dir = get_results_dir('chapter2')
    image = get_test_image('lena', gray=True, size=size)
    mask = generate_mask(image.shape, mode='random_pixel', ratio=0.5, seed=23)
    observed = apply_mask(image, mask)
    lambda_values = np.logspace(-2, 2, 6 if quick else 10)
    psnr_values = []

    for lam in lambda_values:
        recovered, _ = nuclear_norm_admm(
            observed,
            mask,
            lam=float(lam),
            mu=1.0,
            rho=1.1,
            max_iter=60 if quick else 120,
            tol=1e-5,
            true_image=image,
        )
        psnr_values.append(compute_metrics(image, recovered)['PSNR'])

    figure, axis = plt.subplots(figsize=(8, 5))
    axis.semilogx(lambda_values, psnr_values, 'o-', color='forestgreen')
    axis.set_xlabel('lambda')
    axis.set_ylabel('PSNR (dB)')
    axis.set_title('参数敏感性：PSNR vs lambda')
    axis.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'lambda_sensitivity.png'), dpi=150, bbox_inches='tight')
    plt.close(figure)
    return lambda_values, psnr_values


def demonstrate_nuclear_norm_bias(size=(256, 256), quick=False):
    save_dir = get_results_dir('chapter2')
    image = get_test_image('lena', gray=True, size=size)
    mask = generate_mask(image.shape, mode='random_pixel', ratio=0.5, seed=29)
    observed = apply_mask(image, mask)
    recovered, _ = nuclear_norm_admm(
        observed,
        mask,
        lam=5.0,
        mu=1.0,
        rho=1.1,
        max_iter=70 if quick else 140,
        tol=1e-5,
        true_image=image,
    )

    true_sigma, _, _, _ = compute_singular_profile(image)
    rec_sigma, _, _, _ = compute_singular_profile(recovered)
    top_k = min(50, len(true_sigma), len(rec_sigma))
    x_axis = np.arange(top_k)

    figure, axis = plt.subplots(figsize=(8, 5))
    axis.plot(x_axis, true_sigma[:top_k], 'b-o', label='真实奇异值', markersize=3)
    axis.plot(x_axis, rec_sigma[:top_k], 'r-x', label='核范数恢复', markersize=3)
    axis.fill_between(x_axis, true_sigma[:top_k], rec_sigma[:top_k], alpha=0.3, color='red', label='Bias')
    axis.set_title('核范数方法的系统偏差')
    axis.set_xlabel('奇异值序号')
    axis.set_ylabel('奇异值大小')
    axis.legend()
    axis.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'nuclear_norm_bias.png'), dpi=150, bbox_inches='tight')
    plt.close(figure)
    return recovered


def run_chapter2(size=(256, 256), quick=False):
    records = run_missing_rate_experiment(size=size, quick=quick)
    plot_convergence_diagnostics(size=size, quick=quick)
    parameter_sensitivity_experiment(size=size, quick=quick)
    demonstrate_nuclear_norm_bias(size=size, quick=quick)
    print(f'[Chapter2] 已保存结果到 {get_results_dir("chapter2")}')
    return records


if __name__ == '__main__':
    run_chapter2()
