#!/usr/bin/env python3
"""Verify authorized generated fixtures without granting publication approval."""
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.validate_editorial import load, validate, audit_schema
from fortune_labo.editorial.production import verify_run
from fortune_labo.editorial.importer import inventory_view
from fortune_labo.editorial.strategy import canonical_hash


def verify(root=ROOT):
    editorial = root / 'docs/editorial'
    index = load(editorial / 'test-content-index.json')
    actual = load(editorial / 'existing-content-index.json')
    view = load(editorial / 'unified-content-view.json')
    for data, name in [(index, 'test_content_index'), (actual, 'existing_content_inventory'),
                       (view, 'unified_content_view'),
                       (load(editorial / 'content-opportunity-index.json'), 'content_opportunity_index')]:
        schema = load(editorial / ('schemas/' + name + '.schema.json'))
        audit_schema(schema)
        validate(data, schema)
    if view != inventory_view(actual, index):
        raise ValueError('Unified view has drifted from its source indexes')
    if view['counts'] != {'existing': 0, 'test_fixtures': 3, 'total_records': 3}:
        raise ValueError('Fixture and existing counts must remain separate')
    if {item['content_id'] for item in index['items']} != {'FL-TEST-A', 'FL-TEST-B', 'FL-TEST-C'}:
        raise ValueError('Unexpected authorized fixture set')
    for item in index['items']:
        folder = editorial / 'test-articles' / item['content_id']
        with tempfile.TemporaryDirectory() as private:
            copied = Path(private) / item['content_id']
            shutil.copytree(folder, copied)
            run = verify_run(copied, private_root=private)
        brief = load(folder / 'brief.json')
        qa = load(folder / 'qa.json')
        validate(qa, load(editorial / 'schemas/qa_handoff.schema.json'))
        if qa['brief_sha256'] != canonical_hash(brief) or qa['draft_sha256'] != run['draft_sha256']:
            raise ValueError('QA references a different brief or draft')
        if qa['seo_policy_version'] != brief['seo_policy_version']:
            raise ValueError('QA policy trace mismatch')
        if [stage['agent'] for stage in qa['stages']] != ['A29', 'A32', 'A28']:
            raise ValueError('QA stage order mismatch')
        for field in ['content_id', 'title', 'genre', 'search_intent', 'access_type', 'content_depth', 'seo_policy_version']:
            if item[field] != brief[field]:
                raise ValueError('Index/brief mismatch: ' + field)
        if item['primary_keyword'] != brief['keyword'] or item['internal_links'] != brief['internal_link_candidates']:
            raise ValueError('Index keyword/link intent drift')
        if not load(folder / 'claims.json')['claims']:
            raise ValueError('Claim extraction missing')
        for relative in item['artifacts'].values():
            path = (root / relative).resolve()
            if root.resolve() not in path.parents or not path.is_file():
                raise ValueError('Missing or unsafe artifact')
    return {'existing': 0, 'test_fixtures': 3, 'publication_allowed': False}


if __name__ == '__main__':
    print('PASS: ' + json.dumps(verify()))
