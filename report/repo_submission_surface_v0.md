# Repo Submission Surface v0

## 目的
把当前仓库里应该进入提交的研究资产，与本地噪声和缓存文件分开，降低 `git status` 噪声，方便中期材料和后续 commit 分批整理。

## 1. 当前应保留的研究资产

### 顶层说明
- `README.md`
- `当前进度汇报_2026-04-12.md`
- `TimeLine.docx`
- `talktoai.pdf`
- `大研课题规划建议.pdf`

### 主线研究目录
- `task_cards/`
- `prompts/`
- `runs/`
- `metrics/`
- `report/`
- `problems/`
- `solutions/`
- `hw2-op2/`

### 输出资产
- `outputs/hw1_op1/`：已是 A1 证据链的一部分，可继续保留
- `outputs/hw2_op2/`：属于 A2 证据链，但更适合按“代表性结果优先、全量输出次之”的顺序分批整理

## 2. 当前不应进入提交面的本地噪声
- `Microsoft/`：误入工作区的 PowerShell 模块缓存
- `__pycache__/`
- `*.pyc`
- `.venv/`
- `.tmp_ustc_mm26/`
- `outputs/hw2_op2/_tmp_*`

## 3. 推荐的 staging 顺序
1. 先提交说明和协议：
   - `README.md`
   - `report/*.md`
   - `task_cards/*.md`
   - `problems/*.md`
2. 再提交指标与代码本：
   - `metrics/*.csv`
   - `metrics/*codebook*.md`
3. 再提交代码与 prompt：
   - `hw2-op2/`
   - `solutions/`
   - `prompts/`
4. 再提交 run 文档：
   - `runs/*.md`
5. 最后再决定是否提交全量输出：
   - `outputs/hw2_op2/`

## 4. 提交前最小复核
- `git status` 中不再出现缓存目录或 `.pyc`
- `hw2-op2/` 不被误当成本地噪声忽略
- `metrics/` 和 `report/` 保持可直接打开
- 结论类文档能回指到对应 `runs/` 与 `metrics/`

## 5. 当前判断
- 当前最需要清理的是缓存和误入目录，不是继续隐藏真实研究资产
- `hw2-op2/`、`runs/`、`metrics/`、`report/` 这些新增内容都应被视为主线提交对象，而不是噪声
