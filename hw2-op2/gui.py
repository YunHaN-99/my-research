"""
gui.py - 低秩分解图像修复交互式 GUI (Gradio)

启动方式: python gui.py
"""

import os
import sys
import time
from glob import glob
from pathlib import Path

import gradio as gr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from utils import (
    apply_mask,
    compute_metrics,
    fill_missing_with_mean,
    generate_mask,
    get_test_image,
    normalize_image,
    to_gray,
)
from chapter4_patch_rpca import rpca_ialm, patch_based_inpainting
from chapter5_rslt import rslt_inpainting, rslt_texture_repair
from chapter6_tilt import tilt

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'STHeiti', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False

DEMO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gui_demos')


# ===================== 核心处理函数 =====================


def load_and_prepare_image(image_name, uploaded_image, image_size=256):
    """加载图片：优先使用上传的，否则用预置的。"""
    if uploaded_image is not None:
        img = normalize_image(uploaded_image.astype(np.float64))
        img = to_gray(img)
        from utils import resize_image
        img = resize_image(img, (image_size, image_size))
        return normalize_image(img)
    return get_test_image(image_name, gray=True, size=(image_size, image_size))


def create_corruption(img_gray, corruption_type, corruption_rate):
    """生成污染图像和掩码。"""
    h, w = img_gray.shape

    if corruption_type == '文字叠加':
        mask = generate_mask((h, w), mode='text', ratio=corruption_rate, text='LOW RANK')
        corrupted = apply_mask(img_gray, mask, fill_value=1.0)
    elif corruption_type == '划痕':
        mask = generate_mask((h, w), mode='scratch', ratio=corruption_rate)
        corrupted = apply_mask(img_gray, mask, fill_value=1.0)
    elif corruption_type == '随机像素缺失':
        mask = generate_mask((h, w), mode='random_pixel', ratio=corruption_rate)
        corrupted = apply_mask(img_gray, mask, fill_value=0.0)
    elif corruption_type == '中心块缺失':
        mask = generate_mask((h, w), mode='center_block', ratio=corruption_rate)
        corrupted = apply_mask(img_gray, mask, fill_value=0.0)
    elif corruption_type == '随机块缺失':
        mask = generate_mask((h, w), mode='random_block', ratio=corruption_rate)
        corrupted = apply_mask(img_gray, mask, fill_value=0.0)
    elif corruption_type == '整列缺失':
        mask = generate_mask((h, w), mode='column_missing', ratio=corruption_rate)
        corrupted = apply_mask(img_gray, mask, fill_value=0.0)
    else:
        mask = np.ones_like(img_gray)
        corrupted = img_gray.copy()

    return corrupted, mask


def run_repair(original, corrupted, mask, method, corruption_type):
    """运行修复算法。所有污染类型都有已知 mask，均使用 mask 约束式修复。"""
    # 按污染类型区分迭代强度：文字/划痕掩盖面积较大，需更多迭代
    heavy = corruption_type in ['文字叠加', '划痕']
    history = {}

    start = time.time()

    if method == 'RPCA':
        repaired, history = _rpca_inpainting(
            corrupted, mask, original,
            outer_iter=10 if heavy else 6,
            inner_iter=80 if heavy else 50,
        )

    elif method == 'RSLT':
        repaired, history = rslt_inpainting(
            corrupted, mask,
            stride=4, candidate_step=4,
            search_window=20, num_similar=15,
            rpca_max_iter=60 if heavy else 50,
            outer_iter=4 if heavy else 3,
            true_image=original,
        )

    elif method == 'TILT':
        # TILT 不吃 mask：先用均值填充再交给 TILT
        init = fill_missing_with_mean(corrupted, mask)
        init[mask > 0.5] = corrupted[mask > 0.5]
        low_rank, sparse, params, history = tilt(
            init, max_outer=10, inner_iter=60, step_size=0.5,
        )
        repaired = np.clip(low_rank, 0, 1)
        # 强制已知像素保持不变
        repaired[mask > 0.5] = corrupted[mask > 0.5]

    elif method == 'Patch-WNN':
        repaired, hist = patch_based_inpainting(
            corrupted, mask,
            shrinkage='wnn',
            outer_iter=6 if heavy else 4,
            stride=4, candidate_step=4,
            search_window=20, num_similar=15,
            true_image=original,
        )
        history = hist

    else:
        repaired = corrupted.copy()

    elapsed = time.time() - start
    return repaired, history, elapsed


def _rpca_inpainting(observed, mask, true_image, outer_iter=6, inner_iter=50):
    """RPCA 迭代补全：在已知像素约束下反复做低秩投影。"""
    current = fill_missing_with_mean(observed, mask)
    current[mask > 0.5] = observed[mask > 0.5]
    history = {'psnr': [], 'rpca_error': []}

    for _ in range(outer_iter):
        low_rank, _, errors = rpca_ialm(current, max_iter=inner_iter)
        current = low_rank
        current[mask > 0.5] = observed[mask > 0.5]
        if true_image is not None:
            metrics = compute_metrics(true_image, np.clip(current, 0, 1))
            history['psnr'].append(metrics['PSNR'])
        if errors:
            history['rpca_error'].append(errors[-1])

    return np.clip(current, 0, 1), history


def make_convergence_plot(history):
    """生成收敛曲线 matplotlib figure。"""
    fig, ax = plt.subplots(figsize=(5, 3.5))

    has_data = False
    if 'psnr' in history and len(history.get('psnr', [])) > 0:
        ax.plot(history['psnr'], 'o-', color='royalblue', label='PSNR (dB)', markersize=4)
        ax.set_ylabel('PSNR (dB)')
        has_data = True
    if 'rpca_error' in history and len(history.get('rpca_error', [])) > 0:
        ax.semilogy(np.maximum(history['rpca_error'], 1e-15), 's-', color='darkorange', label='RPCA 残差', markersize=4)
        ax.set_ylabel('Error')
        has_data = True
    if 'delta_norm' in history and len(history.get('delta_norm', [])) > 0:
        ax.semilogy(np.maximum(history['delta_norm'], 1e-15), 'D-', color='forestgreen', label='TILT ||Δτ||', markersize=4)
        ax.set_ylabel('||Δτ||')
        has_data = True
    if 'sparse_energy' in history and len(history.get('sparse_energy', [])) > 0:
        ax.plot(history['sparse_energy'], '^-', color='crimson', label='稀疏能量', markersize=4)
        has_data = True

    if not has_data:
        ax.text(0.5, 0.5, '无收敛数据', ha='center', va='center', fontsize=14, color='gray')
    else:
        ax.set_xlabel('迭代次数')
        ax.set_title('收敛曲线')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def to_display(arr):
    """float64 [0,1] → uint8 for Gradio Image。"""
    return np.clip(arr * 255, 0, 255).astype(np.uint8)


# ===================== 主处理流程 =====================


def main_process(image_name, uploaded_image, corruption_type, corruption_rate, method):
    """Gradio 回调。"""
    original = load_and_prepare_image(image_name, uploaded_image)
    corrupted, mask = create_corruption(original, corruption_type, corruption_rate)
    repaired, history, elapsed = run_repair(original, corrupted, mask, method, corruption_type)

    metrics = compute_metrics(original, repaired)
    metrics_text = (
        f"PSNR:  {metrics['PSNR']:.2f} dB\n"
        f"SSIM:  {metrics['SSIM']:.4f}\n"
        f"RSE:   {metrics['RSE']:.4f}\n"
        f"耗时:  {elapsed:.2f} 秒"
    )

    fig = make_convergence_plot(history)
    return to_display(original), to_display(corrupted), to_display(repaired), metrics_text, fig


# ===================== Demo 数据加载 =====================


def load_demo_data():
    """扫描 gui_demos/ 目录，加载预生成的修复效果数据。"""
    info_files = sorted(glob(os.path.join(DEMO_DIR, '*_info.txt')))
    demos = []
    for info_file in info_files:
        tag = Path(info_file).stem.replace('_info', '')
        orig = os.path.join(DEMO_DIR, f'{tag}_orig.png')
        corrupt = os.path.join(DEMO_DIR, f'{tag}_corrupt.png')
        repair = os.path.join(DEMO_DIR, f'{tag}_repair.png')
        if not os.path.exists(orig) or not os.path.exists(repair):
            continue
        # For real damaged photos, corrupt may not exist; use orig as corrupt
        if not os.path.exists(corrupt):
            corrupt = orig
        with open(info_file, 'r', encoding='utf-8') as f:
            parts = f.read().strip().split('|')
        if len(parts) >= 6:
            img_name, corr_type, rate, method = parts[0], parts[1], parts[2], parts[3]
            psnr, ssim = parts[4], parts[5]
            label = f'{img_name} · {corr_type} · {method} · {psnr} · {ssim}'
        else:
            label = tag
        demos.append({'orig': orig, 'corrupt': corrupt, 'repair': repair, 'label': label})
    return demos


# ===================== 算法说明 =====================

ALGO_INTRO = r"""
## Robust PCA (RPCA)

将观测矩阵 $D$ 分解为低秩矩阵 $L$ 和稀疏矩阵 $S$：

$$\min_{L,S} \|L\|_* + \lambda \|S\|_1 \quad \text{s.t.} \quad D = L + S$$

- $\|L\|_*$ 核范数（奇异值之和）—— 鼓励低秩
- $\|S\|_1$ L1 范数 —— 鼓励稀疏
- 通过 **增广拉格朗日乘子法 (ALM)** 或 **ADMM** 求解

**适用场景**: 文字/划痕去除、视频背景分离

---

## RSLT — 稀疏低秩纹理修复

在 Patch 级别做 RPCA 分解：

1. 提取相似 patch group，堆叠为矩阵
2. 对 patch 矩阵做 RPCA 分解 $M = L + S$
3. 低秩部分 $L$ 保留纹理结构，稀疏部分 $S$ 剥离污染
4. 聚合回原图

$$\text{Patch Group Matrix} = \underbrace{L}_{\text{纹理结构}} + \underbrace{S}_{\text{稀疏污染}}$$

**优势**: 比整图 RPCA 更好地保留局部纹理细节

---

## TILT — 变换不变低秩纹理

联合估计仿射变换 $\tau$ 和低秩+稀疏分解：

$$\min_{L,S,\tau} \|L\|_* + \lambda \|S\|_1 \quad \text{s.t.} \quad D \circ \tau = L + S$$

通过 **迭代线性化** 求解：
1. 对变换进行线性化 $D \circ (\tau + \Delta\tau) \approx D \circ \tau + J \cdot \Delta\tau$
2. 每步求解标准 RPCA + 最小二乘更新 $\Delta\tau$
3. 迭代直至收敛

**适用场景**: 带几何畸变的纹理恢复、图像矫正

---

## Patch-WNN — 加权核范数 Patch 修复

对 patch group 使用 **加权核范数最小化 (WNN)** 代替软阈值：

$$\min_{L} \sum_i w_i \sigma_i(L), \quad w_i = \frac{c}{\sigma_i + \epsilon}$$

较大奇异值（重要结构）惩罚小，较小奇异值（噪声）惩罚大，减少核范数的系统偏差。
"""


# ===================== Gradio 界面 =====================

test_image_names = ['lena', 'barbara', 'baboon', 'cameraman', 'peppers',
                    'old_scratch1', 'old_scratch2', 'old_scratch3']

_css = """
.gr-block { border-radius: 12px !important; }
footer { display: none !important; }
"""

with gr.Blocks(title='低秩分解图像修复') as demo:

    gr.Markdown('# 低秩分解图像修复演示系统')
    gr.Markdown('*Robust PCA / RSLT / TILT / Patch-WNN*')

    with gr.Tabs():

        # ==================== Tab 1: 交互修复 ====================
        with gr.TabItem('交互修复'):

            with gr.Row(equal_height=False):
                # 左侧控制面板
                with gr.Column(scale=1, min_width=300):

                    with gr.Accordion('图片选择', open=True):
                        image_name = gr.Dropdown(
                            test_image_names, label='预置图片', value='lena',
                        )
                        uploaded_image = gr.Image(
                            label='或上传自定义图片', type='numpy', height=140,
                        )

                    with gr.Accordion('污染设置', open=True):
                        corruption_type = gr.Radio(
                            ['文字叠加', '划痕', '随机像素缺失', '中心块缺失', '随机块缺失', '整列缺失'],
                            label='污染类型', value='随机像素缺失',
                        )
                        corruption_rate = gr.Slider(
                            0.05, 0.9, step=0.05, label='污染率', value=0.5,
                        )

                    with gr.Accordion('修复方法', open=True):
                        method = gr.Radio(
                            ['RPCA', 'RSLT', 'TILT', 'Patch-WNN'],
                            label='算法', value='RSLT',
                        )

                    run_btn = gr.Button('运行修复', variant='primary', size='lg')

                # 右侧结果展示
                with gr.Column(scale=3):

                    with gr.Row():
                        output_original = gr.Image(label='原图', type='numpy')
                        output_corrupted = gr.Image(label='污染图', type='numpy')
                        output_repaired = gr.Image(label='修复图', type='numpy')

                    with gr.Row():
                        metrics_output = gr.Textbox(
                            label='评价指标', lines=4, max_lines=4, scale=1,
                        )
                        convergence_plot = gr.Plot(label='收敛曲线', scale=2)

            run_btn.click(
                fn=main_process,
                inputs=[image_name, uploaded_image, corruption_type, corruption_rate, method],
                outputs=[output_original, output_corrupted, output_repaired, metrics_output, convergence_plot],
            )

            gr.Markdown('#### 快速示例（点击自动填入参数）')
            gr.Examples(
                examples=[
                    ['barbara', None, '随机像素缺失', 0.15, 'RSLT'],
                    ['lena', None, '文字叠加', 0.15, 'RPCA'],
                    ['lena', None, '随机像素缺失', 0.2, 'Patch-WNN'],
                    ['barbara', None, '划痕', 0.1, 'RSLT'],
                    ['peppers', None, '随机像素缺失', 0.15, 'TILT'],
                ],
                inputs=[image_name, uploaded_image, corruption_type, corruption_rate, method],
                label='',
            )

        # ==================== Tab 2: 效果展示 ====================
        with gr.TabItem('效果展示'):
            gr.Markdown('## 预生成效果概览')
            gr.Markdown('不同算法在不同污染类型下的修复效果 · 每组依次为：**原图 → 污染图 → 修复图**')

            demo_data = load_demo_data()
            if not demo_data:
                gr.Markdown('> `gui_demos/` 目录下未找到展示图片。')
            else:
                gallery_items = []
                for item in demo_data:
                    gallery_items.append((item['orig'], f'{item["label"]} · 原图'))
                    gallery_items.append((item['corrupt'], f'{item["label"]} · 污染图'))
                    gallery_items.append((item['repair'], f'{item["label"]} · 修复图'))
                gr.Gallery(
                    value=gallery_items,
                    columns=3,
                    rows=len(demo_data),
                    object_fit='contain',
                    height='auto',
                    show_label=False,
                    allow_preview=True,
                )

        # ==================== Tab 3: 算法说明 ====================
        with gr.TabItem('算法说明'):
            gr.Markdown(
                ALGO_INTRO,
                latex_delimiters=[
                    {'left': '$$', 'right': '$$', 'display': True},
                    {'left': '$', 'right': '$', 'display': False},
                ],
            )

    gr.Markdown(
        '<center style="color:#aaa; padding:16px 0 8px;">'
        '数学建模 HW2 · 低秩分解在图像修复中的应用'
        '</center>'
    )


if __name__ == '__main__':
    demo.launch(theme=gr.themes.Soft(), css=_css)
