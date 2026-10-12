# Prime-LM 2022 — published data and code reuse boundaries

**Primary**: Sinclair, Jumelet, Zuidema & Fernández, TACL 2022, [paper](https://aclanthology.org/2022.tacl-1.60/), [authors' repository](https://github.com/dmg-illc/prime-lm). **Reading scope**: official repository README, directory list/corpora/vocabulary listing and primary paper methodological summary checked 2026-10-12. Not every corpus CSV or full paper appendix examined.

## Scientific motivation and reusable assets

- Human structural priming reflects prior syntactic exposure, but LM experiments can be confounded by overlapping words and semantic coherence. The paper separated prime-conditioned target log-probability and generated many independently controlled structural/lexical conditions.
- Corpus covers core/simple, semantically anomalous, complex, lexical boosts and recency cases; 48 transitive verbs, 16 ditransitive verbs, 119 nouns reported in main article; generation manually checked on subset by native English speakers.
- Typical corpora: ~1,500 distinct target sentences each paired with 10 primes per target for 15,000 prime-target rows per target structure; overall ~1.3M rows over many conditions. **This is not 1.3M independent families**.
- The scoring pipeline produces target log probabilities under structurally congruent and incongruent primes, and compares differences within identical targets; therefore target's baseline probability cancels in the paired contrast.

## Critical mismatch for Garden Path project

The dataset names 'transitive' and 'ditransitive' mean:
- 'transitive' = **active vs passive voice** in an otherwise transitive construction.
- 'dative' = **prepositional object vs double object** ditransitives.

Our NP/Z experiment needs the **same early verb** to permit genuine **transitive vs intransitive** interpretations, and the *GP* source must undergo a temporary mismatch. Therefore NO existing Prime-LM target can be relabeled as our target without semantic/valence audit and adaptation.

Transfer value is **methodological/engineering**: lexical-category constraints, positive control priming, held-fixed target likelihood contrasts, attention to function-word reuse, and a large corpus vocabulary/source pool.

## Originality calibration

Generic priming in LMs is established by Prime-LM. The specific **human 2006 wrong-initial-parse** priming effect has a different scientific object; a reliable modern-LLM transfer (or a robust failure under positive generic priming controls) may be meaningful even if we cannot prove a new latent mechanism.

## Provenance/rights

The author's repo exposes README and corpora, but the root listing accessed here did not show a standalone LICENSE. **Do not vendor its entire corpus or assume redistribution rights** without checking license/permissions. Link to source data and reproduce via pinned version when needed, with attribution and source identity.
