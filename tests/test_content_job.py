import copy
import unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.validate_editorial import load
from scripts.verify_creative_fixtures import verify,article_descriptor
from fortune_labo.editorial.content_job import build_job,record_failure,FAILURE_STATES
from fortune_labo.editorial.strategy import canonical_hash
from fortune_labo.editorial.wordpress_draft import build_draft_payload


class ContentJobTests(unittest.TestCase):
    def setUp(self):
        self.source=ROOT/'docs/editorial/test-articles/FL-TEST-A'
        self.root=ROOT/'docs/editorial/creative-fixtures/FL-TEST-A'
        self.plan,self.qa,self.payload,self.job=[load(self.root/n) for n in ['image-plan.json','qa.json','wordpress-draft-payload.json','job.json']]

    def build(self,plan=None,qa=None,payload=None,previous=None):
        return build_job(self.source/'article.md',self.source/'blueprint.json',plan or self.plan,qa or self.qa,payload or self.payload,
            asset_root=self.root,artifact_references=self.job['artifacts'],previous_job=previous)

    def test_three_complete_offline_jobs(self):
        self.assertEqual(verify(),{'jobs':3,'featured':3,'inline':2,'no_image':8,'actual_wordpress_drafts':0})

    def test_all_failures_preserve_article_assets_and_inputs(self):
        before=copy.deepcopy(self.job)
        for stage,state in FAILURE_STATES.items():
            failed=record_failure(self.job,stage,'Synthetic retry test failure')
            self.assertIn(state,failed['statuses'])
            self.assertIn('article_ready',failed['statuses'])
            for key in ['draft_sha256','artifacts','assets']:
                self.assertEqual(failed[key],before[key])
            self.assertFalse(failed['publication_allowed'])
        self.assertEqual(before,self.job)

    def test_successful_revalidation_retains_retry_history(self):
        failed=record_failure(self.job,'images','Synthetic generation failure')
        result=self.build(previous=failed)
        self.assertEqual(result['stage_status']['images'],'images_ready')
        self.assertEqual(len(result['attempts']),1)
        self.assertEqual(result['job_id'],self.job['job_id'])

    def test_pending_image_keeps_article_ready(self):
        plan=copy.deepcopy(self.plan)
        plan['images'][0].update(generation_status='planned',generated_asset_reference=None)
        plan['status']='partially_generated'
        qa=copy.deepcopy(self.qa);qa['image_plan_sha256']=canonical_hash(plan)
        qa['gates']['A28']['status']='pending'
        package=build_draft_payload(article_descriptor('A'),plan,qa)
        result=self.build(plan,qa,package)
        self.assertIn('image_generation_pending',result['statuses'])
        self.assertIn('image_incomplete',result['statuses'])
        self.assertEqual(result['stage_status']['article'],'article_ready')
        self.assertIsNone(package['request_payload'])

    def test_each_failed_qa_gate_blocks_payload(self):
        for stage in ['A29','A32','A28']:
            qa=copy.deepcopy(self.qa);qa['gates'][stage]['status']='failed'
            package=build_draft_payload(article_descriptor('A'),self.plan,qa)
            job=self.build(qa=qa,payload=package)
            self.assertIn(FAILURE_STATES[stage],job['statuses'])
            self.assertIsNone(package['request_payload'])

    def test_mixed_article_job_rejected(self):
        qa=copy.deepcopy(self.qa);qa['content_id']='FL-TEST-B'
        with self.assertRaises(ValueError):self.build(qa=qa)

    def test_stale_image_qa_rejected(self):
        qa=copy.deepcopy(self.qa);qa['image_plan_sha256']='0'*64
        with self.assertRaises(ValueError):self.build(qa=qa)

    def test_mutated_package_rejected(self):
        package=copy.deepcopy(self.payload);package['proposed_payload']['content']+='changed'
        with self.assertRaises(ValueError):self.build(payload=package)

    def test_publish_status_rejected_at_job_boundary(self):
        package=copy.deepcopy(self.payload);package['proposed_payload']['status']='publish'
        with self.assertRaises(ValueError):self.build(payload=package)

    def test_different_source_cannot_resume_existing_job(self):
        previous=copy.deepcopy(self.job);previous['draft_sha256']='0'*64
        with self.assertRaises(ValueError):self.build(previous=previous)

    def test_policy_and_access_cannot_diverge_from_blueprint(self):
        for key,value in [('seo_policy_version','wrong-policy'),('access_type','PREMIUM')]:
            article=article_descriptor('A');article[key]=value
            package=build_draft_payload(article,self.plan,self.qa)
            with self.assertRaisesRegex(ValueError,'source Blueprint'):
                self.build(payload=package)

    def test_pass_without_evidence_stays_pending(self):
        qa=copy.deepcopy(self.qa);qa['gates']['A29']['evidence_ref']=None
        package=build_draft_payload(article_descriptor('A'),self.plan,qa)
        job=self.build(qa=qa,payload=package)
        self.assertEqual(job['stage_status']['A29'],'pending')
        self.assertIsNone(package['request_payload'])
