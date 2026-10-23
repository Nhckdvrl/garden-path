"""E015 items: overridden statements (see README). Deterministic (seed 0).

Every context starts with a short label and a colon, so that the overridden statement S(E,A) is always
preceded by a space and tokenizes identically in CORR, PRE, CTRL and the CTRL donor.
Output: data/gp_behavior/derived/e015_items_v1.jsonl
"""
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "data/gp_behavior/derived/e015_items_v1.jsonl"

FRAMES = [
    ("The {e} is on {v}.", "To confirm, the {e} is on", ["meeting", "party", "exam", "interview", "dinner"],
     ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]),
    ("The {e} are in the {v}.", "To confirm, the {e} are in the", ["keys", "tickets", "documents", "glasses", "chargers"],
     ["kitchen", "garage", "office", "bedroom", "car", "basement"]),
    ("{e} lives in {v}.", "To confirm, {e} lives in", ["Anna", "Peter", "Maria", "David", "Laura"],
     ["Paris", "Berlin", "Madrid", "Rome", "Vienna", "Lisbon"]),
    ("The {e} starts at {v}.", "To confirm, the {e} starts at", ["concert", "lecture", "game", "show", "class"],
     ["five", "six", "seven", "eight", "nine", "ten"]),
    ("{e}'s favorite color is {v}.", "To confirm, {e}'s favorite color is", ["Tom", "Lisa", "Mark", "Sarah", "Ben"],
     ["red", "blue", "green", "yellow", "purple", "orange"]),
    ("The {e} is due in {v}.", "To confirm, the {e} is due in", ["report", "thesis", "essay", "proposal", "invoice"],
     ["March", "April", "May", "June", "July", "August"]),
    ("The {e} works as a {v}.", "To confirm, the {e} works as a", ["neighbor", "cousin", "landlord", "uncle", "tenant"],
     ["teacher", "nurse", "lawyer", "baker", "pilot", "farmer"]),
    ("The {e} is made of {v}.", "To confirm, the {e} is made of", ["table", "statue", "bridge", "box", "frame"],
     ["wood", "steel", "glass", "stone", "plastic", "copper"]),
    ("{e} plays the {v}.", "To confirm, {e} plays the", ["Emma", "Jack", "Olivia", "Leo", "Mia"],
     ["piano", "guitar", "violin", "drums", "flute", "cello"]),
    ("The {e} speaks {v}.", "To confirm, the {e} speaks", ["guide", "driver", "host", "clerk", "chef"],
     ["French", "German", "Spanish", "Italian", "Dutch", "Greek"]),
]


def main():
    rng = random.Random(0)
    items = []
    for fi, (stmt, probe, ents, vals) in enumerate(FRAMES):
        for e in ents:
            other = rng.choice([x for x in ents if x != e])
            for _ in range(2):
                a, b = rng.sample(vals, 2)
                for A, B in ((a, b), (b, a)):  # counterbalanced
                    S = lambda ent, v: stmt.format(e=ent, v=v)  # noqa: E731
                    items.append({
                        "id": f"f{fi}_{e}_{A}_{B}", "frame": fi, "entity": e, "distractor": other, "A": A, "B": B,
                        "claim_A": S(e, A), "claim_A_other": S(other, A), "claim_B": S(e, B),
                        "CORR": f"Note: {S(e, A)} Correction: {S(e, B)}",
                        "PRE": f"Mistake: {S(e, A)} Correction: {S(e, B)}",
                        "CTRL": f"Note: {S(other, A)} Also: {S(e, B)}",
                        "CTRL_PRE": f"Mistake: {S(other, A)} Also: {S(e, B)}",
                        "probe": probe.format(e=e)})
    with open(OUT, "w") as fo:
        for it in items:
            fo.write(json.dumps(it) + "\n")
    print(f"wrote {len(items)} items to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
