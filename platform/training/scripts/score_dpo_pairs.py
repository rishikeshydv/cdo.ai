import argparse
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def safe_json_loads(text: str) -> Optional[Dict[str, Any]]:
    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return obj
    except Exception:
        return None
    return None


def extract_between(text: str, start_tag: str, end_tag: Optional[str]) -> str:
    start = text.find(start_tag)
    if start < 0:
        return ""
    start += len(start_tag)
    if end_tag is None:
        return text[start:].strip()
    end = text.find(end_tag, start)
    if end < 0:
        return ""
    return text[start:end].strip()


def parse_prompt_context(prompt: str) -> Dict[str, Any]:
    bucket_match = re.search(r"<BUCKET=([ABC])>", prompt)
    bucket = bucket_match.group(1) if bucket_match else ""

    ui_raw = extract_between(prompt, "<UI_INTENT>", "<CDO_BRIEF>")
    brief_raw = extract_between(prompt, "<CDO_BRIEF>", "<SELECTED_STRATEGY>")
    selected_raw = extract_between(prompt, "<SELECTED_STRATEGY>", "<TASK>")
    task_raw = extract_between(prompt, "<TASK>", None)

    ui = safe_json_loads(ui_raw) or {}
    selected = safe_json_loads(selected_raw) or {}

    target_file_match = re.search(r"<TARGET_FILE>([^<]+)</TARGET_FILE>", prompt)
    target_file = target_file_match.group(1).strip() if target_file_match else ""

    return {
        "bucket": bucket,
        "has_ui_intent": bool(ui_raw),
        "has_cdo_brief": bool(brief_raw),
        "has_selected_strategy": bool(selected_raw),
        "has_task": bool(task_raw),
        "ui_intent": ui,
        "selected_strategy": selected,
        "task": task_raw,
        "target_file": target_file,
    }


def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z_][a-zA-Z0-9_\-]*", text.lower())


def jaccard_distance(a: str, b: str) -> float:
    ta, tb = set(tokenize(a)), set(tokenize(b))
    if not ta and not tb:
        return 0.0
    union = ta | tb
    inter = ta & tb
    if not union:
        return 0.0
    sim = len(inter) / len(union)
    return 1.0 - sim


def check_syntax_balance(text: str) -> float:
    pairs = [("(", ")"), ("{", "}"), ("[", "]")]
    score = 1.0
    for l, r in pairs:
        if text.count(l) != text.count(r):
            score -= 0.34
    return max(0.0, score)


def check_class_attr_regression(text: str) -> float:
    # class= in TSX is typically a regression from className=
    bad = len(re.findall(r"\bclass=", text))
    return 1.0 if bad == 0 else 0.0


def strategy_keyword_alignment(content: str, selected_strategy: Dict[str, Any], task: str) -> float:
    keys: List[str] = []
    for k in ["strategy_id", "intent", "hero_focus"]:
        v = selected_strategy.get(k)
        if isinstance(v, str):
            keys.extend(tokenize(v.replace("_", " ")))

    info_order = selected_strategy.get("information_order", [])
    if isinstance(info_order, list):
        for item in info_order:
            if isinstance(item, str):
                keys.extend(tokenize(item.replace("_", " ")))

    keys.extend(tokenize(task))
    keyset = {k for k in keys if len(k) > 2}
    if not keyset:
        return 0.5

    content_tokens = set(tokenize(content))
    overlap = len(content_tokens & keyset)
    return min(1.0, overlap / max(8, min(40, len(keyset))))


def policy_checks(content: str, ui_intent: Dict[str, Any]) -> Dict[str, float]:
    motion = str(ui_intent.get("motion_policy", "")).lower()
    creative = str(ui_intent.get("creative_license", "")).lower()
    cta = ui_intent.get("cta_policy", {}) if isinstance(ui_intent.get("cta_policy", {}), dict) else {}
    cta_timing = str(cta.get("timing", "")).lower()

    first_chunk = content[:800].lower()
    full = content.lower()

    motion_ok = 1.0
    if motion == "none":
        if any(tok in full for tok in ["animate-", "transition", "motion", "framer-motion"]):
            motion_ok = 0.0

    creative_ok = 1.0
    if creative == "none":
        if any(tok in full for tok in ["gradient", "blur", "backdrop-blur"]):
            creative_ok = 0.0

    cta_ok = 1.0
    if cta_timing in {"delayed", "progressive"}:
        if any(tok in first_chunk for tok in ["get started", "book", "start", "sign up", "request demo", "contact us"]):
            cta_ok = 0.0

    return {
        "motion_policy_compliance": motion_ok,
        "creative_policy_compliance": creative_ok,
        "cta_timing_compliance": cta_ok,
        "policy_compliance": (motion_ok + creative_ok + cta_ok) / 3.0,
    }


def modularity_proxy(content: str, target_path: str) -> float:
    lines = len(content.splitlines())
    if target_path.endswith("/page.tsx"):
        if lines <= 220:
            return 1.0
        if lines <= 320:
            return 0.7
        if lines <= 420:
            return 0.4
        return 0.0
    # component files
    if lines <= 160:
        return 1.0
    if lines <= 260:
        return 0.7
    return 0.2


def issue_resolution_rate(content: str, issues: List[str]) -> float:
    if not issues:
        return 1.0

    resolved = 0
    for issue in issues:
        if issue == "missing_import":
            if re.search(r"^\s*import\s+", content, flags=re.MULTILINE):
                resolved += 1
        elif issue == "jsx_attr_regression":
            if "class=" not in content:
                resolved += 1
        elif issue == "missing_closer":
            if check_syntax_balance(content) >= 1.0:
                resolved += 1
        elif issue == "truncated_tail":
            if content.strip().endswith("}") or content.strip().endswith("};"):
                resolved += 1
        else:
            # Unknown issue type: do not fail hard.
            resolved += 0

    return resolved / max(1, len(issues))


@dataclass
class SideEval:
    total: float
    pqpt: Dict[str, float]
    checks: Dict[str, float]
    critical_failures: List[str]


def eval_side(
    text_blob: str,
    prompt_ctx: Dict[str, Any],
    issues: List[str],
    spec: Dict[str, Any],
) -> SideEval:
    obj = safe_json_loads(text_blob)
    checks: Dict[str, float] = {}

    checks["json_valid"] = 1.0 if obj else 0.0

    path = ""
    content = ""
    if obj:
        path = str(obj.get("path", ""))
        content = str(obj.get("content", ""))

    target_path = prompt_ctx.get("target_file", "")
    checks["target_path_match"] = 1.0 if target_path and path == target_path else 0.0
    checks["non_empty_content"] = 1.0 if content.strip() else 0.0
    checks["syntax_balance"] = check_syntax_balance(content)
    checks["class_attr_regression_absent"] = check_class_attr_regression(content)

    checks.update(policy_checks(content, prompt_ctx.get("ui_intent", {})))

    checks["strategy_keyword_alignment"] = strategy_keyword_alignment(
        content,
        prompt_ctx.get("selected_strategy", {}),
        prompt_ctx.get("task", ""),
    )
    checks["modularity_proxy"] = modularity_proxy(content, target_path)
    checks["issue_resolution_rate"] = issue_resolution_rate(content, issues)

    # Build PQPT dimensions from spec.
    dim_scores: Dict[str, float] = {}
    total = 0.0
    total_w = 0.0

    dimensions = spec["pqpt"]["dimensions"]
    for dim_name, dim_cfg in dimensions.items():
        criteria = dim_cfg["criteria"]
        vals = [checks.get(c, 0.0) for c in criteria]
        dim_score = sum(vals) / max(1, len(vals))
        dim_scores[dim_name] = round(dim_score, 4)

        w = float(dim_cfg["weight"])
        total += dim_score * w
        total_w += w

    total = total / total_w if total_w > 0 else 0.0

    critical_failures: List[str] = []
    for c in spec.get("critical_checks", []):
        if checks.get(c, 0.0) < 1.0:
            critical_failures.append(c)

    return SideEval(
        total=round(total, 4),
        pqpt=dim_scores,
        checks={k: round(v, 4) for k, v in checks.items()},
        critical_failures=critical_failures,
    )


def build_h_signals(
    chosen_eval: SideEval,
    rejected_eval: SideEval,
    prompt_ctx: Dict[str, Any],
    chosen_text: str,
    rejected_text: str,
) -> Dict[str, float]:
    margin = chosen_eval.total - rejected_eval.total
    strategic_delta = (
        chosen_eval.pqpt.get("strategic_coherence", 0.0)
        - rejected_eval.pqpt.get("strategic_coherence", 0.0)
    )
    policy_delta = (
        chosen_eval.checks.get("policy_compliance", 0.0)
        - rejected_eval.checks.get("policy_compliance", 0.0)
    )
    distance = jaccard_distance(chosen_text, rejected_text)

    has_context = all(
        [
            prompt_ctx.get("has_ui_intent", False),
            prompt_ctx.get("has_cdo_brief", False),
            prompt_ctx.get("has_selected_strategy", False),
            prompt_ctx.get("has_task", False),
        ]
    )

    issue_delta = (
        chosen_eval.checks.get("issue_resolution_rate", 0.0)
        - rejected_eval.checks.get("issue_resolution_rate", 0.0)
    )
    prod_delta = (
        chosen_eval.pqpt.get("production_readiness", 0.0)
        - rejected_eval.pqpt.get("production_readiness", 0.0)
    )

    h1 = max(0.0, min(1.0, margin / 0.35))
    h2 = max(0.0, min(1.0, (strategic_delta + policy_delta) / 2.0 + 0.5))
    h3 = 1.0 if (distance >= 0.04 and prompt_ctx.get("selected_strategy", {}).get("strategy_id")) else 0.0
    h4 = 1.0 if has_context else 0.0
    h5 = max(0.0, min(1.0, 0.5 + (issue_delta + prod_delta) / 2.0))

    return {
        "h1_preference_strength": round(h1, 4),
        "h2_business_alignment_delta": round(h2, 4),
        "h3_distinctness_signal": round(h3, 4),
        "h4_explainability_context": round(h4, 4),
        "h5_time_to_acceptable_proxy": round(h5, 4),
        "pair_margin": round(margin, 4),
        "chosen_rejected_distance": round(distance, 4),
    }


def evaluate_pair(row: Dict[str, Any], spec: Dict[str, Any]) -> Dict[str, Any]:
    prompt = str(row.get("prompt", ""))
    chosen = str(row.get("chosen", ""))
    rejected = str(row.get("rejected", ""))
    issues = row.get("issues", [])
    if not isinstance(issues, list):
        issues = []

    prompt_ctx = parse_prompt_context(prompt)

    chosen_eval = eval_side(chosen, prompt_ctx, issues, spec)
    rejected_eval = eval_side(rejected, prompt_ctx, issues, spec)

    h = build_h_signals(chosen_eval, rejected_eval, prompt_ctx, chosen, rejected)
    pair_kind = str(row.get("kind", ""))

    hypothesis_applicability = {
        "H1": True,
        "H2": True,
        "H3": pair_kind != "repair_preference",
        "H4": True,
        "H5": True,
    }

    gates = spec["gates"]
    gate_pass = True
    reasons: List[str] = []

    if chosen_eval.total < gates["min_chosen_total"]:
        gate_pass = False
        reasons.append("LOW_CHOSEN_TOTAL")

    if h["pair_margin"] < gates["min_margin"]:
        gate_pass = False
        reasons.append("LOW_MARGIN")

    if len(chosen_eval.critical_failures) > gates["max_chosen_critical_failures"]:
        gate_pass = False
        reasons.append("CHOSEN_CRITICAL_FAILURE")

    if gates.get("require_h4_context", False) and h["h4_explainability_context"] < 1.0:
        gate_pass = False
        reasons.append("MISSING_EXPLAINABILITY_CONTEXT")

    if gates.get("require_issue_resolution_gain", False):
        issue_delta = (
            chosen_eval.checks.get("issue_resolution_rate", 0.0)
            - rejected_eval.checks.get("issue_resolution_rate", 0.0)
        )
        if issue_delta <= 0:
            gate_pass = False
            reasons.append("NO_ISSUE_RESOLUTION_GAIN")

    out = {
        "id": row.get("id"),
        "project": row.get("project"),
        "bucket": row.get("bucket"),
        "system": row.get("system"),
        "prompt": prompt,
        "chosen": chosen,
        "rejected": rejected,
        "rubric": {
            "rubric_version": spec.get("rubric_version", "dpo_rubric_v1"),
            "chosen_total": chosen_eval.total,
            "rejected_total": rejected_eval.total,
            "pair_margin": h["pair_margin"],
            "pqpt": {
                "chosen": chosen_eval.pqpt,
                "rejected": rejected_eval.pqpt,
            },
            "checks": {
                "chosen": chosen_eval.checks,
                "rejected": rejected_eval.checks,
            },
            "critical_failures": {
                "chosen": chosen_eval.critical_failures,
                "rejected": rejected_eval.critical_failures,
            },
            "hypotheses": h,
            "hypothesis_applicability": hypothesis_applicability,
            "gate_pass": gate_pass,
            "gate_fail_reasons": reasons,
        },
    }

    return out


def summary(rows: List[Dict[str, Any]]) -> None:
    total = len(rows)
    kept = [r for r in rows if r["rubric"]["gate_pass"]]

    print("=== DPO RUBRIC SUMMARY ===")
    print(f"pairs_total: {total}")
    print(f"pairs_kept:  {len(kept)}")
    print(f"pairs_drop:  {total - len(kept)}")

    fail_counts = defaultdict(int)
    for r in rows:
        for reason in r["rubric"].get("gate_fail_reasons", []):
            fail_counts[reason] += 1

    if fail_counts:
        print("\nTop fail reasons:")
        for k, v in sorted(fail_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {k}: {v}")

    def avg_signal(name: str) -> float:
        vals = [r["rubric"]["hypotheses"].get(name, 0.0) for r in rows]
        return sum(vals) / max(1, len(vals))

    print("\nHypothesis signal averages:")
    for name in [
        "h1_preference_strength",
        "h2_business_alignment_delta",
        "h3_distinctness_signal",
        "h4_explainability_context",
        "h5_time_to_acceptable_proxy",
    ]:
        print(f"  {name}: {avg_signal(name):.4f}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Input DPO seed pairs JSONL")
    ap.add_argument("--spec", required=True, help="Rubric spec JSON")
    ap.add_argument("--out_scored", required=True, help="All pairs with rubric metadata")
    ap.add_argument("--out_trainable", required=True, help="Gate-passing DPO pairs only")
    args = ap.parse_args()

    input_path = Path(args.input).resolve()
    spec_path = Path(args.spec).resolve()
    out_scored = Path(args.out_scored).resolve()
    out_trainable = Path(args.out_trainable).resolve()

    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    rows = read_jsonl(input_path)

    scored = [evaluate_pair(r, spec) for r in rows]
    trainable = [r for r in scored if r["rubric"]["gate_pass"]]

    write_jsonl(out_scored, scored)
    write_jsonl(out_trainable, trainable)

    summary(scored)
    print("\nOutput files:")
    print(f"  scored:    {out_scored}")
    print(f"  trainable: {out_trainable}")


if __name__ == "__main__":
    main()
