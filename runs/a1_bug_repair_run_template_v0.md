# A1 bug-repair run template

## Meta
- run_id:
- case_id: A1
- track: bug_repair
- bug_id:
- mode:
- prompt_file:
- task_card_version:
- protocol_file: report/a1_bug_repair_protocol_v0.md
- env:

## Fixed materials checklist
- [ ] symptom.md used
- [ ] buggy_code.py used
- [ ] diagnosis.md withheld from model
- [ ] fixed_code.py withheld from model
- [ ] patched code produced
- [ ] scoring completed

## Input material paths
- symptom:
- buggy_code:
- diagnosis_reference:
- fixed_code_reference:

## First-pass assessment
- diagnosis_correct:
- patch_runnable:
- regression_pass:
- first_error_summary:

## Fix log
- fix_rounds:
- fix_step_1:
- fix_step_2:
- final_working_time_min:

## Output artifacts
- patched_code_path:
- model_raw_response_path:

## CSV row to append
- CSV target: metrics/a1_failure_repair_eval_v0.csv
- row:

## Notes
- protocol deviation:
- notable behavior:
- scoring rationale:
