"""
utils.py - 深度分析版低秩图像修复通用工具

覆盖以下能力：
1. 数据加载与经典图像回退
2. 缺失模式/污染模式生成
3. 评价指标与 LaTeX 表格导出
4. 奇异值分析、可视化
5. 整图低秩算子（SVT / shrink / truncated SVD）
6. Patch 提取、block matching、聚合
7. 多尺度 resize 与 TV 后处理
"""

from collections import OrderedDict
import os

import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from skimage.metrics import structural_similarity
from skimage.restoration import denoise_tv_chambolle


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
IMAGE_DIR = os.path.join(DATA_DIR, 'images')
VIDEO_DIR = os.path.join(DATA_DIR, 'videos')
RESULTS_DIR = os.path.join(ROOT_DIR, 'results')


plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'STHeiti', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False


IMAGE_ALIASES = {
    'lena': ['lena', 'lena_gray', 'lenna'],
    'barbara': ['barbara', 'barbara_gray'],
    'peppers': ['peppers', 'pepper'],
    'baboon': ['baboon', 'mandrill'],
    'selfie': ['selfie', 'custom_photo', 'myphoto', 'phone_photo', 'portrait'],
    'custom_photo': ['custom_photo', 'selfie', 'myphoto', 'phone_photo', 'portrait'],
    'cameraman': ['cameraman', 'camera'],
    'astronaut': ['astronaut'],
    'chelsea': ['chelsea'],
}


SKIMAGE_FALLBACKS = {
    'lena': 'astronaut',
    'barbara': 'brick',
    'peppers': 'coffee',
    'baboon': 'grass',
    'selfie': 'astronaut',
    'custom_photo': 'astronaut',
    'cameraman': 'camera',
    'astronaut': 'astronaut',
    'chelsea': 'chelsea',
}


IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path


def get_results_dir(chapter=None):
    if chapter is None:
        return ensure_dir(RESULTS_DIR)
    return ensure_dir(os.path.join(RESULTS_DIR, chapter))


def normalize_image(image):
    image = image.astype(np.float64)
    if image.max() > 1.0:
        image = image / 255.0
    return np.clip(image, 0.0, 1.0)


def resize_image(image, size):
    target_w, target_h = size[1], size[0]
    current_h, current_w = image.shape[:2]
    interpolation = cv2.INTER_AREA if target_h < current_h or target_w < current_w else cv2.INTER_LINEAR
    return cv2.resize(image, (target_w, target_h), interpolation=interpolation)


def to_gray(image):
    if image.ndim == 2:
        return normalize_image(image)
    image_uint8 = np.clip(image * 255.0, 0, 255).astype(np.uint8) if image.max() <= 1.0 else image.astype(np.uint8)
    gray = cv2.cvtColor(image_uint8, cv2.COLOR_RGB2GRAY)
    return normalize_image(gray)


def to_rgb(image):
    if image.ndim == 3:
        return normalize_image(image)
    rgb = np.stack([image, image, image], axis=-1)
    return normalize_image(rgb)


def load_image(path, gray=False, size=(256, 256)):
    if gray:
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    else:
        image = cv2.imread(path, cv2.IMREAD_COLOR)
        if image is not None:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if image is None:
        raise FileNotFoundError(f'Cannot load image: {path}')
    image = normalize_image(image)
    if gray and image.ndim == 3:
        image = to_gray(image)
    if not gray and image.ndim == 2:
        image = to_rgb(image)
    return normalize_image(resize_image(image, size))


def _candidate_image_paths(name):
    aliases = IMAGE_ALIASES.get(name.lower(), [name.lower()])
    suffixes = ['png', 'jpg', 'jpeg', 'bmp', 'tif', 'tiff']
    paths = []
    for alias in aliases:
        for suffix in suffixes:
            paths.append(os.path.join(IMAGE_DIR, f'{alias}.{suffix}'))
            paths.append(os.path.join(IMAGE_DIR, f'{alias.upper()}.{suffix}'))
    return paths


def _find_generic_local_photo():
    if not os.path.exists(IMAGE_DIR):
        return None

    known_aliases = set()
    for aliases in IMAGE_ALIASES.values():
        known_aliases.update(alias.lower() for alias in aliases)

    all_files = sorted(
        file for file in os.listdir(IMAGE_DIR)
        if file.lower().endswith(IMAGE_EXTENSIONS)
    )
    if not all_files:
        return None

    preferred_keywords = ['selfie', 'custom', 'myphoto', 'phone', 'portrait', 'photo', 'img']
    for file in all_files:
        lower = file.lower()
        if any(keyword in lower for keyword in preferred_keywords):
            return os.path.join(IMAGE_DIR, file)

    for file in all_files:
        stem = os.path.splitext(file)[0].lower()
        if stem not in known_aliases:
            return os.path.join(IMAGE_DIR, file)

    return os.path.join(IMAGE_DIR, all_files[0])


def _load_skimage_fallback(name):
    from skimage import data as skdata

    key = SKIMAGE_FALLBACKS.get(name.lower())
    if key is None:
        return None, None
    sample = getattr(skdata, key)()
    source = f'skimage:{key}'
    return normalize_image(sample), source


def _generate_synthetic_image(name='synthetic', size=(256, 256)):
    height, width = size
    x = np.linspace(0, 1, width)
    y = np.linspace(0, 1, height)
    grid_x, grid_y = np.meshgrid(x, y)

    if name.lower() == 'baboon':
        image = 0.45 + 0.25 * np.sin(16 * np.pi * grid_x) * np.cos(14 * np.pi * grid_y)
        image += 0.15 * np.sin(41 * np.pi * (grid_x + grid_y))
        image += 0.1 * ((np.floor(grid_x * 24) + np.floor(grid_y * 18)) % 2)
    elif name.lower() == 'barbara':
        image = 0.45 + 0.2 * np.sin(10 * np.pi * grid_x) * np.sin(12 * np.pi * grid_y)
        image += 0.15 * ((np.floor(grid_x * 18) + np.floor(grid_y * 18)) % 2)
    elif name.lower() == 'peppers':
        image = 0.3 + 0.4 * np.exp(-((grid_x - 0.35) ** 2 + (grid_y - 0.45) ** 2) / 0.03)
        image += 0.35 * np.exp(-((grid_x - 0.65) ** 2 + (grid_y - 0.55) ** 2) / 0.04)
    else:
        image = 0.35 + 0.25 * np.exp(-((grid_x - 0.5) ** 2 + (grid_y - 0.4) ** 2) / 0.05)
        image += 0.15 * np.sin(4 * np.pi * grid_x) * np.cos(4 * np.pi * grid_y)
    return normalize_image(image)


def get_test_image(name='lena', gray=True, size=(256, 256), return_source=False):
    key = name.lower()
    for candidate in _candidate_image_paths(key):
        if os.path.exists(candidate):
            image = load_image(candidate, gray=gray, size=size)
            return (image, f'local:{os.path.basename(candidate)}') if return_source else image

    if key in {'selfie', 'custom_photo'}:
        generic_photo = _find_generic_local_photo()
        if generic_photo is not None:
            image = load_image(generic_photo, gray=gray, size=size)
            return (image, f'local:{os.path.basename(generic_photo)}') if return_source else image

    image, source = _load_skimage_fallback(key)
    if image is None:
        image = _generate_synthetic_image(key, size=size)
        source = f'synthetic:{key}'
    if gray:
        image = to_gray(image)
    else:
        image = to_rgb(image)
    image = normalize_image(resize_image(image, size))
    return (image, source) if return_source else image


def get_test_images(names=None, size=(256, 256), gray=True, return_sources=False):
    if names is None:
        names = get_core_image_names(quick=False)
    images = OrderedDict()
    sources = OrderedDict()
    for name in names:
        image, source = get_test_image(name, gray=gray, size=size, return_source=True)
        images[name] = image
        sources[name] = source
    if return_sources:
        return images, sources
    return images


def get_core_image_names(quick=False):
    return ['lena', 'barbara'] if quick else ['lena', 'barbara', 'selfie']


def get_core_images(size=(256, 256), gray=True, quick=False, return_sources=False):
    return get_test_images(get_core_image_names(quick=quick), size=size, gray=gray, return_sources=return_sources)


def get_default_video_path():
    if not os.path.exists(VIDEO_DIR):
        return None
    for filename in sorted(os.listdir(VIDEO_DIR)):
        if filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            return os.path.join(VIDEO_DIR, filename)
    return None


def generate_mask(shape, mode='random_pixel', ratio=0.5, seed=42, **kwargs):
    rng = np.random.RandomState(seed)
    height, width = shape[:2]
    mask_2d = np.ones((height, width), dtype=np.float64)

    if mode == 'random_pixel':
        mask_2d = (rng.rand(height, width) > ratio).astype(np.float64)

    elif mode == 'random_block':
        current_missing = 0.0
        attempts = 0
        while current_missing < ratio and attempts < 512:
            block_h = rng.randint(max(6, height // 16), max(8, height // 4))
            block_w = rng.randint(max(6, width // 16), max(8, width // 4))
            top = rng.randint(0, max(1, height - block_h + 1))
            left = rng.randint(0, max(1, width - block_w + 1))
            mask_2d[top:top + block_h, left:left + block_w] = 0
            current_missing = 1.0 - mask_2d.mean()
            attempts += 1

    elif mode == 'text':
        text = kwargs.get('text', 'LOW RANK')
        overlay = np.full((height, width), 255, dtype=np.uint8)
        repeats = max(3, int(4 + ratio * 8))
        font = cv2.FONT_HERSHEY_SIMPLEX
        for _ in range(repeats):
            scale = rng.uniform(0.7, 1.4)
            thickness = rng.randint(1, 3)
            x = rng.randint(0, max(1, width - 100))
            y = rng.randint(20, max(21, height))
            angle = rng.uniform(-30, 30)
            temp = np.zeros_like(overlay)
            cv2.putText(temp, text, (x, y), font, scale, 255, thickness, cv2.LINE_AA)
            matrix = cv2.getRotationMatrix2D((x, y), angle, 1.0)
            temp = cv2.warpAffine(temp, matrix, (width, height))
            overlay[temp > 0] = 0
        mask_2d = overlay.astype(np.float64) / 255.0

    elif mode == 'scratch':
        overlay = np.full((height, width), 255, dtype=np.uint8)
        current_missing = 0.0
        while current_missing < ratio:
            x1, y1 = rng.randint(0, width), rng.randint(0, height)
            x2, y2 = rng.randint(0, width), rng.randint(0, height)
            thickness = rng.randint(1, max(2, min(height, width) // 48 + 2))
            cv2.line(overlay, (x1, y1), (x2, y2), 0, thickness)
            current_missing = 1.0 - overlay.mean() / 255.0
        mask_2d = overlay.astype(np.float64) / 255.0

    elif mode == 'center_block':
        center_size = kwargs.get('center_size')
        if center_size is not None:
            block_h, block_w = center_size
        else:
            center_fraction = kwargs.get('center_fraction')
            if center_fraction is None:
                block_h = int(height * np.sqrt(ratio))
                block_w = int(width * np.sqrt(ratio))
            else:
                block_h = int(height * center_fraction)
                block_w = int(width * center_fraction)
        block_h = min(block_h, height)
        block_w = min(block_w, width)
        top = (height - block_h) // 2
        left = (width - block_w) // 2
        mask_2d[top:top + block_h, left:left + block_w] = 0

    elif mode == 'column_missing':
        num_cols = max(1, int(width * ratio))
        columns = rng.choice(width, size=num_cols, replace=False)
        mask_2d[:, columns] = 0

    else:
        raise ValueError(f'Unknown mode: {mode}')

    if len(shape) == 3:
        return np.repeat(mask_2d[..., None], shape[2], axis=2)
    return mask_2d


def apply_mask(image, mask, fill_value=0.0):
    if np.isscalar(fill_value):
        return image * mask + fill_value * (1.0 - mask)
    return image * mask + fill_value * (1.0 - mask)


def fill_missing_with_mean(observed, mask):
    filled = observed.copy()
    if observed.ndim == 2:
        observed_values = observed[mask > 0]
        mean_value = observed_values.mean() if observed_values.size > 0 else 0.5
        filled[mask == 0] = mean_value
        return filled

    for channel in range(observed.shape[2]):
        channel_mask = mask[:, :, channel] > 0
        values = observed[:, :, channel][channel_mask]
        mean_value = values.mean() if values.size > 0 else 0.5
        filled[:, :, channel][~channel_mask] = mean_value
    return filled


def overlay_text_corruption(image, text='LOW RANK', repeats=3, seed=42):
    rng = np.random.RandomState(seed)
    corrupted = to_gray(image).copy()
    canvas = np.clip(corrupted * 255, 0, 255).astype(np.uint8)
    font = cv2.FONT_HERSHEY_SIMPLEX
    for _ in range(repeats):
        scale = rng.uniform(0.8, 1.3)
        thickness = rng.randint(1, 3)
        x = rng.randint(0, max(1, canvas.shape[1] - 100))
        y = rng.randint(20, canvas.shape[0])
        cv2.putText(canvas, text, (x, y), font, scale, 255, thickness, cv2.LINE_AA)
    corrupted = canvas.astype(np.float64) / 255.0
    sparse_mask = (np.abs(corrupted - to_gray(image)) > 1e-6).astype(np.float64)
    return corrupted, sparse_mask


def overlay_scratch_corruption(image, num_lines=12, seed=42):
    rng = np.random.RandomState(seed)
    corrupted = to_gray(image).copy()
    canvas = np.clip(corrupted * 255, 0, 255).astype(np.uint8)
    for _ in range(num_lines):
        x1, y1 = rng.randint(0, canvas.shape[1]), rng.randint(0, canvas.shape[0])
        x2, y2 = rng.randint(0, canvas.shape[1]), rng.randint(0, canvas.shape[0])
        thickness = rng.randint(1, 3)
        cv2.line(canvas, (x1, y1), (x2, y2), 255, thickness)
    corrupted = canvas.astype(np.float64) / 255.0
    sparse_mask = (np.abs(corrupted - to_gray(image)) > 1e-6).astype(np.float64)
    return corrupted, sparse_mask


def compute_psnr(original, recovered):
    mse = np.mean((original - recovered) ** 2)
    if mse < 1e-12:
        return 100.0
    return 10.0 * np.log10(1.0 / mse)


def compute_ssim(original, recovered):
    if original.ndim == 3:
        return structural_similarity(original, recovered, channel_axis=2, data_range=1.0)
    return structural_similarity(original, recovered, data_range=1.0)


def compute_rse(original, recovered):
    denominator = max(np.linalg.norm(original.ravel()), 1e-12)
    return np.linalg.norm((original - recovered).ravel()) / denominator


def compute_metrics(original, recovered):
    return {
        'PSNR': compute_psnr(original, recovered),
        'SSIM': compute_ssim(original, recovered),
        'RSE': compute_rse(original, recovered),
    }


def save_latex_table(headers, rows, save_path, caption='', label='tab:results'):
    ensure_dir(os.path.dirname(save_path))
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write('\\begin{table}[htbp]\n')
        file.write('\\centering\n')
        if caption:
            file.write(f'\\caption{{{caption}}}\n')
        if label:
            file.write(f'\\label{{{label}}}\n')
        file.write('\\small\n')
        file.write('\\begin{tabular}{' + '|' + '|'.join(['c'] * len(headers)) + '|}\n')
        file.write('\\hline\n')
        file.write(' & '.join(headers) + ' \\\\\n')
        file.write('\\hline\n')
        for row in rows:
            file.write(' & '.join(str(item) for item in row) + ' \\\\\n')
        file.write('\\hline\n')
        file.write('\\end{tabular}\n')
        file.write('\\end{table}\n')


def plot_comparison(original, masked, recovered, title='', metrics=None, save_path=None):
    figure, axes = plt.subplots(1, 3, figsize=(12, 4))
    cmap = 'gray' if original.ndim == 2 else None
    for axis, image, axis_title in zip(
        axes,
        [original, masked, recovered],
        ['原图', '观测图', '恢复图'],
    ):
        axis.imshow(np.clip(image, 0, 1), cmap=cmap)
        axis.set_title(axis_title)
        axis.axis('off')

    if metrics is not None:
        axes[2].set_title(
            f'恢复图\nPSNR={metrics.get("PSNR", 0):.2f} dB\nSSIM={metrics.get("SSIM", 0):.4f}'
        )
    if title:
        figure.suptitle(title, fontsize=14)
    plt.tight_layout()
    if save_path:
        ensure_dir(os.path.dirname(save_path))
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(figure)


def plot_image_grid(images, titles, save_path, ncols=3, figsize=None, cmap=None, suptitle=None):
    num_images = len(images)
    nrows = int(np.ceil(num_images / ncols))
    if figsize is None:
        figsize = (4 * ncols, 4 * nrows)
    figure, axes = plt.subplots(nrows, ncols, figsize=figsize)
    axes = np.atleast_1d(axes).ravel()
    for axis in axes:
        axis.axis('off')
    for axis, image, title in zip(axes, images, titles):
        local_cmap = cmap if cmap is not None else ('gray' if np.asarray(image).ndim == 2 else None)
        axis.imshow(np.clip(image, 0, 1), cmap=local_cmap)
        axis.set_title(title)
        axis.axis('off')
    if suptitle:
        figure.suptitle(suptitle, fontsize=14)
    plt.tight_layout()
    ensure_dir(os.path.dirname(save_path))
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(figure)


def plot_convergence(history_dict, save_path=None, title='收敛曲线', ylabel='Value', logy=True):
    figure, axis = plt.subplots(figsize=(8, 5))
    if isinstance(history_dict, dict):
        for label, values in history_dict.items():
            values = np.asarray(values, dtype=np.float64)
            if values.size == 0:
                continue
            y_values = np.maximum(values, 1e-12) if logy else values
            if logy:
                axis.semilogy(y_values, label=label)
            else:
                axis.plot(y_values, label=label)
        axis.legend()
    else:
        values = np.asarray(history_dict, dtype=np.float64)
        if values.size > 0:
            y_values = np.maximum(values, 1e-12) if logy else values
            if logy:
                axis.semilogy(y_values)
            else:
                axis.plot(y_values)
    axis.set_xlabel('Iteration')
    axis.set_ylabel(ylabel)
    axis.set_title(title)
    axis.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        ensure_dir(os.path.dirname(save_path))
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(figure)


def compute_singular_profile(matrix):
    if matrix.ndim == 3:
        matrix = to_gray(matrix)
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    cumulative = np.cumsum(singular_values) / max(np.sum(singular_values), 1e-12)
    k95 = int(np.searchsorted(cumulative, 0.95) + 1)
    k99 = int(np.searchsorted(cumulative, 0.99) + 1)
    return singular_values, cumulative, k95, k99


def plot_singular_values(matrix, title='奇异值分布', save_path=None, top_k=80):
    singular_values, cumulative, k95, k99 = compute_singular_profile(matrix)
    top_values = singular_values[:top_k]

    figure, axes = plt.subplots(1, 3, figsize=(15, 4))
    axes[0].plot(top_values)
    axes[0].set_title(f'{title} - 线性')
    axes[0].set_xlabel('奇异值序号')
    axes[0].set_ylabel('奇异值大小')

    axes[1].semilogy(np.maximum(top_values, 1e-12))
    axes[1].set_title(f'{title} - 对数')
    axes[1].set_xlabel('奇异值序号')

    axes[2].plot(cumulative)
    axes[2].axhline(0.95, linestyle='--', color='r', label=f'95% @ {k95}')
    axes[2].axhline(0.99, linestyle=':', color='g', label=f'99% @ {k99}')
    axes[2].legend()
    axes[2].set_title(f'{title} - 累积能量')
    axes[2].set_xlabel('奇异值序号')
    axes[2].set_ylabel('累计能量占比')

    plt.tight_layout()
    if save_path:
        ensure_dir(os.path.dirname(save_path))
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(figure)


def plot_missing_patterns_demo(image, ratio=0.5, save_path=None):
    modes = ['random_pixel', 'random_block', 'text', 'scratch', 'center_block', 'column_missing']
    labels = ['随机像素', '随机块', '文字遮挡', '划痕', '中心块', '整列缺失']
    figure, axes = plt.subplots(2, 3, figsize=(14, 9))
    axes = axes.ravel()
    cmap = 'gray' if image.ndim == 2 else None
    for axis, mode, label in zip(axes, modes, labels):
        mask = generate_mask(image.shape, mode=mode, ratio=ratio)
        corrupted = apply_mask(image, mask)
        missing_ratio = 1.0 - (mask[:, :, 0].mean() if mask.ndim == 3 else mask.mean())
        axis.imshow(np.clip(corrupted, 0, 1), cmap=cmap)
        axis.set_title(f'{label}\n缺失率={missing_ratio:.1%}')
        axis.axis('off')
    figure.suptitle('六种缺失模式展示', fontsize=15)
    plt.tight_layout()
    if save_path:
        ensure_dir(os.path.dirname(save_path))
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(figure)


def plot_iteration_snapshots(snapshots, iterations, title='恢复过程', save_path=None):
    if not snapshots:
        return
    figure, axes = plt.subplots(1, len(snapshots), figsize=(4 * len(snapshots), 4))
    axes = np.atleast_1d(axes)
    cmap = 'gray' if np.asarray(snapshots[0]).ndim == 2 else None
    for axis, snapshot, iteration in zip(axes, snapshots, iterations):
        axis.imshow(np.clip(snapshot, 0, 1), cmap=cmap)
        axis.set_title(f'Iter {iteration}')
        axis.axis('off')
    figure.suptitle(title, fontsize=14)
    plt.tight_layout()
    if save_path:
        ensure_dir(os.path.dirname(save_path))
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(figure)


def svt(matrix, threshold):
    u, singular_values, vt = np.linalg.svd(matrix, full_matrices=False)
    singular_values = np.maximum(singular_values - threshold, 0)
    rank = int(np.sum(singular_values > 1e-10))
    return (u * singular_values) @ vt, rank


def shrink(matrix, threshold):
    return np.sign(matrix) * np.maximum(np.abs(matrix) - threshold, 0)


def truncated_svd(matrix, rank):
    rank = max(1, min(rank, min(matrix.shape)))
    u, singular_values, vt = np.linalg.svd(matrix, full_matrices=False)
    singular_values[rank:] = 0
    return (u * singular_values) @ vt


def iterative_truncated_svd_inpainting(observed, mask, rank, max_iter=20, tol=1e-4):
    current = fill_missing_with_mean(observed, mask)
    history = {'change': []}
    norm_current = max(np.linalg.norm(current.ravel()), 1e-12)
    mask_bool = mask > 0

    for _ in range(max_iter):
        recovered = truncated_svd(current, rank)
        recovered[mask_bool] = observed[mask_bool]
        change = np.linalg.norm((recovered - current).ravel()) / norm_current
        history['change'].append(change)
        current = recovered
        norm_current = max(np.linalg.norm(current.ravel()), 1e-12)
        if change < tol:
            break
    return np.clip(current, 0, 1), history


def downsample_image_and_mask(image, mask=None, scale=0.5):
    target_size = (
        max(1, int(round(image.shape[0] * scale))),
        max(1, int(round(image.shape[1] * scale))),
    )
    image_small = normalize_image(resize_image(image, target_size))
    if mask is None:
        return image_small
    mask_small = resize_image(mask.astype(np.float64), target_size)
    mask_small = (mask_small > 1e-8).astype(np.float64)
    return image_small, mask_small


def upsample_image(image, target_shape):
    return normalize_image(resize_image(image, target_shape))


def tv_refine(image, mask, observed, weight):
    refined = denoise_tv_chambolle(image, weight=weight)
    refined[mask > 0] = observed[mask > 0]
    return normalize_image(refined)


def iter_patch_positions(image_shape, patch_size=8, stride=4):
    height, width = image_shape[:2]
    row_positions = list(range(0, max(height - patch_size + 1, 1), stride))
    col_positions = list(range(0, max(width - patch_size + 1, 1), stride))
    if row_positions[-1] != height - patch_size:
        row_positions.append(max(0, height - patch_size))
    if col_positions[-1] != width - patch_size:
        col_positions.append(max(0, width - patch_size))
    for top in row_positions:
        for left in col_positions:
            yield (top, left)


def extract_patch(image, position, patch_size=8):
    top, left = position
    return image[top:top + patch_size, left:left + patch_size].copy()


def insert_patch(accumulator, weight_map, patch, position, patch_weight=1.0):
    top, left = position
    if accumulator.ndim == 2:
        accumulator[top:top + patch.shape[0], left:left + patch.shape[1]] += patch_weight * patch
        weight_map[top:top + patch.shape[0], left:left + patch.shape[1]] += patch_weight
    else:
        accumulator[top:top + patch.shape[0], left:left + patch.shape[1], :] += patch_weight * patch
        weight_map[top:top + patch.shape[0], left:left + patch.shape[1], :] += patch_weight


def compute_patch_distance(patch_a, patch_b, mask_a, mask_b, min_overlap_ratio=0.5):
    if patch_a.ndim == 3:
        overlap = (mask_a[:, :, 0] > 0.5) & (mask_b[:, :, 0] > 0.5)
        overlap_count = overlap.sum()
        min_required = int(min_overlap_ratio * patch_a.shape[0] * patch_a.shape[1])
        if overlap_count < min_required:
            fallback = np.mean((patch_a - patch_b) ** 2) + 1.0
            return fallback
        diff = patch_a - patch_b
        return np.sum((diff ** 2)[overlap[:, :, None]]) / max(overlap_count * patch_a.shape[2], 1)

    overlap = (mask_a > 0.5) & (mask_b > 0.5)
    overlap_count = overlap.sum()
    min_required = int(min_overlap_ratio * patch_a.shape[0] * patch_a.shape[1])
    if overlap_count < min_required:
        return np.mean((patch_a - patch_b) ** 2) + 1.0
    return np.sum(((patch_a - patch_b) ** 2)[overlap]) / max(overlap_count, 1)


def find_similar_patches(
    image,
    mask,
    reference_position,
    patch_size=8,
    search_window=20,
    num_similar=15,
    candidate_step=2,
    min_overlap_ratio=0.5,
):
    height, width = image.shape[:2]
    ref_top, ref_left = reference_position
    ref_patch = extract_patch(image, reference_position, patch_size)
    ref_mask = extract_patch(mask, reference_position, patch_size)

    top_min = max(0, ref_top - search_window)
    top_max = min(height - patch_size, ref_top + search_window)
    left_min = max(0, ref_left - search_window)
    left_max = min(width - patch_size, ref_left + search_window)

    candidates = []
    for top in range(top_min, top_max + 1, max(1, candidate_step)):
        for left in range(left_min, left_max + 1, max(1, candidate_step)):
            position = (top, left)
            patch = extract_patch(image, position, patch_size)
            patch_mask = extract_patch(mask, position, patch_size)
            distance = compute_patch_distance(ref_patch, patch, ref_mask, patch_mask, min_overlap_ratio=min_overlap_ratio)
            candidates.append((distance, position, patch, patch_mask))

    candidates.sort(key=lambda item: item[0])
    selected = candidates[:max(1, num_similar)]
    distances = [item[0] for item in selected]
    positions = [item[1] for item in selected]
    patches = [item[2] for item in selected]
    masks = [item[3] for item in selected]
    return patches, masks, positions, distances


def stack_patches(patches):
    return np.vstack([patch.reshape(1, -1) for patch in patches])


def unstack_patches(matrix, patch_shape):
    return [row.reshape(patch_shape) for row in matrix]


def aggregate_patches(patches, positions, image_shape, weights=None):
    accumulator = np.zeros(image_shape, dtype=np.float64)
    weight_map = np.zeros(image_shape, dtype=np.float64)
    if weights is None:
        weights = np.ones(len(patches), dtype=np.float64)
    for patch, position, patch_weight in zip(patches, positions, weights):
        insert_patch(accumulator, weight_map, patch, position, patch_weight)
    return accumulator / np.maximum(weight_map, 1e-12)


if __name__ == '__main__':
    chapter_dir = get_results_dir('chapter1')
    lena = get_test_image('lena', gray=True)
    plot_missing_patterns_demo(lena, ratio=0.5, save_path=os.path.join(chapter_dir, 'all_masks_demo.png'))
    plot_singular_values(lena, title='Lena 奇异值示意', save_path=os.path.join(chapter_dir, 'lena_singular_values.png'))
    print('utils 自检完成')
