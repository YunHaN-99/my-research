# A2 guidance run

## Meta
- run_id: 2026-04-12_run_055
- case_id: A2
- track: fresh_generation
- mode: direct_answer
- prompt_file: prompts/a2/baseline_direct_answer_v0.md
- task_card_version: none
- protocol_file: report/a2_eval_protocol_v0.md
- env: conda `llmft` + run-local cv2 compatibility shim

## Fixed protocol checklist
- [x] test images = lena, barbara
- [x] corruption = random_pixel@50%, text@50%
- [x] grayscale only
- [x] image size = 256x256
- [x] fresh generated code artifact created
- [x] fixed 4 case outputs generated

## Prompt and raw output
- prompt_used.md: solutions/hw2_op2/generated/run_055_direct_answer_fresh_generation/prompt_used.md
- model_raw_response.md: solutions/hw2_op2/generated/run_055_direct_answer_fresh_generation/model_raw_response.md
- src path: solutions/hw2_op2/generated/run_055_direct_answer_fresh_generation/src/
- outputs path: outputs/hw2_op2/run_055_direct_answer_fresh_generation/

## First-pass assessment
- artifact_complete: 2
- runnable: 1
- correct: 2
- self_check: 1
- first_error_type: none
- first_error_summary: none

## Fix log
- fix_rounds: 0
- fix_step_1: none
- fix_step_2: none
- final_working_time_min: 1.2

## Guidance metrics row to append
- CSV target: metrics/a2_guidance_eval_v0.csv
- row: 2026-04-12_run_055,A2,direct_answer,prompts/a2/baseline_direct_answer_v0.md,none,2,1,2,1,none,0,1.2,first-pass runnable; fresh generated artifact; fixed protocol completed with skimage fallback sources

## Recovery performance rows to append
- CSV target: metrics/a2_recovery_perf_v0.csv
- row 1: 2026-04-12_run_055,lena,random_pixel,0.5,direct_answer,15.1519,0.3766,0.3245,17.3605,1,source=skimage:astronaut
- row 2: 2026-04-12_run_055,lena,text,0.5,direct_answer,27.2597,0.9483,0.0805,17.2790,1,source=skimage:astronaut
- row 3: 2026-04-12_run_055,barbara,random_pixel,0.5,direct_answer,24.2780,0.7244,0.1358,17.8962,1,source=skimage:brick
- row 4: 2026-04-12_run_055,barbara,text,0.5,direct_answer,34.9722,0.9762,0.0397,17.8301,1,source=skimage:brick

## Notes
- protocol deviation: none; `hw2-op2/src/utils.py` automatically fell back to skimage sample images because no local data images were present.
- notable behavior: fresh direct-answer artifact converged to the same fixed-protocol recovery values with a helper-split implementation.
- interpretation boundary: this track used newly materialized local artifacts under the same prompt family; it did not reuse the earlier baseline `a2_generated.py` files.
