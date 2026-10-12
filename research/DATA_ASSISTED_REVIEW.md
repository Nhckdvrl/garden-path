# OpenCode 免费模型辅助数据构造/检验 — 最小可审计工作流

Created 2026-10-12. **尚未实际调用 OpenCode 模型、尚未产生新标注**。目标不是制造人工标注负担，而是将免费模型用于最有价值的材料处理，同时留下可追溯的错误与不确定性。

## 0. 外部服务与零费用原则

- OpenCode CLI [官方文档](https://opencode.ai/docs/models/) 支持 `opencode run --model provider/model "..." `；[官方 Zen 价格表](https://docs.opencode.ai/docs/zen/) 会公布免费/收费模型。免费条目可能随时变化，**不要硬编码永久免费**。
- 用户本地 Opencode CLI/账号需要已登录提供商，能看到当前可用免费模型后才执行。模型可能有试用限制/数据记录；不得把未公开研究信息、账号、私有邮箱或密钥放入请求。
- 本仓库只保留**公开或获许可的研究刺激、用于审核的局部提示、无秘密的回复、验证日志和成本声明**；凭据绝不提交。
- 若未检查价格/付费提示或选不到明确免费的模型，取消外部请求改用本地/人工审阅；**不得自动回退到付费模型，也不得启用账户自动充值**。

## 1. 什么时候值得调用？

| 场景 | 建议 | 不建议 |
|---|---|---|
| 社区发表原题，无改动且无已知错误 | 自动 schema 全量检查＋事前抽样（如10–20%）审核 | 每道原题做四次大模型复核 |
| 社区原题有 source–question 矛盾、语病或歧义点定位不明 | 定点标记 **全部高风险**，单项/成对模型评审 | 直接当研究模型的“错误”结果 |
| 新增无歧义对照/自然句 | 模型生成**候选**，独立模型审自然性，再规则/人工抽样 | 一模型生成即当正式定稿 |
| 新增依赖关系 source-gold（最重要） | 首次源语义标注、模糊项复核；区分 `ENTAILED` / `CONTRADICTED` / `NOT_ENTAILED` | 让被评测模型当自己的 Gold 裁判 |
| 扩增新 family 且缺自然素材 | 优先从出版材料或真实语料筛选，再用模型少量改造并核验 | 机械模板一口气造千条高度重复句 |

## 2. 输出协议（严格 JSON） 

建议分批每次 3–5 个 family（或独立 target），交给一个与后续受测模型不同的免费模型。
- `family_id`、`candidate_id`、`source_sha256` 必须原样回显。
- `acceptability`: `VALID` / `MARGINAL` / `INVALID` / `UNCERTAIN`。
- `source_gold`: 对每个提供的 proposition 单独输出 `ENTAILED` / `CONTRADICTED` / `NOT_ENTAILED` / `UNRESOLVED`，说明一句短依据；不把未说过等同不可能。
- `construction`, `ambiguity_span`, `disambiguation_token_span`, `control_changes`。
- `needs_escalation` 与 `reason_codes`（grammar、gold ambiguity、lexical bias、construction mismatch、question leakage、format）。
- 不允许静默补充/修改原句；给出建议修订时必须独立 `proposed_revision`，并保留原始字符串。

单个自由模型的置信度仅用于**风险排序**，不是真值概率。

## 3. 具体执行流程（推荐）

1. 运行 `research/tools/make_review_queue.py` 生成有固定 seed 的随机和高风险 family 队列；输出不会包含后验 model-success 筛选。
1a. 用 `research/tools/make_model_review_batches.py` 将审查队列拆为每批 2–4 条成对 source 的固定 JSON，附 SHA。审查模型响应另用 `research/tools/check_model_review.py` 验证字段/ID/源哈希（**不会自动把外部标注提升为 Gold**）。
2. 对现成原题仅复核风险队列和事前随机质量样本；对**新增关键 Gold** 做每项一次独立审核；新增整句材料需验证自然性。
3. 先用**现成 golden calibration**（约 20 条已核实的正、负、不蕴含及真实争议例子）评估所选免费模型的 Gold 错误率；高错误率则只做建议，不能用于直接授权自动通过。
4. 对有冲突的标注或高风险部分用第二个独立免费模型审阅；仍不一致再提交人工/来源研究的语义判定。**禁止投票直接冲掉真实歧义**。
5. 冻结来源 hash、提示、所用免费模型和 response 文件；记录费率检查、队列/成功/失败数量；不把 429、断流、JSON 缺失视为标注不合格或 negative。
6. 结合抽样复核正确率决定是否扩大随机审查比例；不为形式而全量过度审核。

## 4. 完整模板

- [Source-grounded audit prompt](model_assisted/REVIEW_PROMPT.md)
- [Natural construction prompt](model_assisted/CONSTRUCTION_PROMPT.md)
- [Batch builder](tools/make_model_review_batches.py) / [Response schema check](tools/check_model_review.py) — **off-line only**, no API execution or hidden spending

示例（**手动选择已验证免费 model ID**，切勿把下面的示例当作当前可用性保证）：

```bash
opencode models
opencode run --model opencode/<CURRENT_VERIFIED_FREE_MODEL_ID> "Review the public candidate according to research/model_assisted/REVIEW_PROMPT.md ..."
```

脚本可以将一个 family 的数据复制到临时 review 文件，但**没有当前连接/授权时不得在 CI 或 GitHub Actions 中自动向 OpenCode 发请求**。本地的 JSON 结果导入/验证应单独处理，不自动替换正式金标。
