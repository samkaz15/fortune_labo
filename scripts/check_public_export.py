#!/usr/bin/env python3
"""Check an explicit export manifest without emitting matching private content."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_PARTS = {'private', '.editorial-private', '.editorial-source', 'imports', '__pycache__'}
FORBIDDEN_NAMES = {'genre-research.json', 'content-index.json', 'content-opportunities.json', 'classification-results.json'}
FIXTURE_IDS = {'FL-TEST-A', 'FL-TEST-B', 'FL-TEST-C'}
FIXTURE_FILES = {'brief.json', 'blueprint.json', 'production-prompt.md', 'draft-prompt.md',
                 'article.md', 'self-review.json', 'claims.json', 'qa.json', 'comparison.md',
                 'manifest.json', 'run.json', 'writing-rules.md', 'writing-findings.json'}
CREATIVE_FILES = {'image-plan.json', 'assets.json', 'job.json', 'qa.json',
                  'wordpress-draft-payload.json', 'media-upload-plan.json', 'manifest.json'}
RASTER_SUFFIXES = {'.png', '.jpg', '.jpeg', '.webp'}
ASSET_SUFFIXES = RASTER_SUFFIXES | {'.svg'}
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


def _creative_check(relative, allowed):
    """Bind an explicitly selected generated asset to its authorized article."""
    p = Path(relative)
    errors, asset = [], None
    base = ('docs', 'editorial', 'creative-fixtures')
    valid_root = len(p.parts) >= 5 and p.parts[:3] == base and p.parts[3] in FIXTURE_IDS
    valid_text = len(p.parts) == 5 and p.name in CREATIVE_FILES
    valid_overlay = len(p.parts) == 5 and p.name.startswith('overlay') and p.suffix == '.svg'
    valid_image = len(p.parts) == 6 and p.parts[4] == 'images' and p.suffix.lower() in ASSET_SUFFIXES
    if not valid_root or not (valid_text or valid_overlay or valid_image):
        return [f'{relative}: not an authorized creative fixture path'], None
    folder = Path(*p.parts[:4])
    receipt_path = folder / 'manifest.json'
    full_receipt = ROOT / receipt_path
    if (receipt_path.as_posix() not in allowed or full_receipt.is_symlink()
            or ROOT not in full_receipt.resolve().parents):
        return [f'{relative}: creative export receipt is not safely allowlisted'], None
    try:
        receipt = json.loads(full_receipt.read_text(encoding='utf-8'))
        expected_article = f'docs/editorial/test-articles/{p.parts[3]}/article.md'
        article = ROOT / expected_article
        if (receipt.get('export_scope') != 'explicitly_authorized_creative_fixture'
                or receipt.get('content_id') != p.parts[3]
                or receipt.get('contains_private_source') is not False
                or receipt.get('contains_legacy_draft') is not False
                or receipt.get('publication_allowed') is not False
                or receipt.get('source_article_ref') != expected_article
                or expected_article not in allowed or article.is_symlink()
                or ROOT not in article.resolve().parents
                or receipt.get('source_article_sha256') != hashlib.sha256(article.read_bytes()).hexdigest()):
            return [f'{relative}: creative receipt is not bound to the authorized source article'], None
        assets = receipt.get('assets')
        if not isinstance(assets, list) or not all(isinstance(row, dict) for row in assets):
            return [f'{relative}: creative receipt needs an explicit asset list'], None
        paths = [row.get('path') for row in assets]
        if len(paths) != len(set(paths)):
            errors.append(f'{relative}: duplicate creative asset path')
        for row in assets:
            path = row.get('path', '')
            asset_path = Path(path)
            if (not isinstance(path, str) or path not in allowed or asset_path.is_absolute()
                    or '..' in asset_path.parts or folder not in asset_path.parents
                    or asset_path.suffix.lower() not in ASSET_SUFFIXES
                    or row.get('origin') not in ('generated', 'native_vector')
                    or not isinstance(row.get('generator'), str) or not row['generator'].strip()
                    or row.get('privacy_review') != 'passed'
                    or row.get('source_article_sha256') != receipt['source_article_sha256']):
                errors.append(f'{relative}: invalid creative asset provenance')
                continue
            full_asset = ROOT / asset_path
            if (not full_asset.is_file() or full_asset.is_symlink() or ROOT not in full_asset.resolve().parents
                    or row.get('sha256') != hashlib.sha256(full_asset.read_bytes()).hexdigest()):
                errors.append(f'{relative}: creative asset bytes do not match provenance')
            if path == relative:
                asset = row
        if (valid_image or valid_overlay) and asset is None:
            errors.append(f'{relative}: creative asset is not listed in its receipt')
    except (OSError, ValueError, KeyError, TypeError):
        errors.append(f'{relative}: invalid creative export receipt')
    return errors, asset


def _valid_raster(data, suffix):
    if suffix == '.png':
        return data.startswith(b'\x89PNG\r\n\x1a\n')
    if suffix in ('.jpg', '.jpeg'):
        return data.startswith(b'\xff\xd8\xff')
    if suffix == '.webp':
        return data[:4] == b'RIFF' and data[8:12] == b'WEBP'
    return False


def _safe_svg(body):
    if re.search(r'<!DOCTYPE|<!ENTITY', body, re.I):
        return False
    try:
        root = ET.fromstring(body)
        if root.tag.rsplit('}', 1)[-1] != 'svg':
            return False
        for node in root.iter():
            if node.tag.rsplit('}', 1)[-1].lower() in ('script', 'foreignobject', 'iframe', 'image',
                                                      'animate', 'animatemotion', 'animatetransform', 'set'):
                return False
            if node.tag.rsplit('}', 1)[-1].lower() == 'style' and re.search(
                    r'@import|url\((?!\s*#)|javascript:|expression\(', node.text or '', re.I):
                return False
            for key, value in node.attrib.items():
                name = key.rsplit('}', 1)[-1].lower()
                if name.startswith('on') or name == 'href' and not value.startswith('#'):
                    return False
                if re.search(r'url\((?!\s*#)|javascript:', value, re.I):
                    return False
        return True
    except ET.ParseError:
        return False


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
        if 'test-articles' in p.parts:
            fixture_prefix = ('docs', 'editorial', 'test-articles')
            if (len(p.parts) != 5 or p.parts[:3] != fixture_prefix
                    or p.parts[3] not in FIXTURE_IDS or p.name not in FIXTURE_FILES):
                errors.append(f'{relative}: not an authorized generated fixture path')
                continue
            receipt_path = p.parent / 'manifest.json'
            if receipt_path.as_posix() not in allowed:
                errors.append(f'{relative}: fixture export receipt is not allowlisted')
                continue
            try:
                receipt = json.loads((ROOT / receipt_path).read_text(encoding='utf-8'))
                if (receipt.get('export_scope') != 'explicitly_authorized_a07_a08_fixture'
                        or receipt.get('content_id') != p.parts[3]
                        or receipt.get('contains_private_source') is not False
                        or receipt.get('contains_legacy_draft') is not False
                        or receipt.get('publication_allowed') is not False):
                    errors.append(f'{relative}: invalid generated fixture export receipt')
                    continue
            except (OSError, ValueError, TypeError):
                errors.append(f'{relative}: missing generated fixture export receipt')
                continue
        creative_asset = None
        if 'creative-fixtures' in p.parts:
            creative_errors, creative_asset = _creative_check(relative, allowed)
            if creative_errors:
                errors.extend(creative_errors)
                continue
        full = ROOT / p
        if not full.is_file() or full.is_symlink() or ROOT not in full.resolve().parents:
            errors.append(f'{relative}: missing file or unsafe resolution')
            continue
        data = full.read_bytes()
        if p.suffix.lower() in RASTER_SUFFIXES:
            if creative_asset is None or not _valid_raster(data, p.suffix.lower()):
                errors.append(f'{relative}: raster requires generated provenance and matching media signature')
            if any(value.encode('utf-8') in data for value in private_fragments | private_identifiers):
                errors.append(f'{relative}: private source metadata in raster')
            metadata_text = data.decode('utf-8', errors='ignore')
            for name, pattern in CONTENT_PATTERNS.items():
                if pattern.search(metadata_text):
                    errors.append(f'{relative}: {name} in raster metadata')
            # Rendering/semantic image review is separate from this byte and provenance check.
            continue
        try:
            body = full.read_text(encoding='utf-8')
        except UnicodeError:
            errors.append(f'{relative}: binary exports require separate review')
            continue
        if creative_asset is not None and p.suffix.lower() == '.svg' and not _safe_svg(body):
            errors.append(f'{relative}: unsafe or externally linked native SVG')
        for name, pattern in CONTENT_PATTERNS.items():
            if pattern.search(body):
                errors.append(f'{relative}: {name}')
        if any(value in body for value in private_identifiers):
            errors.append(f'{relative}: private source identifier')
        if any(value in body for value in private_fragments):
            errors.append(f'{relative}: retained private source passage')
        if relative == 'docs/editorial/existing-content-index.json':
            try:
                inventory = json.loads(body)
                scope = inventory['scope']
                if (inventory.get('items') != [] or inventory.get('duplicates') != []
                        or scope.get('source_type') != 'user_confirmation'
                        or scope.get('expected_count') != 0 or scope.get('imported_count') != 0):
                    errors.append(f'{relative}: only the user-confirmed empty inventory is public')
            except (ValueError, KeyError, TypeError):
                errors.append(f'{relative}: invalid empty-inventory fixture')
        if relative == 'docs/editorial/test-content-index.json':
            try:
                items = json.loads(body)['items']
                if len(items) != 3 or {row['content_id'] for row in items} != FIXTURE_IDS:
                    errors.append(f'{relative}: only the three authorized generated fixtures may be indexed')
                for row in items:
                    if (row.get('status') != 'test_draft' or row.get('wordpress_post_id') is not None
                            or row.get('url') is not None or row.get('publish_date') is not None):
                        errors.append(f'{relative}: real article record is not public-fixture data')
            except (ValueError, KeyError, TypeError):
                errors.append(f'{relative}: invalid test-fixture index')
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
