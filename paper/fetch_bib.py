"""Replace refs.bib entries with official BibTeX: ACL Anthology (.bib), arXiv (/bibtex/<id>), Crossref (DOI).

Each fetched entry is renamed to our citation key and checked against the expected title; mismatches are
"""
import difflib
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = {
    # key: (kind, id, expected title)
    "amouyal2025": ("acl", "2025.acl-long.403", "When the LM misunderstood the human chuckled"),
    "amouyal2026": ("acl", "2026.acl-long.1040", "Comparing human and language models sentence processing difficulties on complex structures"),
    "yoshida2026": ("acl", "2026.acl-long.1694", "An Existence Proof for Neural Language Models That Can Explain Garden-Path Effects via Surprisal"),
    "jumelet2024": ("acl", "2024.findings-acl.877", "Do Language Models Exhibit Human-like Structural Priming Effects"),
    "zhou2025icl": ("acl", "2025.naacl-long.586", "Is In-Context Learning a Type of Error-Driven Learning"),
    "hanna2025": ("acl", "2025.naacl-long.164", "Incremental Sentence Processing Mechanisms in Autoregressive Transformer Language Models"),
    "michaelov2023": ("acl", "2023.emnlp-main.227", "Structural Priming Demonstrates Abstract Grammatical Representations in Multilingual Language Models"),
    "vanschijndel2018": ("acl", "D18-1499", "A Neural Model of Adaptation in Reading"),
    "sinclair2022": ("acl", "2022.tacl-1.60", "Structural Persistence in Language Models"),
    "futrell2019": ("acl", "N19-1004", "Neural language models as psycholinguistic subjects"),
    "arehalli2022": ("acl", "2022.conll-1.20", "Syntactic Surprisal From Neural Models Predicts, But Underestimates"),
    "gauthier2020": ("acl", "2020.acl-demos.10", "SyntaxGym"),
    "schuster2022": ("acl", "2022.naacl-main.71", "When a sentence does not introduce a discourse entity"),
    "prasad2019": ("acl", "K19-1007", "Using Priming to Uncover the Organization of Syntactic Representations"),
    "kamoi2024": ("acl", "2024.tacl-1.78", "When Can LLMs Actually Correct Their Own Mistakes"),
    "li2024incremental": ("arxiv", "2405.16042", "Incremental Comprehension of Garden-Path Sentences by Large Language Models"),
    "pucci2026": ("arxiv", "2609.04484", "Patterns of Priming in Production"),
    "timkey2026": ("arxiv", "2605.15440", "Why are language models less surprised than humans"),
    "yang2025retraction": ("arxiv", "2505.16170", "When Do LLMs Admit Their Mistakes"),
    "prakash2026": ("arxiv", "2505.14685", "Language Models use Lookbacks to Track Beliefs"),
    "touvron2023llama": ("arxiv", "2307.09288", "Llama 2: Open Foundation and Fine-Tuned Chat Models"),
    "grattafiori2024llama": ("arxiv", "2407.21783", "The Llama 3 Herd of Models"),
    "jiang2023mistral": ("arxiv", "2310.06825", "Mistral 7B"),
    "gemma2024gemma2": ("arxiv", "2408.00118", "Gemma 2: Improving Open Language Models at a Practical Size"),
    "gemma2025gemma3": ("arxiv", "2503.19786", "Gemma 3 Technical Report"),
    "qwen2024qwen25": ("arxiv", "2412.15115", "Qwen2.5 Technical Report"),
    "yang2025qwen3": ("arxiv", "2505.09388", "Qwen3 Technical Report"),
    "biderman2023pythia": ("arxiv", "2304.01373", "Pythia: A Suite for Analyzing Large Language Models Across Training and Scaling"),
    "zhang2024patching": ("arxiv", "2309.16042", "Towards Best Practices of Activation Patching in Language Models"),
    "meng2022locating": ("arxiv", "2202.05262", "Locating and Editing Factual Associations in GPT"),
    "vig2020causal": ("arxiv", "2004.12265", "Causal Mediation Analysis for Interpreting Neural NLP"),
    "vangompel2006": ("doi", "10.1016/j.jml.2006.06.004", "The activation of inappropriate analyses in garden-path sentences"),
    "christianson2001": ("doi", "10.1006/cogp.2001.0752", "Thematic Roles Assigned along the Garden Path Linger"),
    "slattery2013": ("doi", "10.1016/j.jml.2013.04.001", "Lingering misinterpretations of garden path sentences arise from competing syntactic representations"),
    "huang2024": ("doi", "10.1016/j.jml.2024.104510", "Large-scale benchmark yields no evidence that language model surprisal explains syntactic disambiguation difficulty"),
    "pickering1998": ("doi", "10.1006/jmla.1998.2592", "The Representation of Verbs: Evidence from Syntactic Priming in Language Production"),
    "chang2006": ("doi", "10.1037/0033-295X.113.2.234", "Becoming syntactic"),
    "jaeger2013": ("doi", "10.1016/j.cognition.2012.10.013", "Alignment as a consequence of expectation adaptation"),
    "fine2013": ("doi", "10.1371/journal.pone.0077661", "Rapid Expectation Adaptation during Syntactic Comprehension"),
    "fujita2020": ("doi", "10.1017/S0142716420000351", "Lingering misinterpretation in native and nonnative sentence processing"),
    "tabor2004": ("doi", "10.1016/j.jml.2004.01.001", "Effects of merely local syntactic coherence on sentence processing"),
    "dersimonian1986": ("doi", "10.1016/0197-2456(86)90046-2", "Meta-analysis in clinical trials"),
    "frazier1982": ("doi", "10.1016/0010-0285(82)90008-1", "Making and correcting errors during sentence comprehension"),
    "sturt1996": ("doi", "10.1080/016909696387123", "Monotonic Syntactic Processing: A Cross-linguistic Study of Attachment and Reanalysis"),
    "vanschijndel2021": ("doi", "10.1111/cogs.12988", "Single-Stage Prediction Models Do Not Explain the Magnitude of Syntactic Disambiguation Difficulty"),
    "ferreira2003": ("doi", "10.1016/S0010-0285(03)00005-7", "The misinterpretation of noncanonical sentences"),
    "harringtonstack2018": ("doi", "10.3758/s13421-018-0808-6", "A failure to replicate rapid syntactic adaptation in comprehension"),
    "prasad2021": ("doi", "10.1037/xlm0001046", "Rapid syntactic adaptation in self-paced reading"),
    "reitter2011": ("doi", "10.1111/j.1551-6709.2010.01165.x", "A Computational Cognitive Model of Syntactic Priming"),
    "hartsuiker2008": ("doi", "10.1016/j.jml.2007.07.003", "Syntactic priming persists while the lexical boost decays"),
    "bock1986": ("doi", "10.1016/0010-0285(86)90004-6", "Syntactic persistence in language production"),
    "cehakova2025": ("doi", "10.1080/0163853X.2025.2513210", "Beyond initial misanalysis"),
    "kwon2023vllm": ("doi", "10.1145/3600006.3613165", "Efficient Memory Management for Large Language Model Serving with PagedAttention"),
}


def get(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=60).stdout


def fetch(kind, ident):
    if kind == "acl":
        return get(["curl", "-sL", f"https://aclanthology.org/{ident}.bib"])
    if kind == "arxiv":
        return get(["curl", "-sL", f"https://arxiv.org/bibtex/{ident}"])
    return get(["curl", "-sL", "-H", "Accept: application/x-bibtex", f"https://doi.org/{ident}"])


def title_of(bib):
    m = re.search(r"\btitle\s*=\s*", bib, re.I)
    if not m:
        return ""
    i = m.end()
    if bib[i] == '"':
        j = bib.index('"', i + 1)
        return re.sub(r"[{}\\]", "", bib[i + 1:j])
    depth, j = 0, i
    for j in range(i, len(bib)):
        depth += {"{": 1, "}": -1}.get(bib[j], 0)
        if depth == 0:
            break
    return re.sub(r"[{}\\]", "", bib[i + 1:j])


PROPER = ['Mistral', 'Llama', 'Gemma', 'Qwen', 'Qwen2.5', 'Qwen3', 'Pythia', 'GPT', 'Transformer', 'Transformers', 'English', 'SyntaxGym', 'PagedAttention', 'LLMs', 'LLM', 'LM', 'LMs', 'NLP', 'RNN', 'ACT-R']


def protect_title(bib):
    def fix(m):
        head, val, tail = m.group(1), m.group(2), m.group(3)

        def word(w):
            core = w.group(0)
            if core.startswith("{"):
                return core
            if core in PROPER or re.search(r"[A-Z].*[A-Z0-9]|[0-9][A-Z]", core[1:]) or re.search(r"[0-9][A-Z]", core):
                return "{" + core + "}"
            return core
        return head + re.sub(r"\{[^{}]*\}|[A-Za-z0-9.\-]+", word, val) + tail
    return re.sub(r"(\btitle\s*=\s*[{\"])(.*?)([}\"]\s*,\s*\n)", fix, bib, flags=re.S | re.I)


def clean(bib):
    """Crossref returns HTML entities and long month names that BibTeX/LaTeX do not accept."""
    bib = bib.replace("&amp;", "\\&").replace("&lt;", "<").replace("&gt;", ">")
    bib = re.sub(r"month\s*=\s*(\w+)", lambda m: "month = " + {"july": "jul", "june": "jun", "sept": "sep"}.get(m.group(1).lower(), m.group(1)), bib)
    return bib


def pretty(bib):
    if "\n" in bib.strip():
        return bib
    return re.sub(r",\s*(\w+)=", r",\n  \1 = ", bib).replace("}}", "}\n}") if bib.endswith("}}") else re.sub(r",\s*(\w+)=", r",\n  \1 = ", bib)


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower())


def blocks(text):
    out, cur = {}, None
    for line in text.splitlines(keepends=True):
        m = re.match(r"@\w+\{([^,]+),", line)
        if m:
            cur = m.group(1).strip()
            out[cur] = line
        elif cur:
            out[cur] += line
    return out


def main():
    old = blocks((HERE / "refs.bib").read_text())
    new, bad = {}, []
    for key, (kind, ident, exp) in SRC.items():
        bib = fetch(kind, ident).strip()
        time.sleep(0.5)
        if not bib.startswith("@"):
            bad.append((key, "no bibtex returned"))
            continue
        bib = re.sub(r"^(@\w+\{)[^,]+,", lambda m: m.group(1) + key + ",", bib, count=1)
        t = title_of(bib + "\n")
        ratio = difflib.SequenceMatcher(None, norm(exp), norm(t)[: len(norm(exp)) + 10]).ratio()
        if norm(exp) in norm(t):
            ratio = 1.0
        if ratio < 0.8:
            bad.append((key, f"title mismatch ({ratio:.2f}): got '{t[:90]}'"))
            continue
        new[key] = protect_title(clean(pretty(bib)) + "\n")
    keep = {k: v for k, v in old.items() if k not in new}
    (HERE / "refs.bib").write_text("% Official BibTeX: ACL Anthology, arXiv and Crossref (fetched by fetch_bib.py).\n"
                                   + "".join(new[k] + "\n" for k in sorted(new))
                                   + "% Entries not fetched (no official source or mismatch); kept from the hand-written file.\n"
                                   + "".join(keep[k] for k in sorted(keep)))
    print(f"official: {len(new)}; kept hand-written: {len(keep)}")
    for k, why in bad:
        print("CHECK", k, why)


if __name__ == "__main__":
    sys.exit(main())
