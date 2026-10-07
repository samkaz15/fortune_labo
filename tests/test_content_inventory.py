"""Synthetic fixtures only: no live article, private URL or research content."""
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest

from fortune_labo.editorial.importer import import_rest, import_wxr, fetch_public_rest, write_private_json, inventory_view
from fortune_labo.editorial.classification import classify_article, classify_inventory
from fortune_labo.editorial.opportunities import generate_opportunities
from fortune_labo.editorial.performance import empty_observation, validate_observation, performance_context

POST = {'id': 7, 'title': {'rendered': '仕事 &amp; 暮らし'}, 'slug': 'work',
        'link': 'https://example.invalid/work/', 'status': 'publish', 'type': 'post',
        'date_gmt': '2026-01-01T00:00:00', 'modified_gmt': '2026-01-02T00:00:00',
        'content': {'rendered': '<p>仕事の整理 one two</p><script>secret</script><a href="/guide/">次へ</a><a href="https://outside.invalid/">外</a>'},
        'categories': [3], 'tags': [], 'featured_media': 9,
        '_embedded': {'wp:term': [[{'id': 3, 'name': '仕事', 'slug': 'career', 'taxonomy': 'category'}]],
                      'wp:featuredmedia': [{'id': 9, 'source_url': 'https://example.invalid/image.png', 'alt_text': '机'}]},
        'meta': {'access': 'FREE', 'editorial_genre': 'career'}}
TAXONOMY = {'version': 'test-1', 'genres': [{'genre_id': 'career', 'genre_name': '仕事', 'subgenres': []},
                                           {'genre_id': 'love', 'genre_name': '恋愛', 'subgenres': []}]}
INTELLIGENCE = {'version': 'test-1', 'genres': [{'genre_id': 'career', 'free_content_role': '一般的な疑問を解決する',
                   'premium_content_role': '条件別の行動計画と振り返り', 'seo_role': '検索入口',
                   'engagement_role': '理解', 'conversion_role': '相談判断', 'retention_role': '振り返り'},
                   {'genre_id': 'love', 'free_content_role': '一般的な整理', 'premium_content_role': '条件別の計画'}]}
TOPIC = {'genre': 'career', 'topic': '仕事の整理', 'keyword': '働き方の整理', 'search_intent': 'informational',
         'reader_need': '条件を整理する', 'free_premium_candidate': 'FREE', 'evidence_refs': ['synthetic:topic-1']}


class InventoryTests(unittest.TestCase):
    def test_import_fields_and_unknowns(self):
        result = import_rest([POST], 'synthetic-site')
        item = result['items'][0]
        self.assertEqual(item['title'], '仕事 & 暮らし')
        self.assertEqual(item['category'][0], {'id': 3, 'name': '仕事', 'slug': 'career'})
        self.assertEqual(item['featured_image']['wordpress_media_id'], 9)
        self.assertEqual(item['internal_links'], ['https://example.invalid/guide/'])
        self.assertEqual(item['publish_date'], '2026-01-01T00:00:00Z')
        self.assertEqual(item['word_count'], 10)  # 5+2+2+1 CJK/token units.
        self.assertIsNone(item['genre'])
        self.assertIsNone(item['access_type'])  # Public HTTP visibility does not prove membership tier.
        self.assertIsNone(item['seo_policy_version'])
        self.assertNotIn('content', item)
        self.assertNotIn('secret', json.dumps(result))

    def test_stable_namespace_dedup_and_conflict(self):
        first = import_rest([POST, POST], 'a', completeness='complete', coverage_complete=True)
        self.assertEqual(len(first['items']), 1)
        self.assertFalse(first['duplicates'][0]['conflict'])
        self.assertNotEqual(first['items'][0]['content_id'], import_rest([POST], 'b')['items'][0]['content_id'])
        changed = copy.deepcopy(POST)
        changed['title'] = '新しい題名'
        changed['modified_gmt'] = '2026-02-02T00:00:00'
        result = import_rest([POST, changed], 'a', completeness='complete', coverage_complete=True)
        self.assertEqual(result['scope']['completeness'], 'partial')
        self.assertFalse(result['scope']['coverage_complete'])
        self.assertEqual(result['items'][0]['title'], '新しい題名')

    def test_metadata_requires_explicit_mapping(self):
        item = import_rest([POST], 'a', field_map={'access_type': 'meta.access', 'genre': 'meta.editorial_genre'})['items'][0]
        self.assertEqual(item['access_type'], 'FREE')
        self.assertEqual(item['field_provenance']['genre'], 'wordpress_metadata:meta.editorial_genre')

    def test_missing_and_protected_body_are_unknown(self):
        for content in (None, {'protected': True, 'rendered': '<p>password prompt</p>'}):
            post = dict(POST, content=content)
            item = import_rest([post], 'a')['items'][0]
            self.assertIsNone(item['word_count'])
            self.assertIsNone(item['internal_links'])
            self.assertFalse(item['body_available'])

    def test_reject_invalid_identity(self):
        for value in (None, 0, True, '7'):
            with self.assertRaises(ValueError):
                import_rest([dict(POST, id=value)], 'a')

    def test_wxr_post_status_media_and_terms(self):
        wxr = '''<rss xmlns:wp="http://wordpress.org/export/1.2/" xmlns:content="http://purl.org/rss/1.0/modules/content/"><channel>
        <wp:wxr_version>1.2</wp:wxr_version><link>https://example.invalid</link>
        <wp:category><wp:term_id>3</wp:term_id><wp:category_nicename>career</wp:category_nicename><wp:cat_name>仕事</wp:cat_name></wp:category>
        <item><wp:post_id>9</wp:post_id><wp:post_type>attachment</wp:post_type><wp:attachment_url>https://example.invalid/image.png</wp:attachment_url></item>
        <item><title>仕事 &amp; 時間</title><link>https://example.invalid/work/</link><wp:post_id>7</wp:post_id><wp:post_type>post</wp:post_type>
        <wp:status>draft</wp:status><wp:post_name>work</wp:post_name><wp:post_date_gmt>0000-00-00 00:00:00</wp:post_date_gmt>
        <content:encoded><![CDATA[<p>整理</p>]]></content:encoded><category domain="category" nicename="career">仕事</category>
        <wp:postmeta><wp:meta_key>_thumbnail_id</wp:meta_key><wp:meta_value>9</wp:meta_value></wp:postmeta></item></channel></rss>'''
        inventory = import_wxr(wxr, 'synthetic', complete_export=True)
        item = inventory['items'][0]
        self.assertEqual(item['status'], 'draft')
        self.assertIsNone(item['publish_date'])
        self.assertEqual(item['featured_image']['url'], 'https://example.invalid/image.png')
        self.assertEqual(item['category'][0]['id'], 3)
        self.assertEqual(inventory['scope']['completeness'], 'complete')
        with self.assertRaises(ValueError):
            import_wxr('<!DOCTYPE rss []>' + wxr, 'synthetic')

    def test_pagination_get_only_and_public_scope(self):
        calls = []
        class Response(io.BytesIO):
            headers = {'X-WP-Total': '2', 'X-WP-TotalPages': '2'}
        def opener(request, timeout):
            calls.append(request)
            post = dict(POST, id=len(calls))
            return Response(json.dumps([post]).encode())
        inventory = fetch_public_rest('https://example.invalid', 'test', opener=opener)
        self.assertEqual(len(calls), 2)
        self.assertTrue(all(call.method == 'GET' for call in calls))
        self.assertIn('page=2', calls[1].full_url)
        self.assertEqual(len(inventory['items']), 2)
        self.assertEqual(inventory['scope']['completeness'], 'partial')
        self.assertTrue(inventory['scope']['coverage_complete'])

    def test_changing_pagination_is_incomplete(self):
        calls = []
        class Response(io.BytesIO):
            pass
        def opener(request, timeout):
            calls.append(request)
            response = Response(json.dumps([dict(POST, id=len(calls))]).encode())
            response.headers = {'X-WP-Total': str(len(calls) + 1), 'X-WP-TotalPages': '2'}
            return response
        self.assertFalse(fetch_public_rest('https://example.invalid', 'test', opener=opener)['scope']['coverage_complete'])

    def test_private_write_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(ValueError):
                write_private_json({'secret': 'private'}, root/'docs'/'index.json', repository=root)
            output = root/'.private'/'index.json'
            write_private_json({'count': 1}, output, repository=root)
            self.assertEqual(json.loads(output.read_text()), {'count': 1})
            self.assertEqual(output.stat().st_mode & 0o777, 0o600)


class ClassificationTests(unittest.TestCase):
    def test_existing_article_candidate_does_not_mutate(self):
        record = import_rest([POST], 'test', field_map={'access_type': 'meta.access'})['items'][0]
        original = copy.deepcopy(record)
        result = classify_article(record, INTELLIGENCE, TAXONOMY)
        self.assertEqual(result['candidates']['genre']['value'], 'career')
        self.assertEqual(result['candidates']['genre']['confidence'], 'medium')
        self.assertEqual(result['candidates']['access_type']['value'], 'FREE')
        self.assertIsNone(result['candidates']['subgenre']['value'])
        self.assertTrue(result['human_review_required'])
        self.assertEqual(record, original)

    def test_unknown_and_ambiguous_classification(self):
        record = import_rest([dict(POST, categories=[], title='お知らせ')], 'test')['items'][0]
        result = classify_article(record, INTELLIGENCE, TAXONOMY)
        self.assertEqual(result['status'], 'unclassified')
        self.assertEqual(result['confidence'], 'low')
        self.assertTrue(all(v['value'] is None for v in result['candidates'].values()))
        record['category'] = [{'name': '仕事'}, {'name': '恋愛'}]
        self.assertIsNone(classify_article(record, INTELLIGENCE, TAXONOMY)['candidates']['genre']['value'])

    def test_paid_keyword_does_not_imply_premium(self):
        record = import_rest([dict(POST, title='仕事 PREMIUM 有料 無料')], 'test')['items'][0]
        self.assertIsNone(classify_article(record, INTELLIGENCE, TAXONOMY)['candidates']['access_type']['value'])

    def test_formal_commercial_intent_is_preserved(self):
        record = import_rest([POST], 'test')['items'][0]
        record['search_intent'] = 'commercial'
        result = classify_article(record, INTELLIGENCE, TAXONOMY)
        self.assertEqual(result['candidates']['search_intent']['value'], 'commercial')
        self.assertEqual(result['candidates']['search_intent']['confidence'], 'high')

    def test_unapproved_commercial_alias_needs_explicit_mapping(self):
        record = import_rest([POST], 'test')['items'][0]
        record['search_intent'] = 'commercial_investigation'
        result = classify_article(record, INTELLIGENCE, TAXONOMY)
        self.assertIsNone(result['candidates']['search_intent']['value'])
        self.assertEqual(result['candidates']['search_intent']['confidence'], 'low')
        mapped = classify_article(record, INTELLIGENCE, TAXONOMY,
                                  mappings={'intent_terms': {'仕事': 'commercial'}})
        self.assertEqual(mapped['candidates']['search_intent']['value'], 'commercial')
        self.assertEqual(mapped['candidates']['search_intent']['confidence'], 'medium')
        invalid_mapping = classify_article(record, INTELLIGENCE, TAXONOMY,
                                           mappings={'intent_terms': {'仕事': 'commercial_investigation'}})
        self.assertIsNone(invalid_mapping['candidates']['search_intent']['value'])
        self.assertEqual(record['search_intent'], 'commercial_investigation')

    def test_count_definitions(self):
        inventory = import_rest([POST, dict(POST, id=8, categories=[])], 'test')
        result = classify_inventory(inventory, INTELLIGENCE, TAXONOMY)
        self.assertEqual(result['counts'], {'total': 2, 'classified': 1, 'unclassified': 1, 'human_review': 2})


class OpportunityTests(unittest.TestCase):
    def test_gap_candidate_not_unwritten_claim_when_partial(self):
        result = generate_opportunities(import_rest([POST], 'test'), [TOPIC, TOPIC])
        self.assertEqual(len(result['opportunities']), 1)
        self.assertEqual(result['opportunities'][0]['coverage_status'], 'potential_gap')
        self.assertIsNone(result['opportunities'][0]['priority_candidate'])
        self.assertEqual(result['opportunities'][0]['evidence_refs'], ['synthetic:topic-1'])

    def test_overlap_suppression_stable_id(self):
        inventory = import_rest([POST], 'test')
        first = generate_opportunities(inventory, [TOPIC])['opportunities'][0]
        inventory['items'][0]['primary_keyword'] = TOPIC['keyword']
        result = generate_opportunities(inventory, [TOPIC])
        self.assertFalse(result['opportunities'])
        self.assertEqual(result['suppressed'][0]['opportunity_id'], first['opportunity_id'])
        self.assertEqual(result['suppressed'][0]['existing_content_overlap'][0]['reasons'], ['same_registered_keyword'])

    def test_evidence_and_numeric_score_rejected(self):
        inventory = import_rest([], 'test')
        for topic in (dict(TOPIC, evidence_refs=[]), dict(TOPIC, priority_candidate=80)):
            with self.assertRaises(ValueError):
                generate_opportunities(inventory, [topic])


    def test_registered_drafts_prevent_duplicate_opportunities(self):
        existing = import_rest([], 'test')
        draft = {'content_id': 'TEST-DRAFT', 'title': 'Different title', 'primary_keyword': TOPIC['keyword'], 'search_intent': 'informational'}
        result = generate_opportunities(existing, [TOPIC], draft_index={'items': [draft]})
        self.assertFalse(result['opportunities'])
        self.assertEqual(result['suppressed'][0]['existing_content_overlap'][0]['content_id'], 'TEST-DRAFT')

    def test_explicit_editorial_overlap_needs_traceable_ids(self):
        existing = import_rest([], 'test')
        original = generate_opportunities(existing, [TOPIC])['opportunities'][0]
        draft = {'content_id': 'TEST-DRAFT', 'title': 'Different wording', 'search_intent': 'informational'}
        review = {'opportunity_id': original['opportunity_id'], 'content_ids': ['TEST-DRAFT'],
                  'evidence_refs': ['synthetic:editor-review'], 'reason': 'Reviewed topic coverage in an existing draft.'}
        result = generate_opportunities(existing, [TOPIC], draft_index={'items': [draft]}, reviewed_overlaps=[review])
        self.assertEqual(len(result['suppressed']), 1)
        self.assertIn('synthetic:editor-review', result['suppressed'][0]['evidence_refs'])
        self.assertEqual(result['suppressed'][0]['existing_content_overlap'][0]['reasons'], ['reviewed_editorial_overlap'])
        self.assertTrue(result['suppressed'][0]['human_review_required'])
        for key, value in [('content_ids', ['MISSING']), ('opportunity_id', 'unknown-opportunity'), ('evidence_refs', [])]:
            invalid = dict(review, **{key: value})
            with self.subTest(key=key), self.assertRaises(ValueError):
                generate_opportunities(existing, [TOPIC], draft_index={'items': [draft]}, reviewed_overlaps=[invalid])


class PerformanceTests(unittest.TestCase):
    def test_unconnected_metrics_are_null_not_zero(self):
        observation = empty_observation('synthetic-1', 'GA4', '2026-01-01', '2026-01-31')
        self.assertEqual(len(observation['metrics']), 17)
        self.assertTrue(all(value is None for value in observation['metrics'].values()))
        self.assertEqual(validate_observation(observation), observation)

    def test_raw_metric_trace_and_scale(self):
        observation = empty_observation('synthetic-1', 'Search Console', '2026-01-01', '2026-01-31')
        observation['metrics']['ctr'] = 0.1
        with self.assertRaises(ValueError):
            validate_observation(observation)
        observation['collected_at'] = '2026-02-01T00:00:00Z'
        observation['source_reference'] = 'private-import:synthetic'
        observation['metric_metadata']['ctr'].update(source_metric='ctr', definition='clicks / impressions', aggregation='source_report_ratio')
        validate_observation(observation)
        for value in (10, -1, float('nan'), True):
            observation['metrics']['ctr'] = value
            with self.assertRaises(ValueError):
                validate_observation(observation)

    def test_scores_and_reversed_period_rejected(self):
        observation = empty_observation('test', 'WordPress', '2026-01-01', '2026-01-31')
        observation['metrics']['score'] = 100
        with self.assertRaises(ValueError):
            validate_observation(observation)
        observation = empty_observation('test', 'SNS', '2026-01-31', '2026-01-01')
        with self.assertRaises(ValueError):
            validate_observation(observation)


class PerformanceFeedbackTests(unittest.TestCase):
    def observation(self, source, metric, value):
        item = empty_observation('synthetic-1', source, '2026-01-01', '2026-01-31', timezone='UTC',
                                 source_reference='private-report:' + source)
        item['collected_at'] = '2026-02-01T00:00:00Z'
        item['metrics'][metric] = value
        item['metric_metadata'][metric].update(source_metric=metric, definition='synthetic test metric', aggregation='source_report')
        return item

    def context(self, items):
        return performance_context(items, content_id='synthetic-1', period_start='2026-01-01', period_end='2026-01-31', timezone='UTC')

    def test_sources_units_and_raw_provenance_survive_feedback(self):
        gsc = self.observation('Search Console', 'clicks', 0)
        ga4 = self.observation('GA4', 'scroll_depth', 75)
        original = copy.deepcopy([gsc, ga4])
        context = self.context([gsc, ga4])
        self.assertEqual(context['metric_groups']['seo']['clicks'], 0)
        self.assertEqual(context['metric_groups']['engagement']['scroll_depth'], 75)
        self.assertEqual(context['observed_groups'], ['seo', 'engagement'])
        self.assertEqual(context['evidence_refs'], ['private-report:GA4', 'private-report:Search Console'])
        self.assertEqual(context['raw_observations'], original)
        self.assertEqual(context['raw_observations'][1]['metric_metadata']['scroll_depth']['unit'], 'percent')
        context['raw_observations'][0]['filters']['test'] = 'changed-copy'
        self.assertEqual([gsc, ga4], original)

    def test_mixed_reporting_scopes_rejected(self):
        for key, value in [('period_start', '2026-01-02'), ('period_end', '2026-02-01'), ('timezone', 'Asia/Tokyo'),
                           ('content_id', 'another'), ('filters', {'country': 'JP'}), ('dimensions', {'device': 'mobile'})]:
            item = self.observation('GA4', 'users', 10)
            item[key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'selected reporting scope'):
                self.context([item])

    def test_ambiguous_metric_provider_and_definition_version_rejected(self):
        ga4 = self.observation('GA4', 'users', 10)
        wordpress = self.observation('WordPress', 'users', 10)
        with self.assertRaisesRegex(ValueError, 'same metric'):
            self.context([ga4, wordpress])
        gsc = self.observation('Search Console', 'clicks', 10)
        gsc['definition_version'] = 'another-version'
        with self.assertRaisesRegex(ValueError, 'definition versions'):
            self.context([ga4, gsc])

    def test_unmeasured_and_missing_provenance(self):
        context = self.context([])
        self.assertEqual(context['status'], 'unmeasured')
        self.assertEqual(context['observed_groups'], [])
        item = self.observation('GA4', 'sessions', 10)
        item['source_reference'] = None
        with self.assertRaisesRegex(ValueError, 'source reference'):
            self.context([item])
        item = self.observation('GA4', 'sessions', 10)
        item['score'] = 100
        with self.assertRaisesRegex(ValueError, 'unknown field'):
            self.context([item])


class InventorySchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from scripts.validate_editorial import validate, audit_schema
        cls.validate = staticmethod(validate)
        cls.audit_schema = staticmethod(audit_schema)
        cls.root = Path(__file__).resolve().parents[1]

    def check(self, name, record):
        schema = json.loads((self.root/'docs/editorial/schemas'/f'{name}.schema.json').read_text())
        self.audit_schema(schema)
        self.validate(record, schema)

    def test_all_contract_shapes(self):
        inventory = import_rest([POST], 'synthetic')
        self.check('existing_content_inventory', inventory)
        self.check('existing_article_classification', classify_article(inventory['items'][0], INTELLIGENCE, TAXONOMY))
        self.check('content_opportunity_index', generate_opportunities(inventory, [TOPIC]))
        self.check('performance_observation', empty_observation('synthetic', 'GA4', '2026-01-01', '2026-01-31'))

    def test_confirmed_empty_state_and_public_opportunities(self):
        for name, filename in [('existing_content_inventory', 'existing-content-index.json'),
                               ('content_opportunity_index', 'content-opportunity-index.json')]:
            record = json.loads((self.root/'docs/editorial'/filename).read_text())
            self.check(name, record)
        inventory = json.loads((self.root/'docs/editorial/existing-content-index.json').read_text())
        self.assertEqual(inventory['scope']['source_type'], 'user_confirmation')
        self.assertEqual(inventory['items'], [])

    def test_combined_view_preserves_actual_vs_fixture_counts(self):
        existing = import_rest([], 'synthetic')
        test_index = {'items': [{'content_id': 'TEST-1', 'title': '試作用', 'status': 'test_draft', 'genre': 'career',
                                 'access_type': 'FREE', 'internal_links': [{'target_url': None, 'status': 'candidate'}]}]}
        view = inventory_view(existing, test_index)
        self.assertEqual(view['counts'], {'existing': 0, 'test_fixtures': 1, 'total_records': 1})
        self.assertEqual(view['records'][0]['record_type'], 'test_fixture')
        self.assertIsNone(view['records'][0]['metadata']['wordpress_post_id'])
        self.assertIsNone(view['records'][0]['metadata']['word_count'])
        self.assertIsNone(view['records'][0]['metadata']['internal_links'])
        self.check('unified_content_view', view)

    def test_schema_rejects_raw_body_and_low_confidence_without_review(self):
        inventory = import_rest([POST], 'synthetic')
        inventory['items'][0]['body'] = 'must not persist'
        with self.assertRaises(ValueError):
            self.check('existing_content_inventory', inventory)
        candidate = classify_article(import_rest([POST], 'synthetic')['items'][0], INTELLIGENCE, TAXONOMY)
        candidate['human_review_required'] = False
        with self.assertRaises(ValueError):
            self.check('existing_article_classification', candidate)


if __name__ == '__main__':
    unittest.main()
