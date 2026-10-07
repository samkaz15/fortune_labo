"""A25 offline packaging tests; all attachment/post IDs are explicit fakes."""
import copy
import json
from pathlib import Path
import unittest
from fortune_labo.editorial.wordpress_draft import build_draft_payload, digest, canonical_hash, association_plan, execute_draft
from scripts.validate_editorial import validate, audit_schema


class WordPressDraftTests(unittest.TestCase):
    def setUp(self):
        self.article={'content_id':'TEST-A25','title':'確認のための記事','content':'# 確認のための記事\n\n最初の説明。\n\n## 条件を確認する\n\n本文はそのまま残す。\n\n| 項目 | 内容 |\n| --- | --- |\n| 予定 | 自分で確認 |\n',
            'article_version':'article-1.0.0','access_type':'FREE','seo_policy_version':'seo-test-draft',
            'excerpt':None,'slug':None,'categories':None,'tags':None,'internal_links':[],'cta':{'type':'none'},'seo_meta':{'description':'試作の概要'}}
        self.article['draft_sha256']=digest(self.article['content'])
        self.plan={'content_id':'TEST-A25','article_version':'article-1.0.0','visual_style_version':'visual-style-0.1.0',
            'draft_sha256':self.article['draft_sha256'],'images':[
            {'content_id':'TEST-A25','image_id':'featured','placement':'featured','section_heading':None,'generation_status':'generated','alt':'机のイラスト','caption':'説明用イラスト',
             'generated_asset_reference':{'asset_id':'asset-featured','image_sha256':'a'*64,'relative_path':'featured.png','state':'generated','mime_type':'image/png'}},
            {'content_id':'TEST-A25','image_id':'inline-1','placement':'after_h2','section_heading':'条件を確認する','generation_status':'generated','alt':'確認の順番','caption':'順序を示す図',
             'generated_asset_reference':{'asset_id':'asset-inline','image_sha256':'b'*64,'relative_path':'inline.png','state':'generated','mime_type':'image/png'}}]}
        self.qa={'content_id':'TEST-A25','draft_sha256':self.article['draft_sha256'],'image_plan_sha256':canonical_hash(self.plan),'scope':'offline_fixture','blockers':[],
            'gates':{name:{'status':'passed','evidence_ref':'synthetic:'+name,'reviewer_kind':'model_review'} for name in ('A29','A32','A28')}}
        self.receipts=[{'asset_id':'asset-featured','content_id':'TEST-A25','image_sha256':'a'*64,'attachment_id':101,'source_url':'https://example.invalid/featured.png','site_id':'synthetic-site','state':'uploaded','response_reference':'synthetic-response:101','receipt_type':'test_fixture'},
            {'asset_id':'asset-inline','content_id':'TEST-A25','image_sha256':'b'*64,'attachment_id':102,'source_url':'https://example.invalid/inline.png','site_id':'synthetic-site','state':'uploaded','response_reference':'synthetic-response:102','receipt_type':'test_fixture'}]

    def package(self, **kwargs):
        return build_draft_payload(self.article,self.plan,self.qa,**kwargs)

    def ready(self):
        return self.package(media_receipts=self.receipts,site_config={'site_id':'synthetic-site'},fixture_mode=True)

    def refresh(self):
        self.qa['image_plan_sha256']=canonical_hash(self.plan)

    def test_preview_without_upload_has_no_invented_ids(self):
        before=copy.deepcopy([self.article,self.plan,self.qa])
        result=self.package()
        self.assertFalse(result['payload_ready'])
        self.assertFalse(result['network_ready'])
        self.assertIsNone(result['request_payload'])
        self.assertIsNone(result['proposed_payload']['featured_media'])
        self.assertIn('pending image: inline-1',result['proposed_payload']['content'])
        self.assertEqual(result['proposed_payload']['meta'],{})
        self.assertEqual(result['editorial_metadata']['seo_policy_version'],'seo-test-draft')
        self.assertEqual(before,[self.article,self.plan,self.qa])

    def test_fake_upload_receipts_then_draft_association(self):
        result=self.ready()
        self.assertTrue(result['payload_ready'])
        self.assertEqual(result['request_payload']['status'],'draft')
        self.assertEqual(result['request_payload']['featured_media'],101)
        self.assertIn('wp-image-102',result['request_payload']['content'])
        self.assertIn('<figcaption>順序を示す図</figcaption>',result['request_payload']['content'])
        self.assertIn('本文はそのまま残す。',result['request_payload']['content'])
        self.assertIn('<table>',result['request_payload']['content'])
        self.assertNotIn('<h1>',result['request_payload']['content'])
        self.assertNotIn('categories',result['request_payload'])
        post={'site_id':'synthetic-site','id':201,'status':'draft','content_id':'TEST-A25','response_reference':'synthetic:post201','receipt_type':'test_fixture'}
        associations=association_plan(result,post)
        self.assertEqual([row['payload'] for row in associations],[{'post':201},{'post':201}])
        self.assertTrue(all(row['endpoint'].startswith('/wp/v2/media/') for row in associations))

    def test_no_human_approval_needed_for_prepared_draft_but_publish_disabled(self):
        result=self.ready()
        self.assertTrue(result['payload_ready'])
        self.assertTrue(result['human_approval_required_before_publish'])
        self.assertFalse(result['publication_allowed'])
        with self.assertRaisesRegex(RuntimeError,'not connected'):
            execute_draft(result)
        for status in ('publish','future','private','pending'):
            with self.subTest(status=status),self.assertRaisesRegex(ValueError,'draft only'):
                self.package(requested_status=status)

    def test_qa_identity_and_versions_are_bound(self):
        self.qa['content_id']='OTHER'
        with self.assertRaisesRegex(ValueError,'same content ID'):
            self.package()
        self.qa['content_id']='TEST-A25';self.qa['draft_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'stale'):
            self.package()
        self.qa['draft_sha256']=self.article['draft_sha256'];self.plan['article_version']='article-2.0.0'
        with self.assertRaisesRegex(ValueError,'versions differ'):
            self.package()

    def test_each_qa_gate_must_pass_with_evidence(self):
        for key in self.qa['gates']:
            qa=copy.deepcopy(self.qa);qa['gates'][key]['status']='contract_pending'
            result=build_draft_payload(self.article,self.plan,qa,media_receipts=self.receipts,site_config={'site_id':'synthetic-site'},fixture_mode=True)
            self.assertFalse(result['payload_ready'])
            self.assertIn(key+'_not_passed_with_evidence',result['blockers'])
        self.qa['gates']['A29']['evidence_ref']=None
        self.assertFalse(self.package()['payload_ready'])

    def test_failed_or_uncreated_images_stay_incomplete(self):
        self.plan['images'][1]['generation_status']='failed';self.plan['images'][1]['generated_asset_reference']=None;self.refresh()
        result=self.package()
        self.assertIn('image_incomplete:inline-1',result['blockers'])
        self.assertIsNone(result['inline_media'][0]['attachment_id'])

    def test_fake_ids_and_unrelated_receipts_rejected_in_normal_mode(self):
        with self.assertRaisesRegex(ValueError,'fixture attachment'):
            self.package(media_receipts=self.receipts,site_config={'site_id':'synthetic-site'})
        self.receipts[0]['image_sha256']='c'*64
        with self.assertRaisesRegex(ValueError,'identity mismatch'):
            self.ready()

    def test_dedup_and_retry_keep_stable_identity(self):
        self.plan['images'][1]['generated_asset_reference']=copy.deepcopy(self.plan['images'][0]['generated_asset_reference']);self.refresh()
        result=self.package()
        self.assertEqual(len(result['media_upload_plan']),1)
        failed=dict(self.receipts[0],state='failed',attachment_id=None,source_url=None)
        retry=self.package(media_receipts=[failed],site_config={'site_id':'synthetic-site'},fixture_mode=True)
        again=self.package(media_receipts=[failed],site_config={'site_id':'synthetic-site'},fixture_mode=True)
        self.assertEqual(retry['media_upload_plan'][0]['action'],'retry_upload')
        self.assertEqual(retry['media_upload_plan'][0]['dedup_key'],again['media_upload_plan'][0]['dedup_key'])

    def test_registered_metadata_mapping_only(self):
        with self.assertRaisesRegex(ValueError,'unverified REST registration'):
            self.package(site_config={'meta_mapping':{'access_type':'premium_plugin_tier'}})
        config={'meta_mapping':{'access_type':'registered_access','seo.description':'registered_description'},
            'registered_meta':{name:{'rest_writable':True,'type':'string','registration_reference':'synthetic:registered'} for name in ['registered_access','registered_description']}}
        result=self.package(site_config=config)
        self.assertEqual(result['proposed_payload']['meta'],{'registered_access':'FREE','registered_description':'試作の概要'})
        self.assertNotIn('seo_policy_version',result['proposed_payload']['meta'])

    def test_svg_requires_explicit_conversion(self):
        self.plan['images'][1]['generated_asset_reference'].update(mime_type='image/svg+xml',relative_path='native.svg');self.refresh()
        result=self.package()
        self.assertIn('media_format_requires_conversion:inline-1',result['blockers'])
        self.assertEqual(result['media_upload_plan'][1]['action'],'requires_conversion')

    def test_stale_package_or_published_post_cannot_associate(self):
        result=self.ready();post={'site_id':'synthetic-site','id':201,'status':'publish','content_id':'TEST-A25','response_reference':'synthetic','receipt_type':'test_fixture'}
        with self.assertRaisesRegex(ValueError,'DRAFT response'):
            association_plan(result,post)
        result['proposed_payload']['content']='changed'
        with self.assertRaisesRegex(ValueError,'changed after'):
            association_plan(result,post)

    def test_cross_site_post_receipt_cannot_associate_media(self):
        result=self.ready()
        post={'site_id':'another-site','id':201,'status':'draft','content_id':'TEST-A25','response_reference':'synthetic','receipt_type':'test_fixture'}
        with self.assertRaisesRegex(ValueError,'site identity'):
            association_plan(result,post)

    def test_official_field_schema(self):
        root=Path(__file__).resolve().parents[1]
        schema=json.loads((root/'fortune_labo/agents/wordpress/schemas/draft_payload.schema.json').read_text())
        audit_schema(schema)
        validate(self.package(),schema)
        validate(self.ready(),schema)
        result=self.package();result['proposed_payload']['status']='publish'
        with self.assertRaises(ValueError):
            validate(result,schema)


if __name__=='__main__':
    unittest.main()
