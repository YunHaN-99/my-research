"""
chapter6_tilt.py - 第六章：TILT 变换不变低秩纹理

核心思想：给定观测图像 D，联合估计仿射变换 τ 和低秩+稀疏分解：
    min ||L||_* + λ||S||_1
    s.t. D∘τ = L + S

通过迭代线性化，每一步将非线性约束转化为标准 RPCA 问题求解。
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
    compute_metrics,
    get_results_dir,
    get_test_image,
    normalize_image,
    plot_convergence,
    save_latex_table,
    to_gray,
)
from chapter4_patch_rpca import rpca_ialm


# ===================== 仿射变换工具函数 =====================


def affine_identity():
    """返回恒等仿射变换参数 [a, b, tx, c, d, ty]。"""
    return np.array([1.0, 0.0, 0.0, 0.0, 1.0, 0.0], dtype=np.float64)


def params_to_matrix(params):
    """6 参数 → 2×3 仿射矩阵。"""
    return np.array([
        [params[0], params[1], params[2]],
        [params[3], params[4], params[5]],
    ], dtype=np.float64)


def matrix_to_params(matrix):
    """2×3 仿射矩阵 → 6 参数。"""
    return np.array([
        matrix[0, 0], matrix[0, 1], matrix[0, 2],
        matrix[1, 0], matrix[1, 1], matrix[1, 2],
    ], dtype=np.float64)


def warp_image_affine(image, params):
    """使用仿射变换参数对图像进行变换。"""
    matrix = params_to_matrix(params)
    h, w = image.shape[:2]
    return cv2.warpAffine(
        image, matrix, (w, h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REPLICATE,
    )


def compute_affine_jacobian(image, params):
    """计算 d(vec(D∘τ))/d(τ) 的 Jacobian 矩阵。

    对于仿射变换 [a b tx; c d ty]，变换后像素 I(ax+by+tx, cx+dy+ty)，
    对参数求导得到 Jacobian：(h*w, 6) 矩阵。
    """
    warped = warp_image_affine(image, params)
    grad_x = cv2.Sobel(warped, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(warped, cv2.CV_64F, 0, 1, ksize=3)

    h, w = warped.shape[:2]
    ys, xs = np.mgrid[0:h, 0:w]
    xs = xs.astype(np.float64) / max(w - 1, 1)
    ys = ys.astype(np.float64) / max(h - 1, 1)

    jacobian = np.column_stack([
        (grad_x * xs).ravel(),
        (grad_x * ys).ravel(),
        grad_x.ravel(),
        (grad_y * xs).ravel(),
        (grad_y * ys).ravel(),
        grad_y.ravel(),
    ])
    return jacobian


def compose_affine(params, delta):
    """组合仿射变换：将 delta 增量叠加到 params 上。"""
    return params + delta


# ===================== TILT 核心算法 =====================


def tilt(
    observed,
    lam=None,
    max_outer=10,
    inner_iter=50,
    inner_tol=1e-7,
    tol=1e-4,
    step_size=1.0,
    verbose=False,
):
    """TILT: Transform Invariant Low-rank Textures。

    给定观测图像 D，联合求解仿射变换 τ 和分解 D∘τ = L + S。

    Parameters
    ----------
    observed : ndarray (h, w)
        输入灰度图像。
    lam : float or None
        RPCA 中稀疏项的权重，默认 1/sqrt(max(h,w))。
    max_outer : int
        外层迭代次数。
    inner_iter : int
        内层 RPCA 最大迭代次数。
    tol : float
        变换参数收敛阈值。
    step_size : float
        变换更新步长。

    Returns
    -------
    low_rank : ndarray (h, w)
        低秩纹理。
    sparse : ndarray (h, w)
        稀疏污染。
    params : ndarray (6,)
        估计的仿射变换参数。
    history : dict
        收敛历史。
    """
    observed = observed.astype(np.float64)
    if observed.ndim == 3:
        observed = to_gray(observed)

    params = affine_identity()
    history = {
        'delta_norm': [],
        'rpca_error': [],
        'transform_params': [params.copy()],
    }

    for k in range(max_outer):
        warped = warp_image_affine(observed, params)
        low_rank, sparse, errors = rpca_ialm(
            warped, lam=lam, max_iter=inner_iter, tol=inner_tol,
        )

        residual = warped - low_rank - sparse
        jacobian = compute_affine_jacobian(observed, params)
        delta, _, _, _ = np.linalg.lstsq(jacobian, residual.ravel(), rcond=None)

        delta_norm = np.linalg.norm(delta)
        history['delta_norm'].append(delta_norm)
        history['rpca_error'].append(errors[-1] if errors else 0.0)

        params = compose_affine(params, step_size * delta)
        history['transform_params'].append(params.copy())

        if verbose:
            print(f'  TILT outer {k}: ||Δτ||={delta_norm:.6e}, RPCA err={errors[-1] if errors else 0:.6e}')

        if delta_norm < tol:
            break

    warped = warp_image_affine(observed, params)
    low_rank, sparse, _ = rpca_ialm(warped, lam=lam, max_iter=inner_iter, tol=inner_tol)

    return np.clip(low_rank, 0, 1), sparse, params, history


# ===================== 合成纹理生成 =====================


def generate_low_rank_texture(size=(128, 128), pattern='checkerboard', rank=5):
    """生成已知低秩的规则纹理。"""
    h, w = size

    if pattern == 'checkerboard':
        block = max(4, min(h, w) // 16)
        rows = np.arange(h) // block
        cols = np.arange(w) // block
        texture = ((rows[:, None] + cols[None, :]) % 2).astype(np.float64) * 0.6 + 0.2

    elif pattern == 'stripes':
        x = np.linspace(0, 1, w)
        freq = rank * 2
        stripe_row = 0.5 + 0.4 * np.sin(2 * np.pi * freq * x)
        texture = np.tile(stripe_row, (h, 1))

    elif pattern == 'grid':
        x = np.linspace(0, 1, w)
        y = np.linspace(0, 1, h)
        gx, gy = np.meshgrid(x, y)
        freq = max(3, rank)
        texture = 0.5 + 0.2 * np.sin(2 * np.pi * freq * gx) + 0.2 * np.sin(2 * np.pi * freq * gy)

    elif pattern == 'brick':
        block_h = max(4, h // 12)
        block_w = max(6, w // 8)
        texture = np.zeros((h, w), dtype=np.float64)
        for row_idx in range(0, h, block_h):
            for col_idx in range(0, w, block_w):
                offset = (block_w // 2) * ((row_idx // block_h) % 2)
                actual_col = (col_idx + offset) % w
                r_end = min(row_idx + block_h - 1, h)
                c_end = min(actual_col + block_w - 1, w)
                texture[row_idx:r_end, actual_col:c_end] = 0.6
                texture[row_idx:row_idx + 1, :] = 0.3
        texture = np.clip(texture, 0.2, 0.8)

    else:
        x = np.linspace(0, 1, w)
        y = np.linspace(0, 1, h)
        gx, gy = np.meshgrid(x, y)
        texture = 0.5 + 0.3 * np.sin(4 * np.pi * gx) * np.cos(4 * np.pi * gy)

    return normalize_image(texture)


def apply_affine_transform(image, angle_deg=0, shear=0.0, scale=1.0, tx=0, ty=0):
    """对图像施加已知的仿射变换。"""
    h, w = image.shape[:2]
    cx, cy = w / 2.0, h / 2.0

    angle_rad = np.deg2rad(angle_deg)
    cos_a = np.cos(angle_rad) * scale
    sin_a = np.sin(angle_rad) * scale

    a = cos_a + shear * sin_a
    b = -sin_a + shear * cos_a
    c = sin_a
    d = cos_a

    tx_total = cx - a * cx - b * cy + tx
    ty_total = cy - c * cx - d * cy + ty

    matrix = np.array([[a, b, tx_total], [c, d, ty_total]], dtype=np.float64)
    warped = cv2.warpAffine(image, matrix, (w, h),
                            flags=cv2.INTER_LINEAR,
                            borderMode=cv2.BORDER_REPLICATE)
    return warped, matrix_to_params(matrix)


def add_sparse_noise(image, noise_ratio=0.1, seed=42):
    """添加稀疏 salt-and-pepper 噪声。"""
    rng = np.random.RandomState(seed)
    noisy = image.copy()
    mask = rng.rand(*image.shape) < noise_ratio
    noisy[mask] = rng.choice([0.0, 1.0], size=mask.sum())
    return noisy, mask.astype(np.float64)


# ===================== 实验函数 =====================


def demo_tilt_synthetic(size=(128, 128), quick=False):
    """合成实验：低秩纹理 + 已知仿射变换 + 稀疏噪声 → TILT 恢复。"""
    save_dir = get_results_dir('chapter6')
    texture_size = (96, 96) if quick else size

    patterns = ['checkerboard', 'stripes'] if quick else ['checkerboard', 'stripes', 'grid']
    angle = 15.0
    shear = 0.1
    noise_ratio = 0.05
    records = []

    for pattern in patterns:
        clean_texture = generate_low_rank_texture(texture_size, pattern=pattern)

        warped, true_params = apply_affine_transform(
            clean_texture, angle_deg=angle, shear=shear,
        )
        noisy, noise_mask = add_sparse_noise(warped, noise_ratio=noise_ratio, seed=91)

        low_rank, sparse, est_params, history = tilt(
            noisy,
            max_outer=5 if quick else 10,
            inner_iter=30 if quick else 50,
            tol=1e-4,
            step_size=0.5,
        )

        metrics = compute_metrics(clean_texture, low_rank)
        param_error = np.linalg.norm(est_params - affine_identity())
        records.append({
            'pattern': pattern,
            'param_error': param_error,
            **metrics,
        })

        figure, axes = plt.subplots(1, 5, figsize=(20, 4))
        for axis, img, title in zip(
            axes,
            [clean_texture, warped, noisy, np.clip(low_rank, 0, 1), np.clip(np.abs(sparse), 0, 1)],
            [
                '原始纹理',
                f'仿射变换\n(角度={angle}°, shear={shear})',
                f'+ 稀疏噪声 ({noise_ratio:.0%})',
                f'TILT 低秩 L\nPSNR={metrics["PSNR"]:.2f}',
                'TILT 稀疏 |S|',
            ],
        ):
            axis.imshow(np.clip(img, 0, 1), cmap='gray')
            axis.set_title(title, fontsize=9)
            axis.axis('off')
        figure.suptitle(f'TILT 合成实验: {pattern}', fontsize=13)
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, f'tilt_synthetic_{pattern}.png'), dpi=150, bbox_inches='tight')
        plt.close(figure)

    save_latex_table(
        ['Pattern', 'PSNR', 'SSIM', 'Param Error'],
        [[r['pattern'], f'{r["PSNR"]:.2f}', f'{r["SSIM"]:.3f}', f'{r["param_error"]:.4f}'] for r in records],
        os.path.join(save_dir, 'tilt_synthetic_table.tex'),
        caption='TILT 合成纹理实验结果',
        label='tab:chapter6_tilt_synthetic',
    )
    return records


def demo_tilt_real_texture(size=(128, 128), quick=False):
    """真实图像实验：对 Barbara 纹理区域做 TILT 分解。"""
    save_dir = get_results_dir('chapter6')
    texture_size = (96, 96) if quick else size
    image = get_test_image('barbara', gray=True, size=(256, 256))

    h, w = image.shape
    region = image[h // 4:h // 4 + texture_size[0], w // 4:w // 4 + texture_size[1]].copy()

    noisy_region, _ = add_sparse_noise(region, noise_ratio=0.08, seed=101)

    low_rank, sparse, params, history = tilt(
        noisy_region,
        max_outer=5 if quick else 8,
        inner_iter=30 if quick else 50,
        tol=1e-4,
        step_size=0.3,
    )

    metrics = compute_metrics(region, low_rank)

    figure, axes = plt.subplots(1, 4, figsize=(16, 4))
    for axis, img, title in zip(
        axes,
        [region, noisy_region, np.clip(low_rank, 0, 1), np.clip(np.abs(sparse), 0, 1)],
        ['Barbara 纹理区域', '+ 稀疏噪声', f'TILT 低秩 L\nPSNR={metrics["PSNR"]:.2f}', 'TILT 稀疏 |S|'],
    ):
        axis.imshow(np.clip(img, 0, 1), cmap='gray')
        axis.set_title(title)
        axis.axis('off')
    figure.suptitle('TILT 真实纹理分解 (Barbara)', fontsize=13)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'tilt_real_barbara.png'), dpi=150, bbox_inches='tight')
    plt.close(figure)

    return metrics, params, history


def tilt_convergence_analysis(size=(128, 128), quick=False):
    """TILT 收敛分析：绘制变换参数和 RPCA 误差随迭代的变化。"""
    save_dir = get_results_dir('chapter6')
    texture_size = (96, 96) if quick else size
    texture = generate_low_rank_texture(texture_size, pattern='checkerboard')
    warped, true_params = apply_affine_transform(texture, angle_deg=20, shear=0.15)
    noisy, _ = add_sparse_noise(warped, noise_ratio=0.08, seed=107)

    _, _, est_params, history = tilt(
        noisy,
        max_outer=8 if quick else 15,
        inner_iter=30 if quick else 50,
        tol=1e-6,
        step_size=0.5,
        verbose=False,
    )

    figure, axes = plt.subplots(1, 3, figsize=(15, 4))

    axes[0].semilogy(np.maximum(history['delta_norm'], 1e-15), 'o-', color='royalblue')
    axes[0].set_xlabel('Outer Iteration')
    axes[0].set_ylabel('||Δτ||')
    axes[0].set_title('变换增量收敛')
    axes[0].grid(True, alpha=0.3)

    axes[1].semilogy(np.maximum(history['rpca_error'], 1e-15), 's-', color='darkorange')
    axes[1].set_xlabel('Outer Iteration')
    axes[1].set_ylabel('RPCA Error')
    axes[1].set_title('内层 RPCA 残差')
    axes[1].grid(True, alpha=0.3)

    param_history = np.array(history['transform_params'])
    identity = affine_identity()
    param_errors = [np.linalg.norm(p - identity) for p in param_history]
    axes[2].plot(param_errors, 'D-', color='forestgreen')
    axes[2].set_xlabel('Outer Iteration')
    axes[2].set_ylabel('||τ - I||')
    axes[2].set_title('变换参数轨迹')
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'tilt_convergence.png'), dpi=150, bbox_inches='tight')
    plt.close(figure)

    return history


def tilt_noise_robustness(size=(128, 128), quick=False):
    """TILT 对不同稀疏噪声水平的鲁棒性测试。"""
    save_dir = get_results_dir('chapter6')
    texture_size = (96, 96) if quick else size
    texture = generate_low_rank_texture(texture_size, pattern='stripes')
    warped, _ = apply_affine_transform(texture, angle_deg=12, shear=0.08)

    noise_ratios = [0.02, 0.05, 0.1, 0.15] if quick else [0.02, 0.05, 0.08, 0.1, 0.15, 0.2]
    records = []

    for nr in noise_ratios:
        noisy, _ = add_sparse_noise(warped, noise_ratio=nr, seed=113)
        low_rank, sparse, params, history = tilt(
            noisy,
            max_outer=5 if quick else 8,
            inner_iter=30 if quick else 50,
            step_size=0.5,
        )
        metrics = compute_metrics(texture, low_rank)
        records.append({'noise_ratio': nr, **metrics})

    figure, axis = plt.subplots(figsize=(8, 5))
    axis.plot([r['noise_ratio'] for r in records], [r['PSNR'] for r in records], 'o-', color='crimson')
    axis.set_xlabel('稀疏噪声比例')
    axis.set_ylabel('PSNR (dB)')
    axis.set_title('TILT 噪声鲁棒性: PSNR vs 噪声比例')
    axis.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'tilt_noise_robustness.png'), dpi=150, bbox_inches='tight')
    plt.close(figure)

    save_latex_table(
        ['Noise Ratio', 'PSNR', 'SSIM'],
        [[f'{r["noise_ratio"]:.0%}', f'{r["PSNR"]:.2f}', f'{r["SSIM"]:.3f}'] for r in records],
        os.path.join(save_dir, 'tilt_noise_robustness_table.tex'),
        caption='TILT 噪声鲁棒性测试',
        label='tab:chapter6_tilt_robustness',
    )
    return records


def run_chapter6(size=(128, 128), quick=False):
    demo_tilt_synthetic(size=size, quick=quick)
    demo_tilt_real_texture(size=size, quick=quick)
    tilt_convergence_analysis(size=size, quick=quick)
    tilt_noise_robustness(size=size, quick=quick)
    print(f'[Chapter6] 已保存结果到 {get_results_dir("chapter6")}')


if __name__ == '__main__':
    run_chapter6()
