import json
import os
import sys
import time

import matplotlib
matplotlib.use('Agg')


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
RUN_DIR = os.path.abspath(os.path.join(THIS_DIR, '..'))
ROOT_DIR = os.path.abspath(os.path.join(THIS_DIR, '..', '..', '..', '..', '..'))
GOLD_SRC = os.path.join(ROOT_DIR, 'hw2-op2', 'src')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'outputs', 'hw2_op2', 'run_041_coe_guided_rep3')

if THIS_DIR not in sys.path:
    sys.path.insert(0, THIS_DIR)
if GOLD_SRC not in sys.path:
    sys.path.insert(1, GOLD_SRC)

from a2_generated import rslt_inpainting
from utils import apply_mask, compute_metrics, generate_mask, get_test_images, plot_comparison


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    image_names = ['lena', 'barbara']
    images, sources = get_test_images(image_names, size=(256, 256), gray=True, return_sources=True)
    cases = [
        ('random_pixel', 0.5),
        ('text', 0.5),
    ]

    records = []
    eval_start = time.time()

    for image_name in image_names:
        image = images[image_name]
        source = sources[image_name]

        for corruption_mode, corruption_ratio in cases:
            mask = generate_mask(image.shape, mode=corruption_mode, ratio=corruption_ratio, seed=97)
            observed = apply_mask(image, mask)

            case_label = f'{image_name}_{corruption_mode}_{int(corruption_ratio * 100)}'
            case_dir = os.path.join(OUTPUT_DIR, case_label)
            os.makedirs(case_dir, exist_ok=True)

            start = time.time()
            recovered, history = rslt_inpainting(
                observed,
                mask,
                patch_size=8,
                stride=6,
                search_window=16,
                num_similar=10,
                candidate_step=4,
                rpca_max_iter=30,
                outer_iter=2,
                true_image=image,
            )
            elapsed = time.time() - start
            metrics = compute_metrics(image, recovered)

            plot_comparison(
                image,
                observed,
                recovered,
                title=f'{image_name} / {corruption_mode}@{corruption_ratio:.0%}',
                metrics=metrics,
                save_path=os.path.join(case_dir, 'compare.png'),
            )

            history_payload = {
                'image_name': image_name,
                'image_source': source,
                'corruption_mode': corruption_mode,
                'corruption_ratio': corruption_ratio,
                'runtime_s': elapsed,
                'metrics': metrics,
                'history': history,
            }
            with open(os.path.join(case_dir, 'summary.json'), 'w', encoding='utf-8') as file:
                json.dump(history_payload, file, indent=2)

            records.append({
                'image_name': image_name,
                'image_source': source,
                'corruption_mode': corruption_mode,
                'corruption_ratio': corruption_ratio,
                'runtime_s': elapsed,
                'PSNR': metrics['PSNR'],
                'SSIM': metrics['SSIM'],
                'RSE': metrics['RSE'],
                'output_ok': 1,
            })

    payload = {
        'run_id': '2026-04-12_run_041',
        'mode': 'coe_guided',
        'eval_runtime_s': time.time() - eval_start,
        'records': records,
    }
    with open(os.path.join(OUTPUT_DIR, 'eval_summary.json'), 'w', encoding='utf-8') as file:
        json.dump(payload, file, indent=2)

    print(json.dumps(payload, indent=2))


if __name__ == '__main__':
    main()

