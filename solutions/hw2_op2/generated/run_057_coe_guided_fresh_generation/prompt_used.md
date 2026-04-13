# Prompt Used

- mode: coe_guided
- prompt_file: prompts/a2/coe_multi_role_v0.md
- task: implement `rslt_inpainting(observed, mask, ...)` for A2 chapter5
- track: fresh_generation_replication
- constraints:
  - grayscale only
  - fixed protocol images: `lena`, `barbara`
  - fixed protocol corruptions: `random_pixel@50%`, `text@50%`
  - do not enter GUI / video / chapter7 extensions
  - materialize a fresh code artifact instead of copying an existing generated file
- provided materials:
  - problems/a2_requirement.md
  - task_cards/A2_rslt_inpainting_taskcard_v1.md
  - report/a2_eval_protocol_v0.md
  - fixed multi-role structure
