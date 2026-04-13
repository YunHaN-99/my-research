import importlib.util
import json
import os
import sys
import time
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
GOLD_SRC = ROOT / 'hw2-op2' / 'src'
GENERATED_ROOT = ROOT / 'solutions' / 'hw2_op2' / 'generated'
OUTPUT_ROOT = ROOT / 'outputs' / 'hw2_op2'
RUNS_DIR = ROOT / 'runs'
EVAL_CSV = ROOT / 'metrics' / 'a2_expanded_scope_eval_v0.csv'
PERF_CSV = ROOT / 'metrics' / 'a2_expanded_scope_perf_v0.csv'

IMAGE_NAMES = ['lena', 'barbara', 'peppers', 'cameraman']
CASE_SPECS = [
    {'corruption_mode': 'random_pixel', 'corruption_ratio': 0.3, 'seed': 101},
    {'corruption_mode': 'random_pixel', 'corruption_ratio': 0.7, 'seed': 103},
    {'corruption_mode': 'center_block', 'corruption_ratio': 0.35, 'seed': 107},
    {'corruption_mode': 'text', 'corruption_ratio': 0.3, 'seed': 109},
]
PARAMS = {
    'patch_size': 8,
    'stride': 6,
    'search_window': 16,
    'num_similar': 10,
    'candidate_step': 4,
    'rpca_max_iter': 30,
    'outer_iter': 2,
}

RUNS = [
    {
        'run_id': '2026-04-12_run_052',
        'mode': 'direct_answer',
        'source_artifact_run_id': '2026-04-12_run_030',
        'source_dir_name': 'run_030_direct_answer',
        'output_dir_name': 'run_052_direct_answer_expanded_scope',
        'run_doc_name': '2026-04-12_run_052_a2_direct_answer_expanded_scope.md',
    },
    {
        'run_id': '2026-04-12_run_053',
        'mode': 'plain_guidance',
        'source_artifact_run_id': '2026-04-12_run_031',
        'source_dir_name': 'run_031_plain_guidance',
        'output_dir_name': 'run_053_plain_guidance_expanded_scope',
        'run_doc_name': '2026-04-12_run_053_a2_plain_guidance_expanded_scope.md',
    },
    {
        'run_id': '2026-04-12_run_054',
        'mode': 'coe_guided',
        'source_artifact_run_id': '2026-04-12_run_032',
        'source_dir_name': 'run_032_coe_guided',
        'output_dir_name': 'run_054_coe_guided_expanded_scope',
        'run_doc_name': '2026-04-12_run_054_a2_coe_guided_expanded_scope.md',
    },
]


def load_generated_module(source_dir_name, module_name):
    run_src = GENERATED_ROOT / source_dir_name / 'src'
    run_src_str = str(run_src)
    gold_src_str = str(GOLD_SRC)
    if run_src_str not in sys.path:
        sys.path.insert(0, run_src_str)
    if gold_src_str not in sys.path:
        sys.path.insert(1, gold_src_str)

    module_path = run_src / 'a2_generated.py'
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, run_src


def to_builtin_metrics(metrics):
    return {key: float(value) for key, value in metrics.items()}


def to_builtin_history(history):
    payload = {}
    for key, values in history.items():
        payload[key] = [float(v) for v in values]
    return payload


def build_run_doc(run_cfg, eval_payload):
    perf_rows = []
    for idx, record in enumerate(eval_payload['records'], start=1):
        perf_rows.append(
            f"- row {idx}: {record['run_id']},{record['image_name']},{record['corruption_mode']},{record['corruption_ratio']},"
            f"{record['mode']},{record['PSNR']:.4f},{record['SSIM']:.4f},{record['RSE']:.4f},{record['runtime_s']:.4f},"
            f"{record['output_ok']},{record['notes']}"
        )
    perf_rows_text = '\n'.join(perf_rows)

    return (
        '# A2 expanded-scope run\n\n'
        '## Meta\n'
        f"- run_id: {run_cfg['run_id']}\n"
        '- case_id: A2\n'
        '- track: expanded_scope\n'
        f"- mode: {run_cfg['mode']}\n"
        f"- source_artifact_run_id: {run_cfg['source_artifact_run_id']}\n"
        f"- source_generated_path: solutions/hw2_op2/generated/{run_cfg['source_dir_name']}/src/a2_generated.py\n"
        '- protocol_file: report/a2_expanded_scope_protocol_v0.md\n'
        '- env: conda `llmft` + reused run-local cv2 compatibility shim\n\n'
        '## Expanded scope checklist\n'
        '- [x] images = lena, barbara, peppers, cameraman\n'
        '- [x] corruption = random_pixel@30%, random_pixel@70%, center_block@35%, text@30%\n'
        '- [x] grayscale only\n'
        '- [x] image size = 256x256\n'
        '- [x] fixed 16 case outputs generated\n\n'
        '## Output artifacts\n'
        f"- outputs path: outputs/hw2_op2/{run_cfg['output_dir_name']}/\n"
        f"- eval_summary_path: outputs/hw2_op2/{run_cfg['output_dir_name']}/eval_summary.json\n\n"
        '## Run-level assessment\n'
        '- artifact_complete: 2\n'
        '- runnable: 1\n'
        f"- image_count: {eval_payload['image_count']}\n"
        f"- case_count: {eval_payload['case_count']}\n"
        f"- output_ok_count: {eval_payload['output_ok_count']}\n\n"
        '## Eval metrics row to append\n'
        '- CSV target: metrics/a2_expanded_scope_eval_v0.csv\n'
        f"- row: {run_cfg['run_id']},{run_cfg['mode']},{run_cfg['source_artifact_run_id']},a2_expanded_scope_v0,"
        f"{eval_payload['image_count']},{eval_payload['case_count']},2,1,{eval_payload['output_ok_count']},"
        'reused baseline artifact; expanded image/corruption cases completed\n\n'
        '## Performance rows to append\n'
        '- CSV target: metrics/a2_expanded_scope_perf_v0.csv\n'
        f'{perf_rows_text}\n\n'
        '## Notes\n'
        '- protocol deviation: none\n'
        '- notable behavior: expanded-scope validation reused the baseline generated artifact and only expanded the evaluation set.\n'
        '- interpretation boundary: this run does not estimate fresh-generation variance because it reuses an existing generated code artifact.\n'
    )


def main():
    eval_rows = []
    perf_rows = []

    for idx, run_cfg in enumerate(RUNS):
        module, run_src = load_generated_module(run_cfg['source_dir_name'], f"a2_expanded_{idx}")
        from utils import apply_mask, compute_metrics, generate_mask, get_test_images, plot_comparison

        output_dir = OUTPUT_ROOT / run_cfg['output_dir_name']
        output_dir.mkdir(parents=True, exist_ok=True)

        images, sources = get_test_images(IMAGE_NAMES, size=(256, 256), gray=True, return_sources=True)
        records = []
        eval_start = time.time()

        for image_name in IMAGE_NAMES:
            image = images[image_name]
            source = sources[image_name]

            for case_spec in CASE_SPECS:
                corruption_mode = case_spec['corruption_mode']
                corruption_ratio = case_spec['corruption_ratio']
                seed = case_spec['seed']

                mask = generate_mask(image.shape, mode=corruption_mode, ratio=corruption_ratio, seed=seed)
                observed = apply_mask(image, mask)

                case_label = f"{image_name}_{corruption_mode}_{int(corruption_ratio * 100)}"
                case_dir = output_dir / case_label
                case_dir.mkdir(parents=True, exist_ok=True)

                start = time.time()
                recovered, history = module.rslt_inpainting(
                    observed,
                    mask,
                    true_image=image,
                    **PARAMS,
                )
                runtime_s = time.time() - start
                metrics = to_builtin_metrics(compute_metrics(image, recovered))
                output_ok = int(
                    recovered.shape == image.shape
                    and np.all(np.isfinite(recovered))
                    and float(np.min(recovered)) >= -1e-6
                    and float(np.max(recovered)) <= 1.0 + 1e-6
                )

                plot_comparison(
                    image,
                    observed,
                    recovered,
                    title=f"{image_name} / {corruption_mode}@{corruption_ratio:.0%}",
                    metrics=metrics,
                    save_path=str(case_dir / 'compare.png'),
                )

                case_payload = {
                    'run_id': run_cfg['run_id'],
                    'mode': run_cfg['mode'],
                    'source_artifact_run_id': run_cfg['source_artifact_run_id'],
                    'image_name': image_name,
                    'image_source': source,
                    'corruption_mode': corruption_mode,
                    'corruption_ratio': float(corruption_ratio),
                    'runtime_s': float(runtime_s),
                    'metrics': metrics,
                    'history': to_builtin_history(history),
                    'output_ok': output_ok,
                }
                (case_dir / 'summary.json').write_text(json.dumps(case_payload, indent=2), encoding='utf-8')

                record = {
                    'run_id': run_cfg['run_id'],
                    'image_name': image_name,
                    'corruption_mode': corruption_mode,
                    'corruption_ratio': float(corruption_ratio),
                    'mode': run_cfg['mode'],
                    'runtime_s': float(runtime_s),
                    'PSNR': metrics['PSNR'],
                    'SSIM': metrics['SSIM'],
                    'RSE': metrics['RSE'],
                    'output_ok': output_ok,
                    'notes': f'source={source}',
                }
                records.append(record)
                perf_rows.append(record)

        eval_payload = {
            'run_id': run_cfg['run_id'],
            'mode': run_cfg['mode'],
            'scope_id': 'a2_expanded_scope_v0',
            'source_artifact_run_id': run_cfg['source_artifact_run_id'],
            'source_generated_path': f"solutions/hw2_op2/generated/{run_cfg['source_dir_name']}/src/a2_generated.py",
            'image_count': len(IMAGE_NAMES),
            'case_count': len(records),
            'output_ok_count': int(sum(record['output_ok'] for record in records)),
            'eval_runtime_s': float(time.time() - eval_start),
            'records': records,
        }

        (output_dir / 'eval_summary.json').write_text(json.dumps(eval_payload, indent=2), encoding='utf-8')
        (RUNS_DIR / run_cfg['run_doc_name']).write_text(build_run_doc(run_cfg, eval_payload), encoding='utf-8')

        eval_rows.append(
            {
                'run_id': run_cfg['run_id'],
                'mode': run_cfg['mode'],
                'source_artifact_run_id': run_cfg['source_artifact_run_id'],
                'scope_id': 'a2_expanded_scope_v0',
                'image_count': len(IMAGE_NAMES),
                'case_count': len(records),
                'artifact_complete': 2,
                'runnable': 1,
                'output_ok_count': int(sum(record['output_ok'] for record in records)),
                'notes': 'reused baseline artifact; expanded image/corruption cases completed',
            }
        )

        print(json.dumps({'run_id': run_cfg['run_id'], 'case_count': len(records), 'output_ok_count': eval_payload['output_ok_count']}, indent=2))

    eval_csv_lines = ['run_id,mode,source_artifact_run_id,scope_id,image_count,case_count,artifact_complete,runnable,output_ok_count,notes']
    for row in eval_rows:
        eval_csv_lines.append(
            f"{row['run_id']},{row['mode']},{row['source_artifact_run_id']},{row['scope_id']},{row['image_count']},"
            f"{row['case_count']},{row['artifact_complete']},{row['runnable']},{row['output_ok_count']},{row['notes']}"
        )
    EVAL_CSV.write_text('\n'.join(eval_csv_lines) + '\n', encoding='utf-8')

    perf_csv_lines = ['run_id,image_name,corruption_mode,corruption_ratio,mode,psnr,ssim,rse,runtime_s,output_ok,notes']
    for row in perf_rows:
        perf_csv_lines.append(
            f"{row['run_id']},{row['image_name']},{row['corruption_mode']},{row['corruption_ratio']},{row['mode']},"
            f"{row['PSNR']:.4f},{row['SSIM']:.4f},{row['RSE']:.4f},{row['runtime_s']:.4f},{row['output_ok']},{row['notes']}"
        )
    PERF_CSV.write_text('\n'.join(perf_csv_lines) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
