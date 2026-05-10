import argparse
import csv
import json
import os
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv

try:
    from openai import AzureOpenAI
except Exception:
    AzureOpenAI = None  # type: ignore


def load_json_if_exists(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


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


def pct(x: float) -> float:
    return round(x * 100.0, 2)


def count_filled_rows(path: Path, tracked_fields: List[str]) -> int:
    if not path.exists():
        return 0
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            if any(str(row.get(field, "")).strip() for field in tracked_fields):
                count += 1
        return count


def to_real_hypothesis_block(real_metrics: Dict[str, Any]) -> Dict[str, Any]:
    metrics = real_metrics.get("metrics", {})
    targets = real_metrics.get("targets", {})

    h1_sft = float(metrics.get("H1_vs_sft", {}).get("win_rate", 0.0))
    h1_v0 = float(metrics.get("H1_vs_v0", {}).get("win_rate", 0.0))
    h2 = float(metrics.get("H2", {}).get("win_rate", 0.0))
    h3 = float(metrics.get("H3", {}).get("pct_meaningfully_distinct", 0.0))
    h4 = float(metrics.get("H4", {}).get("improvement", 0.0))
    h5 = float(metrics.get("H5", {}).get("time_reduction", 0.0))

    return {
        "n_total_pairs": int(metrics.get("H1_vs_sft", {}).get("n", 0)) + int(metrics.get("H1_vs_v0", {}).get("n", 0)),
        "n_gate_pass": None,
        "gate_pass_rate": None,
        "means": {
            "H1_vs_sft": round(h1_sft, 4),
            "H1_vs_v0": round(h1_v0, 4),
            "H2": round(h2, 4),
            "H3": round(h3, 4),
            "H4": round(h4, 4),
            "H5": round(h5, 4),
        },
        "hypothesis_results": {
            "H1": {
                "proposal_target": ">=65% preference vs SFT-only and >=75% vs v0.dev",
                "real_metric": "human_blinded_preference_win_rate",
                "real_value": {"vs_sft": round(h1_sft, 4), "vs_v0": round(h1_v0, 4)},
                "status": "real_supported" if bool(real_metrics.get("status", {}).get("H1", False)) else "real_not_met",
                "p_values": {
                    "vs_sft": metrics.get("H1_vs_sft", {}).get("p_value", 1.0),
                    "vs_v0": metrics.get("H1_vs_v0", {}).get("p_value", 1.0),
                },
            },
            "H2": {
                "proposal_target": ">=60% business-alignment improvement",
                "real_metric": "human_business_alignment_win_rate",
                "real_value": round(h2, 4),
                "status": "real_supported" if bool(real_metrics.get("status", {}).get("H2", False)) else "real_not_met",
                "p_value": metrics.get("H2", {}).get("p_value", 1.0),
            },
            "H3": {
                "proposal_target": ">=70% meaningfully distinct strategies",
                "real_metric": "human_distinctness_rate",
                "real_value": round(h3, 4),
                "status": "real_supported" if bool(real_metrics.get("status", {}).get("H3", False)) else "real_not_met",
                "p_value": metrics.get("H3", {}).get("p_value", 1.0),
            },
            "H4": {
                "proposal_target": ">=10% confidence/collaboration improvement",
                "real_metric": "human_confidence_collaboration_improvement",
                "real_value": round(h4, 4),
                "status": "real_supported" if bool(real_metrics.get("status", {}).get("H4", False)) else "real_not_met",
                "p_value": metrics.get("H4", {}).get("p_value", 1.0),
            },
            "H5": {
                "proposal_target": ">=25% time reduction to acceptable design",
                "real_metric": "human_time_to_acceptable_reduction",
                "real_value": round(h5, 4),
                "status": "real_supported" if bool(real_metrics.get("status", {}).get("H5", False)) else "real_not_met",
                "p_value": metrics.get("H5", {}).get("p_value", 1.0),
            },
        },
        "targets": targets,
    }


def build_methodology_phases(
    dpo_info: Dict[str, Any],
    brand_info: Dict[str, Any],
    dpo_status: str,
    brand_status: str,
    hypothesis_results: Dict[str, Any],
    blind_pack_exists: bool,
    human_ratings_collected: bool,
    h4_logged: bool,
    designer_recruitment_logged: bool,
    paper_tables_compiled: bool,
) -> List[Dict[str, Any]]:
    dpo_model_id = str(dpo_info.get("dpo_model_id", "")).strip()
    brand_model_id = str(brand_info.get("fine_tuned_model", "")).strip()

    h = hypothesis_results.get("hypothesis_results", {})
    h2_ok = h.get("H2", {}).get("status") == "real_supported"
    h3_ok = h.get("H3", {}).get("status") == "real_supported"
    h4_ok = h.get("H4", {}).get("status") == "real_supported"
    h1_ok = h.get("H1", {}).get("status") == "real_supported"
    h5_ok = h.get("H5", {}).get("status") == "real_supported"

    return [
        {
            "phase": "Phase 1 (Weeks 1–3)",
            "goal": "Context schema, high-quality dataset, and recruit 3–5 designers",
            "status": "completed" if designer_recruitment_logged else "in_progress",
            "checks": {
                "context_schema_and_pipeline": True,
                "dataset_built": True,
                "designer_recruitment_evidence_logged": designer_recruitment_logged,
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
            "status": "completed_real" if (h2_ok and h3_ok) else "in_progress",
            "checks": {
                "h2_real_supported": h2_ok,
                "h3_real_supported": h3_ok,
            },
        },
        {
            "phase": "Phase 4 (Weeks 8–10)",
            "goal": "HITL rationale/collaboration loop (H4)",
            "status": "completed_real" if (h4_ok and h4_logged) else "in_progress",
            "checks": {
                "h4_real_supported": h4_ok,
                "human_session_data_logged": h4_logged,
            },
        },
        {
            "phase": "Phase 5 (Weeks 10–12)",
            "goal": "Blind baseline comparison vs SFT-only and v0.dev (H1/H5)",
            "status": "completed_real" if (blind_pack_exists and human_ratings_collected and h1_ok and h5_ok) else "in_progress",
            "checks": {
                "blind_pack_prepared": blind_pack_exists,
                "human_blind_ratings_collected": human_ratings_collected,
                "h1_real_supported": h1_ok,
                "h5_real_supported": h5_ok,
            },
        },
        {
            "phase": "Phase 6 (Weeks 12–14)",
            "goal": "Publication package + deployment assets",
            "status": "completed" if (bool(dpo_model_id) and bool(brand_model_id) and paper_tables_compiled) else "in_progress",
            "checks": {
                "dpo_checkpoint_ready": bool(dpo_model_id),
                "brand_strategy_model_ready": bool(brand_model_id) or brand_status == "succeeded",
                "paper_tables_and_figures_compiled": paper_tables_compiled,
            },
        },
    ]


def build_md(summary: Dict[str, Any]) -> str:
    h = summary.get("hypotheses", {})
    hr = h.get("hypothesis_results", {})
    phases = summary.get("methodology_phases", [])

    lines: List[str] = []
    lines.append("# AI-CDO Real Hypothesis and Methodology Status Report")
    lines.append("")
    lines.append("## Hypothesis Results (Real)")
    lines.append("| Hypothesis | Target | Current (Real) | Status |")
    lines.append("|---|---|---:|---|")
    lines.append(
        f"| H1 | {hr.get('H1', {}).get('proposal_target', '')} | vs SFT={pct(float(hr.get('H1', {}).get('real_value', {}).get('vs_sft', 0.0)))}%, vs v0={pct(float(hr.get('H1', {}).get('real_value', {}).get('vs_v0', 0.0)))}% | {hr.get('H1', {}).get('status', 'unknown')} |"
    )
    for label in ["H2", "H3", "H4", "H5"]:
        row = hr.get(label, {})
        lines.append(
            f"| {label} | {row.get('proposal_target','')} | {pct(float(row.get('real_value',0.0)))}% via `{row.get('real_metric','')}` | {row.get('status','unknown')} |"
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

    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--real-metrics-json", required=True)
    ap.add_argument("--dpo-info", default="platform/training/dpo_model_info_v2p25.json")
    ap.add_argument("--brand-info", default="platform/training/brand_model_info_v2.json")
    ap.add_argument("--real-blind-pack", default="platform/training/reports/real_metrics/phase5_blind_pack_real_v1.json")
    ap.add_argument("--human-ratings-csv", default="")
    ap.add_argument("--h4-csv", default="")
    ap.add_argument("--designer-recruitment-evidence", default="")
    ap.add_argument("--paper-tables-compiled", action="store_true")
    ap.add_argument("--azure-api-version", default="2024-10-21")
    ap.add_argument("--out-json", default="platform/training/reports/hypothesis_methodology_results_real_v1.json")
    ap.add_argument("--out-md", default="platform/training/reports/hypothesis_methodology_results_real_v1.md")
    args = ap.parse_args()

    real_metrics = load_json_if_exists(Path(args.real_metrics_json).resolve())
    if not real_metrics:
        raise FileNotFoundError(f"Missing real metrics JSON: {args.real_metrics_json}")

    dpo_info = load_json_if_exists(Path(args.dpo_info).resolve())
    brand_info = load_json_if_exists(Path(args.brand_info).resolve())

    dpo_status = try_get_job_status(str(dpo_info.get("job_id", "")), args.azure_api_version)
    brand_status = try_get_job_status(str(brand_info.get("job_id", "")), args.azure_api_version)

    hblock = to_real_hypothesis_block(real_metrics)

    blind_pack_exists = Path(args.real_blind_pack).resolve().exists()
    human_ratings_count = 0
    if args.human_ratings_csv:
        human_ratings_count = count_filled_rows(
            Path(args.human_ratings_csv).resolve(),
            [
                "preferred_output",
                "premium_quality_A",
                "premium_quality_B",
                "business_alignment_A",
                "business_alignment_B",
                "distinctness_A",
                "distinctness_B",
                "confidence_collaboration_A",
                "confidence_collaboration_B",
                "time_to_acceptable_A_min",
                "time_to_acceptable_B_min",
                "notes",
            ],
        )

    h4_count = 0
    if args.h4_csv:
        h4_count = count_filled_rows(
            Path(args.h4_csv).resolve(),
            [
                "confidence_rationale_on",
                "confidence_rationale_off",
                "collaboration_rationale_on",
                "collaboration_rationale_off",
                "notes",
            ],
        )

    human_ratings_collected = human_ratings_count > 0
    h4_logged = h4_count > 0
    designer_recruitment_logged = bool(args.designer_recruitment_evidence) and Path(args.designer_recruitment_evidence).resolve().exists()

    summary: Dict[str, Any] = {
        "artifacts": {
            "real_metrics_json": str(Path(args.real_metrics_json).resolve()),
            "dpo_info": str(Path(args.dpo_info).resolve()),
            "brand_info": str(Path(args.brand_info).resolve()),
            "real_blind_pack": str(Path(args.real_blind_pack).resolve()),
            "human_ratings_csv": str(Path(args.human_ratings_csv).resolve()) if args.human_ratings_csv else "",
            "h4_csv": str(Path(args.h4_csv).resolve()) if args.h4_csv else "",
            "human_ratings_filled_rows": human_ratings_count,
            "h4_filled_rows": h4_count,
        },
        "job_status": {
            "dpo_job_id": str(dpo_info.get("job_id", "")),
            "dpo_status": dpo_status,
            "brand_job_id": str(brand_info.get("job_id", "")),
            "brand_status": brand_status,
        },
        "hypotheses": hblock,
    }

    summary["methodology_phases"] = build_methodology_phases(
        dpo_info=dpo_info,
        brand_info=brand_info,
        dpo_status=dpo_status,
        brand_status=brand_status,
        hypothesis_results=hblock,
        blind_pack_exists=blind_pack_exists,
        human_ratings_collected=human_ratings_collected,
        h4_logged=h4_logged,
        designer_recruitment_logged=designer_recruitment_logged,
        paper_tables_compiled=bool(args.paper_tables_compiled),
    )

    out_json = Path(args.out_json).resolve()
    out_md = Path(args.out_md).resolve()
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    out_md.write_text(build_md(summary), encoding="utf-8")

    print("=== REAL REPORT GENERATED ===")
    print(f"json: {out_json}")
    print(f"md:   {out_md}")
    print("\nHypothesis quick view:")
    for label in ["H1", "H2", "H3", "H4", "H5"]:
        row = summary["hypotheses"]["hypothesis_results"][label]
        print(f"- {label}: {row['status']}")
    print("\nPhase quick view:")
    for p in summary["methodology_phases"]:
        print(f"- {p['phase']}: {p['status']}")


if __name__ == "__main__":
    main()
