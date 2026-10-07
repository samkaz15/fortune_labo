#!/usr/bin/env python3
"""Check an explicit export manifest without emitting matching private content."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_PARTS = {'test-articles', 'private', '.editorial-private', '.editorial-source', 'imports', '__pycache__'}
FORBIDDEN_NAMES = {'genre-research.json', 'content-index.json', 'content-opportunities.json', 'classification-results.json'}
PROVENANCE_KEYS = {'source_id', 'source_type', 'source_title', 'access_scope', 'derived_artifacts'}
# Patterns are assembled so the scanner source itself contains no source locator.
CONTENT_PATTERNS = {
    'private_document_locator': re.compile(r'docs\.' + r'google\.com/(?:document|spreadsheets|presentation)/d/', re.I),
    'source_position_reference': re.compile(r'GR\d{3}:P\d+'),
    'source_metadata': re.compile(r'"(?:revision_id|revisionId|document_id|documentId|start_index|end_index|source_archive)"\s*:'),
    'research_numeric_quote': re.compile(r'(?:市場|調査|購入率|利用率|課金率|購買率|回答者)[^\n]{0,48}\d+(?:\.\d+)?\s*[%％]'),
    'source_purchase_ranking': re.compile(r'(?:購入' + r'優先順位|購入トリガーの' + r'強さ|課金' + r'優先順位)\s*[:：|]'),
}


def _strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)


def scan(manifest_path: Path, selected=None, private_reference=None):
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    allowed = manifest.get('files', [])
    errors = []
    if not isinstance(allowed, list) or not all(isinstance(p, str) for p in allowed):
        return ['manifest: files must be explicit relative file paths']
    if len(allowed) != len(set(allowed)):
        errors.append('manifest: duplicate paths')
    selection = allowed if selected is None else selected
    private_fragments = set()
    private_identifiers = set()
    if private_reference:
        raw = json.loads(Path(private_reference).read_text(encoding='utf-8'))
        for s in _strings(raw):
            # Check long text spans, including strings that straddle chunk boundaries.
            if len(s) >= 48 and re.search(r'[ぁ-んァ-ヶ一-龥]', s):
                private_fragments.update(s[i:i + 48] for i in range(0, len(s) - 47, 16))
            private_identifiers.update(re.findall(r'/d/([A-Za-z0-9_-]{20,})', s))
            private_identifiers.update(re.findall(r'\btab=(t\.[A-Za-z0-9_-]+)', s))
    for relative in selection:
        if relative not in allowed:
            errors.append(f'{relative}: not explicitly allowed')
            continue
        p = Path(relative)
        if p.is_absolute() or '..' in p.parts or any(c in relative for c in '*?['):
            errors.append(f'{relative}: unsafe or non-explicit path')
            continue
        if PRIVATE_PARTS.intersection(p.parts) or p.name in FORBIDDEN_NAMES:
            errors.append(f'{relative}: private artifact path')
            continue
        full = ROOT / p
        if not full.is_file() or full.is_symlink() or ROOT not in full.resolve().parents:
            errors.append(f'{relative}: missing file or unsafe resolution')
            continue
        try:
            body = full.read_text(encoding='utf-8')
        except UnicodeError:
            errors.append(f'{relative}: binary exports require separate review')
            continue
        for name, pattern in CONTENT_PATTERNS.items():
            if pattern.search(body):
                errors.append(f'{relative}: {name}')
        if any(value in body for value in private_identifiers):
            errors.append(f'{relative}: private source identifier')
        if any(value in body for value in private_fragments):
            errors.append(f'{relative}: retained private source passage')
        if p.name == 'provenance.json':
            try:
                data = json.loads(body)
                for record in data['sources']:
                    if set(record) != PROVENANCE_KEYS:
                        errors.append(f'{relative}: provenance key outside allowlist')
                    if record.get('access_scope') != 'private':
                        errors.append(f'{relative}: unexpected source access scope')
                    if not re.fullmatch(r'GR\d{3}', record.get('source_id', '')):
                        errors.append(f'{relative}: source ID must be opaque')
                    if not re.fullmatch(r'Private editorial source \d{2}', record.get('source_title', '')):
                        errors.append(f'{relative}: source title must be a generic alias')
                    for artifact in record.get('derived_artifacts', []):
                        if artifact not in allowed:
                            errors.append(f'{relative}: derived artifact outside manifest')
            except (ValueError, KeyError, TypeError):
                errors.append(f'{relative}: invalid provenance structure')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=ROOT / 'docs/editorial/public-export-manifest.json')
    parser.add_argument('--file', action='append', dest='selected')
    parser.add_argument('--private-reference', type=Path)
    args = parser.parse_args()
    errors = scan(args.manifest, args.selected, args.private_reference)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    count = len(args.selected) if args.selected is not None else len(json.loads(args.manifest.read_text())['files'])
    print(f'PASS: {count} explicitly allowed public files; no blocked content detected')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
