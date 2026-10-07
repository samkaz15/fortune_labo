import unittest
import json
import tempfile
from pathlib import Path
from test_agents_pipeline import fixture_brief, fixture_draft, fixture_review
from fortune_labo.editorial.qa_contract import build_qa_handoff, extract_claim_candidates
from fortune_labo.editorial.production import prepare_run, accept_draft, verify_run
from fortune_labo.editorial.strategy import canonical_hash
from scripts.verify_test_fixtures import verify


class QAContractTests(unittest.TestCase):
    def test_fact_candidates_include_unnumbered_assertions(self):
        candidates = extract_claim_candidates('A source says this happened.\nThis always succeeds.')
        self.assertGreaterEqual(len(candidates['claims']), 2)
        self.assertTrue(all(c['status'] == 'requires_fact_review' for c in candidates['claims']))
        self.assertTrue(candidates['requires_full_draft_review'])

    def test_qa_handoff_never_grants_approval(self):
        brief = fixture_brief()
        envelope = build_qa_handoff(brief, fixture_draft(brief))
        self.assertEqual([s['agent'] for s in envelope['stages']], ['A29', 'A32', 'A28'])
        self.assertIsNone(envelope['human_approval'])
        self.assertFalse(envelope['wordpress_handoff_allowed'])
        self.assertFalse(envelope['publication_allowed'])
        self.assertEqual(envelope['seo_policy_version'], brief['seo_policy_version'])

    def test_generated_fixtures_preserve_contracts(self):
        self.assertEqual(verify()['test_fixtures'], 3)

    def test_self_review_policy_cannot_drift_even_with_recomputed_hash(self):
        with tempfile.TemporaryDirectory() as private:
            brief = fixture_brief()
            run = Path(private) / 'run'
            prepare_run(brief, run, private_root=private)
            accept_draft(run, fixture_draft(brief), fixture_review(), private_root=private)
            review = json.loads((run / 'self-review.json').read_text())
            review['seo_policy_version'] = 'seo-policy-999.0.0-draft'
            (run / 'self-review.json').write_text(json.dumps(review))
            manifest = json.loads((run / 'run.json').read_text())
            manifest['self_review_sha256'] = canonical_hash(review)
            (run / 'run.json').write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, 'Self review SEO policy'):
                verify_run(run, private_root=private)
