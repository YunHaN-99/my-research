# Pilot Round 1 Task Pack Checklist v0

## 目的
把首轮 pilot 每个 session 该发什么、不该发什么、结束后必须回收什么写成固定清单，避免正式执行时材料混发或泄露 scorer-only 文件。

## 通用规则
- 参与者可见材料和研究者内部材料必须分开打包。
- 不向参与者暴露任何 `diagnosis.md`、`fixed_code.py`、既有 `patched_code.py`、`prompt_used.md`、`model_raw_response.md`。
- `session_record`、`scoring_sheet`、CSV 模板属于研究者侧材料，不属于 participant pack。
- `process_guided_workflow` 比 `baseline_workflow` 只多给 task card 摘要、最小 checklist 和 notes template，不多给 gold answer。
- 发放前研究者先在 participant-visible 模板里预填 `session_id`、`task_id`、`condition`、`session_stage`。
- 每个 session 建议先建独立目录，并固定使用以下落盘命名：
  - `participant_form_filled.md`
  - `participant_submission.md`
  - `participant_notes_filled.md`（仅 `process_guided_workflow`）
  - `session_record_filled.md`
  - `scoring_sheet_filled.md`
  - `src/`

## 研究者通用底包
每个 session 都要提前备好以下研究者侧文件：
- `pilot/pilot_session_record_template_v0.md`
- `pilot/pilot_scoring_sheet_v0.md`
- `metrics/pilot_session_log_template_v0.csv`
- `metrics/pilot_session_log_codebook_v0.md`
- 对应任务的 bug-repair protocol：
  - A1 用 `report/a1_bug_repair_protocol_v0.md`
  - A2 用 `report/a2_bug_repair_protocol_v0.md`

## DRY-01

### 参与者可见
- 若选 A1：
  - `solutions/hw1_op1/failure_cases/bug_01_dp_boundary/symptom.md`
  - `solutions/hw1_op1/failure_cases/bug_01_dp_boundary/buggy_code.py`
  - `task_cards/A1_seam_carving_taskcard_v1.md`
  - `task_cards/A1_bug_repair_taskcard_v0.md`
- 若选 A2：
  - `solutions/hw2_op2/failure_cases/bug_01_missing_mask_constraint/symptom.md`
  - `solutions/hw2_op2/failure_cases/bug_01_missing_mask_constraint/buggy_code.py`
  - `task_cards/A2_rslt_inpainting_taskcard_v1.md`
  - `task_cards/A2_bug_repair_taskcard_v0.md`
- 通用：
  - `pilot/pilot_participant_form_v0.md`
  - `pilot/pilot_participant_submission_template_v0.md`
  - `pilot/pilot_bug_repair_checklist_v0.md`
  - `pilot/pilot_bug_repair_notes_template_v0.md`

### 结束后必须回收
- participant form
- participant submission
- notes template
- session record
- scoring sheet
- `1` 行带 `internal_dry_run` 的 CSV 草稿
- 最终代码路径与最小验证产物路径

## S01: `T2_A1_bug_01` + `baseline_workflow`

### 参与者可见
- `solutions/hw1_op1/failure_cases/bug_01_dp_boundary/symptom.md`
- `solutions/hw1_op1/failure_cases/bug_01_dp_boundary/buggy_code.py`
- `pilot/pilot_participant_form_v0.md`
- `pilot/pilot_participant_submission_template_v0.md`

### 研究者内部参考
- `report/a1_bug_repair_protocol_v0.md`
- `task_cards/A1_bug_repair_taskcard_v0.md`

### 严禁暴露
- `solutions/hw1_op1/failure_cases/bug_01_dp_boundary/diagnosis.md`
- `solutions/hw1_op1/failure_cases/bug_01_dp_boundary/fixed_code.py`
- `solutions/hw1_op1/generated/run_020_bug_01_direct_answer/*`
- `solutions/hw1_op1/generated/run_021_bug_01_plain_guidance/*`
- `solutions/hw1_op1/generated/run_022_bug_01_coe_guided/*`

### 结束后必须回收
- participant form
- participant submission
- session record
- scoring sheet
- CSV 草稿
- 最终代码路径
- 最小验证或输出路径

## S02: `T2_A1_bug_01` + `process_guided_workflow`

### 参与者可见
- `solutions/hw1_op1/failure_cases/bug_01_dp_boundary/symptom.md`
- `solutions/hw1_op1/failure_cases/bug_01_dp_boundary/buggy_code.py`
- `task_cards/A1_seam_carving_taskcard_v1.md`
- `task_cards/A1_bug_repair_taskcard_v0.md`
- `pilot/pilot_bug_repair_checklist_v0.md`
- `pilot/pilot_bug_repair_notes_template_v0.md`
- `pilot/pilot_participant_form_v0.md`
- `pilot/pilot_participant_submission_template_v0.md`

### 研究者内部参考
- `report/a1_bug_repair_protocol_v0.md`

### 严禁暴露
- `solutions/hw1_op1/failure_cases/bug_01_dp_boundary/diagnosis.md`
- `solutions/hw1_op1/failure_cases/bug_01_dp_boundary/fixed_code.py`
- `solutions/hw1_op1/generated/run_020_bug_01_direct_answer/*`
- `solutions/hw1_op1/generated/run_021_bug_01_plain_guidance/*`
- `solutions/hw1_op1/generated/run_022_bug_01_coe_guided/*`

### 结束后必须回收
- participant form
- participant submission
- notes template
- session record
- scoring sheet
- CSV 草稿
- 最终代码路径
- 最小验证或输出路径

## S03: `T3_A2_bug_01` + `baseline_workflow`

### 参与者可见
- `solutions/hw2_op2/failure_cases/bug_01_missing_mask_constraint/symptom.md`
- `solutions/hw2_op2/failure_cases/bug_01_missing_mask_constraint/buggy_code.py`
- `pilot/pilot_participant_form_v0.md`
- `pilot/pilot_participant_submission_template_v0.md`

### 研究者内部参考
- `report/a2_bug_repair_protocol_v0.md`
- `task_cards/A2_bug_repair_taskcard_v0.md`

### 严禁暴露
- `solutions/hw2_op2/failure_cases/bug_01_missing_mask_constraint/diagnosis.md`
- `solutions/hw2_op2/failure_cases/bug_01_missing_mask_constraint/fixed_code.py`
- `solutions/hw2_op2/generated/run_043_bug_01_direct_answer/*`
- `solutions/hw2_op2/generated/run_044_bug_01_plain_guidance/*`
- `solutions/hw2_op2/generated/run_045_bug_01_coe_guided/*`

### 结束后必须回收
- participant form
- participant submission
- session record
- scoring sheet
- CSV 草稿
- 最终代码路径
- 最小验证或输出路径

## S04: `T3_A2_bug_01` + `process_guided_workflow`

### 参与者可见
- `solutions/hw2_op2/failure_cases/bug_01_missing_mask_constraint/symptom.md`
- `solutions/hw2_op2/failure_cases/bug_01_missing_mask_constraint/buggy_code.py`
- `task_cards/A2_rslt_inpainting_taskcard_v1.md`
- `task_cards/A2_bug_repair_taskcard_v0.md`
- `pilot/pilot_bug_repair_checklist_v0.md`
- `pilot/pilot_bug_repair_notes_template_v0.md`
- `pilot/pilot_participant_form_v0.md`
- `pilot/pilot_participant_submission_template_v0.md`

### 研究者内部参考
- `report/a2_bug_repair_protocol_v0.md`

### 严禁暴露
- `solutions/hw2_op2/failure_cases/bug_01_missing_mask_constraint/diagnosis.md`
- `solutions/hw2_op2/failure_cases/bug_01_missing_mask_constraint/fixed_code.py`
- `solutions/hw2_op2/generated/run_043_bug_01_direct_answer/*`
- `solutions/hw2_op2/generated/run_044_bug_01_plain_guidance/*`
- `solutions/hw2_op2/generated/run_045_bug_01_coe_guided/*`

### 结束后必须回收
- participant form
- participant submission
- notes template
- session record
- scoring sheet
- CSV 草稿
- 最终代码路径
- 最小验证或输出路径
