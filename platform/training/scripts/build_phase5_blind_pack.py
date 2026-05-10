import argparse
import json
import random
from pathlib import Path
from typing import Any, Dict, List


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--scored-jsonl', required=True)
    ap.add_argument('--n-briefs', type=int, default=40)
    ap.add_argument('--seed', type=int, default=1337)
    ap.add_argument('--out-pack', required=True)
    ap.add_argument('--out-key', required=True)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    rows = read_jsonl(Path(args.scored_jsonl).resolve())
    kept = [r for r in rows if r.get('rubric', {}).get('gate_pass', False)]
    rng.shuffle(kept)

    selected = kept[: min(args.n_briefs, len(kept))]

    pack: List[Dict[str, Any]] = []
    key: List[Dict[str, Any]] = []

    for i, r in enumerate(selected, 1):
        # Randomize A/B placement to reduce ordering bias.
        if rng.random() < 0.5:
            a_out, b_out = r['chosen'], r['rejected']
            a_sys, b_sys = 'ai_cdo_dpo', 'baseline_proxy'
        else:
            a_out, b_out = r['rejected'], r['chosen']
            a_sys, b_sys = 'baseline_proxy', 'ai_cdo_dpo'

        bid = f'brief-{i:03d}'
        pack.append(
            {
                'brief_id': bid,
                'project': r.get('project'),
                'bucket': r.get('bucket'),
                'prompt': r.get('prompt'),
                'output_A': a_out,
                'output_B': b_out,
                'rating_form': {
                    'preference': 'A_or_B',
                    'premium_quality_1_10': 'int',
                    'business_alignment_1_10': 'int',
                    'distinctness_1_10': 'int',
                    'confidence_collaboration_1_10': 'int',
                    'time_to_acceptable_minutes': 'float',
                },
            }
        )
        key.append({'brief_id': bid, 'A_system': a_sys, 'B_system': b_sys})

    out_pack = Path(args.out_pack).resolve()
    out_key = Path(args.out_key).resolve()
    out_pack.parent.mkdir(parents=True, exist_ok=True)
    out_key.parent.mkdir(parents=True, exist_ok=True)

    out_pack.write_text(json.dumps({'briefs': pack}, indent=2), encoding='utf-8')
    out_key.write_text(json.dumps({'mapping': key}, indent=2), encoding='utf-8')

    print('=== PHASE5 BLIND PACK ===')
    print(f'source_gate_pass_rows: {len(kept)}')
    print(f'briefs_written:        {len(pack)}')
    print(f'pack:                  {out_pack}')
    print(f'key:                   {out_key}')


if __name__ == '__main__':
    main()
