"""Naturalness rating of PASS_C sentences by Llama-3.1-8B-Instruct (same protocol as E006)."""
import json, importlib.util
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
ROOT = Path(__file__).resolve().parents[3]
J = "NousResearch/Meta-Llama-3.1-8B-Instruct"
Q = ('Rate how natural and grammatical this English sentence is, from 1 (very unnatural or '
     'ungrammatical) to 5 (perfectly natural).\nSentence: "{s}"\nAnswer with a single digit.')
rows = [json.loads(l) for l in open(Path(__file__).with_name("spec.jsonl"))]
rows = [r for r in rows if r["cond"] == "PASS_C"]
tok = AutoTokenizer.from_pretrained(J); tok.padding_side = "left"; tok.pad_token = tok.pad_token or tok.eos_token
m = AutoModelForCausalLM.from_pretrained(J, dtype=torch.bfloat16, device_map="cuda").eval()
ids = [tok.encode(str(d), add_special_tokens=False)[0] for d in range(1, 6)]
out = {}
for i in range(0, len(rows), 32):
    b = rows[i:i + 32]
    ps = [tok.apply_chat_template([{"role": "user", "content": Q.format(s=r["prime"])}], tokenize=False, add_generation_prompt=True) for r in b]
    enc = tok(ps, return_tensors="pt", padding=True, add_special_tokens=False).to("cuda")
    with torch.no_grad():
        p = m(**enc).logits[:, -1, ids].float().softmax(-1).cpu()
    for r, q in zip(b, p):
        out[r["family_id"]] = float((q * torch.arange(1, 6)).sum())
json.dump(out, open(ROOT / "results/gp/E011/passive_naturalness.json", "w"), indent=0)
print(len(out), "rated")
