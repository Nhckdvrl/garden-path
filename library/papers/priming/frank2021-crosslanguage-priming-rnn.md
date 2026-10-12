# Frank 2021 — Cross-language structural priming in RNN LMs (CogSci 2021 abstract/short paper)

**Source:** Stefan L. Frank, *Cross-language structural priming in recurrent neural network language models*, CogSci 2021 (2-page). [PDF](https://lst.cls.ru.nl/~sfrank/pubs/CogSci2021.pdf). **Read scope: FULL (the whole 2-page paper, read 2026-10-12).**

## What it did

- Construction: Dutch/English **NP/S-coordination** garden paths (*The wizard guards the king and the princess protects…*); 120 items from Hoeks et al. 2006, plus English translations.
- Models: 5 bilingual LSTMs (single 600-unit layer, 225M tokens).
- Priming = **error-driven weight adaptation** (lr 0.2, one gradient step on the prime, then reset), following van Schijndel & Linzen 2018 and Chang et al. 2006. **Not** in-context priming.
- Primes were presented **only up to and including the critical verb**, in ambiguous vs comma condition. DV = target garden-path effect (surprisal of the disambiguating verb, no-comma minus comma).
- Result: target GP effect stronger after an unambiguous (comma) prime than after an ambiguous prime. Within-language priming was stronger than between-language priming.

## What it licenses / does not

- Shows that an RNN adapted to the *ambiguous-then-resolved* string expects the resolved structure more (adaptation to the **final** analysis), and that this transfers across languages.
- It does **not** test whether a ruled-out initial analysis persists (the van Gompel question). The ambiguous prime's update is driven by the whole string including disambiguation. It uses gradient adaptation, not context, and RNNs, not transformers.

## Relation to our E001/E002

The closest LM ancestor of using **target GP surprisal as a priming DV**, which E002 adopts as a comma-free measure. The direction differs: Frank asks whether the final structure primes; we ask whether the abandoned transient analysis primes, in frozen transformers with in-context primes. Related adaptation work to read next: van Schijndel & Linzen 2018 (*A neural model of adaptation in reading*, EMNLP) and Prasad & Linzen 2021 (syntactic adaptation detectability).
