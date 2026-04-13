# run 019 - a1 bug-repair bootstrap

date: 2026-04-12
stage: bootstrap only

## objective
在不伪造实验结果的前提下，把 A1 bug-repair benchmark 补到可直接执行的状态。

## completed
1. created task_cards/A1_bug_repair_taskcard_v0.md
2. created report/a1_bug_repair_protocol_v0.md
3. created prompts/a1/bug_repair_direct_answer_v0.md
4. created prompts/a1/bug_repair_plain_guidance_v0.md
5. created prompts/a1/bug_repair_coe_v0.md
6. created runs/2026-04-12_a1_bug_repair_queue_v0.md
7. created runs/a1_bug_repair_run_template_v0.md
8. created this run record

## boundary
- no bug-repair experimental run executed
- no row appended to metrics/a1_failure_repair_eval_v0.csv
- no final benchmark conclusion this week

## next
- execute 9 planned bug-repair runs under report/a1_bug_repair_protocol_v0.md
- after first 3 runs, check whether scoring fields need clarification
- after all 9 runs, write a1 bug-repair summary v0
