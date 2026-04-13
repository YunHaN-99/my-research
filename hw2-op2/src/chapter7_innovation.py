"""
chapter7_innovation.py - 第七章：多尺度 Patch + WNN + TV 创新方法
"""

import os
import sys
import time
from collections import OrderedDict

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from utils import (
    apply_mask,
    compute_metrics,
    downsample_image_and_mask,
    generate_mask,
    get_results_dir,
    get_test_image,
    plot_comparison,
    save_latex_table,
    upsample_image,
)
from chapter2_nuclear_norm import nuclear_norm_admm
from chapter3_nonconvex import schatten_p_admm
from chapter4_patch_rpca import patch_based_inpainting


def multi_scale_patch_wnn_tv_inpainting(
    observed,
    mask,
    scales=(0.25, 0.5, 1.0),
    patch_size=8,
    search_window=20,
    num_similar=15,
    outer_iter=5,
    stride=4,
    candidate_step=4,
    tv_weight=0.08,
    true_image=None,
):
    current_initial = None
    combined_history = {'rse': [], 'psnr': [], 'rank': []}

    for scale in scales:
        if scale < 1.0:
            observed_s, mask_s = downsample_image_and_mask(observed, mask, scale=scale)
            init_s = None if current_initial is None else upsample_image(current_initial, observed_s.shape)
            if init_s is not None:
                init_s[mask_s > 0.5] = observed_s[mask_s > 0.5]
            recovered_s, history_s = patch_based_inpainting(
                observed_s,
                mask_s,
                patch_size=patch_size,
                search_window=max(10, int(search_window * scale * 2)),
                num_similar=max(8, int(num_similar * 0.8)),
                shrinkage='soft',
                outer_iter=2,
                stride=max(2, stride),
                candidate_step=max(2, candidate_step // 2),
                tau=0.05,
                initial=init_s,
                true_image=None if true_image is None else downsample_image_and_mask(true_image, scale=scale),
            )
            current_initial = upsample_image(recovered_s, observed.shape)
        else:
            init_full = observed.copy() if current_initial is None else current_initial.copy()
            init_full[mask > 0.5] = observed[mask > 0.5]
            recovered_s, history_s = patch_based_inpainting(
                observed,
                mask,
                patch_size=patch_size,
                search_window=search_window,
                num_similar=num_similar,
                shrinkage='wnn',
                outer_iter=outer_iter,
                stride=stride,
                candidate_step=candidate_step,
                c=0.15,
                eps=1e-3,
                tv_weight=tv_weight,
                tv_decay=True,
                initial=init_full,
                true_image=true_image,
            )
            current_initial = recovered_s

        for key in combined_history:
            combined_history[key].extend(history_s.get(key, []))

    return np.clip(current_initial, 0, 1), combined_history


def ablation_experiment(size=(256, 256), quick=False):
    save_dir = get_results_dir('chapter7')
    image = get_test_image('lena', gray=True, size=size)
    ratios = [0.5, 0.7] if quick else [0.3, 0.5, 0.7, 0.9]
    configs = OrderedDict([
        ('A: Patch+NNM', lambda observed, mask: patch_based_inpainting(observed, mask, shrinkage='soft', outer_iter=3 if quick else 6, stride=6 if quick else 4, candidate_step=4, tau=0.05, true_image=image)[0]),
        ('B: Patch+WNN', lambda observed, mask: patch_based_inpainting(observed, mask, shrinkage='wnn', outer_iter=3 if quick else 6, stride=6 if quick else 4, candidate_step=4, c=0.15, true_image=image)[0]),
        ('C: Patch+WNN+TV', lambda observed, mask: patch_based_inpainting(observed, mask, shrinkage='wnn', outer_iter=3 if quick else 8, stride=6 if quick else 4, candidate_step=4, c=0.15, tv_weight=0.05, tv_decay=True, true_image=image)[0]),
        ('D: MS+Patch+WNN+TV', lambda observed, mask: multi_scale_patch_wnn_tv_inpainting(observed, mask, outer_iter=3 if quick else 6, stride=6 if quick else 4, candidate_step=4, tv_weight=0.05, true_image=image)[0]),
    ])

    records = []
    for ratio in ratios:
        mask = generate_mask(image.shape, mode='random_pixel', ratio=ratio, seed=71)
        observed = apply_mask(image, mask)
        for config_name, runner in configs.items():
            start = time.time()
            recovered = runner(observed, mask)
            elapsed = time.time() - start
            metrics = compute_metrics(image, recovered)
            records.append({'ratio': ratio, 'config': config_name, 'time': elapsed, **metrics})
            if abs(ratio - 0.5) < 1e-9:
                plot_comparison(
                    image,
                    observed,
                    recovered,
                    title=f'{config_name} @ 50%',
                    metrics=metrics,
                    save_path=os.path.join(save_dir, f'ablation_{config_name.replace(":", "").replace("+", "_").replace(" ", "_")}.png'),
                )

    figure, axes = plt.subplots(1, 2, figsize=(14, 5))
    x_positions = np.arange(len(ratios))
    width = 0.18
    for idx, config_name in enumerate(configs.keys()):
        config_records = [item for item in records if item['config'] == config_name]
        psnr_values = [next(item['PSNR'] for item in config_records if abs(item['ratio'] - ratio) < 1e-9) for ratio in ratios]
        ssim_values = [next(item['SSIM'] for item in config_records if abs(item['ratio'] - ratio) < 1e-9) for ratio in ratios]
        axes[0].bar(x_positions + idx * width, psnr_values, width=width, label=config_name)
        axes[1].bar(x_positions + idx * width, ssim_values, width=width, label=config_name)

    for axis, ylabel, title in zip(axes, ['PSNR (dB)', 'SSIM'], ['消融实验 - PSNR', '消融实验 - SSIM']):
        axis.set_xticks(x_positions + width * 1.5)
        axis.set_xticklabels([f'{ratio:.0%}' for ratio in ratios])
        axis.set_ylabel(ylabel)
        axis.set_title(title)
        axis.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'ablation_bar_chart.png'), dpi=150, bbox_inches='tight')
    plt.close(figure)

    table_rows = [[f'{item["ratio"]:.0%}', item['config'], f'{item["PSNR"]:.2f}', f'{item["SSIM"]:.3f}'] for item in records]
    save_latex_table(
        ['Ratio', 'Config', 'PSNR', 'SSIM'],
        table_rows,
        os.path.join(save_dir, 'ablation_table.tex'),
        caption='第七章消融实验',
        label='tab:chapter7_ablation',
    )
    return records


def failure_case_analysis(size=(256, 256), quick=False):
    save_dir = get_results_dir('chapter7')
    lena = get_test_image('lena', gray=True, size=size)
    barbara = get_test_image('barbara', gray=True, size=size)

    center_size = (min(80, size[0] // 2), min(80, size[1] // 2))
    center_mask = generate_mask(lena.shape, mode='center_block', ratio=0.4, center_size=center_size, seed=79)
    lena_observed = apply_mask(lena, center_mask)
    lena_recovered, _ = multi_scale_patch_wnn_tv_inpainting(
        lena_observed,
        center_mask,
        outer_iter=2 if quick else 4,
        stride=6 if quick else 4,
        candidate_step=4,
        tv_weight=0.08,
        true_image=lena,
    )

    barbara_mask = generate_mask(barbara.shape, mode='random_pixel', ratio=0.7, seed=83)
    barbara_observed = apply_mask(barbara, barbara_mask)
    barbara_recovered, _ = multi_scale_patch_wnn_tv_inpainting(
        barbara_observed,
        barbara_mask,
        outer_iter=2 if quick else 4,
        stride=6 if quick else 4,
        candidate_step=4,
        tv_weight=0.08,
        true_image=barbara,
    )

    plot_comparison(
        lena,
        lena_observed,
        lena_recovered,
        title='失败案例：Lena center block',
        metrics=compute_metrics(lena, lena_recovered),
        save_path=os.path.join(save_dir, 'failure_lena_center_block.png'),
    )
    plot_comparison(
        barbara,
        barbara_observed,
        barbara_recovered,
        title='失败案例：Barbara 70% random pixel',
        metrics=compute_metrics(barbara, barbara_recovered),
        save_path=os.path.join(save_dir, 'failure_barbara_random70.png'),
    )

    return {
        'lena_center_block': compute_metrics(lena, lena_recovered),
        'barbara_random70': compute_metrics(barbara, barbara_recovered),
    }


def run_chapter7(size=(256, 256), quick=False):
    ablation_experiment(size=size, quick=quick)
    failure_case_analysis(size=size, quick=quick)
    print(f'[Chapter7] 已保存结果到 {get_results_dir("chapter7")}')


if __name__ == '__main__':
    run_chapter7()
