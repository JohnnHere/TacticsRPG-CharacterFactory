"""Thin entry checker for `main-orc-onehanded-entry-v1`.

Preflights the frozen orchestrator plan and delegates the contract verification to the existing
single implementation (`node tools/entry-main-orc.mjs verify`), which writes
`experiments/main-orc-entry-v1/entry-check.json`. No duplicated rule set, no new framework, no
artistic acceptance: the creator still approves the artwork.
"""
from pathlib import Path
import json, shutil, subprocess, sys

R = Path(__file__).resolve().parents[2]
E = R / 'experiments' / 'main-orc-entry-v1'
PLAN = E / 'entry-plan.json'
REQUIRED = ('revision', 'baseline', 'output', 'masters', 'sequences', 'impactIndex')


def say(message, code=1):
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    print(message)
    return code


def main():
    if not PLAN.is_file():
        return say(f'FAIL plano ausente: {PLAN.relative_to(R)}. O scaffold nao cria plano padrao nem reposiciona a mao.', 2)
    try:
        plan = json.loads(PLAN.read_text(encoding='utf-8-sig'))
    except json.JSONDecodeError as error:
        return say(f'FAIL plano invalido em {PLAN.relative_to(R)}: {error}', 2)
    missing = [key for key in REQUIRED if key not in plan]
    if missing:
        return say(f'FAIL plano sem campos obrigatorios: {", ".join(missing)}', 2)
    for category in ('Sword', 'Axe'):
        sequence = plan.get('sequences', {}).get(category)
        if not isinstance(sequence, list) or len(sequence) < 2:
            return say(f'FAIL sequences.{category} ausente ou com menos de 2 entradas', 2)
        if not isinstance(plan.get('impactIndex', {}).get(category), int):
            return say(f'FAIL impactIndex.{category} ausente ou nao inteiro', 2)
    node = shutil.which('node')
    if not node:
        return say('NOT_RUN node ausente; nenhuma verificacao executada.', 3)
    result = subprocess.run([node, 'tools/entry-main-orc.mjs', 'verify'], cwd=R, text=True,
                            capture_output=True, encoding='utf-8', errors='replace')
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)
    report = E / 'entry-check.json'
    if report.is_file():
        summary = json.loads(report.read_text(encoding='utf-8-sig'))['summary']
        print(f'relatorio: {report.relative_to(R)} | PASS={summary["PASS"]} FAIL={summary["FAIL"]} '
              f'INFO={summary["INFO"]} REQUIRES_HUMAN_REVIEW={summary["REQUIRES_HUMAN_REVIEW"]}')
    return result.returncode


if __name__ == '__main__':
    sys.exit(main())
