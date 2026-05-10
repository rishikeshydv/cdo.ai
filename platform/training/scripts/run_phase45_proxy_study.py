import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def step_proxy(prod_readiness: float, issue_resolution: float) -> float:
    return 1.0 + 2.0 * (1.0 - prod_readiness) + 2.0 * (1.0 - issue_resolution)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--scored-jsonl', required=True)
    ap.add_argument('--out-json', required=True)
    args = ap.parse_args()

    rows = read_jsonl(Path(args.scored_jsonl).resolve())
    kept = [r for r in rows if r.get('rubric', {}).get('gate_pass', False)]

    # H4 proxy: compare rationale/context-present vs no-rationale baseline.
    h4_vals = [float(r['rubric']['hypotheses'].get('h4_explainability_context', 0.0)) for r in kept]
    h4_with = mean(h4_vals) if h4_vals else 0.0
    h4_without = 0.0
    h4_improvement = h4_with - h4_without

    # H5 proxy: expected steps-to-acceptable reduction chosen vs rejected.
    reductions: List[float] = []
    for r in kept:
        rubric = r.get('rubric', {})
        c_p = float(rubric.get('pqpt', {}).get('chosen', {}).get('production_readiness', 0.0))
        r_p = float(rubric.get('pqpt', {}).get('rejected', {}).get('production_readiness', 0.0))
        c_i = float(rubric.get('checks', {}).get('chosen', {}).get('issue_resolution_rate', 0.0))
        r_i = float(rubric.get('checks', {}).get('rejected', {}).get('issue_resolution_rate', 0.0))

        c_steps = step_proxy(c_p, c_i)
        r_steps = step_proxy(r_p, r_i)
        if r_steps > 0:
            reductions.append((r_steps - c_steps) / r_steps)

    h5_reduction = mean(reductions) if reductions else 0.0

    out = {
        'input_rows_total': len(rows),
        'input_rows_gate_pass': len(kept),
        'h4_proxy': {
            'with_rationale': round(h4_with, 4),
            'without_rationale_baseline': round(h4_without, 4),
            'improvement': round(h4_improvement, 4),
            'target': 0.10,
            'pass': h4_improvement >= 0.10,
        },
        'h5_proxy': {
            'mean_time_reduction': round(h5_reduction, 4),
            'target': 0.25,
            'pass': h5_reduction >= 0.25,
        },
    }

    out_path = Path(args.out_json).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding='utf-8')

    print('=== PHASE4/5 PROXY STUDY ===')
    print(f'rows_total:      {out["input_rows_total"]}')
    print(f'rows_gate_pass:  {out["input_rows_gate_pass"]}')
    print(f'H4 improvement:  {out["h4_proxy"]["improvement"]} pass={out["h4_proxy"]["pass"]}')
    print(f'H5 reduction:    {out["h5_proxy"]["mean_time_reduction"]} pass={out["h5_proxy"]["pass"]}')
    print(f'out:             {out_path}')


if __name__ == '__main__':
    main()
