# 从论文如何“长出来”学习研究：Garden Path 实验设计逆向图谱

2026-10-12。不是作者传记；除作者明确写出的动机外，以下“可能的选题生长路径”统一标为 **RECONSTRUCTED**。与本库原始论文卡配套。方法：把每个实验倒回**尚不知道结果**的时刻，先列竞争解释、对立预测、最便宜且可辨别的操作，再看作者实际如何选择。

## 1. Christianson → Slattery 2013：旧误读残留是否意味着新结构没有建立？

- **Parent belief:** Garden Path 后的错误回答意味着初始解释还在；但是“没能建立新的正确结构”和“新的结构已建立、旧误读仍干扰”都能导致同一回答。
- **Pressure:** 单独询问旧命题无法区分两种解释，提问本身还可能使旧解释重新活跃。
- **New premise / change of object:** 不再以回答错误作为唯一变量；找一个只有正确新结构才能支持的、在线功能性后续依赖，再独立测旧语义对后句的影响。
- **Experiment chain (RECONSTRUCTED):**
  1. 给 GP 与 comma 条件相同的后续反身代词性别依赖，测试新结构是否可用；若 GP 不敏感，可能未建立它。
  2. 给下一句只在早期错误解释上有特别自然衔接的材料，测阅读成本是否携带旧分析影响。
  3. 位置、合理性及非关键区域控制，区分整句困难和局部语义干扰。
- **Scale of increment:** 改变**证据类型**，不是全新的 GP 现象，也不是完整脑机制；“新关系可用”和“旧关系已失活”可能分离。
- **Important limit:** Online mismatch sensitivity 并非直接观测全局语义图；不同实验人群/条目不保证单试次同时持有两整棵树。
- **What to learn:** 先确定哪一种结果会使我们改变解释，然后寻找一个能让错误答案与正确结构功能解耦的自然依赖任务。
- [Paper note](papers/human/slattery2013-competing-representations.md), [published manuscript](https://faculty.wcas.northwestern.edu/myo507/Papers/SlatteryEtAL_GoodEnough_Published.pdf).

## 2. van Gompel et al. 2006：怎样测一个已不应存在的分析？

- **Parent:** 如果最终阅读恢复了正确结构，初始错误结构也许已彻底停用；但直接问旧内容会污染检测。
- **Revealing move (DOCUMENTED in abstract):** 阅读句作 prime，随后让人完成另一句；测与**最初不合适分析**一致的结构选择。GP 与明确分隔版本比较。
- **Critical distinction:** 对 NP/Z，早期错误解是及物结构（把 NP 当作前动词宾语），最终正确解是前动词不及物＋新主句；**不能把后续更偏正确结构误称为错误路径残留**。
- **Competing post-results:** 一种是部分 reanalysis，一种是 episodic memory trace；即使有 priming，也不唯一识别神经/计算存储。
- **Scale:** 把旧解析残留变成**跨任务行为读数**；不是新增 parser。
- **LM research distance:** Sinclair 2022 已证明一般 LM priming；2026 production works进一步建立词汇/语义混合。**把经典人类范式迁移到现代 LLM 本身也可能是增量**，因为一般 LM priming 并未直接回答被推翻的初始句法解析是否产生后效应。GP-specific 交互可进一步提高解释力，但不是必须先完成的机制门槛。
- **Read scope:** 当前仅原 SSN 卡的摘要/介绍片段和出版社摘要，**未假装全文精读**；正式 protocol 需补全文及条件表。
- [Note](papers/human/vangompel2006-garden-path-priming.md), [publisher](https://doi.org/10.1016/j.jml.2006.06.004).

## 3. Amouyal et al. ACL 2025 → ACL 2026：人机“困难相似”究竟到哪一层？

- **Parent:** LM surprisal 可以定位不寻常的 disambiguator，但不等于最终句子真的被正确理解，亦不等于人机使用相同解释策略。
- **Pressure:** 大部分此前工作是 token/结构指标；同一行为问答下人机是否受类似因素支配尚不清楚。
- **Changed premise:** 用人类心理语言学的竞争假说决定材料操纵：结构、语义合理性、动词/论元需求；同样的理解任务用于人和 LLM，再以释义、文生图交叉验证。
- **Experiment logic (RECONSTRUCTED):** 先用 canonical GP/control 确认有困难 → 语义合理性拉开预测 → 论元需求测试传统“错绑定”解释 → 其他下游表现挑战仅响应格式伪影 → 2026 横跨七类困难结构/多模型比较边界。
- **Owned contribution:** 语言模型确实存在很大的结构相关理解困难；更大模型与人类有时更加接近；跨结构差异。
- **Critical unresolved measurement:** 一些问题如 'Did the man hunt the deer?' 严格来说是 NOT ENTAILED，不是 CONTRADICTED。答 Yes 有时是语用推断；不能强行把原 GoldNo 全称为虚假世界信念。
- **Distance for us:** 人类与 LLM 在**相同、足够自然且可靠的材料**上的直接比较有研究价值；如果此前 LLM 已有近邻，则关系类型、依赖结构和未被提问用途可进一步扩大认知。后者是深入方向，不是未经检验时的入场硬门槛。
- [2025](papers/behavior/amouyal2025-garden-path-humans-llms.md), [2026](papers/behavior/amouyal-2026-processing-difficulties.md).

## 4. Ceháková & Chromý 2025：为什么不只问最初误读？

- **Parent:** Good-enough 文献通常将理解失败看成初始错误解释的 lingering residue；另有关于重新分析不充分和局部树不连贯的理论。
- **Pressure:** 如果最终局部句法调整正确，句子的**其他部分**是否也被正确理解？先前问答未充分检验。
- **Changed premise (DOCUMENTED from abstract/methods snippets):** 对同一句同时测 ambiguous region 和 disambiguating region 的正确/错误理解；NP/Z 与 MV/RR、GP 与无歧义控制。
- **Discriminatory potential:** 仅局部错误论预测主要损伤旧附着关系；更广泛的连贯解释失败预测同句其他关系也受损。需要排除一般复杂度和问句难度。
- **Owned:** 'Errors beyond initial misanalysis' **已有直接前人**；不能换用 LLM 就宣称发现“理解整体破碎”。
- **Idea scale:** 不是复杂工具，而是发现现有问题**问错了位置**，调整测量对象便产生新解释压力。
- **For us:** 必须超越作者已经测试的两区域问答；进一步检验 **哪些关系受影响、影响是否遵循句法依赖图而非词距/问句、是否传递到自然下一任务**。假设可证伪。
- [Note](papers/behavior/cehakova2025-disrupted-final-interpretations.md), [primary](https://doi.org/10.1080/0163853X.2025.2513210), [stimulus source](https://zenodo.org/records/16358492).

## 5. Ceháková & Chromý 2026：'动词偏好' 与整体 misanalysis probability 的距离

- **Parent:** Garden Path processing cost 被不同理论归因于 verb subcategorization bias, surprisal, plausibility, cloze。
- **Pressure:** 各文献跨材料、语言、结构比较时可能给出不同预测；单构式中某个效应并不能构成通用机制。
- **Changed premise (primary abstract/discussion):** 同一行为设计比较多个指标，11 种 ambiguous/unambiguous 类型，对 self-paced reading time 和 comprehension accuracy 都建模。
- **Result:** Cloze-derived misanalysis likelihood 在这批人类数据上最稳定；verb bias/surprisal/plausibility 较不稳定。不是 'surprisal 在任何模型上已被推翻'。
- **Scale:** **比较解释变量**及其泛化范围，而不是发明新 GP 效应。对传统理论的改进来自合理共同支持域与相同数据上的模型比较。
- **LM distance:** 模型自身的 prefix continuation preference 未必等于人类 cloze；高相关预测不证明模型有持续、可干预的“承诺态”。
- **Reverse-design exercise:** 在看到作者结果前，预测各指标在 11 结构内的可辨别差异；设计相同外部准确率但不同初始偏好的材料。不要把单个 β 显著当作机制。
- [2026 paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC13129637/); [new scope note](NEW_READINGS_2026-10-12.md).

## 6. Sinclair et al. TACL 2022 → JML 2026 / Pucci 2026：怎样先造一个可靠的 priming 仪器？

- **Parent:** LM 可能捕捉局部 word order/word identity，而非 abstract structural persistence。
- **Pressure:** 若只观察输出重复某种结构，无法分辨词汇/语义/句法相似性。
- **Changed premise:** Prime-LM 对不同 target/prime 对做 balanced comparison，控制 lexical overlap、semantic relatedness、target baseline；指标在条件对之间作差，而非直接把一个 continuation 的概率当作 '记忆'。
- **Owned 2022:** 一般 LM structural priming exists; structural vs word-order/semantic boundaries.
- **2026 JML:** 在人机共享材料上比 priming 的位置与 item-level 对齐；平均存在 priming 并不意味着模型对每个 item 都像人。
- **2026 Pucci:** 从评分候选变成真正生成的生产分布，讨论词汇与语义的一致性；生成 priming 本身不新。
- **Scale:** 从“现象”到“合格仪器”，再到“跨方法、跨物种比较和真实生成”。我们应该**借 metric 与 matched-contrast 设计，而非借一个名字**。
- **For us:** 先验证 target 的 transitive/intransitive 对比有效，GP/无逗号及 cue/逗号做 2×2 差中差，再加入非歧义一般结构 prime 对照；没有稳定 GP-specific interaction 便不进入追踪 '幽灵解析'。
- [2022 note](papers/priming/sinclair2022-structural-persistence.md), [2026 JML note](papers/priming/sinclair2026-human-lm-priming.md), [2026 production note](papers/priming/pucci2026-primed-production.md).

## 7. Hanna & Mueller NAACL 2025：从可读句法走向功能干预，但在哪个任务边界止步？

- **Parent:** Transformer 懂 syntax 的 probing 结果不意味着它用于预测或实际问答。
- **Changed premise:** 找到影响 GP continuation 的 SAE features，检验它们是否与语法相关，是否表示多个 interpretations；再测后续 QA 是否复用相同 features。
- **Experiment logic:** 从功能性 continuation influence 过滤非因果探针 → 测多个 reading 的 feature → 比较不同任务中的回路 → 对功能性重用作限定结论。
- **Known limits:** 两小模型；QA 主要归于 Gemma 2-2B；feature attribution faithful coverage 有限；0%/0.2% IoU 不能证明所有可能机制都没有重分析。
- **Scale:** 机制测量对象与因果标准的进展，不是唯一可解释模型。
- **For us:** 在行为层出现一条前人不能预测的规律前，不应再画层间余弦/SAE 子空间。功能信号必须预测/选择性改善 **多个互相独立的真实语义用途**。
- [Detailed imported note](papers/mechanisms/hanna-2024-gp-mechanisms.md).

## 8. Yoshida et al. ACL 2026：存在性证明如何反驳一个过强的不可能论？

- **Parent:** 普通 LM surprisal 低估人类 GP reading slowdowns，导致'这种困难不可能仅由 surprisal 解释'的强读法。
- **Pressure:** 现成语言模型的失败，只能说明现成模型与人类预测分布不同，不能证明 *任何* LM 都不可能。
- **Changed premise:** 不再只比较现成预训练 LM；微调模型，使 surprisal 拟合人类 GP，并在 held-out GP、自然语料和一般 LM 能力上交叉检验。
- **Scale:** 从经验性反例转向理论上 **existence proof** 的论证尺度；与直接发明 processing-cost 函数是不同路线。
- **Limit:** 这种训练成功不能证明真实人类在内部只使用 surprisal，也不意味着当代 instruct LM 的 QA 错误应由 surprisal 单独解释。
- **For us:** 必须明确要解释的是 RT、token probability 还是语义决策，避免让一种现象给另一种理论做稻草人反证。
- [Detailed imported note](papers/psychometrics/yoshida2026-surprisal-existence.md).

## 9. Clark et al. EMNLP 2025 → CoNLL 2026：改变'要被修正的对象'

- **Parent:** Reader may reparse a fixed string; but if source could be noisy, the object of inference is intended text **and** parse.
- **Pressure:** 当前 token surprise 可能预测停顿，却不能预测人会回到哪个**可能出错的词**重读。
- **Changed premise:** 借已有 noisy-channel Bayesian processor 提出'晚来的后缀决定哪些早期位置可能是错误位置'；用匹配前缀、调换后缀来分离难度与有目标的回视。
- **Experimental insight:** 让 baseline 在两个条件下做出相同预测，但扩展对象后的模型预测不同；用动作位置来检验而不是仅看整体准确率。
- **Owned:** 人类 noisy-channel GP 与 targeted regressions；不能以 input-source label 影响 LLM QA 当作新 Bayesian 机制。
- **For us:** SSN E80 已做 “grammar trust vs possibly missing word” 标签操纵而未有稳健联合修复。只有真实噪声生成过程、显式本体区分'加逗号'与'更改命题'才值得重新打开。
- [Detailed imported note](papers/noisy-channel/clark2026-targeted-noisy-channel.md).

## 10. Bates 2025 的负例：33 → 157，先验故事崩塌

- **Initial story:** 消融早层 MLP 应减少 juke-point surprisal，因为早期错误承诺造成 surprise。
- **Pilot:** 33 个 GP 对在量化小模型上的初期结果看起来支持。
- **Expanded evidence:** 157 对、四模型族的新实验中，早层 MLP 消融不再普遍降低 GP token surprisal；观察到的 selective contrast 主要来自正常续写概率被破坏，top-5 overlap 大降。
- **Crucial restraint:** 这也不能证明 universal 'surprisal independent of commitment' circuit；消融改变了整个预测分布。
- **Our lesson:** 行为操作、干预是否保持语言能力、样本多样性和独立验证先于任何几何/回路故事。
- [Technical report](https://jonrbates.ai/2025/07/26/garden-path-sentences.html) (blog, **not** peer-reviewed).

## 共同的 Cho 式研究动作（不等于复制具体工具）

一篇强实验论文应当使实验链沿着 **主假说每步仍有什么未排除的竞争解释**展开：
1. 先选有真实重要性的异常；不是“哪个模型提供了最好看的差异”。
2. 提出至少两个能给出相反预测的解释（若同样预测，实验无信息量）。
3. 设计最便宜、对两种解释造成不对称压力的自然干预。
4. 结果出来后，主动找能推翻自己最想讲的故事的强对照。
5. 提供超出已有数据/构式/问法的外推预测，失败就降级/换问题。
6. 内部机制测量只有在能独立验证行为解释时才有资格进入主线。

**题目不需要无人研究；需要的是能够让现有理论作出不同预测，并最终迫使它们更新的实验。**

## 科学标准修正（2026-10-12）

任何关于“2006 年已做，所以迁移到 LLM 不够新”的旧说法，都须以 [当前创新性标准](../research/SCIENTIFIC_NOVELTY_STANDARD.md) 为准。前人范式是资产，不是自动否决。也要遵守 [数据战略](../research/DATA_STRATEGY.md)：真实且有代表性的样本与证据质量比故事复杂程度更重要。
