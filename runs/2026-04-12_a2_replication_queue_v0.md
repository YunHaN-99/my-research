# A2 replication queue v0

## Scope
- planned runs: run_033 to run_041
- protocol: `report/a2_eval_protocol_v0.md`
- fixed images: `lena`, `barbara`
- fixed corruption: `random_pixel@50%`, `text@50%`
- fixed image format: grayscale, `256x256`
- target function: `rslt_inpainting(observed, mask, ...)`
- replication meaning: rerun copied baseline artifacts under the same fixed seed and protocol; this track does not resample fresh model outputs

## Status
- run_033 (direct_answer rep1): completed
- run_034 (plain_guidance rep1): completed
- run_035 (coe_guided rep1): completed
- run_036 (direct_answer rep2): completed
- run_037 (plain_guidance rep2): completed
- run_038 (coe_guided rep2): completed
- run_039 (direct_answer rep3): completed
- run_040 (plain_guidance rep3): completed
- run_041 (coe_guided rep3): completed
- remaining: none

## Backfill
- run docs: completed for all 9 runs
- `metrics/a2_guidance_eval_v0.csv`: completed
- `metrics/a2_recovery_perf_v0.csv`: completed
