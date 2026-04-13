# A1 bug-repair run

## Meta
- run_id: 2026-04-12_run_020
- case_id: A1
- track: bug_repair
- bug_id: bug_01_dp_boundary
- mode: direct_answer
- prompt_file: prompts/a1/bug_repair_direct_answer_v0.md
- task_card_version: none
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
- symptom: solutions/hw1_op1/failure_cases/bug_01_dp_boundary/symptom.md
- buggy_code: solutions/hw1_op1/failure_cases/bug_01_dp_boundary/buggy_code.py
- diagnosis_reference: solutions/hw1_op1/failure_cases/bug_01_dp_boundary/diagnosis.md
- fixed_code_reference: solutions/hw1_op1/failure_cases/bug_01_dp_boundary/fixed_code.py

## First-pass assessment
- diagnosis_correct: 1
- patch_runnable: 1
- regression_pass: 1
- first_error_summary: none

## Fix log
- fix_rounds: 0
- fix_step_1: none
- fix_step_2: none
- final_working_time_min: 0.6

## Output artifacts
- patched_code_path: solutions/hw1_op1/generated/run_020_bug_01_direct_answer/src/patched_code.py
- model_raw_response_path: solutions/hw1_op1/generated/run_020_bug_01_direct_answer/model_raw_response.md

## CSV row to append
- CSV target: metrics/a1_failure_repair_eval_v0.csv
- row: 2026-04-12_run_020,bug_01_dp_boundary,direct_answer,1,1,1,0,0.6,first-pass correct; rough same-session wall-clock

## Notes
- protocol deviation: none
- notable behavior: direct answer found the boundary-clamp root cause on the first pass.
- scoring rationale: diagnosis matched the reference root cause and patched behavior matched fixed_code.py in llmft regression check.
