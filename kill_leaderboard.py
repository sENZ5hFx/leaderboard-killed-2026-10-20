"""Epistemic gate. Not a measurement of nature.

A product of elicited scores is killed when the rows are different kinds,
the PDFs were not hashed, or the noise test crowns the row that was
already maximal on every axis.
"""
from __future__ import annotations
import json

def kill_leaderboard(rows, rank_probs):
    if not rows:
        return {"verdict": "EMPTY", "mint_allowed": False, "score": 0}
    kinds = {r["kind"] for r in rows}
    axes = ("unexplained", "thinness", "sign_ambiguity")
    leader = max(rank_probs, key=rank_probs.get)
    leader_row = next(r for r in rows if r["name"] == leader)
    prior = all(
        max(rows, key=lambda r: r[ax])["name"] == leader
        and all(r[ax] <= leader_row[ax] for r in rows)
        for ax in axes
    )
    reasons = []
    if len(kinds) > 1:
        reasons.append("MIXED_KINDS")
    if not all(r["pdf_hashed"] for r in rows):
        reasons.append("PDF_BYTES_MISSING")
    if any(not r["measured"] for r in rows):
        reasons.append("ELICITATION_NOT_MEASUREMENT")
    if prior:
        reasons.append("PRIOR_RECOVERED")
    if rank_probs[leader] > 0.5 and prior:
        reasons.append("NOISE_TEST_CROWNS_THE_PRIOR")
    return {
        "verdict": "MINTED" if not reasons else "LEADERBOARD_KILLED",
        "mint_allowed": not reasons,
        "score": 0 if reasons else None,
        "leader_under_noise": leader,
        "p_rank1": round(rank_probs[leader], 3),
        "prior_recovered": prior,
        "n_kinds": len(kinds),
        "reasons": reasons,
    }

# Scores below are this session's elicitations. They are not observations.
ROWS = [
    {"name": "deep Critical Zone CSP1-3", "kind": "unknown biological role", "unexplained": 0.90, "thinness": 0.92, "sign_ambiguity": 1.00, "pdf_hashed": False, "measured": False},
    {"name": "Arctic root-thaw front", "kind": "sign of a carbon feedback", "unexplained": 0.80, "thinness": 0.72, "sign_ambiguity": 1.00, "pdf_hashed": False, "measured": False},
    {"name": "twilight-zone transfer", "kind": "share of model disagreement", "unexplained": 0.83, "thinness": 0.75, "sign_ambiguity": 0.85, "pdf_hashed": False, "measured": False},
    {"name": "gut muco-microbiotic layer", "kind": "clinical causation gap", "unexplained": 0.75, "thinness": 0.82, "sign_ambiguity": 0.70, "pdf_hashed": False, "measured": False},
    {"name": "hot-Jupiter terminator limb", "kind": "retrieval degeneracy", "unexplained": 0.72, "thinness": 0.65, "sign_ambiguity": 0.80, "pdf_hashed": False, "measured": False},
    {"name": "marine-snow viscosity", "kind": "lab structure, global mix unread", "unexplained": 0.70, "thinness": 0.90, "sign_ambiguity": 0.35, "pdf_hashed": False, "measured": False},
    {"name": "avian nutrient transport", "kind": "review phosphorus flux", "unexplained": 0.55, "thinness": 0.60, "sign_ambiguity": 0.40, "pdf_hashed": False, "measured": False},
    {"name": "whale conveyor", "kind": "local nitrogen subsidy", "unexplained": 0.25, "thinness": 0.50, "sign_ambiguity": 0.30, "pdf_hashed": False, "measured": False},
]
PROBS = {
    "deep Critical Zone CSP1-3": 0.792,
    "Arctic root-thaw front": 0.103,
    "twilight-zone transfer": 0.080,
    "gut muco-microbiotic layer": 0.019,
    "hot-Jupiter terminator limb": 0.006,
    "marine-snow viscosity": 0.000,
    "avian nutrient transport": 0.000,
    "whale conveyor": 0.000,
}

if __name__ == "__main__":
    print(json.dumps(kill_leaderboard(ROWS, PROBS), indent=2))
