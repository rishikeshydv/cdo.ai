import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--real-metrics-dir",
        default="/Users/rishi/Desktop/cdo.ai/platform/training/reports/real_metrics",
    )
    ap.add_argument(
        "--reports-dir",
        default="/Users/rishi/Desktop/cdo.ai/platform/training/reports",
    )
    ap.add_argument(
        "--training-dir",
        default="/Users/rishi/Desktop/cdo.ai/platform/training",
    )
    args = ap.parse_args()

    real_metrics_dir = Path(args.real_metrics_dir).resolve()
    reports_dir = Path(args.reports_dir).resolve()
    training_dir = Path(args.training_dir).resolve()
    scripts_dir = training_dir / "scripts"

    ratings_glob = str(real_metrics_dir / "rater_packets_v2_strict20_3raters" / "human_pair_ratings_rater_*.csv")
    h4_glob = str(real_metrics_dir / "rater_packets_v2_strict20_3raters" / "h4_session_rater_*.csv")

    merged_ratings = real_metrics_dir / "human_pair_ratings_real_v2_strict20.csv"
    merged_h4 = real_metrics_dir / "h4_session_real_v2_strict20.csv"
    decoded_long = real_metrics_dir / "human_pair_ratings_decoded_long_real_v2_strict20.csv"
    decoded_pair = real_metrics_dir / "human_pair_ratings_decoded_pair_real_v2_strict20.csv"
    metrics_json = real_metrics_dir / "hypothesis_real_metrics_real_v2_strict20.json"
    report_json = reports_dir / "hypothesis_methodology_results_real_v2_strict20.json"
    report_md = reports_dir / "hypothesis_methodology_results_real_v2_strict20.md"
    recruitment_md = real_metrics_dir / "designer_recruitment_evidence_v1.md"
    blind_pack = real_metrics_dir / "phase5_blind_pack_real_v2_strict20.json"
    blind_key = real_metrics_dir / "phase5_blind_key_real_v2_strict20.json"

    run(
        [
            sys.executable,
            str(scripts_dir / "merge_human_rating_packets.py"),
            "--ratings-glob",
            ratings_glob,
            "--h4-glob",
            h4_glob,
            "--out-ratings",
            str(merged_ratings),
            "--out-h4",
            str(merged_h4),
        ]
    )

    run(
        [
            sys.executable,
            str(scripts_dir / "decode_blind_pair_ratings.py"),
            "--ratings-csv",
            str(merged_ratings),
            "--blind-key",
            str(blind_key),
            "--out-long-csv",
            str(decoded_long),
            "--out-pair-csv",
            str(decoded_pair),
        ]
    )

    run(
        [
            sys.executable,
            str(scripts_dir / "compute_hypothesis_real_metrics.py"),
            "--decoded-long-csv",
            str(decoded_long),
            "--decoded-pair-csv",
            str(decoded_pair),
            "--h4-csv",
            str(merged_h4),
            "--out-json",
            str(metrics_json),
        ]
    )

    run(
        [
            sys.executable,
            str(scripts_dir / "build_hypothesis_methodology_report_real.py"),
            "--real-metrics-json",
            str(metrics_json),
            "--dpo-info",
            str(training_dir / "dpo_model_info_v2p25.json"),
            "--brand-info",
            str(training_dir / "brand_model_info_v2.json"),
            "--real-blind-pack",
            str(blind_pack),
            "--human-ratings-csv",
            str(merged_ratings),
            "--h4-csv",
            str(merged_h4),
            "--designer-recruitment-evidence",
            str(recruitment_md),
            "--azure-api-version",
            "2024-10-21",
            "--out-json",
            str(report_json),
            "--out-md",
            str(report_md),
        ]
    )


if __name__ == "__main__":
    main()
