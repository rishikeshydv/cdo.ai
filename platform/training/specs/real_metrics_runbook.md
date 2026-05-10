# Real Metrics Runbook (Strict20)

## Current status
- Strict real system outputs are generated for 20 held-out briefs:
  - `platform/training/reports/real_metrics/systems_v2_strict20/v0_records.json`
  - `platform/training/reports/real_metrics/systems_v2_strict20/sft_only_records.json`
  - `platform/training/reports/real_metrics/systems_v2_strict20/ai_cdo_dpo_records.json`
- Strict blind pack + key are generated:
  - `platform/training/reports/real_metrics/phase5_blind_pack_real_v2_strict20.json`
  - `platform/training/reports/real_metrics/phase5_blind_key_real_v2_strict20.json`
- Clean preview set is generated:
  - `platform/training/reports/real_metrics/pair_previews_all_v4_strict20/`
- Rater packets are generated:
  - `platform/training/reports/real_metrics/rater_packets_v2_strict20_3raters/`

## 1) Fill ratings

Raters fill:
- `platform/training/reports/real_metrics/rater_packets_v2_strict20_3raters/human_pair_ratings_rater_*.csv`
- `platform/training/reports/real_metrics/rater_packets_v2_strict20_3raters/h4_session_rater_*.csv`

## 2) Refresh all strict20 real-metric artifacts

```bash
python3 platform/training/scripts/refresh_real_metrics_strict20.py
```

Notes:
- The refresh script merges packets, decodes blind labels, computes H1 to H5, and rebuilds the real methodology report.
- Blank template rows are now ignored by the decoder and do not count as human-collected results.
- Publication claims should be tied to `hypothesis_methodology_results_real_v2_strict20.*` generated from filled human ratings.
