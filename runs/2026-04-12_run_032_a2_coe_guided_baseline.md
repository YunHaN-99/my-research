# A2 guidance run

## Meta
- run_id: 2026-04-12_run_032
- case_id: A2
- mode: coe_guided
- prompt_file: prompts/a2/coe_multi_role_v0.md
- task_card_version: v1
- protocol_file: report/a2_eval_protocol_v0.md
- env: conda `llmft` + run-local cv2 compatibility shim

## Fixed protocol checklist
- [x] test images = lena, barbara
- [x] corruption = random_pixel@50%, text@50%
- [x] grayscale only
- [x] image size = 256x256
- [x] fixed 4 case outputs generated

## Prompt and raw output
- prompt_used.md: solutions/hw2_op2/generated/run_032_coe_guided/prompt_used.md
- model_raw_response.md: solutions/hw2_op2/generated/run_032_coe_guided/model_raw_response.md
- src path: solutions/hw2_op2/generated/run_032_coe_guided/src/
- outputs path: outputs/hw2_op2/run_032_coe_guided/

## First-pass assessment
- artifact_complete: 2
- runnable: 1
- correct: 2
- self_check: 2
- first_error_type: none
- first_error_summary: none

## Fix log
- fix_rounds: 0
- fix_step_1: none
- fix_step_2: none
- final_working_time_min: 1.4

## Guidance metrics row to append
- CSV target: metrics/a2_guidance_eval_v0.csv
- row: 2026-04-12_run_032,A2,coe_guided,prompts/a2/coe_multi_role_v0.md,v1,2,1,2,2,none,0,1.4,first-pass runnable; fixed protocol completed with skimage fallback sources

## Recovery performance rows to append
- CSV target: metrics/a2_recovery_perf_v0.csv
- row 1: 2026-04-12_run_032,lena,random_pixel,0.5,coe_guided,15.1519,0.3766,0.3245,15.9925,1,source=skimage:astronaut
- row 2: 2026-04-12_run_032,lena,text,0.5,coe_guided,27.2597,0.9483,0.0805,15.3738,1,source=skimage:astronaut
- row 3: 2026-04-12_run_032,barbara,random_pixel,0.5,coe_guided,24.2780,0.7244,0.1358,16.0406,1,source=skimage:brick
- row 4: 2026-04-12_run_032,barbara,text,0.5,coe_guided,34.9722,0.9762,0.0397,16.1476,1,source=skimage:brick

## Notes
- protocol deviation: none; `hw2-op2/src/utils.py` automatically fell back to skimage sample images because no local data images were present.
- notable behavior: coe output preserved the clearest planner / reviewer / experimenter trail and added explicit state validation inside the generated implementation.
- comparison to prior runs: recovery metrics matched direct_answer and plain_guidance on the fixed 4 cases; review trace was strongest.
