# garden-path

2026-10-09，用户决定重启研究，并将当前仓库迁移为 `garden-path`。此前研究方式存在重大问题；旧研究的结论、失败记录和冻结资产保留，不能自动视为重启后的有效依据。

- 本地位置：`/home/xiang/garden-path`
- GitHub：<https://github.com/Nhckdvrl/garden-path>
- Git 历史：仅当前完整工作区快照作为新的初始提交，不继承旧提交历史。
- 当前阶段（2026-10-12）：**Garden Path 行为研究方案 v0.1 已建立**，包括两个可证伪 Pilot、测量协议、文献知识库与来源迁移。**尚未运行新的模型实验**；旧 G0–G33 仅为历史研究。

## 当前研究入口

- **[新研究问题与路线](research/RESEARCH_PLAN.md)** — 先从行为规律寻找解释空白，不预设机制故事。
- **[测量与金标协议](research/MEASUREMENT_PROTOCOL.md)** — 源蕴含、关系依赖、独立问答/生成、材料质量。
- **[Pilot A：语义依赖损害的拓扑](research/PILOT_A.md)** / **[Pilot B：错误解析的额外结构启动](research/PILOT_B.md)** — 独立问题，不强行合并。
- **[可复用论文知识库](library/README.md)** — 36份带原始读书范围的文献卡、逆向实验设计图谱、Related Work ownership与阅读债务。
- **[SSN研究资产迁移说明](imports/ssn-incremental-revision/README.md)** — 精选结果/代码，外置原始数据仍在来源路径；不能当作新研究结果。
- **[研究决策树](research/DECISIONS.md)** — 竞争假设、负结果处理与后续实验选择。
- **[创新性标准](research/SCIENTIFIC_NOVELTY_STANDARD.md)** — 人类经典心理语言学问题迁移到 LLM 本身可能成立；不人为设定“必须全新机制”的门槛。
- **[数据战略](research/DATA_STRATEGY.md)** / **[OpenCode 辅助数据审核](research/DATA_ASSISTED_REVIEW.md)** — 数据来源、样本量、自然度、质量控制、定点复核与免费模型使用边界。
- **[2026-10-12 数据与创新性审计记录](research/DATA_EXECUTION_DECISION_2026-10-12.md)** — 189句族、57家族审核队列、30离线测试通过、真实研究仍未启动。

## 仓库导航

| 路径 | 内容 |
|---|---|
| `src/`、`scripts/`、`tests/` | 现有代码、运行工具和测试 |
| `data/` | 现有材料、审查记录及外部数据说明 |
| `registrations/`、`preregistrations/` | 原始注册与预注册记录 |
| `results/`、`logs/` | 实际结果、原始输出、执行与失败记录 |
| `archive/`、`stages/` | 历史决策、旧路线与阶段文档 |
| [STATUS.md](STATUS.md) | 当前重启状态及历史结果入口 |
| [REPRODUCE.md](REPRODUCE.md) | 现有结果核验说明 |
| [RESEARCH_HISTORY.md](RESEARCH_HISTORY.md)、[EXPERIMENTS.md](EXPERIMENTS.md) | 历史研究与实验记录 |

## 历史与迁移

2026-09-30 的整题终止决定作为历史记录保存在[旧归档](archive/abandoned_unring_the_bell_2026_09_30/README.md)。2026-10-09 的明确重启决定取代根目录的终止状态，但不改写历史数值、失败判断或材料来源。旧文档中的下一步计划不会自动成为新计划。

[迁移记录](archive/repository_restart_2026_10_09/README.md)保留本次整理前的入口文档。模型权重、外部原始数据、激活缓存及运行缓存沿用 `.gitignore`，保留在本地；GitHub 保存可版本管理的完整项目快照。获取外部数据的说明见 [data/external/README.md](data/external/README.md)。
