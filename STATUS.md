# garden-path 当前状态

日期：2026-10-13。状态：**PAUSED（暂停）**。用户于 2026-10-13 决定暂停本课题，先做别的课题。没有任何运行中的 GPU 任务或后台进程；所有代码、材料和结果均已提交并推送。

**恢复工作时请先读：** [暂停交接文档](research/PAUSE_HANDOFF_2026-10-13.md) → [当前认识](research/CURRENT_UNDERSTANDING.md) → [实验索引](research/experiments/README.md)。

## 截至暂停时的结论（E001–E012，最多 21 个模型；探索性 + 多项预先冻结的检验）

NP/Z 花园路径句在因果语言模型中留下三种可分离的痕迹：

1. **被放弃宾语分析的生产型残留**：van Gompel 2006 的人类效应迁移成功。
   - 所有模型、所有材料上净效应为正；不依赖标点（E009）。
   - 需要真正得到过宾语分析，不是字串效应（E011）。
   - 在自由生成中存在（E012：8/8；与概率读数跨模型 ρ = .81）。
2. **向正确结构的误差驱动适应**：在理解型读数上，句族内因果操纵成立（E006）。只见于非单调再分析（NP/Z、MV/RR），不见于 NP/S（E007/E008）。
3. **理解残留**：问答中仍答"人猎了鹿"。
   - 残留很大，且随歧义区长度增加。
   - 与 (1) 在逐句层面无关（E003，10/10 个模型，信度约 0.9）。
   - 不随花园路径被消除的程度而变化（E003c）。

**方法发现**：人类范式的原始统计量在语言模型上无效。模型会模仿标点风格，自己写出花园路径句（最高 25%），使原始对比反号（E012）。

**下一步（未开始）**：E013 机制检验（残留存在哪里）、E014 承诺的因果操纵、E003d 理解残留的成因。详见交接文档。

---

## 历史状态记录（2026-10-12 及以前，保留原文）

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
