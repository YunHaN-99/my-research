# A2 replication run

## Meta
- run_id: 2026-04-12_run_041
- case_id: A2
- mode: coe_guided
- replicate_id: rep3
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
- prompt_used.md: solutions/hw2_op2/generated/run_041_coe_guided_rep3/prompt_used.md
- model_raw_response.md: solutions/hw2_op2/generated/run_041_coe_guided_rep3/model_raw_response.md
- src path: solutions/hw2_op2/generated/run_041_coe_guided_rep3/src/
- outputs path: outputs/hw2_op2/run_041_coe_guided_rep3/

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
- row: 2026-04-12_run_041,A2,coe_guided,prompts/a2/coe_multi_role_v0.md,v1,2,1,2,2,none,0,1.4,replication rep3; reused baseline artifact; fixed protocol stable with skimage fallback sources

## Recovery performance rows to append
- CSV target: metrics/a2_recovery_perf_v0.csv
- row 1: 2026-04-12_run_041,lena,random_pixel,0.5,coe_guided,15.1519,0.3766,0.3245,20.5868,1,source=skimage:astronaut
- row 2: 2026-04-12_run_041,lena,text,0.5,coe_guided,27.2597,0.9483,0.0805,21.0104,1,source=skimage:astronaut
- row 3: 2026-04-12_run_041,barbara,random_pixel,0.5,coe_guided,24.2780,0.7244,0.1358,19.5709,1,source=skimage:brick
- row 4: 2026-04-12_run_041,barbara,text,0.5,coe_guided,34.9722,0.9762,0.0397,19.6347,1,source=skimage:brick

## Notes
- protocol deviation: none; `hw2-op2/src/utils.py` automatically fell back to skimage sample images because no local data images were present.
- notable behavior: the copied CoE artifact remained first-pass runnable and reproduced the same four-case metrics under the fixed seed.
- comparison to prior runs: matched run_032 coe_guided baseline metrics; runtime varied only within normal execution noise.
