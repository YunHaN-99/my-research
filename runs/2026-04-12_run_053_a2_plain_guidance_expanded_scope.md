# A2 expanded-scope run

## Meta
- run_id: 2026-04-12_run_053
- case_id: A2
- track: expanded_scope
- mode: plain_guidance
- source_artifact_run_id: 2026-04-12_run_031
- source_generated_path: solutions/hw2_op2/generated/run_031_plain_guidance/src/a2_generated.py
- protocol_file: report/a2_expanded_scope_protocol_v0.md
- env: conda `llmft` + reused run-local cv2 compatibility shim

## Expanded scope checklist
- [x] images = lena, barbara, peppers, cameraman
- [x] corruption = random_pixel@30%, random_pixel@70%, center_block@35%, text@30%
- [x] grayscale only
- [x] image size = 256x256
- [x] fixed 16 case outputs generated

## Output artifacts
- outputs path: outputs/hw2_op2/run_053_plain_guidance_expanded_scope/
- eval_summary_path: outputs/hw2_op2/run_053_plain_guidance_expanded_scope/eval_summary.json

## Run-level assessment
- artifact_complete: 2
- runnable: 1
- image_count: 4
- case_count: 16
- output_ok_count: 16

## Eval metrics row to append
- CSV target: metrics/a2_expanded_scope_eval_v0.csv
- row: 2026-04-12_run_053,plain_guidance,2026-04-12_run_031,a2_expanded_scope_v0,4,16,2,1,16,reused baseline artifact; expanded image/corruption cases completed

## Performance rows to append
- CSV target: metrics/a2_expanded_scope_perf_v0.csv
- row 1: 2026-04-12_run_053,lena,random_pixel,0.3,plain_guidance,20.5233,0.5625,0.1748,15.0220,1,source=skimage:astronaut
- row 2: 2026-04-12_run_053,lena,random_pixel,0.7,plain_guidance,13.0882,0.2694,0.4115,15.4812,1,source=skimage:astronaut
- row 3: 2026-04-12_run_053,lena,center_block,0.35,plain_guidance,14.3309,0.6970,0.3566,13.9102,1,source=skimage:astronaut
- row 4: 2026-04-12_run_053,lena,text,0.3,plain_guidance,28.8651,0.9619,0.0669,15.0531,1,source=skimage:astronaut
- row 5: 2026-04-12_run_053,barbara,random_pixel,0.3,plain_guidance,29.4335,0.8981,0.0750,15.3997,1,source=skimage:brick
- row 6: 2026-04-12_run_053,barbara,random_pixel,0.7,plain_guidance,21.7189,0.5795,0.1824,15.1958,1,source=skimage:brick
- row 7: 2026-04-12_run_053,barbara,center_block,0.35,plain_guidance,19.2680,0.7603,0.2418,14.0630,1,source=skimage:brick
- row 8: 2026-04-12_run_053,barbara,text,0.3,plain_guidance,36.5561,0.9848,0.0330,16.0049,1,source=skimage:brick
- row 9: 2026-04-12_run_053,peppers,random_pixel,0.3,plain_guidance,23.1094,0.6368,0.1507,14.8787,1,source=skimage:coffee
- row 10: 2026-04-12_run_053,peppers,random_pixel,0.7,plain_guidance,15.2643,0.3261,0.3719,15.5929,1,source=skimage:coffee
- row 11: 2026-04-12_run_053,peppers,center_block,0.35,plain_guidance,16.8543,0.7341,0.3097,13.8756,1,source=skimage:coffee
- row 12: 2026-04-12_run_053,peppers,text,0.3,plain_guidance,30.3754,0.9699,0.0653,15.7324,1,source=skimage:coffee
- row 13: 2026-04-12_run_053,cameraman,random_pixel,0.3,plain_guidance,21.3495,0.4603,0.1468,14.1186,1,source=skimage:camera
- row 14: 2026-04-12_run_053,cameraman,random_pixel,0.7,plain_guidance,13.4740,0.2204,0.3635,14.9099,1,source=skimage:camera
- row 15: 2026-04-12_run_053,cameraman,center_block,0.35,plain_guidance,13.4256,0.7004,0.3656,13.2811,1,source=skimage:camera
- row 16: 2026-04-12_run_053,cameraman,text,0.3,plain_guidance,29.1733,0.9580,0.0596,16.1262,1,source=skimage:camera

## Notes
- protocol deviation: none
- notable behavior: expanded-scope validation reused the baseline generated artifact and only expanded the evaluation set.
- interpretation boundary: this run does not estimate fresh-generation variance because it reuses an existing generated code artifact.
