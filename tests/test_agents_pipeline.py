"""Synthetic-only A07/A08 tests. No private research or real article fixtures."""
import copy
import json
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fortune_labo.editorial.strategy import build_brief, canonical_hash
from fortune_labo.editorial.production import prepare_run, accept_draft, verify_run, self_review_template, writing_findings


def synthetic_inputs(access_type='FREE'):
    links = [{'target_content_id':None,'target_url':None,'anchor_text':'関連する説明',
              'rationale':'補助テーマを確認する候補','direction':'outbound_from_this_page','status':'candidate'}]
    index = {'content_id':'FL-SYNTH-A','title':'条件を整理して次の行動を決める',
        'genre':'synthetic','primary_keyword':'例 条件整理','secondary_keywords':[],
        'search_intent':'informational','explicit_need':'判断条件を整理したい',
        'latent_need':'自分で決めるための材料がほしい','persona':'選択肢を比較している読者',
        'reader_stage':'consideration','access_type':access_type,'content_depth':'standard',
        'article_type':'situation_guide','internal_links':links,'cta_type':'related_content',
        'cta_destination':None,'seo_policy_version':'seo-policy-0.1.0-draft'}
    genre = {'genre_id':'synthetic','genre_name':'合成テスト', 'recommended_access_type':'BOTH',
        'seo_role':'基本の疑問に回答する','engagement_role':'具体例で整理する',
        'conversion_role':'次に必要な情報を選ぶ','retention_role':'前回の条件を見直す',
        'free_content_role':'基本の問題を解決する','premium_content_role':'再利用できる比較表と見直し手順',
        'evidence_source':[{'source_id':'SYNTHETIC-RESEARCH'}]}
    decision = {'topic':'条件の整理','core_answer':'変えられる条件と確認が必要な条件を分けて考える。',
        'h2_h3_intent':[{'heading_level':'h2','heading':'条件を分ける','purpose':'すぐ使える回答',
            'source_requirement':'ai_structurable','evidence_refs':['SYNTHETIC-RESEARCH']},
            {'heading_level':'h2','heading':'小さく確かめる','purpose':'具体例と実践',
            'source_requirement':'ai_structurable','evidence_refs':['SYNTHETIC-RESEARCH']}],
        'evidence_needed':[{'requirement':'題材の選定根拠','claim_kind':'HYPOTHESIS',
            'source_ref':'SYNTHETIC-RESEARCH','status':'available'}],
        'personal_experience_needed':{'required':False,'source_ref':None,'status':'not_required','handling':'実体験を使用しない'},
        'access_rationale':'無料で基本回答を完結させ、有料価値は再利用支援として区別する。',
        'access_decision':{'basic_answer_complete':True,
            'premium_value_dimensions':['framework','action_plan'] if access_type=='PREMIUM' else [],
            'premium_added_value':['再利用できる比較表'] if access_type=='PREMIUM' else [],
            'premium_value_source_refs':['SYNTHETIC-RESEARCH'] if access_type=='PREMIUM' else []},
        'selection':{'opportunity_id':None,'existing_content_resolution':None,
                     'offline_selection_reason':'ユーザーが選定したオフライン比較用の合成テーマ。'},
        'cta':{'placement':'末尾','copy_direction':'必要な場合に関連テーマを確認する'},
        'source_refs':['SYNTHETIC-RESEARCH'],'tbd':['公開判断は未実施。']}
    policy = {'current_approved_policy':None,'policy_versions':[{'version':'seo-policy-0.1.0-draft',
        'status':'pending_human_approval','permitted_scope':'offline_test_articles_and_qa_only'}]}
    return index, {'version':'synthetic-1','genres':[genre]}, decision, policy


def fixture_brief(access_type='FREE'):
    index, intelligence, decision, policy = synthetic_inputs(access_type)
    return build_brief(index, intelligence, decision=decision, policy_register=policy)


def fixture_draft(brief):
    return '# ' + brief['title'] + '\n\n判断に迷うときは、変えられる条件と確認が必要な条件を分けて考えます。たとえば説明用の仮例では、移動時間と勤務時間を別々に確かめると、今すぐ確認できることが見つかります。\n\n## 条件を分ける\n\n同じ理由に見えても、誰に確認するかは条件によって異なります。説明用の仮例として移動時間は自分で調べ、勤務時間は募集内容や担当者へ確認する流れを考えてみます。\n\n## 小さく確かめる\n\n集めた情報を並べると、まだ判断できない部分が残る場合もあります。その部分を無理に結論へ変えず、次に確認する項目として残しておくと、見直すときの判断材料になります。\n'


def fixture_review():
    review = self_review_template()
    for row in review['checks']:
        row.update(status='passed', evidence='合成Draftの見出し「条件を分ける」とその本文を照合。', notes='合成fixtureの工程テストであり実記事の品質承認ではない。')
    review['known_gaps'] = ['実運用では各基準に固有の箇所を人間またはモデルが評価する。']
    return review


class AgentsPipelineTests(unittest.TestCase):
    def test_brief_preserves_inputs_and_sourced_roles(self):
        inputs = synthetic_inputs('PREMIUM')
        before = copy.deepcopy(inputs)
        brief = build_brief(inputs[0],inputs[1],decision=inputs[2],policy_register=inputs[3])
        self.assertEqual(inputs,before)
        self.assertEqual(brief['premium_value']['source_refs'],['SYNTHETIC-RESEARCH'])
        self.assertIsNone(brief['human_approval'])
        self.assertFalse(brief['publication_allowed'])

    def test_free_does_not_claim_premium_value(self):
        self.assertIsNone(fixture_brief()['premium_value']['statement'])

    def test_withheld_basic_answer_rejected(self):
        index,intelligence,decision,policy=synthetic_inputs()
        decision['access_decision']['basic_answer_complete']=False
        with self.assertRaisesRegex(ValueError,'basic answer'):
            build_brief(index,intelligence,decision=decision,policy_register=policy)

    def test_word_count_only_premium_rejected(self):
        index,intelligence,decision,policy=synthetic_inputs('PREMIUM')
        decision['access_decision']['premium_value_dimensions']=['word_count']
        with self.assertRaisesRegex(ValueError,'word count'):
            build_brief(index,intelligence,decision=decision,policy_register=policy)

    def test_premium_without_added_value_rejected(self):
        index,intelligence,decision,policy=synthetic_inputs('PREMIUM')
        decision['access_decision']['premium_added_value']=[]
        with self.assertRaisesRegex(ValueError,'added value'):
            build_brief(index,intelligence,decision=decision,policy_register=policy)

    def test_premium_unsupported_source_rejected(self):
        index,intelligence,decision,policy=synthetic_inputs('PREMIUM')
        decision['access_decision']['premium_value_source_refs']=['INVENTED']
        with self.assertRaisesRegex(ValueError,'researched premium role'):
            build_brief(index,intelligence,decision=decision,policy_register=policy)

    def opportunity_input(self):
        index,intelligence,decision,policy=synthetic_inputs()
        decision['selection']['opportunity_id']='opp-synthetic'
        decision['selection']['offline_selection_reason']=None
        opportunities={'inventory_completeness':'complete','opportunities':[{
            'opportunity_id':'opp-synthetic','genre':index['genre'],'topic':decision['topic'],
            'keyword':index['primary_keyword'],'search_intent':index['search_intent'],
            'free_premium_candidate':'FREE','evidence_refs':['SYNTHETIC-RESEARCH'],
            'coverage_status':'no_index_match','existing_content_overlap':[]}], 'suppressed':[]}
        return index,intelligence,decision,policy,opportunities

    def test_supplied_opportunity_selected_and_recorded(self):
        index,intelligence,decision,policy,opportunities=self.opportunity_input()
        brief=build_brief(index,intelligence,decision=decision,policy_register=policy,opportunities=opportunities)
        self.assertEqual(brief['selection_context']['opportunity_id'],'opp-synthetic')
        self.assertEqual(brief['selection_context']['coverage_status'],'no_index_match')

    def test_missing_selected_opportunity_rejected(self):
        index,intelligence,decision,policy,opportunities=self.opportunity_input()
        decision['selection']['opportunity_id']='missing'
        with self.assertRaisesRegex(ValueError,'exist exactly once'):
            build_brief(index,intelligence,decision=decision,policy_register=policy,opportunities=opportunities)

    def test_suppressed_overlap_rejected(self):
        index,intelligence,decision,policy,opportunities=self.opportunity_input()
        opportunities['suppressed']=opportunities['opportunities']
        with self.assertRaisesRegex(ValueError,'suppressed'):
            build_brief(index,intelligence,decision=decision,policy_register=policy,opportunities=opportunities)

    def test_topic_without_evidence_rejected(self):
        index,intelligence,decision,policy,opportunities=self.opportunity_input()
        opportunities['opportunities'][0]['evidence_refs']=[]
        with self.assertRaisesRegex(ValueError,'no topic evidence'):
            build_brief(index,intelligence,decision=decision,policy_register=policy,opportunities=opportunities)

    def test_overlap_without_resolution_rejected(self):
        index,intelligence,decision,policy,opportunities=self.opportunity_input()
        opportunities['opportunities'][0]['existing_content_overlap']=[{'content_id':'existing'}]
        with self.assertRaisesRegex(ValueError,'documented resolution'):
            build_brief(index,intelligence,decision=decision,policy_register=policy,opportunities=opportunities)

    def test_incomplete_inventory_not_certain_gap(self):
        index,intelligence,decision,policy,opportunities=self.opportunity_input()
        opportunities['inventory_completeness']='partial'
        with self.assertRaisesRegex(ValueError,'Incomplete inventory'):
            build_brief(index,intelligence,decision=decision,policy_register=policy,opportunities=opportunities)

    def test_measured_group_without_provenance_rejected(self):
        index,intelligence,decision,policy=synthetic_inputs()
        with self.assertRaisesRegex(ValueError,'raw observations'):
            build_brief(index,intelligence,decision=decision,policy_register=policy,performance={'seo':{'clicks':0}})

    def test_raw_performance_provenance_and_units_retained(self):
        from fortune_labo.editorial.performance import empty_observation
        index,intelligence,decision,policy=synthetic_inputs()
        observation=empty_observation(index['content_id'],'GA4','2026-09-01','2026-09-30',
            timezone='Asia/Tokyo',source_reference='SYNTHETIC-METRIC-SOURCE')
        observation['collected_at']='2026-10-07T00:00:00Z'
        observation['metrics']['scroll_depth']=80
        observation['metric_metadata']['scroll_depth'].update(source_metric='synthetic_scroll',
            definition='Synthetic mean maximum scroll percentage',aggregation='mean')
        performance={'observations':[observation],'selection':{'period_start':'2026-09-01','period_end':'2026-09-30','timezone':'Asia/Tokyo'}}
        original=copy.deepcopy(performance)
        brief=build_brief(index,intelligence,decision=decision,policy_register=policy,performance=performance)
        self.assertEqual(brief['performance_context']['metric_groups']['engagement']['scroll_depth'],80)
        self.assertEqual(brief['performance_context']['raw_observations'][0]['metric_metadata']['scroll_depth']['unit'],'percent')
        self.assertEqual(brief['performance_context']['raw_observations'][0]['source_reference'],'SYNTHETIC-METRIC-SOURCE')
        self.assertEqual(performance,original)

    def test_a08_prepare_rejects_unregistered_policy(self):
        brief=fixture_brief()
        brief['seo_policy_version']='seo-policy-999.0.0-draft'
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError,'registered SEO policy'):
                prepare_run(brief,Path(temp)/'run',private_root=temp)
            self.assertFalse((Path(temp)/'run').exists())

    def test_a08_prepare_rejects_registered_wrong_scope(self):
        register=json.loads((ROOT/'docs/seo/SEO_POLICY_REGISTER.json').read_text())
        register['policy_versions'][0]['permitted_scope']='editorial_production'
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'policy.json'; path.write_text(json.dumps(register))
            with patch('fortune_labo.editorial.production.POLICY_REGISTER',path):
                with self.assertRaisesRegex(ValueError,'policy scope'):
                    prepare_run(fixture_brief(),Path(temp)/'run',private_root=temp)

    def test_a08_verify_rechecks_registered_scope(self):
        with tempfile.TemporaryDirectory() as temp:
            run=Path(temp)/'run'; prepare_run(fixture_brief(),run,private_root=temp)
            register=json.loads((ROOT/'docs/seo/SEO_POLICY_REGISTER.json').read_text())
            register['policy_versions'][0]['permitted_scope']='editorial_production'
            path=Path(temp)/'policy.json'; path.write_text(json.dumps(register))
            with patch('fortune_labo.editorial.production.POLICY_REGISTER',path):
                with self.assertRaisesRegex(ValueError,'policy scope'):
                    verify_run(run,private_root=temp)

    def test_a08_verify_rejects_policy_removed_from_register(self):
        with tempfile.TemporaryDirectory() as temp:
            run=Path(temp)/'run'; prepare_run(fixture_brief(),run,private_root=temp)
            path=Path(temp)/'policy.json'; path.write_text(json.dumps({'policy_versions':[]}))
            with patch('fortune_labo.editorial.production.POLICY_REGISTER',path):
                with self.assertRaisesRegex(ValueError,'registered SEO policy'):
                    verify_run(run,private_root=temp)

    def test_a08_rejects_fabricated_policy_approval(self):
        register=json.loads((ROOT/'docs/seo/SEO_POLICY_REGISTER.json').read_text())
        register['policy_versions'][0]['approved_by']='synthetic-invalid-approval'
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'policy.json'; path.write_text(json.dumps(register))
            with patch('fortune_labo.editorial.production.POLICY_REGISTER',path):
                with self.assertRaisesRegex(ValueError,'approval state'):
                    prepare_run(fixture_brief(),Path(temp)/'run',private_root=temp)

    def test_new_register_version_does_not_rewrite_historical_run(self):
        with tempfile.TemporaryDirectory() as temp:
            run=Path(temp)/'run'; brief=fixture_brief(); prepare_run(brief,run,private_root=temp)
            register=json.loads((ROOT/'docs/seo/SEO_POLICY_REGISTER.json').read_text())
            extra=copy.deepcopy(register['policy_versions'][0]); extra['version']='seo-policy-0.2.0-draft'
            register['policy_versions'].append(extra)
            path=Path(temp)/'policy.json'; path.write_text(json.dumps(register))
            with patch('fortune_labo.editorial.production.POLICY_REGISTER',path):
                self.assertEqual(verify_run(run,private_root=temp)['seo_policy_version'],brief['seo_policy_version'])
            self.assertEqual(json.loads((run/'brief.json').read_text()),brief)

    def test_private_complete_pipeline(self):
        with tempfile.TemporaryDirectory() as temp:
            brief=fixture_brief(); run=Path(temp)/'article'
            prepare_run(brief,run,private_root=temp)
            result=accept_draft(run,fixture_draft(brief),fixture_review(),private_root=temp)
            self.assertEqual(result['release_gate'],'blocked')
            self.assertEqual(verify_run(run,private_root=temp)['brief_sha256'],canonical_hash(brief))
            self.assertEqual(json.loads((run/'brief.json').read_text()),brief)

    def test_public_output_refused(self):
        with self.assertRaises(ValueError):
            prepare_run(fixture_brief(),ROOT/'docs'/'forbidden-run',private_root=ROOT/'docs')

    def test_path_escape_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                prepare_run(fixture_brief(),Path(temp).parent/'escape-run',private_root=temp)

    def test_brief_mutation_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            brief=fixture_brief(); run=Path(temp)/'article'; prepare_run(brief,run,private_root=temp)
            changed=json.loads((run/'brief.json').read_text()); changed['core_answer']='変更'
            (run/'brief.json').write_text(json.dumps(changed))
            with self.assertRaisesRegex(ValueError,'Immutable'):
                accept_draft(run,fixture_draft(brief),fixture_review(),private_root=temp)

    def test_incomplete_self_review_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            brief=fixture_brief(); run=Path(temp)/'article'; prepare_run(brief,run,private_root=temp)
            with self.assertRaises(ValueError):
                accept_draft(run,fixture_draft(brief),self_review_template(),private_root=temp)

    def test_changed_outline_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            brief=fixture_brief(); run=Path(temp)/'article'; prepare_run(brief,run,private_root=temp)
            with self.assertRaisesRegex(ValueError,'outline'):
                accept_draft(run,fixture_draft(brief).replace('## 条件を分ける','## 改変'),fixture_review(),private_root=temp)

    def test_completed_draft_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            brief=fixture_brief(); run=Path(temp)/'article'; prepare_run(brief,run,private_root=temp)
            accept_draft(run,fixture_draft(brief),fixture_review(),private_root=temp)
            with self.assertRaisesRegex(ValueError,'immutable'):
                accept_draft(run,fixture_draft(brief),fixture_review(),private_root=temp)

    def test_fragmentation_is_review_signal_not_quality_pass(self):
        result=writing_findings('短い文です。\n\n次の文です。\n\n別の文です。\n\n四つ目です。\n\n五つ目です。')
        self.assertTrue(result['requires_editorial_review'])
        self.assertIn('one_sentence_per_line',[row['code'] for row in result['findings']])


if __name__=='__main__':
    unittest.main()
