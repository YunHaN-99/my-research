# A2 Expanded-Scope Selected Entries v1

## 目的
从 A2 expanded-scope 的 `4 images x 4 corruption = 16 cases` 中挑出更适合进入中期题库的代表案例，避免把整张扩展评测表原样塞进 task-bank。

## 选择原则
- 代表不同图像类型，而不是只选同一张图的不同 corruption。
- 代表不同 corruption 形态与强度，而不是只选“最容易”的 case。
- 代表当前 A2 扩展稳健性的广度，同时保持题库页面简洁。
- 这些条目是“正式题库条目”，对应的是 case 定义本身，不再按 `direct_answer / plain_guidance / coe_guided` 重复计数。

## 固定入库的 4 个代表案例

| entry_id | image | corruption | 代表指标 `(PSNR, SSIM, RSE)` | 选入理由 |
|---|---|---|---|---|
| `A2.exp_lena_text_30` | `lena` | `text@30%` | `28.8651 / 0.9619 / 0.0669` | 代表文字遮挡场景，恢复结果直观，适合展示“结构保留 + 局部遮挡修复” |
| `A2.exp_barbara_center_block_35` | `barbara` | `center_block@35%` | `19.2680 / 0.7603 / 0.2418` | 代表连续块缺失，且 `barbara` 纹理复杂，能体现 patch-group RPCA 的纹理恢复特性 |
| `A2.exp_peppers_random_70` | `peppers` | `random_pixel@70%` | `15.2643 / 0.3261 / 0.3719` | 代表高强度随机缺失，是当前扩展集里更“难”的 case，适合体现任务边界 |
| `A2.exp_cameraman_random_30` | `cameraman` | `random_pixel@30%` | `21.3495 / 0.4603 / 0.1468` | 代表经典灰度图像 + 中等随机缺失，便于和课程图像处理语境对齐 |

## 为什么不把 16 个 case 全部都算成正式题库条目
- expanded-scope 的 16 个 case 主要服务于“扩展稳健性验证”，不是 16 个完全独立的新任务家族。
- 若把 16 个 case 全部硬算成题库条目，中期材料会显得数量很大，但结构不清楚。
- 中期更需要的是“条目层次感”和“代表性”，而不是把所有评测行都挪进题库页。

## 中期题库中的推荐写法
建议中期材料把这 4 个 case 写成：

> A2 在固定协议之外，已从 expanded-scope 验证集中固化出 4 个代表案例，覆盖文字遮挡、连续块缺失和不同强度的随机缺失，用于把 A2 从主案例闭环进一步扩展成更像样的中期题库结构。

## 直接依据
- `report/a2_expanded_scope_protocol_v0.md`
- `report/a2_expanded_scope_summary_v0.md`
- `metrics/a2_expanded_scope_eval_v0.csv`
- `metrics/a2_expanded_scope_perf_v0.csv`
