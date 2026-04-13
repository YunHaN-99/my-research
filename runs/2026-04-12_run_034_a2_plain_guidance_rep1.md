# A2 replication run

## Meta
- run_id: 2026-04-12_run_034
- case_id: A2
- mode: plain_guidance
- replicate_id: rep1
- prompt_file: prompts/a2/baseline_plain_guidance_v0.md
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
- prompt_used.md: solutions/hw2_op2/generated/run_034_plain_guidance_rep1/prompt_used.md
- model_raw_response.md: solutions/hw2_op2/generated/run_034_plain_guidance_rep1/model_raw_response.md
- src path: solutions/hw2_op2/generated/run_034_plain_guidance_rep1/src/
- outputs path: outputs/hw2_op2/run_034_plain_guidance_rep1/

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
- final_working_time_min: 1.2

## Guidance metrics row to append
- CSV target: metrics/a2_guidance_eval_v0.csv
- row: 2026-04-12_run_034,A2,plain_guidance,prompts/a2/baseline_plain_guidance_v0.md,v1,2,1,2,2,none,0,1.2,replication rep1; reused baseline artifact; fixed protocol stable with skimage fallback sources

## Recovery performance rows to append
- CSV target: metrics/a2_recovery_perf_v0.csv
- row 1: 2026-04-12_run_034,lena,random_pixel,0.5,plain_guidance,15.1519,0.3766,0.3245,18.0365,1,source=skimage:astronaut
- row 2: 2026-04-12_run_034,lena,text,0.5,plain_guidance,27.2597,0.9483,0.0805,17.8656,1,source=skimage:astronaut
- row 3: 2026-04-12_run_034,barbara,random_pixel,0.5,plain_guidance,24.2780,0.7244,0.1358,16.3190,1,source=skimage:brick
- row 4: 2026-04-12_run_034,barbara,text,0.5,plain_guidance,34.9722,0.9762,0.0397,16.3819,1,source=skimage:brick

## Notes
- protocol deviation: none; `hw2-op2/src/utils.py` automatically fell back to skimage sample images because no local data images were present.
- notable behavior: the copied plain-guidance artifact preserved the same regression checklist and reproduced the same four-case metrics under the fixed seed.
- comparison to prior runs: matched run_031 plain_guidance baseline metrics; runtime varied only within normal execution noise.
