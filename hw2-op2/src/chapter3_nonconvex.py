"""
chapter3_nonconvex.py - 第三章：Schatten-p 与加权核范数
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
    compute_singular_profile,
    generate_mask,
    get_core_image_names,
    get_results_dir,
    get_test_image,
    get_test_images,
    save_latex_table,
)
from chapter2_nuclear_norm import nuclear_norm_admm


def generalized_shrinkage(w, mu, p, max_newton_iter=20):
    w = np.asarray(w, dtype=np.float64)
    sigma = np.zeros_like(w)

    if abs(p - 1.0) < 1e-12:
        return np.maximum(w - 1.0 / mu, 0.0)

    if abs(p - 0.5) < 1e-12:
        threshold = 1.5 * (1.0 / mu) ** (2.0 / 3.0)
        active = w > threshold
        if np.any(active):
            w_active = w[active]
            argument = (1.0 / (4.0 * mu)) * np.power(np.maximum(w_active / 3.0, 1e-15), -1.5)
            argument = np.clip(argument, -1.0, 1.0)
            phi = np.arccos(argument)
            sigma[active] = (2.0 / 3.0) * w_active * (1 + np.cos(2 * np.pi / 3 - 2 * phi / 3))
        return np.maximum(sigma, 0.0)

    positive = w > 1e-10
    s = w[positive].copy()
    for _ in range(max_newton_iter):
        safe_s = np.maximum(s, 1e-12)
        function = safe_s + (p / mu) * np.power(safe_s, p - 1) - w[positive]
        derivative = 1.0 + (p * (p - 1) / mu) * np.power(safe_s, p - 2)
        derivative = np.where(np.abs(derivative) < 1e-12, 1e-12, derivative)
        s = np.maximum(s - function / derivative, 0.0)

    sigma[positive] = s
    objective_zero = 0.5 * w ** 2
    objective_sigma = 0.5 * (sigma - w) ** 2 + (1.0 / mu) * np.power(np.maximum(sigma, 1e-12), p)
    sigma = np.where(objective_sigma < objective_zero, sigma, 0.0)
    return np.maximum(sigma, 0.0)


def schatten_p_admm(observed, mask, p=0.5, lam=8.0, mu=0.5, rho=1.03, mu_max=80.0, max_iter=200, tol=1e-5, true_image=None):
    mask_bool = mask > 0.5
    x = observed.copy()
    z = x.copy()
    y = np.zeros_like(x)
    norm_obs = max(np.linalg.norm(observed.ravel()), 1e-12)
    history = {'rse': [], 'primal_res': [], 'dual_res': [], 'rank': []}

    for _ in range(max_iter):
        w = z - y / mu
        x = np.where(mask_bool, (lam * observed + mu * w) / (lam + mu), w)
        u, sigma, vt = np.linalg.svd(x + y / mu, full_matrices=False)
        sigma_new = generalized_shrinkage(sigma, mu, p)
        z_new = (u * sigma_new) @ vt
        dual_res = mu * np.linalg.norm(z_new - z)
        z = z_new
        primal_vec = x - z
        y = y + mu * primal_vec
        primal_res = np.linalg.norm(primal_vec)

        history['primal_res'].append(primal_res)
        history['dual_res'].append(dual_res)
        history['rank'].append(int(np.sum(sigma_new > 1e-10)))
        if true_image is not None:
            history['rse'].append(np.linalg.norm((true_image - z).ravel()) / max(np.linalg.norm(true_image.ravel()), 1e-12))

        mu = min(mu * rho, mu_max)
        if primal_res / norm_obs < tol and dual_res / norm_obs < 5 * tol:
            break

    return np.clip(z, 0, 1), history


def weighted_nn_admm(observed, mask, c=1.0, eps=1e-3, lam=8.0, mu=0.5, rho=1.03, mu_max=80.0, max_iter=200, tol=1e-5, true_image=None):
    mask_bool = mask > 0.5
    x = observed.copy()
    z = x.copy()
    y = np.zeros_like(x)
    norm_obs = max(np.linalg.norm(observed.ravel()), 1e-12)
    previous_sigma = np.ones(min(observed.shape), dtype=np.float64)
    history = {'rse': [], 'primal_res': [], 'dual_res': [], 'rank': []}

    for _ in range(max_iter):
        w = z - y / mu
        x = np.where(mask_bool, (lam * observed + mu * w) / (lam + mu), w)
        u, sigma, vt = np.linalg.svd(x + y / mu, full_matrices=False)
        weights = c / (previous_sigma + eps)
        sigma_new = np.maximum(sigma - weights / mu, 0.0)
        z_new = (u * sigma_new) @ vt
        dual_res = mu * np.linalg.norm(z_new - z)
        z = z_new
        primal_vec = x - z
        y = y + mu * primal_vec
        primal_res = np.linalg.norm(primal_vec)
        previous_sigma = sigma_new + eps

        history['primal_res'].append(primal_res)
        history['dual_res'].append(dual_res)
        history['rank'].append(int(np.sum(sigma_new > 1e-10)))
        if true_image is not None:
            history['rse'].append(np.linalg.norm((true_image - z).ravel()) / max(np.linalg.norm(true_image.ravel()), 1e-12))

        mu = min(mu * rho, mu_max)
        if primal_res / norm_obs < tol and dual_res / norm_obs < 5 * tol:
            break

    return np.clip(z, 0, 1), history


def compare_shrinkage_operators(save_dir):
    sigma_range = np.linspace(0, 100, 500)
    tau = 10.0

    figure, axis = plt.subplots(figsize=(8, 6))
    axis.plot(sigma_range, sigma_range, 'k--', alpha=0.4, label='无收缩 y=x')
    axis.plot(sigma_range, np.maximum(sigma_range - tau, 0), label='核范数软阈值', linewidth=2)
    axis.plot(sigma_range, generalized_shrinkage(sigma_range, mu=1.0 / tau, p=0.5), label='Schatten-1/2', linewidth=2)
    weights = tau * 10.0 / (sigma_range + 1.0)
    axis.plot(sigma_range, np.maximum(sigma_range - weights, 0), label='加权核范数', linewidth=2)
    axis.set_xlabel('输入奇异值 σ')
    axis.set_ylabel('输出奇异值 σ̂')
    axis.set_title('三种收缩算子对比')
    axis.legend()
    axis.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'shrinkage_operator_comparison.png'), dpi=150, bbox_inches='tight')
    plt.close(figure)


def p_sweep_experiment(size=(256, 256), quick=False):
    save_dir = get_results_dir('chapter3')
    image = get_test_image('lena', gray=True, size=size)
    mask = generate_mask(image.shape, mode='random_pixel', ratio=0.5, seed=37)
    observed = apply_mask(image, mask)
    p_values = [0.1, 0.3, 0.5, 0.7, 0.9, 1.0] if quick else [0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0]
    psnr_values = []

    for p in p_values:
        recovered, _ = schatten_p_admm(
            observed,
            mask,
            p=p,
            lam=5.0,
            mu=1.0,
            rho=1.1,
            max_iter=50 if quick else 110,
            tol=1e-5,
            true_image=image,
        )
        psnr_values.append(compute_metrics(image, recovered)['PSNR'])

    figure, axis = plt.subplots(figsize=(8, 5))
    axis.plot(p_values, psnr_values, 'o-', color='darkred')
    axis.set_xlabel('p')
    axis.set_ylabel('PSNR (dB)')
    axis.set_title('Schatten-p: PSNR vs p')
    axis.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'p_vs_psnr.png'), dpi=150, bbox_inches='tight')
    plt.close(figure)
    return p_values, psnr_values


def method_comparison(size=(256, 256), quick=False):
    save_dir = get_results_dir('chapter3')
    image_names = get_core_image_names(quick=quick)
    images = get_test_images(image_names, size=size, gray=True)
    rows = []
    latex_rows = []

    for image_name, image in images.items():
        mask = generate_mask(image.shape, mode='random_pixel', ratio=0.5, seed=41)
        observed = apply_mask(image, mask)

        results = {}
        for method_name, runner in [
            ('Nuclear Norm', lambda: nuclear_norm_admm(observed, mask, lam=8.0, mu=0.5, rho=1.03, max_iter=80 if quick else 130, tol=1e-5, true_image=image)[0]),
            ('Schatten-0.5', lambda: schatten_p_admm(observed, mask, p=0.5, lam=8.0, mu=0.5, rho=1.03, max_iter=80 if quick else 130, tol=1e-5, true_image=image)[0]),
            ('WNN', lambda: weighted_nn_admm(observed, mask, c=1.0, eps=1e-3, lam=8.0, mu=0.5, rho=1.03, max_iter=80 if quick else 130, tol=1e-5, true_image=image)[0]),
        ]:
            start = time.time()
            recovered = runner()
            elapsed = time.time() - start
            metrics = compute_metrics(image, recovered)
            metrics['time'] = elapsed
            results[method_name] = (recovered, metrics)
            rows.append([image_name, method_name, f'{metrics["PSNR"]:.2f}', f'{metrics["SSIM"]:.3f}', f'{elapsed:.2f}s'])

        best_psnr = max(metrics['PSNR'] for _, metrics in results.values())
        latex_rows.append([
            image_name,
            *((
                f'\\textbf{{{metrics["PSNR"]:.2f}/{metrics["SSIM"]:.3f}}}'
                if abs(metrics['PSNR'] - best_psnr) < 1e-6 else
                f'{metrics["PSNR"]:.2f}/{metrics["SSIM"]:.3f}'
            ) for _, metrics in results.values())
        ])

        images_to_show = [image, observed] + [item[0] for item in results.values()]
        titles = ['原图', '缺失图'] + [f'{name}\nPSNR={metrics["PSNR"]:.2f}' for name, (_, metrics) in results.items()]
        figure, axes = plt.subplots(1, len(images_to_show), figsize=(4 * len(images_to_show), 4))
        for axis, img, title in zip(axes, images_to_show, titles):
            axis.imshow(np.clip(img, 0, 1), cmap='gray')
            axis.set_title(title)
            axis.axis('off')
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, f'{image_name}_comparison.png'), dpi=150, bbox_inches='tight')
        plt.close(figure)

    save_latex_table(
        ['Image', 'Nuclear Norm', 'Schatten-0.5', 'WNN'],
        latex_rows,
        os.path.join(save_dir, 'method_comparison.tex'),
        caption='第三章方法横评',
        label='tab:chapter3_compare',
    )
    return rows


def bias_improvement_validation(size=(256, 256), quick=False):
    save_dir = get_results_dir('chapter3')
    image = get_test_image('lena', gray=True, size=size)
    mask = generate_mask(image.shape, mode='random_pixel', ratio=0.5, seed=43)
    observed = apply_mask(image, mask)

    recovered_nuclear, _ = nuclear_norm_admm(observed, mask, lam=8.0, mu=0.5, rho=1.03, max_iter=70 if quick else 130, tol=1e-5, true_image=image)
    recovered_schatten, _ = schatten_p_admm(observed, mask, p=0.5, lam=8.0, mu=0.5, rho=1.03, max_iter=70 if quick else 130, tol=1e-5, true_image=image)
    recovered_wnn, _ = weighted_nn_admm(observed, mask, c=1.0, eps=1e-3, lam=8.0, mu=0.5, rho=1.03, max_iter=70 if quick else 130, tol=1e-5, true_image=image)

    true_sigma, _, _, _ = compute_singular_profile(image)
    sigma_nuclear, _, _, _ = compute_singular_profile(recovered_nuclear)
    sigma_schatten, _, _, _ = compute_singular_profile(recovered_schatten)
    sigma_wnn, _, _, _ = compute_singular_profile(recovered_wnn)

    top_k = min(50, len(true_sigma))
    x_axis = np.arange(top_k)

    figure, axis = plt.subplots(figsize=(9, 5))
    axis.plot(x_axis, true_sigma[:top_k], 'k-', linewidth=2, label='真实奇异值')
    axis.plot(x_axis, sigma_nuclear[:top_k], 'r--', label='Nuclear Norm')
    axis.plot(x_axis, sigma_schatten[:top_k], 'b-.', label='Schatten-0.5')
    axis.plot(x_axis, sigma_wnn[:top_k], 'g:', linewidth=2, label='WNN')
    axis.set_title('非凸方法对核范数偏差的改善')
    axis.set_xlabel('奇异值序号')
    axis.set_ylabel('奇异值大小')
    axis.legend()
    axis.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'bias_improvement.png'), dpi=150, bbox_inches='tight')
    plt.close(figure)


def run_chapter3(size=(256, 256), quick=False):
    save_dir = get_results_dir('chapter3')
    compare_shrinkage_operators(save_dir)
    p_sweep_experiment(size=size, quick=quick)
    method_comparison(size=size, quick=quick)
    bias_improvement_validation(size=size, quick=quick)
    print(f'[Chapter3] 已保存结果到 {save_dir}')


if __name__ == '__main__':
    run_chapter3()
