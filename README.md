# garden-path

2026-10-09，用户决定重启研究，并将当前仓库迁移为 `garden-path`。此前研究方式存在重大问题；旧研究的结论、失败记录和冻结资产保留，不能自动视为重启后的有效依据。

- 本地位置：`/home/xiang/garden-path`
- GitHub：<https://github.com/Nhckdvrl/garden-path>
- Git 历史：仅当前完整工作区快照作为新的初始提交，不继承旧提交历史。
- 当前阶段：仓库整理与迁移；新的研究问题、方法和实验计划尚未确定。本次迁移不运行实验。

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
