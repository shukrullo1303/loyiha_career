from typing import Any, Dict


def score_assessment(answers: Dict[str, Any], scoring_rules: Dict[str, Any]) -> Dict[str, float]:
    """
    Generic scoring engine.

    answers: {"q1": 2, "q2": 5, ...}
    scoring_rules: {
      "scales": {
        "HUMAN": {"items": {"q1": +1, "q5": -1}, "range": [0, 20]},
        "INFO":  {"items": {"q2": +1, "q7": +1}}
      }
    }
    """
    out: Dict[str, float] = {}
    for scale, rule in scoring_rules.get("scales", {}).items():
        total = 0.0
        for qid, weight in rule.get("items", {}).items():
            value = answers.get(qid, 0)
            try:
                total += float(value) * float(weight)
            except (TypeError, ValueError):
                continue
        out[scale] = total
    return out

