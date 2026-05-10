import argparse
import json
import os
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List

from dotenv import load_dotenv

try:
    from openai import AzureOpenAI
except Exception:
    AzureOpenAI = None  # type: ignore


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_json_if_exists(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def pct(x: float) -> float:
    return round(x * 100.0, 2)


def try_get_job_status(job_id: str, api_version: str) -> str:
    if not job_id or AzureOpenAI is None:
        return "unknown"

    base_dir = Path(__file__).resolve().parent.parent
    load_dotenv(base_dir.parent / ".env.development", override=False)
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    if not api_key or not endpoint:
        return "unknown"

    try:
        client = AzureOpenAI(api_key=api_key, azure_endpoint=endpoint, api_version=api_version)
        job = client.fine_tuning.jobs.retrieve(job_id)
        return str(getattr(job, "status", "unknown"))
    except Exception:
        return "unknown"


def mean_or_zero(vals: List[float]) -> float:
    return float(mean(vals)) if vals else 0.0


def compute_h_metrics(scored_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(scored_rows)
    kept = [r for r in scored_rows if r.get("rubric", {}).get("gate_pass", False)]
    gate_rate = (len(kept) / total) if total else 0.0

    # All-gate means
    def gate_mean(sig: str) -> float:
        return mean_or_zero([float(r["rubric"]["hypotheses"].get(sig, 0.0)) for r in kept])

    # H3 uses applicability filter.
    h3_app = [
        float(r["rubric"]["hypotheses"].get("h3_distinctness_signal", 0.0))
        for r in kept
        if bool(r.get("rubric", {}).get("hypothesis_applicability", {}).get("H3", True))
    ]

    h1 = gate_rate
    h2 = gate_mean("h2_business_alignment_delta")
    h3 = mean_or_zero(h3_app)
    h4 = gate_mean("h4_explainability_context")
    h5 = gate_mean("h5_time_to_acceptable_proxy")

    return {
        "n_total_pairs": total,
        "n_gate_pass": len(kept),
        "gate_pass_rate": round(gate_rate, 4),
        "means": {
            "H1": round(h1, 4),
            "H2": round(h2, 4),
            "H3": round(h3, 4),
            "H4": round(h4, 4),
            "H5": round(h5, 4),
        },
        "h3_applicable_count": len(h3_app),
    }


def build_hypothesis_results(h: Dict[str, Any], phase45: Dict[str, Any]) -> Dict[str, Any]:
    m = h["means"]

    h4_proxy = phase45.get("h4_proxy", {})
    h5_proxy = phase45.get("h5_proxy", {})

    h1_status = "proxy_supported" if m["H1"] >= 0.65 else "proxy_not_met"
    if m["H1"] >= 0.75:
        h1_status = "proxy_supported_strong"

    return {
        "H1": {
            "proposal_target": ">=65% preference vs SFT-only and >=75% vs v0.dev",
            "proxy_metric": "dpo_gate_pass_rate",
            "proxy_value": m["H1"],
            "status": h1_status,
            "notes": "Proxy from rubric-gated pair superiority; blinded external comparison still needed for publication claim.",
        },
        "H2": {
            "proposal_target": ">=60% business-alignment improvement",
            "proxy_metric": "mean_h2_business_alignment_delta_on_gate_pass_rows",
            "proxy_value": m["H2"],
            "status": "proxy_supported" if m["H2"] >= 0.60 else "proxy_not_met",
            "notes": "Derived from rubric business-alignment signal.",
        },
        "H3": {
            "proposal_target": ">=70% meaningfully distinct strategies",
            "proxy_metric": "mean_h3_distinctness_signal_on_applicable_gate_pass_rows",
            "proxy_value": m["H3"],
            "status": "proxy_supported" if m["H3"] >= 0.70 else "proxy_not_met",
            "notes": "Computed on H3-applicable pairs only (repair-preference excluded).",
        },
        "H4": {
            "proposal_target": ">=10% confidence/collaboration improvement",
            "proxy_metric": "phase4_proxy_confidence_collab_improvement",
            "proxy_value": float(h4_proxy.get("improvement", 0.0)),
            "status": "proxy_supported" if bool(h4_proxy.get("pass", False)) else "insufficient_evidence",
            "notes": "Proxy from rationale-present vs no-rationale baseline; replace with human session data in final paper.",
        },
        "H5": {
            "proposal_target": ">=25% time reduction to acceptable design",
            "proxy_metric": "phase5_proxy_time_reduction",
            "proxy_value": float(h5_proxy.get("mean_time_reduction", 0.0)),
            "status": "proxy_supported" if bool(h5_proxy.get("pass", False)) else "insufficient_evidence",
            "notes": "Proxy from expected steps-to-acceptable; validate with real timed tasks.",
        },
    }


def build_methodology_phases(
    dpo_info: Dict[str, Any],
    brand_info: Dict[str, Any],
    dpo_status: str,
    brand_status: str,
    h_results: Dict[str, Any],
    phase45: Dict[str, Any],
    phase5_pack_exists: bool,
) -> List[Dict[str, Any]]:
    dpo_model_id = str(dpo_info.get("dpo_model_id", "")).strip()
    brand_model_id = str(brand_info.get("fine_tuned_model", "")).strip()

    phase3_done = h_results["H2"]["status"] == "proxy_supported" and h_results["H3"]["status"] == "proxy_supported"
    phase4_done = bool(phase45.get("h4_proxy", {}).get("pass", False))
    phase5_done = bool(phase45.get("h5_proxy", {}).get("pass", False)) and phase5_pack_exists

    return [
        {
            "phase": "Phase 1 (Weeks 1–3)",
            "goal": "Context schema, high-quality dataset, and recruit 3–5 designers",
            "status": "in_progress",
            "checks": {
                "context_schema_and_pipeline": True,
                "dataset_built": True,
                "designer_recruitment_evidence_logged": False,
            },
        },
        {
            "phase": "Phase 2 (Weeks 3–6)",
            "goal": "SFT baseline + preference optimization (DPO)",
            "status": "completed" if bool(dpo_model_id) else "in_progress",
            "checks": {
                "sft_completed": True,
                "dpo_completed": bool(dpo_model_id),
                "dpo_job_status": dpo_status,
            },
        },
        {
            "phase": "Phase 3 (Weeks 6–8)",
            "goal": "Strategic context + reasoning diversity tests (H2/H3)",
            "status": "completed_proxy" if phase3_done else "in_progress",
            "checks": {
                "h2_proxy_supported": h_results["H2"]["status"] == "proxy_supported",
                "h3_proxy_supported": h_results["H3"]["status"] == "proxy_supported",
            },
        },
        {
            "phase": "Phase 4 (Weeks 8–10)",
            "goal": "HITL rationale/collaboration loop (H4)",
            "status": "completed_proxy" if phase4_done else "not_started",
            "checks": {
                "phase4_proxy_pass": phase4_done,
                "human_session_data_logged": False,
            },
        },
        {
            "phase": "Phase 5 (Weeks 10–12)",
            "goal": "Blind baseline comparison vs SFT-only and v0.dev (H1/H5)",
            "status": "completed_proxy" if phase5_done else "not_started",
            "checks": {
                "blind_pack_prepared": phase5_pack_exists,
                "phase5_proxy_pass": bool(phase45.get("h5_proxy", {}).get("pass", False)),
                "human_blind_ratings_collected": False,
            },
        },
        {
            "phase": "Phase 6 (Weeks 12–14)",
            "goal": "Publication package + deployment assets",
            "status": "in_progress" if (dpo_model_id or brand_status in {"running", "pending"}) else "not_started",
            "checks": {
                "dpo_checkpoint_ready": bool(dpo_model_id),
                "brand_strategy_model_ready": bool(brand_model_id),
                "paper_tables_and_figures_compiled": False,
            },
        },
    ]


def build_md(summary: Dict[str, Any]) -> str:
    h = summary["hypotheses"]
    phases = summary["methodology_phases"]
    lines: List[str] = []
    lines.append("# AI-CDO Hypothesis and Methodology Status Report")
    lines.append("")
    lines.append("## Hypothesis Results")
    lines.append(
        f"- Pairs: `{h['n_total_pairs']}` total, `{h['n_gate_pass']}` gate-pass ({pct(h['gate_pass_rate'])}%)."
    )
    lines.append("")
    lines.append("| Hypothesis | Target | Current (Proxy) | Status |")
    lines.append("|---|---|---:|---|")
    for label in ["H1", "H2", "H3", "H4", "H5"]:
        row = h["hypothesis_results"][label]
        lines.append(
            f"| {label} | {row['proposal_target']} | {pct(float(row['proxy_value']))}% via `{row['proxy_metric']}` | {row['status']} |"
        )

    lines.append("")
    lines.append("## Methodology Phase Checklist")
    lines.append("")
    for p in phases:
        lines.append(f"### {p['phase']} - `{p['status']}`")
        lines.append(f"- Goal: {p['goal']}")
        for k, v in p.get("checks", {}).items():
            lines.append(f"- Check `{k}`: `{v}`")
        lines.append("")

    lines.append("## Notes")
    lines.append("- Phases 3–5 marked `completed_proxy` are based on automated proxy studies, not human rater studies.")
    lines.append("- For publication-grade claims, replace proxy metrics with blinded human evaluation and timing logs.")
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scored-jsonl", default="platform/training/data/augmented/dpo_pairs_scored_v4.jsonl")
    ap.add_argument("--dpo-info", default="platform/training/dpo_model_info_v2p25.json")
    ap.add_argument("--brand-info", default="platform/training/brand_model_info_v2.json")
    ap.add_argument("--phase45-proxy", default="platform/training/reports/phase45_proxy_study_v4.json")
    ap.add_argument("--phase5-pack", default="platform/training/reports/phase5_blind_pack_v4.json")
    ap.add_argument("--azure-api-version", default="2024-10-21")
    ap.add_argument("--out-json", default="platform/training/reports/hypothesis_methodology_results_v4.json")
    ap.add_argument("--out-md", default="platform/training/reports/hypothesis_methodology_results_v4.md")
    args = ap.parse_args()

    scored = read_jsonl(Path(args.scored_jsonl).resolve())
    dpo_info = load_json_if_exists(Path(args.dpo_info).resolve())
    brand_info = load_json_if_exists(Path(args.brand_info).resolve())
    phase45 = load_json_if_exists(Path(args.phase45_proxy).resolve())
    phase5_pack_exists = Path(args.phase5_pack).resolve().exists()

    dpo_status = try_get_job_status(str(dpo_info.get("job_id", "")), args.azure_api_version)
    brand_status = try_get_job_status(str(brand_info.get("job_id", "")), args.azure_api_version)

    h_metrics = compute_h_metrics(scored)
    h_results = build_hypothesis_results(h_metrics, phase45)

    summary = {
        "artifacts": {
            "scored_jsonl": str(Path(args.scored_jsonl).resolve()),
            "dpo_info": str(Path(args.dpo_info).resolve()),
            "brand_info": str(Path(args.brand_info).resolve()),
            "phase45_proxy": str(Path(args.phase45_proxy).resolve()),
            "phase5_pack": str(Path(args.phase5_pack).resolve()),
        },
        "job_status": {
            "dpo_job_id": str(dpo_info.get("job_id", "")),
            "dpo_status": dpo_status,
            "brand_job_id": str(brand_info.get("job_id", "")),
            "brand_status": brand_status,
        },
        "hypotheses": {
            **h_metrics,
            "hypothesis_results": h_results,
        },
    }

    summary["methodology_phases"] = build_methodology_phases(
        dpo_info=dpo_info,
        brand_info=brand_info,
        dpo_status=dpo_status,
        brand_status=brand_status,
        h_results=h_results,
        phase45=phase45,
        phase5_pack_exists=phase5_pack_exists,
    )

    out_json = Path(args.out_json).resolve()
    out_md = Path(args.out_md).resolve()
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    out_md.write_text(build_md(summary), encoding="utf-8")

    print("=== REPORT GENERATED ===")
    print(f"json: {out_json}")
    print(f"md:   {out_md}")
    print("\nHypothesis quick view:")
    for label in ["H1", "H2", "H3", "H4", "H5"]:
        row = summary["hypotheses"]["hypothesis_results"][label]
        print(f"- {label}: {row['status']} ({row['proxy_metric']}={row['proxy_value']})")
    print("\nPhase quick view:")
    for p in summary["methodology_phases"]:
        print(f"- {p['phase']}: {p['status']}")


if __name__ == "__main__":
    main()
