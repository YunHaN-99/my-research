# A1 bug-repair run

## Meta
- run_id: 2026-04-12_run_027
- case_id: A1
- track: bug_repair
- bug_id: bug_03_height_transpose
- mode: plain_guidance
- prompt_file: prompts/a1/bug_repair_plain_guidance_v0.md
- task_card_version: A1_v1 + bug_repair_v0
- protocol_file: report/a1_bug_repair_protocol_v0.md
- env: codex_session + conda llmft for regression check

## Fixed materials checklist
- [x] symptom.md used
- [x] buggy_code.py used
- [x] diagnosis.md withheld from model
- [x] fixed_code.py withheld from model
- [x] patched code produced
- [x] scoring completed

## Input material paths
- symptom: solutions/hw1_op1/failure_cases/bug_03_height_transpose/symptom.md
- buggy_code: solutions/hw1_op1/failure_cases/bug_03_height_transpose/buggy_code.py
- diagnosis_reference: solutions/hw1_op1/failure_cases/bug_03_height_transpose/diagnosis.md
- fixed_code_reference: solutions/hw1_op1/failure_cases/bug_03_height_transpose/fixed_code.py

## First-pass assessment
- diagnosis_correct: 1
- patch_runnable: 1
- regression_pass: 1
- first_error_summary: none

## Fix log
- fix_rounds: 0
- fix_step_1: none
- fix_step_2: none
- final_working_time_min: 0.9

## Output artifacts
- patched_code_path: solutions/hw1_op1/generated/run_027_bug_03_plain_guidance/src/patched_code.py
- model_raw_response_path: solutions/hw1_op1/generated/run_027_bug_03_plain_guidance/model_raw_response.md

## CSV row to append
- CSV target: metrics/a1_failure_repair_eval_v0.csv
- row: 2026-04-12_run_027,bug_03_height_transpose,plain_guidance,1,1,1,0,0.9,first-pass correct; rough same-session wall-clock

## Notes
- protocol deviation: none
- notable behavior: plain guidance made the transpose invariant explicit for both color and grayscale paths.
- scoring rationale: diagnosis matched the transpose reference and patched behavior matched fixed_code.py in llmft regression check.
