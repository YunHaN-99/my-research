# A2 bug-repair run

## Meta
- run_id: 2026-04-12_run_046
- case_id: A2
- track: bug_repair
- bug_id: bug_02_mask_polarity_inverted
- mode: direct_answer
- prompt_file: prompts/a2/bug_repair_direct_answer_v0.md
- task_card_version: none
- protocol_file: report/a2_bug_repair_protocol_v0.md
- env: codex_session + conda llmft for regression check

## Fixed materials checklist
- [x] symptom.md used
- [x] buggy_code.py used
- [x] diagnosis.md withheld from model
- [x] fixed_code.py withheld from model
- [x] patched code produced
- [x] scoring completed

## Input material paths
- symptom: solutions/hw2_op2/failure_cases/bug_02_mask_polarity_inverted/symptom.md
- buggy_code: solutions/hw2_op2/failure_cases/bug_02_mask_polarity_inverted/buggy_code.py
- diagnosis_reference: solutions/hw2_op2/failure_cases/bug_02_mask_polarity_inverted/diagnosis.md
- fixed_code_reference: solutions/hw2_op2/failure_cases/bug_02_mask_polarity_inverted/fixed_code.py

## First-pass assessment
- diagnosis_correct: 1
- patch_runnable: 1
- regression_pass: 1
- first_error_summary: none

## Fix log
- fix_rounds: 0
- fix_step_1: none
- fix_step_2: none
- final_working_time_min: 0.1

## Output artifacts
- patched_code_path: solutions/hw2_op2/generated/run_046_bug_02_direct_answer/src/patched_code.py
- model_raw_response_path: solutions/hw2_op2/generated/run_046_bug_02_direct_answer/model_raw_response.md

## CSV row to append
- CSV target: metrics/a2_failure_repair_eval_v0.csv
- row: 2026-04-12_run_046,bug_02_mask_polarity_inverted,direct_answer,1,1,1,0,0.1,first-pass correct; script-assisted benchmark wall-clock

## Notes
- protocol deviation: none
- notable behavior: direct answer corrected the mask polarity without touching unrelated RPCA logic.
- scoring rationale: diagnosis matched the mask-polarity reference and patched behavior matched fixed_code.py in llmft regression check.
