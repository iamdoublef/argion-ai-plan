"""Score a candidate docx and return key metrics."""
import json
import os
import subprocess
import sys

SCORE_SCRIPT = r'D:\work\private\yjsplan\research\yjs-manual-opt\swiss\00_discussions\2026-05-pdf-to-docx-fidelity\score_candidate.py'
TARGET_PDF = r'D:\work\private\yjsplan\research\yjs-manual-opt\swiss\output\imt050-wevac-eu-cn.pdf'
BASELINE_PNGS = r'D:\work\private\yjsplan\research\yjs-manual-opt\swiss\00_discussions\2026-05-pdf-to-docx-fidelity\baseline\target_png'


def score(docx_path: str, quiet=True):
    env = os.environ.copy()
    env['PYTHONUTF8'] = '1'
    r = subprocess.run(
        [sys.executable, SCORE_SCRIPT, docx_path, '--target', TARGET_PDF, '--baseline-pngs', BASELINE_PNGS],
        capture_output=True, text=True, env=env)
    if r.returncode != 0:
        print('SCORE STDERR:', r.stderr)
        raise RuntimeError(f'score failed: {r.returncode}')
    score_json = docx_path.replace('.docx', '.score.json')
    if not os.path.exists(score_json):
        raise RuntimeError(f'score json missing: {score_json}')
    with open(score_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def summary(data):
    v = data['visual']
    e = data['editability']
    pp = v['per_page_mean_diff']
    return {
        'mean': v['overall_mean_diff'],
        'max': v['max_page_diff'],
        'pp': pp,
        'wt': e['wt_count'],
        'pass': data['pass']['overall'],
    }


if __name__ == '__main__':
    s = score(sys.argv[1])
    print(json.dumps(summary(s), indent=2, ensure_ascii=False))
