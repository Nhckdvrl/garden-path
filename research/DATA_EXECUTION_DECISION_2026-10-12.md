# Garden Path — Data & novelty recalibration record (2026-10-12)

**科学决策说明，不是实验结果。** 主仓库：[garden-path](https://github.com/Nhckdvrl/garden-path)。原 SSN 研究只作为历史知识/数据来源。

## 1. 本次改变了什么？

- 明确撤销不合理的“只有获得全新统一机制/完全没人做过的问题才有创新性”的门槛。**2006 人类范式迁移到现代 LLM** 的认真行为检验，有机会成为独立贡献；必须与既有的 generic LM priming 文献对齐，但无需一开始就解释网络内部回路。
- 数据不是分析后的修饰品，而是科学问题的载体；从作者**已发表/社区审查**素材出发，结构、语言自然度、真值/依赖标记和样本量一起设计。小样本可以是仪器检查，不能反复在十几条例句上局部优化直到显著。
- 不强制全部语料多次人工/LLM 复审。已发表、未编辑材料做全自动 schema/来源一致性检查、所有可疑项定点审、事前分层随机抽样；新关键 Gold 和人工改造的条件才加大审核。OpenCode 免费模型只是**辅助检查**，没有单模型裁决真值的权力。

## 2. 已有的原始资产（不是新结果）

| 资产 | 数据规模 | 限制 |
|---|---|---|
| Amouyal 原始开源 CSV（锁定 commit） | 189 独立句族，756 question rows，378 GP/CUE 记录 | NP/Z 的 CUE 是换序，不是逗号；新 source-entailment Gold 未核 |
| Ceháková & Chromý 2025 | 48 个来源句族，8条件/item | 原 Stimuli.zip 在 ssn 有审计和 hash，但还没有在本仓库取得原始字节；需获取 source |
| van Gompel 2006 | 人类 Exp.2 36 / Exp.3 40 句族 | 最贴近 B 的范式；需核原附录完整材料/是否可公开重用 |
| Prime-LM 2022 | 约 1.3M highly repeated prime-target rows | 泛 LM structural priming，T 是 active/passive 不是 transitive/intransitive，不能当成 Pilot B 现成 targets |
| SSN E52/E69/E80/E82/E87/E98/E107 | 已有历史行为/QA/角色分析 | 不得包装为本仓库新实验，也不要再运行同样的 prompt 网格 |

详见 [数据战略](DATA_STRATEGY.md) / [原始数据状态](../data/gp_behavior/README.md) / [历史 SSN 资产](../imports/ssn-incremental-revision/README.md)。

## 3. 静态 QA 实际执行情况

2026-10-12 GitHub Actions [38197763244](https://github.com/Nhckdvrl/garden-path/actions/runs/38197763244) **success**：
- 30 项离线单元测试通过。
- 四份 Amouyal 源 CSV Git blob hash 和 378 条 PENDING 派生候选完全一致。
- 构式分层随机审计选出 **38 families**，加上已知相对关系句自然度风险共 **57 unique families** 要排查（风险规则是启发式，不是“剩余132条一定无错”）。
- 57 句族展开为两条件 source 后，共 **114 candidate rows / 29 review batches**（其中大部分 4 条/批）。
- 示意样本量计算输入 family-level SD=.25、最小效应 .08、α=.05/power=.80 → **约77独立 families**；这是参数假设、非研究数据观察。
- **0 次 OpenCode/LLM 调用、0 次新 GPU、0 条新 Gold 标签、0 条真实 Pilot A/B 结果**。正式模型实验尚未启动。

## 4. 当前两个 Pilot 的正确角色

**优先考虑 Pilot B（人类错误解析启动 → 现代 LLM）的原始范式迁移**，如果能取得 van Gompel Exp.3 的原始材料及自然 GP/cue 条件。它提供一个足够自然、已有明确人类预测、但现代 LLM 仍值得认真对照的切口。首轮 20–30 家族仅 debug，不能作为定论；随后使用所有合格现成材料并按 family SD 扩充，不能盲目套用 Amouyal REORDERED 对照。

**Pilot A 继续平行探索**：局部错误角色、正确新关系与源支持语义的区别。先利用成熟的 Ceháková 2025 与 Amouyal 已发表数据，用合理数量的自然关系题/释义衡量 LLM 是否出现人类式理解分离；不要求一定发现“依赖拓扑定律”才值得研究，但也不冒充从未有人在 LLM 上测过 QA/role 失配。

两个 Pilot 可以分别发展、分别失败，绝不为了合成统一论文而捏造共同机制。

## 5. 信息增益决定下一动作，而不是时间表

1. **数据资格**：获取合法来源/原附录、核真正的 GP 和其自然 control，审查 target 同动词 T/I 自然性；保留尚不能修正的数据。
2. **仪器有效性**：正常结构启动的阳性对照能否工作？旧源 relation Gold 之外的新 claims 是否具有稳定源语义？回答格式的 parser 是否有效？
3. **充分独立样本**：用源家族独立数、方差、效应最小重要差决定扩充；对看不到的小效应不要作负结果结论。
4. **比较人与现代 LLM**：不仅平均准确率/续写概率，还比较结构/模型差异和非显式问答的功能结果。
5. **有价值才追机制**：如果经典行为效应可靠迁移，本身即可成题；有复杂边界才进一步找解释。不从 SAE/几何出发倒造故事。

**重要**：后续本地 agent 执行前，应读 [novelty standard](SCIENTIFIC_NOVELTY_STANDARD.md)、[DATA_STRATEGY](DATA_STRATEGY.md)、[OpenCode review](DATA_ASSISTED_REVIEW.md)、[Pilot A](PILOT_A.md)、[Pilot B](PILOT_B.md)。本记录不是授权机器使用付费服务或额外 GPU 的开关。
