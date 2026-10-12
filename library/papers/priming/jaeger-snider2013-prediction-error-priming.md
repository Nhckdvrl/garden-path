# Jaeger & Snider 2013 — Syntactic priming scales with the prime's prediction error

**Source:** T. F. Jaeger & N. E. Snider, *Alignment as a consequence of expectation adaptation: Syntactic priming is affected by the prime's prediction error given both prior and recent experience*. Cognition 127(1):57–83 (2013). [Author manuscript (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7313543). **Read scope: ABSTRACT + secondary summaries (2026-10-12); full text not yet read.** Do not cite effect sizes from this card.

## Claim (documented)

If priming reflects (near-)rational expectation adaptation, the amount of adaptation should scale with the prediction error experienced while processing the prime. Across conversational speech, picture description and written sentence completion, primes with higher syntactic surprisal produced stronger priming. The relevant error depends on both prior and recent (within-experiment) experience. This prediction is shared by error-based implicit learning (Chang, Dell & Bock 2006) but not by activation-based accounts.

## Why it matters for our NP/Z line

The garden-path prime is a natural place where the two theory families make **opposite** predictions:
- **Activation / residual analysis** (van Gompel et al. 2006; Christianson et al. 2001 lineage): the abandoned transitive analysis stays partly active, so it biases toward **transitive**. Strength ∝ how strongly the object analysis was entertained.
- **Error-driven adaptation** (Chang et al. 2006; Jaeger & Snider 2013): the disambiguation is a large prediction error in favour of the **final, intransitive** structure, so it biases toward **intransitive**. Strength ∝ disambiguation surprisal.

Our E002 discovery result (item level, causal LMs) suggests both components are present, with opposite signs, and nearly uncorrelated predictors (object expectation at the verb vs disambiguation surprisal). E005 tests this on held-out families. Human net data (van Gompel: GP > comma in transitive completions) imply the activation component dominates in humans *at the net level*. Our design asks whether that net effect masks an error-driven component, and how the balance shifts across LMs.

## Neighbours to read in full

Chang, Dell & Bock 2006 (Dual-path, *Psych Review*); Fine, Jaeger, Farmer & Qian 2013 (rapid syntactic adaptation in comprehension, *PLoS ONE*); Zhou et al. NAACL 2025 (inverse-frequency effect as an error-driven signature of LM in-context priming; [card](zhou2025-error-driven-priming.md)); van Schijndel & Linzen 2018 (neural adaptation in reading).
