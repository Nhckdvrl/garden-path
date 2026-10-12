# OpenCode 数据扩增提示词 — 自然语料优先、提出候选而不是自动造 Gold

You are helping prepare **candidate materials only** for an academic behavioral study of Garden Path effects in LLMs. We have already chosen a scientific construction and provided a few verified published **public examples**.

Design a small batch (at most five independent lexical families) of grammatical, natural-sounding English temporary ambiguities in the SPECIFIED structure. Where possible adapt a natural sentence from an allowed public corpus, and document that source; never hallucinate a real corpus citation.

For each candidate:
- Preserve genuine local ambiguity and a valid global disambiguation; both early interpretations must be grammatical/semantically possible at the prefix.
- Avoid exaggerated stereotypes, implausible role assignments, repetitions of the same verb/noun template, unnatural comma omission, and ungrammatical reduced relatives.
- Provide GP and a matched, natural disambiguated version with **minimal structural differences**. If perfect match is impossible, mark explicitly which parts differ; do NOT claim it is a pure punctuation manipulation.
- State which early relation would become obsolete and which later relation is stated.
- Propose one independent supported relation only when available *naturally* in source, and one controlled downstream-use task; don't manufacture vague "bridges" that merely restate the old relation.
- Provide at least one competing interpretation of ambiguous propositions and mark doubtful Gold as UNRESOLVED.
- Use varied lexemes/events and representative language, not dozens of easy-to-guess synthetic templates.
- Exclude inputs already in our published candidate source manifest to avoid duplication.

Return strictly parseable JSON:
{
  "task": "candidate_construction",
  "construction": "NPZ|NPS|MVRR|NPVP",
  "items": [{
    "provisional_family_id": "...",
    "origin_type": "DOCUMENTED_CORPUS|DERIVED_PUBLISHED|MODEL_PROPOSED",
    "origin_url": null,
    "gp": "...",
    "cue": "...",
    "control_change": "...",
    "initial_relation": "...",
    "final_relation": "...",
    "source_asserted_relations": ["..."],
    "semantic_risks": ["..."],
    "lexical_naturalness_risks": ["..."],
    "requires_review": true
  }]
}
No claims of verified naturalness, authorship, Gold correctness, or empirical GP effects. All output requires an independent quality pass.
