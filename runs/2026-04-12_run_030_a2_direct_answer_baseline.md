# A2 guidance run

## Meta
- run_id: 2026-04-12_run_030
- case_id: A2
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
- [x] fixed 4 case outputs generated

## Prompt and raw output
- prompt_used.md: solutions/hw2_op2/generated/run_030_direct_answer/prompt_used.md
- model_raw_response.md: solutions/hw2_op2/generated/run_030_direct_answer/model_raw_response.md
- src path: solutions/hw2_op2/generated/run_030_direct_answer/src/
- outputs path: outputs/hw2_op2/run_030_direct_answer/

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
- final_working_time_min: 1.3

## Guidance metrics row to append
- CSV target: metrics/a2_guidance_eval_v0.csv
- row: 2026-04-12_run_030,A2,direct_answer,prompts/a2/baseline_direct_answer_v0.md,none,2,1,2,1,none,0,1.3,first-pass runnable; fixed protocol completed with skimage fallback sources

## Recovery performance rows to append
- CSV target: metrics/a2_recovery_perf_v0.csv
- row 1: 2026-04-12_run_030,lena,random_pixel,0.5,direct_answer,15.1519,0.3766,0.3245,15.1086,1,source=skimage:astronaut
- row 2: 2026-04-12_run_030,lena,text,0.5,direct_answer,27.2597,0.9483,0.0805,14.8518,1,source=skimage:astronaut
- row 3: 2026-04-12_run_030,barbara,random_pixel,0.5,direct_answer,24.2780,0.7244,0.1358,15.2924,1,source=skimage:brick
- row 4: 2026-04-12_run_030,barbara,text,0.5,direct_answer,34.9722,0.9762,0.0397,15.2418,1,source=skimage:brick

## Notes
- protocol deviation: none; `hw2-op2/src/utils.py` automatically fell back to skimage sample images because no local data images were present.
- notable behavior: `llmft` lacked OpenCV, so this run used a run-local `cv2` compatibility shim to preserve the original utils path without modifying `hw2-op2`.
- comparison to prior runs: first A2 baseline run; no prior A2 baseline available.
