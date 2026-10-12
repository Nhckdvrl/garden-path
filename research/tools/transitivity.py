"""Classify whether the subordinate verb of a completed 'While SUBJ V ...' sentence takes a direct object.

Rule-based on POS tags only (spaCy en_core_web_sm): its dependency parser is itself garden-pathed
on comma-less NP/Z sentences, but its POS tags of the post-NP verb are reliable.

classify(prefix, continuation) -> dict(cls, comma, gp_style, first)
  cls      TRANS | INTR | AMBIG (relative clause / coordination after the NP, or unparseable)
  comma    continuation starts with ',' (explicit clause boundary right after V)
  gp_style INTR without a comma, i.e. the model itself produced a garden-path sentence
"""
from __future__ import annotations

import sys

sys.path.insert(0, "/home/xiang/.local/share/gp_spacy")
import spacy  # noqa: E402

_nlp = None
NP_TAGS = {"DT", "PDT", "PRP$", "JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS", "CD", "POS", "HYPH", "VBN", "VBG"}
FINITE = {"VBD", "VBZ", "VBP", "MD"}
OBJ_PRON = {"him", "her", "them", "me", "us", "himself", "herself", "themselves", "itself", "myself",
            "ourselves", "yourself", "yourselves", "whom"}
SUBJ_PRON = {"he", "she", "they", "we", "i"}


def nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm", disable=["parser", "ner", "lemmatizer"])
    return _nlp


def classify(prefix: str, cont: str, version: int = 1) -> dict:
    c = cont.strip()
    out = {"comma": c.startswith(","), "first": c.split()[0] if c.split() else ""}
    if not c:
        return {**out, "cls": "AMBIG", "gp_style": False}
    if c[0] in ",.;:!?—-)\"'":
        return {**out, "cls": "INTR", "gp_style": False}
    doc = nlp()(prefix.rstrip() + " " + c)
    n0 = len(nlp()(prefix.rstrip()))
    return _decide(list(doc)[n0:], out, version)


def classify_batch(pairs, version: int = 2, batch_size: int = 512):
    """pairs: list of (prefix, continuation). Batched spaCy; same rules as classify()."""
    pre_len = {}
    uniq = sorted({p.rstrip() for p, _ in pairs})
    for p, d in zip(uniq, nlp().pipe(uniq, batch_size=batch_size)):
        pre_len[p] = len(d)
    texts, idx, res = [], [], [None] * len(pairs)
    for k, (p, c) in enumerate(pairs):
        cs = c.strip()
        out = {"comma": cs.startswith(","), "first": cs.split()[0] if cs.split() else ""}
        if not cs:
            res[k] = {**out, "cls": "AMBIG", "gp_style": False}
        elif cs[0] in ",.;:!?—-)\"'":
            res[k] = {**out, "cls": "INTR", "gp_style": False}
        else:
            texts.append(p.rstrip() + " " + cs)
            idx.append((k, pre_len[p.rstrip()], out))
    for (k, n0, out), d in zip(idx, nlp().pipe(texts, batch_size=batch_size)):
        res[k] = _decide(list(d)[n0:], out, version)
    return res


def _np_end(toks, i):
    seen_noun = False
    j = i
    while j < len(toks) and toks[j].tag_ in NP_TAGS:
        if seen_noun and toks[j].tag_ in {"VBN", "VBG", "DT", "PDT", "PRP$"}:
            break
        seen_noun = seen_noun or toks[j].tag_.startswith("NN")
        j += 1
    return j


def _decide(toks, out, version):
    if not toks:
        return {**out, "cls": "AMBIG", "gp_style": False}
    t0 = toks[0]
    w0 = t0.text.lower()
    if w0 in OBJ_PRON:
        return {**out, "cls": "TRANS", "gp_style": False}
    if w0 in SUBJ_PRON:  # 'While she washed he left' : new clause subject, no comma
        return {**out, "cls": "INTR", "gp_style": True}
    if t0.tag_ in {"CC"}:
        return {**out, "cls": "AMBIG", "gp_style": False}
    if t0.tag_ in {"IN", "RB", "RBR", "TO", "WRB"} and w0 not in {"that"}:
        return {**out, "cls": "INTR", "gp_style": False}
    if t0.tag_ == "RP":  # particle: 'washed up the dishes' / 'washed up'
        toks = toks[1:]
        if not toks or toks[0].tag_ not in NP_TAGS | {"PRP"}:
            return {**out, "cls": "INTR", "gp_style": False}
    # NP scan
    i = 0
    if toks[0].tag_ == "PRP":  # it / you
        i = 1
    else:
        seen_noun = False
        while i < len(toks) and toks[i].tag_ in NP_TAGS:
            if seen_noun and toks[i].tag_ in {"VBN", "VBG"}:
                break  # after the head noun a participle-tagged word is the main verb (tagger GP error)
            if seen_noun and toks[i].tag_ in {"DT", "PDT", "PRP$"}:
                break  # a new determiner after the head noun starts a second NP: the first was the object
            seen_noun = seen_noun or toks[i].tag_.startswith("NN")
            i += 1
        if i == 0:
            return {**out, "cls": "AMBIG", "gp_style": False}
    if i >= len(toks):
        return {**out, "cls": "TRANS", "gp_style": False}  # object then end of string
    nxt = toks[i]
    if nxt.tag_ in FINITE or nxt.tag_ == "VBN":
        return {**out, "cls": "INTR", "gp_style": True}
    if version >= 2 and nxt.tag_ == "CC" and i + 1 < len(toks):
        a = toks[i + 1]
        if a.tag_.startswith("VB"):          # 'washed the dishes and left' : VP coordination
            return {**out, "cls": "TRANS", "gp_style": False}
        if a.tag_ in NP_TAGS or a.tag_ == "PRP":  # 'the baby and the dog cried' vs 'the cups and the plates.'
            j = _np_end(toks, i + 1 + (1 if a.tag_ == "PRP" else 0)) if a.tag_ != "PRP" else i + 2
            if j < len(toks) and (toks[j].tag_ in FINITE or toks[j].tag_ == "VBN"):
                return {**out, "cls": "INTR", "gp_style": True}
            return {**out, "cls": "TRANS", "gp_style": False}
    if nxt.tag_ in {"WDT", "WP", "CC", "VBG"} or nxt.text.lower() == "that":
        return {**out, "cls": "AMBIG", "gp_style": False}
    if nxt.tag_ == "RB" and i + 1 < len(toks) and toks[i + 1].tag_ in FINITE:  # 'the baby suddenly cried'
        return {**out, "cls": "INTR", "gp_style": True}
    return {**out, "cls": "TRANS", "gp_style": False}
