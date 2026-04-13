# Prompt Used

- mode: direct_answer
- prompt_file: prompts/a2/bug_repair_direct_answer_v0.md
- symptom: solutions/hw2_op2/failure_cases/bug_01_missing_mask_constraint/symptom.md
- buggy_code: solutions/hw2_op2/failure_cases/bug_01_missing_mask_constraint/buggy_code.py
- goal: keep the original function interface and return a diagnosis, patched code, and brief regression notes
- withheld_from_model:
  - solutions/hw2_op2/failure_cases/bug_01_missing_mask_constraint/diagnosis.md
  - solutions/hw2_op2/failure_cases/bug_01_missing_mask_constraint/fixed_code.py
