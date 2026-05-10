import argparse
import json
from pathlib import Path
from typing import Dict, List

import pandas as pd
from scipy.stats import binomtest, mannwhitneyu, wilcoxon


def parse_set(raw: str) -> List[str]:
    return [x.strip() for x in raw.split(',') if x.strip()]


def h1_preference(pair_df: pd.DataFrame, ai_cdo: str, opp: str) -> Dict[str, float]:
    if pair_df.empty:
        return {"n": 0, "win_rate": 0.0, "p_value": 1.0}

    sub = pair_df[
        ((pair_df['system_A'] == ai_cdo) & (pair_df['system_B'] == opp)) |
        ((pair_df['system_A'] == opp) & (pair_df['system_B'] == ai_cdo))
    ].copy()

    if sub.empty:
        return {"n": 0, "win_rate": 0.0, "p_value": 1.0}

    def is_win(r) -> float:
        ps = str(r.get('preferred_system', ''))
        if ps == ai_cdo:
            return 1.0
        if ps == 'Equal':
            return 0.5
        return 0.0

    sub['ai_win'] = sub.apply(is_win, axis=1)
    non_tie = sub[sub['ai_win'] != 0.5]
    n = len(non_tie)
    wins = int((non_tie['ai_win'] == 1.0).sum())
    win_rate = (wins / n) if n else 0.0

    p = 1.0
    if n > 0:
        p = float(binomtest(wins, n, p=0.5, alternative='greater').pvalue)

    return {"n": n, "wins": wins, "win_rate": round(win_rate, 4), "p_value": round(p, 6)}


def h2_alignment(long_df: pd.DataFrame, ai_cdo: str, baselines: List[str]) -> Dict[str, float]:
    sub = long_df[long_df['system'].isin([ai_cdo] + baselines)].copy()
    if sub.empty:
        return {"n_pairs": 0, "win_rate": 0.0, "p_value": 1.0}

    sub['business_alignment'] = pd.to_numeric(sub['business_alignment'], errors='coerce')
    sub = sub.dropna(subset=['business_alignment'])
    if sub.empty:
        return {"n_pairs": 0, "win_rate": 0.0, "p_value": 1.0}

    wins = 0.0
    n_pairs = 0
    ai_scores = []
    base_scores = []

    for _, grp in sub.groupby(['rater_id', 'pair_id']):
        systems = set(grp['system'].tolist())
        if ai_cdo not in systems:
            continue

        ai_row = grp[grp['system'] == ai_cdo]
        base_row = grp[grp['system'].isin(baselines)]
        if len(ai_row) != 1 or len(base_row) != 1:
            continue

        ai_score = float(ai_row.iloc[0]['business_alignment'])
        base_score = float(base_row.iloc[0]['business_alignment'])
        ai_scores.append(ai_score)
        base_scores.append(base_score)
        n_pairs += 1

        if ai_score > base_score:
            wins += 1.0
        elif ai_score == base_score:
            wins += 0.5

    if n_pairs == 0:
        return {"n_pairs": 0, "win_rate": 0.0, "p_value": 1.0}

    non_tie_n = sum(1 for a, b in zip(ai_scores, base_scores) if a != b)
    non_tie_wins = sum(1 for a, b in zip(ai_scores, base_scores) if a > b)
    p = 1.0
    if non_tie_n > 0:
        p = float(binomtest(non_tie_wins, non_tie_n, p=0.5, alternative='greater').pvalue)

    return {
        "n_pairs": int(n_pairs),
        "wins_equivalent": round(wins, 4),
        "win_rate": round(float(wins / n_pairs), 4),
        "mean_ai_cdo": round(float(sum(ai_scores) / len(ai_scores)), 4),
        "mean_baseline": round(float(sum(base_scores) / len(base_scores)), 4),
        "p_value": round(p, 6),
    }


def h3_distinctness(long_df: pd.DataFrame, target_system: str) -> Dict[str, float]:
    sub = long_df[(long_df['system'] == target_system) & (long_df['evaluation_type'] == 'diversity')]
    if sub.empty:
        sub = long_df[long_df['system'] == target_system]
    d = pd.to_numeric(sub['distinctness'], errors='coerce').dropna()
    if len(d) == 0:
        return {"n": 0, "pct_meaningfully_distinct": 0.0, "p_value": 1.0}

    successes = int((d >= 7).sum())
    n = int(len(d))
    pct_distinct = successes / n
    p = float(binomtest(successes, n, p=0.7, alternative='greater').pvalue)

    return {
        "n": n,
        "successes": successes,
        "pct_meaningfully_distinct": round(pct_distinct, 4),
        "p_value": round(p, 6),
    }


def h4_collaboration(h4_df: pd.DataFrame) -> Dict[str, float]:
    if h4_df.empty:
        return {"n": 0, "improvement": 0.0, "p_value": 1.0}

    c_on = pd.to_numeric(h4_df['confidence_rationale_on'], errors='coerce')
    c_off = pd.to_numeric(h4_df['confidence_rationale_off'], errors='coerce')
    k_on = pd.to_numeric(h4_df['collaboration_rationale_on'], errors='coerce')
    k_off = pd.to_numeric(h4_df['collaboration_rationale_off'], errors='coerce')

    valid = (~c_on.isna()) & (~c_off.isna()) & (~k_on.isna()) & (~k_off.isna())
    c_on, c_off, k_on, k_off = c_on[valid], c_off[valid], k_on[valid], k_off[valid]

    if len(c_on) == 0:
        return {"n": 0, "improvement": 0.0, "p_value": 1.0}

    on_avg = (c_on + k_on) / 2.0
    off_avg = (c_off + k_off) / 2.0
    diff = on_avg - off_avg
    improvement = float(diff.mean()) / 10.0

    p = 1.0
    if len(diff) > 0 and diff.abs().sum() > 0:
        p = float(wilcoxon(on_avg, off_avg, alternative='greater').pvalue)

    return {
        "n": int(len(diff)),
        "mean_on": round(float(on_avg.mean()), 4),
        "mean_off": round(float(off_avg.mean()), 4),
        "improvement": round(improvement, 4),
        "p_value": round(p, 6),
    }


def h5_time(long_df: pd.DataFrame, ai_cdo: str, baselines: List[str]) -> Dict[str, float]:
    sub = long_df[long_df['system'].isin([ai_cdo] + baselines)].copy()
    if sub.empty:
        return {"n_pairs": 0, "time_reduction": 0.0, "p_value": 1.0}

    sub['k'] = sub['rater_id'].astype(str) + '::' + sub['brief_id'].astype(str)

    reductions: List[float] = []
    ai_times = sub[sub['system'] == ai_cdo].set_index('k')['time_to_acceptable_min']
    ai_times = pd.to_numeric(ai_times, errors='coerce').dropna()

    all_base = []
    all_ai = []

    for b in baselines:
        b_times = sub[sub['system'] == b].set_index('k')['time_to_acceptable_min']
        b_times = pd.to_numeric(b_times, errors='coerce').dropna()
        common = ai_times.index.intersection(b_times.index)
        if len(common) == 0:
            continue
        ai_c = ai_times.loc[common]
        b_c = b_times.loc[common]

        for x, y in zip(ai_c.tolist(), b_c.tolist()):
            if y > 0:
                reductions.append((y - x) / y)
                all_ai.append(x)
                all_base.append(y)

    if not reductions:
        return {"n_pairs": 0, "time_reduction": 0.0, "p_value": 1.0}

    p = 1.0
    if len(all_ai) > 0:
        p = float(wilcoxon(all_base, all_ai, alternative='greater').pvalue)

    return {
        "n_pairs": int(len(reductions)),
        "time_reduction": round(float(sum(reductions) / len(reductions)), 4),
        "p_value": round(p, 6),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--decoded-long-csv', default='')
    ap.add_argument('--decoded-pair-csv', default='')
    # Backward-compatible aliases used in earlier runs.
    ap.add_argument('--decoded-long', default='')
    ap.add_argument('--decoded-pair', default='')
    ap.add_argument('--h4-csv', default='')
    ap.add_argument('--out-json', required=True)

    ap.add_argument('--ai-cdo-system', default='ai_cdo_dpo')
    ap.add_argument('--sft-system', default='sft_only')
    ap.add_argument('--v0-system', default='v0')
    ap.add_argument('--structured-systems', default='ai_cdo_dpo,sft_only')
    ap.add_argument('--prompt-only-systems', default='v0,prompt_only,baseline_proxy')
    ap.add_argument('--baseline-systems-for-h5', default='sft_only,v0,baseline_proxy')
    args = ap.parse_args()

    decoded_long = args.decoded_long_csv or args.decoded_long
    decoded_pair = args.decoded_pair_csv or args.decoded_pair
    if not decoded_long or not decoded_pair:
        raise ValueError('Provide --decoded-long-csv/--decoded-pair-csv (or legacy --decoded-long/--decoded-pair).')

    long_df = pd.read_csv(Path(decoded_long).resolve())
    pair_df = pd.read_csv(Path(decoded_pair).resolve())

    for c in ['premium_quality', 'business_alignment', 'distinctness', 'confidence_collaboration', 'time_to_acceptable_min']:
        if c in long_df.columns:
            long_df[c] = pd.to_numeric(long_df[c], errors='coerce')

    h4_df = pd.DataFrame()
    if args.h4_csv:
        p = Path(args.h4_csv).resolve()
        if p.exists():
            h4_df = pd.read_csv(p)

    baselines_h5 = parse_set(args.baseline_systems_for_h5)

    h1_vs_sft = h1_preference(pair_df, args.ai_cdo_system, args.sft_system)
    h1_vs_v0 = h1_preference(pair_df, args.ai_cdo_system, args.v0_system)

    h2 = h2_alignment(long_df, args.ai_cdo_system, baselines_h5)
    h3 = h3_distinctness(long_df, args.ai_cdo_system)
    h4 = h4_collaboration(h4_df)
    h5 = h5_time(long_df, args.ai_cdo_system, baselines_h5)

    targets = {
        'H1_vs_sft': 0.65,
        'H1_vs_v0': 0.75,
        'H2': 0.60,
        'H3': 0.70,
        'H4': 0.10,
        'H5': 0.25,
    }

    summary = {
        'inputs': {
            'decoded_long_csv': str(Path(decoded_long).resolve()),
            'decoded_pair_csv': str(Path(decoded_pair).resolve()),
            'h4_csv': str(Path(args.h4_csv).resolve()) if args.h4_csv else '',
        },
        'metrics': {
            'H1_vs_sft': h1_vs_sft,
            'H1_vs_v0': h1_vs_v0,
            'H2': h2,
            'H3': h3,
            'H4': h4,
            'H5': h5,
        },
        'targets': targets,
        'status': {
            'H1': (h1_vs_sft.get('win_rate', 0.0) >= targets['H1_vs_sft']) and (h1_vs_v0.get('win_rate', 0.0) >= targets['H1_vs_v0']),
            'H2': h2.get('win_rate', 0.0) >= targets['H2'],
            'H3': h3.get('pct_meaningfully_distinct', 0.0) >= targets['H3'],
            'H4': h4.get('improvement', 0.0) >= targets['H4'],
            'H5': h5.get('time_reduction', 0.0) >= targets['H5'],
        }
    }

    out_path = Path(args.out_json).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, indent=2), encoding='utf-8')

    print('=== REAL HYPOTHESIS METRICS ===')
    print(f"H1 vs SFT win rate: {h1_vs_sft.get('win_rate',0)}")
    print(f"H1 vs v0 win rate:  {h1_vs_v0.get('win_rate',0)}")
    print(f"H2 win rate:        {h2.get('win_rate',0)}")
    print(f"H3 distinctness:    {h3.get('pct_meaningfully_distinct',0)}")
    print(f"H4 improvement:     {h4.get('improvement',0)}")
    print(f"H5 time reduction:  {h5.get('time_reduction',0)}")
    print(f"out:                {out_path}")


if __name__ == '__main__':
    main()
