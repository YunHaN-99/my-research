# Prompt Used

- mode: direct_answer
- prompt_file: prompts/a2/baseline_direct_answer_v0.md
- task: implement `rslt_inpainting(observed, mask, ...)` for A2 chapter5
- track: fresh_generation_replication
- constraints:
  - grayscale only
  - fixed protocol images: `lena`, `barbara`
  - fixed protocol corruptions: `random_pixel@50%`, `text@50%`
  - do not enter GUI / video / chapter7 extensions
  - materialize a fresh code artifact instead of copying an existing generated file
- allowed references:
  - problems/a2_requirement.md
  - report/a2_eval_protocol_v0.md
- no task card provided in this mode
