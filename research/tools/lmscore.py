"""Exact continuation log-probabilities for HuggingFace causal LMs.

score(model, tok, items) where each item is (context, continuation) returns,
for every item, the summed natural-log probability of the continuation's
tokens given BOS + context, computed on the jointly tokenized string (so
tokenization at the context/continuation boundary is the model's natural
one). Tokens are attributed to the continuation if their character span
starts at or after the continuation's first character (a leading space is
part of the continuation).
"""
from __future__ import annotations

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer


def load(model_path: str, device: str = "cuda", dtype=torch.bfloat16):
    try:
        tok = AutoTokenizer.from_pretrained(model_path, use_fast=True)
    except Exception:
        if "pythia" not in model_path:
            raise
        tok = AutoTokenizer.from_pretrained("EleutherAI/pythia-160m", use_fast=True)  # shared tokenizer
    model = AutoModelForCausalLM.from_pretrained(model_path, dtype=dtype, device_map=device)
    model.eval()
    return model, tok


def _bos(tok):
    if tok.bos_token_id is not None:
        return tok.bos_token_id
    return tok.eos_token_id


@torch.no_grad()
def score(model, tok, items, batch_size: int = 64, word_spans=None):
    """items: list of (context, continuation).

    Returns list of dicts {lp, ntok, first_lp}. If word_spans is given (list of
    (char_start, char_end) into context+continuation, or None), also returns
    'span_lp': summed log-prob of tokens whose start falls in that span.
    """
    bos = _bos(tok)
    enc = []
    for k, (ctx, cont) in enumerate(items):
        text = ctx + cont
        e = tok(text, add_special_tokens=False, return_offsets_mapping=True)
        ids = [bos] + e["input_ids"]
        offs = [(-1, -1)] + [tuple(o) for o in e["offset_mapping"]]
        start = len(ctx)
        # first token whose span starts at/after the continuation start; a token that
        # straddles the boundary (merges context end with continuation start) is
        # counted as continuation too, and flagged.
        mask = [o[0] >= start or (o[0] < start < o[1]) for o in offs]
        straddle = any(o[0] < start < o[1] for o in offs)
        span = word_spans[k] if word_spans else None
        smask = [span is not None and span[0] <= o[0] < span[1] for o in offs]
        enc.append((ids, mask, smask, straddle))
    order = sorted(range(len(enc)), key=lambda i: -len(enc[i][0]))
    out = [None] * len(enc)
    dev = model.device
    pad = tok.pad_token_id if tok.pad_token_id is not None else bos
    for b in range(0, len(order), batch_size):
        idx = order[b : b + batch_size]
        L = max(len(enc[i][0]) for i in idx)
        ids = torch.full((len(idx), L), pad, dtype=torch.long)
        att = torch.zeros((len(idx), L), dtype=torch.long)
        for r, i in enumerate(idx):
            s = enc[i][0]
            ids[r, : len(s)] = torch.tensor(s)
            att[r, : len(s)] = 1
        ids, att = ids.to(dev), att.to(dev)
        logits = model(input_ids=ids, attention_mask=att).logits.float()
        lp = F.log_softmax(logits[:, :-1], dim=-1).gather(-1, ids[:, 1:, None])[..., 0].cpu()
        for r, i in enumerate(idx):
            _, mask, smask, straddle = enc[i]
            n = len(mask)
            tl = lp[r, : n - 1]  # logprob of token t+1
            m = torch.tensor(mask[1:n])
            sm = torch.tensor(smask[1:n])
            pos = m.nonzero()[:, 0]
            out[i] = {
                "lp": float(tl[m].sum()),
                "ntok": int(m.sum()),
                "first_lp": float(tl[pos[0]]) if len(pos) else float("nan"),
                "span_lp": float(tl[sm].sum()) if word_spans else None,
                "straddle": straddle,
            }
    return out
