"""
chapter8_comparison.py - 第八章：最终横评 + 结论图表
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
    generate_mask,
    get_core_image_names,
    get_results_dir,
    get_test_images,
    save_latex_table,
)
from chapter2_nuclear_norm import nuclear_norm_admm
from chapter3_nonconvex import schatten_p_admm
from chapter4_patch_rpca import patch_based_inpainting
from chapter5_rslt import rslt_inpainting


def _case_label(mode, ratio):
    if mode == 'random_pixel':
        return f'random_pixel@{ratio:.0%}'
    return mode


def run_full_comparison(size=(256, 256), quick=False):
    save_dir = get_results_dir('chapter8')
    image_names = get_core_image_names(quick=quick)
    images = get_test_images(image_names, size=size, gray=True)
    cases = [('random_pixel', 0.5), ('text', 0.5)] if quick else [
        ('random_pixel', 0.3),
        ('random_pixel', 0.5),
        ('random_pixel', 0.7),
        ('text', 0.5),
        ('scratch', 0.5),
        ('center_block', 0.5),
    ]

    methods = {
        'Whole-NNM': lambda observed, mask, image: nuclear_norm_admm(observed, mask, lam=8.0, mu=0.4, rho=1.05, max_iter=80 if quick else 140, tol=1e-5, true_image=image)[0],
        'Whole-Schatten-0.5': lambda observed, mask, image: schatten_p_admm(observed, mask, p=0.5, lam=8.0, mu=0.5, rho=1.03, max_iter=80 if quick else 140, tol=1e-5, true_image=image)[0],
        'Patch-NNM': lambda observed, mask, image: patch_based_inpainting(observed, mask, shrinkage='soft', outer_iter=3 if quick else 6, stride=6 if quick else 4, candidate_step=4, tau=0.15, true_image=image)[0],
        'RSLT-RPCA': lambda observed, mask, image: rslt_inpainting(observed, mask, stride=6 if quick else 4, candidate_step=4, search_window=16 if quick else 20, num_similar=10 if quick else 15, rpca_max_iter=30 if quick else 50, outer_iter=2 if quick else 3, true_image=image)[0],
        'Patch-WNN+TV': lambda observed, mask, image: patch_based_inpainting(observed, mask, shrinkage='wnn', outer_iter=3 if quick else 6, stride=6 if quick else 4, candidate_step=4, c=0.15, tv_weight=0.05, tv_decay=True, true_image=image)[0],
    }

    records = []
    representative_images = None

    for image_name, image in images.items():
        for mode, ratio in cases:
            mask = generate_mask(image.shape, mode=mode, ratio=ratio, seed=97)
            observed = apply_mask(image, mask)
            case_name = _case_label(mode, ratio)
            case_results = {}

            for method_name, method in methods.items():
                start = time.time()
                recovered = method(observed, mask, image)
                elapsed = time.time() - start
                metrics = compute_metrics(image, recovered)
                records.append({
                    'image': image_name,
                    'case': case_name,
                    'method': method_name,
                    'time': elapsed,
                    **metrics,
                })
                case_results[method_name] = (recovered, metrics, elapsed)

            if representative_images is None and image_name == 'lena' and mode == 'random_pixel' and abs(ratio - 0.5) < 1e-9:
                representative_images = (image, observed, case_results)

    latex_rows = []
    for image_name in image_names:
        for mode, ratio in cases:
            case_name = _case_label(mode, ratio)
            row_records = [item for item in records if item['image'] == image_name and item['case'] == case_name]
            if not row_records:
                continue
            best_psnr = max(item['PSNR'] for item in row_records)
            row = [image_name, case_name]
            for method_name in methods.keys():
                record = next(item for item in row_records if item['method'] == method_name)
                content = f'{record["PSNR"]:.2f}/{record["SSIM"]:.3f}'
                row.append(f'\\textbf{{{content}}}' if abs(record['PSNR'] - best_psnr) < 1e-6 else content)
            latex_rows.append(row)

    save_latex_table(
        ['Image', 'Case', *methods.keys()],
        latex_rows,
        os.path.join(save_dir, 'full_comparison_table.tex'),
        caption='第八章最终横评',
        label='tab:chapter8_final',
    )

    if representative_images is not None:
        image, observed, case_results = representative_images
        images_to_show = [image, observed] + [item[0] for item in case_results.values()]
        titles = ['原图', '缺失图'] + [f'{name}\nPSNR={metrics["PSNR"]:.2f}' for name, (_, metrics, _) in case_results.items()]
        figure, axes = plt.subplots(1, len(images_to_show), figsize=(4 * len(images_to_show), 4))
        for axis, img, title in zip(axes, images_to_show, titles):
            axis.imshow(np.clip(img, 0, 1), cmap='gray')
            axis.set_title(title)
            axis.axis('off')
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, 'representative_visual_comparison.png'), dpi=150, bbox_inches='tight')
        plt.close(figure)

    avg_runtime = []
    avg_psnr = []
    for method_name in methods.keys():
        method_records = [item for item in records if item['method'] == method_name]
        avg_runtime.append(np.mean([item['time'] for item in method_records]))
        avg_psnr.append(np.mean([item['PSNR'] for item in method_records]))

    figure, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].bar(range(len(methods)), avg_runtime, color='teal')
    axes[0].set_xticks(range(len(methods)))
    axes[0].set_xticklabels(methods.keys(), rotation=20, ha='right')
    axes[0].set_ylabel('平均时间 (s)')
    axes[0].set_title('平均运行时间')

    axes[1].bar(range(len(methods)), avg_psnr, color='slateblue')
    axes[1].set_xticks(range(len(methods)))
    axes[1].set_xticklabels(methods.keys(), rotation=20, ha='right')
    axes[1].set_ylabel('平均 PSNR (dB)')
    axes[1].set_title('平均恢复质量')
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'runtime_and_quality.png'), dpi=150, bbox_inches='tight')
    plt.close(figure)

    print(f'[Chapter8] 已保存结果到 {save_dir}')
    return records


def run_chapter8(size=(256, 256), quick=False):
    return run_full_comparison(size=size, quick=quick)


if __name__ == '__main__':
    run_full_comparison()
