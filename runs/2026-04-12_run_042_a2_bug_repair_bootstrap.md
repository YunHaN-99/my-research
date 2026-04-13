# run 042 - a2 bug-repair bootstrap

date: 2026-04-12
stage: bootstrap only

## objective
在不伪造实验结果的前提下，把 A2 bug-repair benchmark 补到可直接执行的状态。

## completed
1. created `task_cards/A2_bug_repair_taskcard_v0.md`
2. created `report/a2_bug_repair_protocol_v0.md`
3. created `report/a2_failure_case_design_v0.md`
4. created `prompts/a2/bug_repair_direct_answer_v0.md`
5. created `prompts/a2/bug_repair_plain_guidance_v0.md`
6. created `prompts/a2/bug_repair_coe_v0.md`
7. created `metrics/a2_failure_repair_eval_v0.csv`
8. created `metrics/a2_failure_repair_eval_codebook_v0.md`
9. created `runs/2026-04-12_a2_bug_repair_queue_v0.md`
10. created `runs/a2_bug_repair_run_template_v0.md`
11. created `solutions/hw2_op2/failure_cases/`
12. created this run record

## boundary
- no A2 bug-repair experimental run executed
- no row appended beyond the CSV header in `metrics/a2_failure_repair_eval_v0.csv`
- no final benchmark conclusion this week

## next
- execute 9 planned bug-repair runs under `report/a2_bug_repair_protocol_v0.md`
- after first 3 runs, check whether scoring fields need clarification
- after all 9 runs, write `report/a2_bug_repair_summary_v0.md`
