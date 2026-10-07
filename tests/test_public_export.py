"""Public export rejects private data even when a path was manually allowed."""
import importlib.util
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

SCANNER = Path(__file__).resolve().parents[1] / 'scripts/check_public_export.py'
spec = importlib.util.spec_from_file_location('public_export', SCANNER)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PublicExportTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name).resolve()
        self.original = module.ROOT
        module.ROOT = self.root

    def tearDown(self):
        module.ROOT = self.original
        self.directory.cleanup()

    def scan(self, body, filename='allowed.md', reference=None):
        target = self.root / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body)
        manifest = self.root / 'manifest.json'
        manifest.write_text(json.dumps({'files': [filename]}))
        return module.scan(manifest, private_reference=reference)

    def test_allow_public_summary(self):
        self.assertEqual([], self.scan('公開用の編集ルール。Source reference: GR001。'))

    def test_reject_private_url_even_in_allowlisted_file(self):
        body = 'https://' + 'docs.' + 'google.com/document/d/' + 'synthetic-private-id'
        self.assertTrue(self.scan(body))

    def test_reject_private_artifact_path(self):
        self.assertTrue(self.scan('本文', 'test-articles/article.md'))

    def test_allow_only_receipted_generated_fixtures(self):
        folder = self.root / 'docs/editorial/test-articles/FL-TEST-A'
        folder.mkdir(parents=True)
        receipt = {'export_scope': 'explicitly_authorized_a07_a08_fixture',
                   'content_id': 'FL-TEST-A', 'contains_private_source': False,
                   'contains_legacy_draft': False, 'publication_allowed': False}
        (folder / 'manifest.json').write_text(json.dumps(receipt))
        (folder / 'article.md').write_text('# 新しい生成Fixture\n\n架空の説明例。')
        manifest = self.root / 'manifest.json'
        paths = [str((folder / name).relative_to(self.root)) for name in ['article.md', 'manifest.json']]
        manifest.write_text(json.dumps({'files': paths}))
        self.assertEqual([], module.scan(manifest))
        receipt['contains_legacy_draft'] = True
        (folder / 'manifest.json').write_text(json.dumps(receipt))
        self.assertTrue(module.scan(manifest))

    def test_reject_unreceipted_fixture(self):
        self.assertTrue(self.scan('本文', 'docs/editorial/test-articles/FL-TEST-A/article.md'))

    def test_reject_fourth_fixture(self):
        self.assertTrue(self.scan('本文', 'docs/editorial/test-articles/FL-TEST-D/article.md'))

    def test_public_existing_inventory_stays_empty(self):
        value = {'scope': {'source_type': 'user_confirmation', 'expected_count': 0,
                           'imported_count': 0}, 'items': [], 'duplicates': []}
        path = 'docs/editorial/existing-content-index.json'
        self.assertEqual([], self.scan(json.dumps(value), path))
        value['items'].append({'wordpress_post_id': 42, 'title': 'Actual post'})
        self.assertTrue(self.scan(json.dumps(value), path))

    def test_public_fixture_index_cannot_contain_live_post(self):
        items = [{'content_id': cid, 'status': 'test_draft', 'wordpress_post_id': None,
                  'url': None, 'publish_date': None} for cid in sorted(module.FIXTURE_IDS)]
        path = 'docs/editorial/test-content-index.json'
        self.assertEqual([], self.scan(json.dumps({'items': items}), path))
        items[0]['wordpress_post_id'] = 42
        self.assertTrue(self.scan(json.dumps({'items': items}), path))

    def test_reject_private_paragraph_reference(self):
        self.assertTrue(self.scan('GR' + '001:P001'))

    def test_reject_long_original_passage(self):
        body = 'これは検査専用に作った非公開テキストであり実資料ではない。' * 3
        reference = self.root / 'private.json'
        reference.write_text(json.dumps({'body': body}, ensure_ascii=False))
        self.assertTrue(self.scan(body, reference=reference))

    def test_provenance_forbids_extra_field(self):
        record = {'source_id': 'GR001', 'source_type': 'private_research_document',
                  'source_title': 'Private editorial source 01', 'access_scope': 'private',
                  'derived_artifacts': [], 'body': 'Do not export'}
        self.assertTrue(self.scan(json.dumps({'sources': [record]}), 'provenance.json'))

    def test_reject_unlisted_file(self):
        manifest = self.root / 'manifest.json'
        manifest.write_text(json.dumps({'files': []}))
        self.assertTrue(module.scan(manifest, ['not-allowed.md']))

    def test_reject_traversal(self):
        manifest = self.root / 'manifest.json'
        manifest.write_text(json.dumps({'files': ['../outside.txt']}))
        self.assertTrue(module.scan(manifest))

    def creative_fixture(self, asset_bytes=b'\x89PNG\r\n\x1a\nfixture', suffix='.png', origin='generated'):
        article_rel = 'docs/editorial/test-articles/FL-TEST-A/article.md'
        article = self.root / article_rel
        article.parent.mkdir(parents=True)
        article.write_text('# Generated article\n\nAn illustrative test.')
        digest = hashlib.sha256(article.read_bytes()).hexdigest()
        asset_rel = 'docs/editorial/creative-fixtures/FL-TEST-A/images/featured' + suffix
        asset = self.root / asset_rel
        asset.parent.mkdir(parents=True)
        asset.write_bytes(asset_bytes)
        receipt_rel = 'docs/editorial/creative-fixtures/FL-TEST-A/manifest.json'
        receipt = {'export_scope': 'explicitly_authorized_creative_fixture',
                   'content_id': 'FL-TEST-A', 'contains_private_source': False,
                   'contains_legacy_draft': False, 'publication_allowed': False,
                   'source_article_ref': article_rel, 'source_article_sha256': digest,
                   'assets': [{'path': asset_rel, 'sha256': hashlib.sha256(asset_bytes).hexdigest(),
                               'origin': origin, 'generator': 'synthetic-test',
                               'source_article_sha256': digest, 'privacy_review': 'passed'}]}
        (self.root / receipt_rel).write_text(json.dumps(receipt))
        manifest = self.root / 'creative-manifest.json'
        manifest.write_text(json.dumps({'files': [article_rel, asset_rel, receipt_rel]}))
        return manifest, asset_rel, article

    def test_allow_provenance_bound_generated_raster(self):
        manifest, asset, _ = self.creative_fixture()
        self.assertEqual([], module.scan(manifest, [asset]))

    def test_reject_stale_creative_source_article(self):
        manifest, asset, article = self.creative_fixture()
        article.write_text('# Changed article')
        self.assertTrue(module.scan(manifest, [asset]))

    def test_reject_changed_creative_asset(self):
        manifest, asset, _ = self.creative_fixture()
        (self.root / asset).write_bytes(b'changed')
        self.assertTrue(module.scan(manifest, [asset]))

    def test_reject_non_generated_asset(self):
        manifest, asset, _ = self.creative_fixture(origin='private_reference_photo')
        self.assertTrue(module.scan(manifest, [asset]))

    def test_reject_fake_raster_signature(self):
        manifest, asset, _ = self.creative_fixture(asset_bytes=b'Not a raster')
        self.assertTrue(module.scan(manifest, [asset]))

    def test_reject_private_locator_in_raster_metadata(self):
        data = b'\x89PNG\r\n\x1a\n' + ('https://' + 'docs.' + 'google.com/document/d/private-test').encode()
        manifest, asset, _ = self.creative_fixture(asset_bytes=data)
        self.assertTrue(module.scan(manifest, [asset]))

    def test_allow_safe_native_vector(self):
        svg = b'<svg xmlns="http://www.w3.org/2000/svg"><text x="1" y="10">Example</text></svg>'
        manifest, asset, _ = self.creative_fixture(svg, '.svg', 'native_vector')
        self.assertEqual([], module.scan(manifest, [asset]))

    def test_reject_executable_native_vector(self):
        svg = b'<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>'
        manifest, asset, _ = self.creative_fixture(svg, '.svg', 'native_vector')
        self.assertTrue(module.scan(manifest, [asset]))

    def test_reject_external_stylesheet_in_native_vector(self):
        svg = b'<svg xmlns="http://www.w3.org/2000/svg"><style>@import "remote.css";</style></svg>'
        manifest, asset, _ = self.creative_fixture(svg, '.svg', 'native_vector')
        self.assertTrue(module.scan(manifest, [asset]))


if __name__ == '__main__':
    unittest.main()
