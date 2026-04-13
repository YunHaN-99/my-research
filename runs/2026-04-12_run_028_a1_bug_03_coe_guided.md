# A1 bug-repair run

## Meta
- run_id: 2026-04-12_run_028
- case_id: A1
- track: bug_repair
- bug_id: bug_03_height_transpose
- mode: coe_guided
- prompt_file: prompts/a1/bug_repair_coe_v0.md
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
- final_working_time_min: 1.1

## Output artifacts
- patched_code_path: solutions/hw1_op1/generated/run_028_bug_03_coe_guided/src/patched_code.py
- model_raw_response_path: solutions/hw1_op1/generated/run_028_bug_03_coe_guided/model_raw_response.md

## CSV row to append
- CSV target: metrics/a1_failure_repair_eval_v0.csv
- row: 2026-04-12_run_028,bug_03_height_transpose,coe_guided,1,1,1,0,1.1,first-pass correct; rough same-session wall-clock

## Notes
- protocol deviation: none
- notable behavior: the coe output provided the strongest review trail for axis-order correctness.
- scoring rationale: diagnosis matched the transpose reference and patched behavior matched fixed_code.py in llmft regression check.
