# Garden Path 论文升维讨论：从废弃句法分析到隐式假设修正

> **研究思想备忘录 / Discussion & Ideation Log**  
> 日期：2026-11-23  
> 来源：围绕 arXiv:2610.36797v1 的多轮用户—ChatGPT—Gemini 讨论，结合本仓库既有研究记录与若干相关论文。  
> **状态：探索性讨论，不是已批准的实验计划、预注册、论文结论或新实验结果。**  
> 本文用于保存完整的思想空间、分歧、被纠正的推理、竞争假说和日后可供选择的研究路径。尤其不要根据 PDF 附录中的少量汇总点估计预先指定机制结论。所有新的经验主张都需要上机检验。

## 0. 讨论背景与原则

讨论起点：论文 *Language Models Keep Abandoned Analyses: Residue and Adaptation after Garden-Path Sentences*（Xiang Ding，arXiv:2610.36797v1，2026-10-27）。

起初的问题是：按照 ACL/EMNLP/NAACL 标准，这篇文章属于什么档次，若希望从扎实的 Main 候选提升到有 Oral/Outstanding 竞争力，应该增加什么样的科学贡献？

讨论逐渐形成一个方法论共识：

1. **先确定“值得知道什么”，再决定“怎样测量”。** 当前应积极发散，不要盯着论文 Table 5 / Appendix E/G 的少量汇总数字做局部算术推导，以免助长噱头或扼杀更广的想法。
2. **不把强 Soundness 和更多实验等同于更高科学价值。** 堆叠 Mamba、DAS、SAE、Pythia、多语种、Prompt Engineering 并不能自动形成新理论。
3. **从现有论文独有的控制能力出发。** Garden-Path 提供增量形成、明确消歧点、被放弃结构、前期承诺强度等可控属性；这比一般“旧事实被纠正”任务更接近研究推断过程本身。
4. **重要假说与已证发现严格分开。** “无条件广播”“门控修正”“污染”“幽灵”“滞后”“纯追加心智”目前都是候选解释或比喻，不能抢先写成发现。
5. **允许负结果提供科学信息。** 尤其不应预设某个机制必然跨句法、事实更新和 CoT 泛化。
6. **保持仓库历史真实。** 旧研究（包括 2026-09 废止路线）、2026-10 的重启与冻结检验、当前 arXiv 稿件分别是不同阶段。本文只新增讨论，不改写旧结果或预注册，也不授权新的 GPU / API 工作。

**仓库已有入口：** [当前认识](CURRENT_UNDERSTANDING.md) · [顶会计划](TOPVENUE_PLAN_2026-10-23.md) · [数据战略](DATA_STRATEGY.md) · [创新性标准](SCIENTIFIC_NOVELTY_STANDARD.md) · [测量协议](MEASUREMENT_PROTOCOL.md) · [历史](../RESEARCH_HISTORY.md) · [论文源码](../paper/main.tex)。

## 1. 现有论文的可信出发点（不是新假说）

一个典型 NP/Z Garden-Path：

> While the man hunted the deer ran into the woods.

增量处理时，the deer 可以暂时被分析为 hunted 的宾语；ran 出现后，完整句法要求 deer 是新主句的主语。对照版本在 hunted 后加逗号，使前面的误分析较难形成。

2026-10-27 预印本主要报告：

- **Production residue：** 被放弃的宾语分析会影响后续文本的结构选择；跨 24 个开放模型（部分实验为 22 个）、独立材料和真实采样生成观察到证据；标点习惯、动词偏向、局部字串等有相应控制。
- **Adaptation：** 同一句经历也可产生朝向正确结构的预期调整，且与消歧点预测错误有关；生成类与理解类指标中的净权重不同。
- **机制定位：** 后续预测从歧义消解前 NP 位置的表征读取了部分旧角色信息；歧义消解后主句位置与修正方向的效应相关。Activation Patching、Probe 和角色方向干预提供不同强度的支持。
- **显式 QA 的 lingering 与后续 priming 不等价：** Section 8 观察到两种行为指标跨材料相关性很弱，尽管各自相对可靠；这尚不是“双独立信念系统”的因果证明。
- **事实覆盖任务：** Thursday → Monday 之类显式修正里，旧值仍可影响后续预测；某些模型直接读旧陈述，另一些模型通过后续位置间接传递。
- **范式移植问题：** LLM 会在自由续写中复制无逗号 Garden-Path 风格，导致直接照搬人类原始统计量产生反号，因此需要恰当的标点和句法控制。

论文仍有已注明的限制：主要深入英文 NP/Z、闭源模型未测、若干预设预测失败、行为操纵有未通过检查者、因果干预仅覆盖部分模型，事实更新是模板化实验。**这些边界不能通过换宏大标题消失。**

## 2. 多轮讨论是怎样演进的

### Round A：从 ACL 评分到“如何升档”

初评偏向扎实 ACL Main 候选：严谨性和实验覆盖是优势；潜在上限更多受理论外延、机制深度与普遍意义限制。分数只是主观模拟，不是官方审稿结果。**不应把 Oral 或 Outstanding 当作某组实验可保证达到的分数。**

### Round B：Gemini 第一版的“五个升级轴”

提出：（1）跨架构：双向/PrefixLM、Mamba/SSM、Hybrid；（2）机制细分：Head-level Path Patching、DAS、SAE；（3）多轮纠错与推理期 KV 干预；（4）Base/Instruct 对比和 Pythia 训练动力学；（5）多语言及附录校对。

合理贡献：提醒我们不应只停留在 Span 定位，也不应忽视真实纠错与训练变化。主要问题：**方法菜单过宽**；“KV 不可变 ⇒ 残留必然发生”不成立；不同架构的观察差异也不能单独证明该架构属性为必要/充分条件。DAS 不自动表示语法角色天然有某个维度；SAE 不等于证明因果；多语言需要真正可比的构式。

### Round C：ChatGPT 首轮反驳与竞争机制路线

建议从“表征在哪”推进到“旧解释和正确解释如何竞争、如何按任务被利用”：NP × MC 的因果对照、Head/Path Patching、控制 L/S 指标差异、任务依赖调用。更适合稳健机制论文，但容易把宏大研究问题缩成对已有结果的精细勘误，且一些组合修补早已在附录实现。

### Round D：Gemini 从附录提出“三颗核弹”

1. Appendix E 的 NP / MC / Both 干预提示**可能存在非加性**；但 Both 的反事实计算依赖关系以及状态拼接的分布外效应需要考虑，不能直接宣称发现抑制回路。
2. Appendix G 的部分 Attention Knockout 出现**阻止最终答案直接访问旧陈述，旧值拉力反增**。可以猜测后续状态中继，但不能从 Knockout 等同于删除文本，更不能直接称“白熊污染”。
3. Section 8 的显式问答 lingering 与结构启动残留弱相关，提示不同读出不等价，但不证明它们分别由独立的“显式信念 / 隐式行为系统”支配。

### Round E：四个精巧机制方向

- **Phase-Locked Retrieval：** 目标句所处结构阶段，可能决定当前偏好检索原句的旧 NP 阶段或后期消歧阶段。时间顺序纠错：S 是预测消歧词 *之前* 的 Surprisal，不能说模型“读到该词以后才在这一概率中切换”。该理论尚未验证。
- **Distance × Repetition：** 残留与适应可能具有不同距离/重复敏感性，但 Transformer 上测到的是上下文与干扰效应，不等于证明人类短期激活/长期学习的时间常数。
- **Direct vs. Mediated Retrieval：** 旧信息可以从原位置直接读取，也可能通过后续位置传递；这两个中性概念比 Fossilization / Contagion 更接近已获支持的证据。
- **Soft Hedging / Non-destructive Versioning：** 旧解释仍能访问，可能有利于后续回溯。只有在某些任务中证明“保留历史带来收益”才能把它解释为适应性能力。

### Round F：“1 盘活 + 2 手术刀”与其批评

Gemini 提出统一读出面拆解，以及 Zero-Mention Transplant：

- 论文的 L 可以按自回归链式法则拆为 L1 与 L2；在同一前缀比较逗号与消歧动词的 Logit Difference。它能检查原 L/S 净差异是否来自位置聚合、候选 token 或指标抵消。只是**诊断方法**，结果尚未产生。
- 对现有 QA 使用 NP/MC Patching，可问显式理解与结构启动的差别是否形成因果分离。但一种干预只影响一种任务，严格说只是 Single Dissociation；Double Dissociation 需要另一种反向选择性干预。
- 将原 Context A 的更正句 KV 移入从未出现旧值的 Context B，检测旧值影响是否跟随状态迁移。成功本身只说明后续状态携带历史信息；需要非纠错中继对照、反向移植、匹配位置及不损害新值预测，才谈得上**纠错特异性中继**。

在这阶段用户指出：目前我们只有 PDF 汇总结果，不应对几个点估计过度演算和拟合理论；应先讨论更广的研究方向，必要时再让真实数据决定。这一方法论转向是本备忘录的核心。

### Round G：四个“大问题”

1. **Autoregressive Backtracking 的果蝇模型。** 用 Garden-Path 作为干净的增量推断/撤销场景，延伸到简单推理和 CoT。但“句法重分析”与“模型自己生成并纠正错误 CoT”不能不经验证就称计算同构。
2. **显式认知与隐式行为脱钩。** 关键不只是“嘴上说对，行为仍错”，而是解释的可访问性、当前有效性和下游因果影响能否分离。与已有 Context Update / Stale Memory 文献的边界必须明确。
3. **什么是有效撤销（Undo）。** 更好的正面标准是 Selective Revision：保留历史访问能力，同时解除旧解释对当前行动的不恰当效力。把旧历史全部删除未必是正确修正。
4. **模型主动模仿歧义。** 原始统计量反转提示 LLM 可能学习无逗号 Garden-Path 的局部文本模式；这可作为独立的心理语言学/ICL 方向，但不是简单的“人类绝不模仿、模型才模仿”。

### Round H：Rejected Hypotheses 的生命周期

ChatGPT 提出“**The Fate of Rejected Hypotheses**”：重点关注模型增量计算中**临时形成、却从未明确写入文本的解释**。把研究对象拆成 Formation（是否形成）、Revision（如何修正）、Reuse（后续何时继续影响）。

候选桥梁是：
- 隐式增量形成的句法解释；
- 前提变化后被撤销的隐含推论；
- 模型写出的显式中间结论及其自我纠错。

独特性在于前两者可不涉及任何显式的错误陈述。不能把高概率偏好直接等同于模型“坚定相信”某一个假设。

### Round I：Gemini 最新的三个进一步命题（2026-11-23）

**I. Computational Hysteresis / Path Dependence**：文本最终自洽、没有明确错误陈述，也可能因增量处理历史而留下后效。重要提醒：GP/CUE 并非相同的输入序列，常规顺序、标点、风格差异本来就会造成不同预测；要证明*特异于被弃解释*的额外路径依赖，必须设计强控制。Hysteresis 一词在已有 LLM 文献中有使用，不宜当作新颖性本身。

**II. Addressability Paradox**：显式说出旧假设可能使其更牢固（verbalization entrenchment），也可能反而给模型一个便于指认、否定和抑制的语言抓手（addressable handle），使隐式旧假设更难撤销。两种预测均合理。不同长度、重复、任务指令、显式纠错和自己生成 CoT 是重要混杂变量；不得直接把“无明文错误”同一于“内部不可寻址”。

**III. Append-only State vs. Current-state Control**：普通 causal Transformer 的旧 Token 状态不可逆向重写，但新 Token 的状态可以编码修正后的解释；不能说模型“只有日志、完全没有当前状态”。更合适的问题是：修正后的当前解释是否在不同下游读出中被一致采用？早期信息是被后期表征重塑、被读取时选择，还是多者共同作用？

## 3. 我们真正想区分的“科学对象”

| 类别 | 输入中是否明确表达旧解释？ | 修正方式 | 典型场景 | 最重要的混杂 |
|---|---|---|---|---|
| 隐式句法假设 | 否（但局部词序支持其形成） | 后来的句法结构迫使重分析 | NP/Z Garden-Path | 标点、普通结构启动、可选解析的强弱 |
| 隐式语义/场景假设 | 否，线索只暗示 A | 晚到的证据使 B 成为更合理解释 | Red herring、frame shift | 世界知识、故事常识与线索的明暗程度 |
| 隐式可撤销推论 | 结论 A 未说出 | 增加例外/反证条件 | 逻辑/日常推理 | A 是否真的由前提支持；任务目标变化 |
| 显式事实或推理断言 | 是 | Correction、反证、重新推导 | Thursday→Monday；CoT A→B | 明文旧值、重复与纠错提示 |
| 自生成的显式旧结论 | 是，并由模型输出 | 自我纠错或外部反馈 | CoT backtracking | 生成轨迹选择偏差、模型自我承诺与外部强制差别 |

**关键区分：** 不要把“没有任何一句假话”直接解释为“模型内部形成了唯一确定的错误假设”。需由行为、可解码性及必要时因果作用三方面共同支持。还需区分真实事件被推翻与仅仅被重语境化（例如“原来是在拍电影”并没有取消电影内部发生的事件）。

## 4. 三个最新大命题的比较：应各司其职，而不是竞争口号

### 4.1 建议的主问题：Revision of Unspoken Hypotheses

> 当模型在增量加工中临时形成过一个未明确写出的解释，后续证据使其不再成立时，旧解释以什么形式留存、是否有当前效力、何时影响新行为？

优点：
- Garden-Path 的已建基础直接服务于这个问题；
- 与“文本里有显式旧值”的一般 Stale Memory 任务有合理区分；
- 可延伸到语义重框、可撤销推理，但不要求从第一天就全部覆盖；
- 无论观察到残留、完全撤销或条件性结果，都可能形成明确边界。

风险：
- “旧假设”可能只是概率分布中的偏好，而非单一可定位表征；
- 普通 lexical/structural priming、语篇风格、话题延续、记忆检索可能足以解释一部分；
- 扩展到 CoT 不代表机制相同。

### 4.2 作为行为现象的 Path Dependence（比喊 Hysteresis 更稳健）

强版本问题：当完整输入在目标语义、证据和任务要求上受到严格匹配时，*曾经诱导过被弃解释的增量历史*是否还产生可归因的额外下游影响？

弱版本现象：仅仅因为两段文本顺序或标点不同，模型输出就不同。**弱版本不是新科学发现。**

要警惕：即使最终真值条件相同，也不代表完整 token 条件分布本该相同。若未来把“hysteresis”作为正式术语，必须给出明确的 operational definition 与对照基线，并查与既有 Prompt Hysteresis、Semantic/Contextual Inertia 的关系。

### 4.3 作为解释变量的 Addressability

两种对立假设：

- **Entrenchment：** 明确说出 A 增加可检索、可模仿、可延续的锚点，使 A 更难撤销。
- **Addressable Correction：** 明确说出 A 使其成为可指认对象，模型更容易执行“此版本无效，但历史上存在”。
- **Null/conditional：** 效果由纠错形式、任务、角色、模型训练等决定，未必有统一方向。

注意本仓库 2026-09 历史曾在另一个“证据排除”语境研究 semantic addressability，并最终否定以“更具体目标更容易排除”作为独立顶会贡献的写法（见 RESEARCH_HISTORY.md）。**这里可以复用教训，不可把不同任务混为一谈，也不可只换新术语重复旧思路。**

### 4.4 作为待检验机制的 Selective Revision / Version Validity

一个成功的系统应可能同时满足：
- **Historical Access：** 知道此前 A 曾经被考虑/陈述；
- **Current-State Control：** 当前问答、生成、决策不误用失效的 A；
- **Conditional Reuse：** 当任务明确要求回忆历史或反事实时，能正确访问 A。

“写入时重塑”与“读取时选择”可能同时存在，不是非此即彼；某些架构也可能依赖后期汇总状态，不要求每次都全量扫描旧 Token。“完全擦掉旧信息”既未必可行，也未必理想。

## 5. 哪些非句法场景真正配得上 Garden-Path？

**首选：未点名红鲱鱼（Unnamed Red Herring / Latent Frame Shift）。** 一组真实、相容的前期线索支持解释 A（文本不明说 A）；后来的强证据使 B 更合理；后续任务同时测当前 B 的正确使用以及 A 的不恰当残留。优先考虑能明确确定最终解释、控制先验和线索强度的场景，避免仅凭创作性故事判定真值。这个方向与 Garden-Path 在“旧解释未显式陈述”上最接近。

**次选：可撤销推理的隐式/显式双生对照。** 同一前提序列，分别不写 A 与明确写 A，再提供相同新证据。它最直接针对 Addressability，但显式写 A 必然增加 Token、重复和任务导向；需要足够仔细的对照，不能把比较自然地等同于“latent reasoning vs explicit CoT”的全面比较。模型自己写 A 又会引入选择偏差。

**探索性：语用/模态取消。** 例如“闹钟响起，原来是在做梦”“导演喊卡，原来是在拍摄”。比较有戏剧性，但不同语境层的事件仍可能成立；容易把“世界事实变更”误当作“语篇框架切换”。仅适合作为后续生态有效性验证，不能贸然称为干净的逻辑推翻。

**明确保留的反例/边界：** 与上述 implicit pole 不同，Thursday→Monday 是明确的旧陈述，应作为 Explicit Pole 或不同机制的对照，而不是硬说与 GP 共享相同电路。

## 6. 可竞争的解释地图（尚未实验）

| 竞争解释 | 它能解释什么 | 它还不能自动解释什么 |
|---|---|---|
| 普通结构启动/语篇风格模仿 | GP 影响后续语法分布、模型自己造 GP | 为什么效应特异于曾经被构建而随后放弃的解析 |
| 早期旧状态被后续读取 | GP 的 NP patching 效应 | 任何旧信息都会无条件影响所有未来读出 |
| 后期新状态覆盖/抑制旧影响 | MC 的反向效应 | 存在统一明确的抑制头、门控器或当前状态寄存器 |
| 后续位置中继 | 事实更正 Attention Knockout 的部分模式 | 中继只发生在 Correction 句、且必然“污染” |
| 显式 verbalization 固化错误 | 旧答案被写出后被重复引用 | 隐式旧假设一定较易消除 |
| 可寻址性改善纠错 | 明文旧值可被指认、标失效 | 隐式旧假设一定不可被内部抑制 |
| 单纯长度/顺序/标点/任务偏置 | 不同前缀、输出任务产生不同概率 | 精确匹配对照下的因果表征特异性（若被观察到） |

任何理想研究都应让至少两个真正有竞争关系的解释在某些新条件下给出不同预测，而非先指定某种故事、再选择支持它的样本。

## 7. 可能的研究主线及其“成功/失败价值”

| 路线 | 核心问题 | 成功时能新增什么 | 不成功仍值得知道什么 | 目前定位 |
|---|---|---|---|---|
| **A. Revision of Unspoken Hypotheses** | 未陈述的旧解释会否在被弃后持续影响未来？ | 将 GP 现象推进到隐式推断的更新 | 哪类隐式推断能被充分修正；边界与普通 priming 的区别 | **最推荐主线** |
| **B. Addressability Paradox** | 说出 A 会固化还是帮助撤销 A？ | 验证显式化对撤销有效性的因果作用 | 无统一方向；纠错表达方式/任务是主要变量 | A 的优先解释变量 |
| **C. Path Dependence / Hysteresis** | 终点语义近似等价，历史路径仍有特异后效吗？ | 动态解释历史的真正效应 | 多数差异由普通文本条件化解释 | A 的候选行为规律 |
| **D. Selective Revision** | 保留历史同时撤销当前效力能否分离？ | 版本有效性的功能性理论与评估 | “忘记”并非唯一的合格修正标准 | 正面规范性目标 |
| E. Structural imitation | 模型何时模仿歧义的生成风格？ | LLM 结构启动/语篇模式学习的新解释 | 文化/范式迁移中测量偏差的边界 | 可能独立成篇 |
| F. Architecture / Training / Dynamics | 路径依赖如何受架构与后训练改变？ | 机制和规模/训练泛化 | 不是所有 GPT 式现象都是 KV 不可变决定 | 仅在主问题明确后扩展 |

## 8. 从研究愿景到上机：目前只留“观察窗口”，不冻结协议

这里**不选择最终模型、具体统计量、数据量或结论阈值**。先列若决定探索必须解决的概念问题：

1. **如何确认 A 在证伪前真的被模型形成或至少显著偏好？** 观察前缀条件概率、行为选择、可解码性；不要单凭一次 QA 或 Probe 宣称有稳定“信念”。
2. **如何确认新增证据真正推翻 A，而不是仅仅把 B 也变得可能？** 最终语义、时态、世界状态必须有可审核的 ground truth。
3. **如何把普通 priming/风格模仿与被弃假设的特异残留区分？** 同词汇、相似格式、相同最后解释、可逆操作等对照可能需要，但应由具体材料决定。
4. **如何控制“显式说出 A”额外引入的内容？** 明文旧值、token 长度、任务提示、来源角色（self vs user vs quoted）、纠错标记不能随意混在一起。
5. **如何衡量正确的 selective revision？** 同时有当前状态、历史追忆与恰当反事实调用，避免把“旧值一律无法恢复”误判为好。
6. **何时进入内部因果机制？** 先有稳定、具可区分预测的行为规律；激活修补、Head Patching 或 KV 操作是必要时的显微镜，不是研究命题本身。
7. **如何处理闭源推理模型和 latent reasoning？** 不应把没有输出错误句的外显任务直接等同于模型进行了未观测到的连续隐空间推理，更不能仅凭 GP 结果作该跨域外推。

可以作为未来低成本侦察的选项（**不是现阶段已经拍板的项目**）：L1/L2 链式拆解、同前缀候选 logit 比较、GP-Priming 与 QA 的同位置因果读出、NP/MC/Both 非加性复核、匹配非纠错中继对照的状态移植、距离×重复、严格配对的隐式/显式旧假设条件。

## 9. 文献与新颖性：已知邻居和阅读债务

**来源：** 以下仅为已使用/已检索到的主要邻居，既不是穷尽文献表，也不意味着全部有同等强度的因果发现。正式 Related Work 要进一步逐篇核对任务、材料、模型、可比性和全文证据。

- 原始论文：[arXiv:2610.36797](https://arxiv.org/abs/2610.36797)；仓库 [paper](../paper/)。
- 人类被弃解析启动：van Gompel et al. (2006), *The activation of inappropriate analyses in garden-path sentences: Evidence from structural priming*, JML（原论文参考文献）。
- LM Garden-Path 理解：[Amouyal et al., ACL 2025, *When the LM misunderstood the human chuckled*](https://aclanthology.org/2025.acl-long.403/)。
- 句法 belief update：[Zhou et al., EMNLP 2026, *Syntactic Belief Update as the Driver of Garden Path Processing Difficulty*](https://aclanthology.org/2026.emnlp-main.1805/)。
- Contextual inertia：[Chen et al., Findings ACL 2026, *Breaking Contextual Inertia*](https://aclanthology.org/2026.findings-acl.313/)。
- Semantic inertia：[IJCAI 2026, *Quantifying Semantic Inertia in Large Language Models Under Rapid Topic Switching*](https://ijcai.org/proceedings/2026/88)。
- Prompt hysteresis：[OpenReview, *Prompt Hysteresis: Task Inertia and Metastable States in In-Context*](https://openreview.net/pdf?id=Noe0KyCAla)。**注意：具体发表状态和方法范围需重新核对。**
- Explicit context update / current state：[Guo et al., *When Context Changes: Understanding Update Failures in LLMs*](https://arxiv.org/abs/2609.38866)（2026 预印本）。
- 自我修正与错误上下文拖拽：相关 ICLR 2026、2026 自我修订风险研究可作比对，但必须区分明确旧答案的重做与未明说旧假设的撤销。
- 本仓库 [library/](../library/) 包含已有文献卡；优先阅读原研究和较近同对象论文，避免根据二手摘要宣布“首创”。

## 10. 2026-11-23 的暂定综合意见（可被未来证据推翻）

**首选研究主角：** *Revision of Unspoken / Implicitly Formed Hypotheses*。  
**潜在现象命名：** path-dependent after-effects of abandoned interpretations；在有严格控制之前，不急于宣称“Computational Hysteresis”。  
**关键可检验维度：** 是否显式表达旧假设（addressability/verbalization）、修正是否明确、不同下游任务是否恰当利用历史。  
**机制待定：** 早期状态回读、后期状态中继、不同候选的任务条件检索、后训练影响；不预设某个头或统一 KV 定律。  
**最值得找的非句法兄弟：** 不明说旧结论、但前期线索强烈诱导 A、晚期证据使 B 成立的受控推理/语义重框场景。  
**研究目标：** 解释“形成—废弃—再利用”，而非仅仅“旧信息没被删”。目标中的历史访问与当前效力应被区分。  
**工作节奏：** 先概念发散与文献阅读 → 挑能区分竞争假说的自然问题 → 小规模可证伪 pilot → 再按实验结果决定要不要升级论文主线。暂不根据附录的少数点估计为机制命名，不启动未经计划批准的新实验。

### 一句话论文愿景（不是已证明的 claim）

> **What happens to an interpretation a language model formed but never stated, once later evidence makes it invalid?**

中文：**“当语言模型从未明确说出、却在增量理解中形成过的解释被后续证据否定时，这个解释究竟经历了什么？”**

这既保留了 Garden-Path 已证明的特殊价值，也为更宽的信念修正、推理回溯与非破坏性历史管理留出了自然的研究空间。

---

*维护约定：后续讨论可追加日期小节；任何新假说均标记探索性，实验结果必须回到实验卡和冻结数据源；本备忘录不能取代论文稿件、预注册或仓库 CURRENT_UNDERSTANDING。*
