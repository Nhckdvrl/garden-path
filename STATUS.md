# garden-path 当前状态

日期：2026-10-12。状态：**EXPLORATORY_RUNS_ACTIVE**（保留2026-10-09重启授权）。

> **2026-10-12 更新：** 首批真实模型实验已运行（E001–E005，NP/Z 错误解析启动）。当前认识与变化原因见 **[research/CURRENT_UNDERSTANDING.md](research/CURRENT_UNDERSTANDING.md)**；实验卡片见 `research/experiments/`。核心发现（探索性，held-out 验证进行中）：GP 启动的净效应是“残余激活（+）”与“预测误差驱动适应（−）”两种相反力量的平衡，其平衡随模型而变。下文“尚未运行”的描述已过时，保留为历史。

用户明确决定重启，指出此前研究方式存在重大问题。仓库改名为 `garden-path`，迁至 `/home/xiang/garden-path`，以当前完整快照建立新的 Git 历史并上传到 `Nhckdvrl/garden-path`。

2026-10-12 已将研究问题、两条候选行为 Pilot、材料与推断合同、知识库以及精选 SSN 历史资产写入本仓库。**目前没有新实验结果、没有新的GPU/API运行、没有已确认paper idea，也不自动复活旧方案。** 旧材料与结果保持原样；旧失败不改写为成功。新路线详见 [RESEARCH_PLAN](research/RESEARCH_PLAN.md) 和 [library](library/README.md)。

## 新一轮行为研究：当前边界

- 主问题：Garden Path 造成的关系失败遵循什么规律，是否存在超出常规结构启动的后效应？
- Pilot A：局部错误 vs 依赖拓扑和整体理解；最近邻 Ceháková & Chromý 2025、旧 SSN E70/E107。
- Pilot B：词汇独立、标点和普通 priming 控制下的错误解析特异性影响；最近邻 van Gompel 2006、Sinclair TACL 2022。
- **2026-10-12 科研原则更新：** 不追求完全空白问题；2006 年人类实验迁移到 LLM 可以有原创价值，不以“必须发现统一新机制”为门槛。[创新性标准](research/SCIENTIFIC_NOVELTY_STANDARD.md)。
- **数据战略：** 现成发表数据优先；依独立句族数量、效应尺度与方差决定扩增。质量复核风险导向，不全量机械重审；OpenCode 免费模型可用于关键构造/审核，但没有任何已执行免费 API 调用。[完整数据标准](research/DATA_STRATEGY.md)。
- **工程现状：** 189 已发表句族（378 GP/对照候选），均为 PENDING。GitHub Actions 已验证 **30项测试**与源数据一致性；事前抽样+定点风险队列覆盖 57 family / 29 OpenCode *待审核批次*，**尚未调用任何外部审核模型**。[证据与下一动作](research/DATA_EXECUTION_DECISION_2026-10-12.md)。
- 先验证具有科学价值且可证伪的行为规律；仅在必要时进入白盒机制。
- [文件来源与外置数据界限](imports/ssn-incremental-revision/README.md)、[stop/gates](research/DECISIONS.md)。

## 历史结果

2026-09-30 的整题终止状态被本次用户重启决定取代，其原文见[整理前状态](archive/repository_restart_2026_10_09/STATUS.md.before_restart.txt)，完整资产地图见[历史归档](archive/abandoned_unring_the_bell_2026_09_30/README.md)。

G33 历史结果为 200 个冻结 claim families、三个模型、43,200 个唯一 cell；候选推进条件为 0/3。原始统计与科学判断保持不变，见 [完整统计](results/g33/g33_registered_summaries.md)及[历史判断](results/g33/g33_integrated_assessment.md)。ConfB 等实验的实际数值、失败确认、post-hoc 身份及材料问题同样保留。
