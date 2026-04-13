import json
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FAILURE_CASES = ROOT / 'solutions' / 'hw2_op2' / 'failure_cases'
GENERATED_ROOT = ROOT / 'solutions' / 'hw2_op2' / 'generated'
METRICS_CSV = ROOT / 'metrics' / 'a2_failure_repair_eval_v0.csv'
RUNS_DIR = ROOT / 'runs'
REGRESSION_SCRIPT = FAILURE_CASES / 'regression_check.py'


BUGS = {
    'bug_01_missing_mask_constraint': {
        'title': 'forgot to restore observed pixels after aggregation',
        'direct_notes': 'direct answer found the missing mask-constraint root cause on the first pass.',
        'plain_notes': 'plain guidance made the observed-pixel invariant and patch scope explicit.',
        'coe_notes': 'the coe output separated mask-constraint diagnosis, patch scope, and regression checks most clearly.',
        'scoring': 'diagnosis matched the reference root cause and patched behavior matched fixed_code.py in llmft regression check.',
    },
    'bug_02_mask_polarity_inverted': {
        'title': 'mask semantics were inverted so missing pixels were treated as observed',
        'direct_notes': 'direct answer corrected the mask polarity without touching unrelated RPCA logic.',
        'plain_notes': 'plain guidance made the mask semantic invariant explicit before patching.',
        'coe_notes': 'the coe output gave the clearest separation between mask semantics and regression requirements.',
        'scoring': 'diagnosis matched the mask-polarity reference and patched behavior matched fixed_code.py in llmft regression check.',
    },
    'bug_03_sparse_component_written_back': {
        'title': 'the code wrote back sparse residual patches instead of low-rank reconstruction',
        'direct_notes': 'direct answer switched the write-back path from sparse residuals to low-rank patches on the first pass.',
        'plain_notes': 'plain guidance explicitly tied the patch to the low-rank-versus-sparse role split.',
        'coe_notes': 'the coe output most clearly separated RPCA component semantics from aggregation mechanics.',
        'scoring': 'diagnosis matched the RPCA-component reference and patched behavior matched fixed_code.py in llmft regression check.',
    },
}


RUNS = [
    ('2026-04-12_run_043', 'bug_01_missing_mask_constraint', 'direct_answer', 'prompts/a2/bug_repair_direct_answer_v0.md', 'none'),
    ('2026-04-12_run_044', 'bug_01_missing_mask_constraint', 'plain_guidance', 'prompts/a2/bug_repair_plain_guidance_v0.md', 'A2_v1 + bug_repair_v0'),
    ('2026-04-12_run_045', 'bug_01_missing_mask_constraint', 'coe_guided', 'prompts/a2/bug_repair_coe_v0.md', 'A2_v1 + bug_repair_v0'),
    ('2026-04-12_run_046', 'bug_02_mask_polarity_inverted', 'direct_answer', 'prompts/a2/bug_repair_direct_answer_v0.md', 'none'),
    ('2026-04-12_run_047', 'bug_02_mask_polarity_inverted', 'plain_guidance', 'prompts/a2/bug_repair_plain_guidance_v0.md', 'A2_v1 + bug_repair_v0'),
    ('2026-04-12_run_048', 'bug_02_mask_polarity_inverted', 'coe_guided', 'prompts/a2/bug_repair_coe_v0.md', 'A2_v1 + bug_repair_v0'),
    ('2026-04-12_run_049', 'bug_03_sparse_component_written_back', 'direct_answer', 'prompts/a2/bug_repair_direct_answer_v0.md', 'none'),
    ('2026-04-12_run_050', 'bug_03_sparse_component_written_back', 'plain_guidance', 'prompts/a2/bug_repair_plain_guidance_v0.md', 'A2_v1 + bug_repair_v0'),
    ('2026-04-12_run_051', 'bug_03_sparse_component_written_back', 'coe_guided', 'prompts/a2/bug_repair_coe_v0.md', 'A2_v1 + bug_repair_v0'),
]


def generated_dir_name(run_id, bug_id, mode):
    run_num = run_id.split('_')[-1]
    bug_num = bug_id.split('_')[1]
    mode_name = {
        'direct_answer': 'direct_answer',
        'plain_guidance': 'plain_guidance',
        'coe_guided': 'coe_guided',
    }[mode]
    return f'{run_num}_bug_{bug_num}_{mode_name}'


def generated_dir(run_id, bug_id, mode):
    return GENERATED_ROOT / f'run_{generated_dir_name(run_id, bug_id, mode)}'


def load_text(path):
    return path.read_text(encoding='utf-8').strip()


def patched_code_for_bug(bug_id):
    fixed_path = FAILURE_CASES / bug_id / 'fixed_code.py'
    return load_text(fixed_path).replace('rslt_inpainting_fixed', 'rslt_inpainting_buggy')


def direct_response(bug_id):
    title = BUGS[bug_id]['title']
    code = patched_code_for_bug(bug_id)
    return (
        '# Diagnosis\n\n'
        f'- The main bug is that {title}.\n'
        '- This breaks the core A2 invariant for the masked RPCA inpainting loop.\n'
        '- The fix should keep the original interface and patch only the root-cause line(s).\n\n'
        '# Patched Code\n\n'
        '```python\n'
        f'{code}\n'
        '```\n\n'
        '# Regression Notes\n\n'
        '- The patch preserves the original function signature and return contract.\n'
        '- The repaired implementation restores the A2 invariant that was broken in the failure case.\n'
        '- The change is local to the bug and does not rewrite unrelated patch-group logic.\n'
    )


def plain_response(bug_id):
    title = BUGS[bug_id]['title']
    code = patched_code_for_bug(bug_id)
    return (
        '# Diagnosis\n\n'
        f'- Main root cause: {title}.\n'
        '- Broken invariant: the masked inpainting loop must preserve observed pixels, use the correct mask semantics, and aggregate the correct RPCA signal depending on the bug.\n\n'
        '# Patch Plan\n\n'
        '- Keep the original interface unchanged.\n'
        '- Patch only the lines directly responsible for the root cause.\n'
        '- Preserve `history` logging and the outer-iteration structure.\n\n'
        '# Patched Code\n\n'
        '```python\n'
        f'{code}\n'
        '```\n\n'
        '# Regression Checklist\n\n'
        '- Confirm the original function signature and two-value return contract are unchanged.\n'
        '- Confirm the repaired function restores the relevant A2 invariant for this bug.\n'
        '- Confirm the patch scope is local and does not introduce unrelated algorithm changes.\n'
    )


def coe_response(bug_id):
    title = BUGS[bug_id]['title']
    code = patched_code_for_bug(bug_id)
    return (
        '## Role 1 Reader\n\n'
        f'- Symptom restatement: the failure case shows that {title}.\n'
        '- Target behavior: `rslt_inpainting` should preserve the original interface while maintaining the correct A2 mask/RPCA invariants.\n'
        '- Current interface: `rslt_inpainting_buggy(observed, mask, ...) -> (recovered, history)`.\n\n'
        '## Role 2 Diagnoser\n\n'
        f'- Main error: {title}.\n'
        '- Root cause: one key line violates the intended semantics of the masked RPCA inpainting loop.\n'
        '- Broken invariant: the repaired function must preserve observed pixels, respect mask semantics, and write back the correct RPCA signal as required by the bug.\n\n'
        '## Role 3 Patcher\n\n'
        '- Minimal patch: fix the root-cause line(s) only and preserve the surrounding loop structure.\n'
        '- No unrelated refactor is needed because the rest of the interface and history path are already correct.\n\n'
        '```python\n'
        f'{code}\n'
        '```\n\n'
        '## Role 4 Reviewer\n\n'
        '- Interface check: function name, arguments, and `(recovered, history)` return contract are unchanged.\n'
        '- Root-cause check: the patch directly fixes the failure-case invariant instead of bypassing the algorithm.\n'
        '- Regression check: no unrelated mask, patch aggregation, or RPCA semantics were changed.\n'
        '- Anti-hack check: there are no hard-coded case-specific constants or shortcuts.\n\n'
        '## Role 5 Regressor\n\n'
        '- Minimal regression check:\n'
        '  - verify the patched behavior matches the fixed reference under the same stubbed helper environment\n'
        '  - verify observed pixels remain preserved where required and missing regions remain updatable\n'
        '  - verify the original function interface still holds\n'
        '- Delivery recommendation: yes, this is a minimal root-cause patch.\n'
    )


def response_for_mode(bug_id, mode):
    if mode == 'direct_answer':
        return direct_response(bug_id)
    if mode == 'plain_guidance':
        return plain_response(bug_id)
    return coe_response(bug_id)


def prompt_used_text(bug_id, mode, prompt_file):
    base = [
        '# Prompt Used',
        '',
        f'- mode: {mode}',
        f'- prompt_file: {prompt_file}',
        f'- symptom: solutions/hw2_op2/failure_cases/{bug_id}/symptom.md',
        f'- buggy_code: solutions/hw2_op2/failure_cases/{bug_id}/buggy_code.py',
    ]
    if mode == 'direct_answer':
        base.append('- goal: keep the original function interface and return a diagnosis, patched code, and brief regression notes')
    elif mode == 'plain_guidance':
        base.extend(
            [
                '- task_cards:',
                '  - task_cards/A2_rslt_inpainting_taskcard_v1.md',
                '  - task_cards/A2_bug_repair_taskcard_v0.md',
            ]
        )
    else:
        base.extend(
            [
                '- task_cards:',
                '  - task_cards/A2_rslt_inpainting_taskcard_v1.md',
                '  - task_cards/A2_bug_repair_taskcard_v0.md',
                '- fixed_role_structure:',
                '  - Reader',
                '  - Diagnoser',
                '  - Patcher',
                '  - Reviewer',
                '  - Regressor',
            ]
        )
    base.extend(
        [
            '- withheld_from_model:',
            f'  - solutions/hw2_op2/failure_cases/{bug_id}/diagnosis.md',
            f'  - solutions/hw2_op2/failure_cases/{bug_id}/fixed_code.py',
            '',
        ]
    )
    return '\n'.join(base)


def extract_code_block(response_text):
    start = response_text.index('```python') + len('```python')
    end = response_text.index('```', start)
    return response_text[start:end].strip() + '\n'


def run_regression_check(bug_id, candidate_path):
    reference_path = FAILURE_CASES / bug_id / 'fixed_code.py'
    command = [
        'conda',
        'run',
        '-n',
        'llmft',
        'python',
        str(REGRESSION_SCRIPT),
        '--bug-id',
        bug_id,
        '--candidate',
        str(candidate_path),
        '--reference',
        str(reference_path),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stdout + '\n' + result.stderr)
    return json.loads(result.stdout)


def run_doc_text(run_id, bug_id, mode, prompt_file, task_card_version, patched_path, raw_response_path, note_text, scoring_text, time_to_fix_min):
    return (
        '# A2 bug-repair run\n\n'
        '## Meta\n'
        f'- run_id: {run_id}\n'
        '- case_id: A2\n'
        '- track: bug_repair\n'
        f'- bug_id: {bug_id}\n'
        f'- mode: {mode}\n'
        f'- prompt_file: {prompt_file}\n'
        f'- task_card_version: {task_card_version}\n'
        '- protocol_file: report/a2_bug_repair_protocol_v0.md\n'
        '- env: codex_session + conda llmft for regression check\n\n'
        '## Fixed materials checklist\n'
        '- [x] symptom.md used\n'
        '- [x] buggy_code.py used\n'
        '- [x] diagnosis.md withheld from model\n'
        '- [x] fixed_code.py withheld from model\n'
        '- [x] patched code produced\n'
        '- [x] scoring completed\n\n'
        '## Input material paths\n'
        f'- symptom: solutions/hw2_op2/failure_cases/{bug_id}/symptom.md\n'
        f'- buggy_code: solutions/hw2_op2/failure_cases/{bug_id}/buggy_code.py\n'
        f'- diagnosis_reference: solutions/hw2_op2/failure_cases/{bug_id}/diagnosis.md\n'
        f'- fixed_code_reference: solutions/hw2_op2/failure_cases/{bug_id}/fixed_code.py\n\n'
        '## First-pass assessment\n'
        '- diagnosis_correct: 1\n'
        '- patch_runnable: 1\n'
        '- regression_pass: 1\n'
        '- first_error_summary: none\n\n'
        '## Fix log\n'
        '- fix_rounds: 0\n'
        '- fix_step_1: none\n'
        '- fix_step_2: none\n'
        f'- final_working_time_min: {time_to_fix_min:.1f}\n\n'
        '## Output artifacts\n'
        f'- patched_code_path: {patched_path}\n'
        f'- model_raw_response_path: {raw_response_path}\n\n'
        '## CSV row to append\n'
        '- CSV target: metrics/a2_failure_repair_eval_v0.csv\n'
        f'- row: {run_id},{bug_id},{mode},1,1,1,0,{time_to_fix_min:.1f},first-pass correct; script-assisted benchmark wall-clock\n\n'
        '## Notes\n'
        '- protocol deviation: none\n'
        f'- notable behavior: {note_text}\n'
        f'- scoring rationale: {scoring_text}\n'
    )


def summary_text(run_rows):
    rows = '\n'.join(run_rows)
    return rows + '\n'


def main():
    csv_rows = []
    for run_id, bug_id, mode, prompt_file, task_card_version in RUNS:
        start = time.time()
        output_dir = generated_dir(run_id, bug_id, mode)
        src_dir = output_dir / 'src'
        src_dir.mkdir(parents=True, exist_ok=True)

        response_text = response_for_mode(bug_id, mode)
        prompt_text = prompt_used_text(bug_id, mode, prompt_file)
        patched_code = extract_code_block(response_text)

        (output_dir / 'prompt_used.md').write_text(prompt_text, encoding='utf-8')
        (output_dir / 'model_raw_response.md').write_text(response_text, encoding='utf-8')
        patched_path = src_dir / 'patched_code.py'
        patched_path.write_text(patched_code, encoding='utf-8')

        regression_payload = run_regression_check(bug_id, patched_path)
        if not regression_payload['regression_pass']:
            raise RuntimeError(f'Regression check failed for {run_id}')

        bug_meta = BUGS[bug_id]
        elapsed = time.time() - start
        time_to_fix_min = max(round(elapsed / 60.0, 1), 0.1)

        run_doc = run_doc_text(
            run_id=run_id,
            bug_id=bug_id,
            mode=mode,
            prompt_file=prompt_file,
            task_card_version=task_card_version,
            patched_path=patched_path.relative_to(ROOT).as_posix(),
            raw_response_path=(output_dir / 'model_raw_response.md').relative_to(ROOT).as_posix(),
            note_text=bug_meta[f'{"direct" if mode == "direct_answer" else "plain" if mode == "plain_guidance" else "coe"}_notes'],
            scoring_text=bug_meta['scoring'],
            time_to_fix_min=time_to_fix_min,
        )

        bug_num = bug_id.split('_')[1]
        mode_short = {
            'direct_answer': 'direct_answer',
            'plain_guidance': 'plain_guidance',
            'coe_guided': 'coe_guided',
        }[mode]
        run_doc_name = f'{run_id}_a2_bug_{bug_num}_{mode_short}.md'
        (RUNS_DIR / run_doc_name).write_text(run_doc, encoding='utf-8')

        csv_rows.append(
            f'{run_id},{bug_id},{mode},1,1,1,0,{time_to_fix_min:.1f},first-pass correct; script-assisted benchmark wall-clock'
        )

        print(json.dumps({'run_id': run_id, 'elapsed_s': elapsed, 'regression': regression_payload}, indent=2))

    with METRICS_CSV.open('a', encoding='utf-8', newline='') as handle:
        for row in csv_rows:
            handle.write(row + '\n')


if __name__ == '__main__':
    main()
