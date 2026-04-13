# run 029 - a2 chapter5 scope setup

date: 2026-04-12
stage: scope + pipeline setup

## objective
把 A2 从 bootstrap-only 状态推进到可直接开始 baseline 实验的状态，并明确 `chapter5` 为主案例。

## completed
1. updated `problems/a2_requirement.md`
2. created `task_cards/A2_rslt_inpainting_taskcard_v1.md`
3. created `report/a2_eval_protocol_v0.md`
4. created `prompts/a2/baseline_direct_answer_v0.md`
5. created `prompts/a2/baseline_plain_guidance_v0.md`
6. created `prompts/a2/coe_multi_role_v0.md`
7. created `metrics/a2_guidance_eval_v0.csv`
8. created `metrics/a2_guidance_eval_codebook_v0.md`
9. created `metrics/a2_recovery_perf_v0.csv`
10. created `metrics/a2_recovery_perf_codebook_v0.md`
11. created `runs/a2_guidance_run_template_v0.md`
12. created `runs/2026-04-12_a2_baseline_queue_v0.md`
13. created this run record

## scope decision
- A2 gold reference = `hw2-op2/src/chapter5_rslt.py::rslt_inpainting`
- A2 不把 `hw2-op2` 的八章作为单任务
- `chapter2/3/4/8` 作为 baseline、协议参考或后续扩展

## boundary
- no A2 baseline run executed in this step
- no row appended to A2 metrics in this step
- no A2 generated code in this step

## next
- execute A2 baseline run 1: direct_answer
- then plain_guidance / coe_guided under the same fixed protocol
