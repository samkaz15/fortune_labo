"""A07: evidence-linked, offline brief assembly. No model, network, or publishing."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROLE_MAP = {'acquisition_role':'seo_role', 'engagement_role':'engagement_role',
            'conversion_role':'conversion_role', 'retention_role':'retention_role',
            'premium_value':'premium_content_role'}
DECISION_FIELDS = ('topic', 'core_answer', 'h2_h3_intent', 'evidence_needed',
                   'personal_experience_needed', 'access_rationale', 'access_decision', 'selection')


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(',', ':'), allow_nan=False).encode('utf-8')).hexdigest()


def _validator():
    spec = importlib.util.spec_from_file_location('_editorial_validator', ROOT / 'scripts/validate_editorial.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_brief(brief):
    validator = _validator()
    schema = validator.load(ROOT / 'fortune_labo/agents/content-strategy/schemas/brief.schema.json')
    validator.audit_schema(schema)
    validator.validate(brief, schema)
    if brief['mode'] != 'offline_test' or brief['handoff']['state'] != 'offline_test_only':
        raise ValueError('Executable A07/A08 foundation supports offline tests only; normal production handoff remains blocked')
    return True


def _refs(genre, field):
    provenance = genre.get('field_provenance', {}).get(field, {})
    evidence = provenance.get('evidence_source', genre.get('evidence_source', []))
    return sorted({entry['source_id'] for entry in evidence if isinstance(entry, dict) and entry.get('source_id')})


def _role(genre, field):
    value = genre.get(field)
    if value in (None, '', 'TBD', []):
        return {'statement':None, 'source_refs':[], 'status':'TBD'}
    if isinstance(value, list):
        value = ' / '.join(str(item) for item in value)
    refs = _refs(genre, field)
    return {'statement':str(value), 'source_refs':refs,
            'status':'derived_from_intelligence' if refs else 'TBD'}


def _check_access(index, genre, decision):
    access = decision['access_decision']
    if access.get('basic_answer_complete') is not True:
        raise ValueError('FREE and PREMIUM must both complete the promised basic answer')
    if not isinstance(access.get('premium_added_value'), list) or not isinstance(access.get('premium_value_source_refs'), list):
        raise ValueError('Access decision requires explicit added-value and evidence lists')
    dimensions = access.get('premium_value_dimensions', [])
    allowed_dimensions = {'depth','personalization','continuity','framework','action_plan'}
    if not isinstance(dimensions, list) or not set(dimensions).issubset(allowed_dimensions):
        raise ValueError('Premium dimensions must describe value, never word count or a label alone')
    if index['access_type'] == 'PREMIUM':
        if not dimensions:
            raise ValueError('PREMIUM needs a researched added-value dimension beyond length')
        value = _role(genre, 'premium_content_role')
        if value['status'] != 'derived_from_intelligence':
            raise ValueError('PREMIUM requires sourced premium intelligence')
        if not access['premium_added_value'] or any(not isinstance(row, str) or not row.strip() for row in access['premium_added_value']):
            raise ValueError('PREMIUM requires concrete reusable, practical, personalized or continuing added value')
        if not access['premium_value_source_refs'] or not set(access['premium_value_source_refs']).issubset(set(value['source_refs'])):
            raise ValueError('PREMIUM added value must reference the researched premium role')


def _select_opportunity(index, decision, opportunities):
    selection = decision['selection']
    selected_id = selection.get('opportunity_id')
    if opportunities is None:
        if selected_id is not None or not selection.get('offline_selection_reason'):
            raise ValueError('Without opportunities, an explicit user-selected offline reason is required')
        return {'status':'user_requested_offline_fixture', 'opportunity_id':None,
                'inventory_completeness':'not_supplied', 'coverage_status':'not_assessed',
                'evidence_refs':[], 'existing_content_overlap':[], 'human_review_required':True}
    if not selected_id:
        raise ValueError('Select one supplied opportunity explicitly')
    if any(row.get('opportunity_id') == selected_id for row in opportunities.get('suppressed', [])):
        raise ValueError('Selected opportunity is suppressed by overlap; resolve upstream first')
    matches = [row for row in opportunities.get('opportunities', []) if row.get('opportunity_id') == selected_id]
    if len(matches) != 1:
        raise ValueError('Selected opportunity must exist exactly once')
    selected = matches[0]
    if not selected.get('evidence_refs'):
        raise ValueError('Selected opportunity has no topic evidence')
    for source, actual in [('genre', index['genre']), ('topic', decision['topic']),
                          ('keyword', index['primary_keyword']), ('search_intent', index['search_intent'])]:
        if selected.get(source) is not None and selected[source] != actual:
            raise ValueError('Selected opportunity differs from Brief: ' + source)
    if selected.get('free_premium_candidate') not in (None, index['access_type']):
        raise ValueError('Selected opportunity access candidate differs from Brief')
    overlap = selected.get('existing_content_overlap', [])
    if overlap and not selection.get('existing_content_resolution'):
        raise ValueError('Existing-content overlap requires a documented resolution')
    completeness = opportunities.get('inventory_completeness', 'unknown')
    coverage = selected.get('coverage_status')
    if completeness != 'complete' and coverage == 'no_index_match':
        raise ValueError('Incomplete inventory cannot establish a no-index-match opportunity')
    return {'status':'selected_for_offline_test', 'opportunity_id':selected_id,
            'inventory_completeness':completeness, 'coverage_status':coverage,
            'evidence_refs':copy.deepcopy(selected['evidence_refs']),
            'existing_content_overlap':copy.deepcopy(overlap), 'human_review_required':True}


def build_brief(index_item, intelligence, *, decision, a06_brief=None,
                a06_opportunity=None, performance=None, opportunities=None,
                policy_register=None):
    """Assemble an offline v2 brief without mutating any caller input.

    A model/human supplies the editorial decision; this function never claims to
    originate strategy or measured results. Roles come from structured research.
    A06 objects are retained as hashed inputs, never presented as approved output.
    """
    index = copy.deepcopy(index_item)
    plan = copy.deepcopy(decision)
    genres = intelligence.get('genres', [intelligence])
    matches = [genre for genre in genres if genre.get('genre_id') == index['genre']]
    if len(matches) != 1:
        raise ValueError('Exactly one researched genre is required')
    genre = matches[0]
    missing = [key for key in DECISION_FIELDS if key not in plan]
    if missing:
        raise ValueError('Missing editorial decision fields: ' + ', '.join(missing))
    _check_access(index, genre, plan)
    selection_context = _select_opportunity(index, plan, opportunities)
    register = policy_register if policy_register is not None else json.loads((ROOT / 'docs/seo/SEO_POLICY_REGISTER.json').read_text(encoding='utf-8'))
    policies = {row['version']:row for row in register['policy_versions']}
    policy = policies.get(index['seo_policy_version'])
    if not policy or policy.get('permitted_scope') != 'offline_test_articles_and_qa_only':
        raise ValueError('An explicitly registered offline-test policy is required')
    if policy.get('status') != 'pending_human_approval':
        raise ValueError('This executable does not promote or select operational policy')
    roles = {target:_role(genre, source) for target, source in ROLE_MAP.items()}
    if index['access_type'] == 'FREE':
        roles['premium_value'] = {'statement':None, 'source_refs':[], 'status':'not_applicable'}
    raw_performance = performance if performance is not None else index.get('performance')
    if raw_performance is not None and 'observations' in raw_performance:
        from .performance import performance_context as adapt_performance
        selected_window = raw_performance.get('selection', {})
        if not all(selected_window.get(key) for key in ('period_start','period_end','timezone')):
            raise ValueError('Raw performance needs explicit period and timezone selection')
        performance_context = adapt_performance(raw_performance['observations'], content_id=index['content_id'], **selected_window)
        performance_context['assessment'] = plan.get('performance_assessment', 'Raw observations remain separated; no performance winner or priority score is inferred.')
    else:
        if raw_performance is not None and set(raw_performance) - {'seo','engagement','conversion','retention','measurement'}:
            raise ValueError('Only raw metric groups are supported; scores and weights are forbidden')
        metric_groups = {group:copy.deepcopy(raw_performance.get(group)) if raw_performance else None for group in ('seo','engagement','conversion','retention')}
        observed = [group for group, values in metric_groups.items() if values and any(value is not None for value in values.values())]
        if observed:
            raise ValueError('Measured performance requires raw observations with full source, window and unit provenance')
        performance_context = {'status':'unmeasured', 'metric_groups':metric_groups, 'observed_groups':[],
            'assessment':plan.get('performance_assessment', 'No performance winner or priority score is inferred; review each purpose separately.'),
            'evidence_refs':[], 'raw_observations':[]}
    blockers = list(plan.get('tbd', []))
    for key, role in roles.items():
        if role['status'] == 'TBD':
            blockers.append(key + ': missing sourced intelligence; do not infer')
    allowed = genre.get('recommended_access_type')
    if allowed not in ('BOTH', index['access_type']):
        blockers.append('access_type differs from researched recommendation; human strategy review required')
    source_refs = sorted(set(plan.get('source_refs', []) + _refs(genre, 'genre_name')))
    if not source_refs:
        raise ValueError('Sourced intelligence references are required')
    brief = {'schema_version':'2.0.0', 'content_id':index['content_id'], 'mode':'offline_test',
             'title':index['title'], 'genre':index['genre'], 'keyword':index['primary_keyword'],
             'secondary_keywords':index['secondary_keywords'], 'search_intent':index['search_intent'],
             'explicit_need':index['explicit_need'], 'latent_need':index['latent_need'],
             'persona':index['persona'], 'reader_stage':index['reader_stage'],
             'access_type':index['access_type'], 'content_depth':index['content_depth'],
             'article_type':index['article_type'], 'internal_link_candidates':index['internal_links'],
             'cta':{'type':index['cta_type'], 'destination':index['cta_destination'],
                    'placement':plan.get('cta', {}).get('placement', 'TBD'),
                    'copy_direction':plan.get('cta', {}).get('copy_direction', 'TBD'), 'status':'candidate'},
             'seo_policy_version':index['seo_policy_version'],
             'a06_source':{'status':'not_issued', 'brief_ref':None, 'opportunity_ref':None,
                 'brief_id':None, 'opportunity_id':None, 'tier':None, 'content_path':None,
                 'visit_record_id':None,
                 'binding_gaps':['A06 acceptance and production strategy differences are unresolved; offline test only.']},
             'strategy_assessment':{'moat_alignment':'conflicting', 'strategy_review_status':'pending',
                 'rationale':'The requested offline rerun does not resolve the existing A06 production positioning constraints.'},
             'source_refs':source_refs, 'source_status':'structured_from_user_research',
             'handoff':{'from':'A07', 'to':'A08', 'state':'offline_test_only',
                 'next_stages':['A29','A32','A28','human_approval','A25_wordpress_draft']},
             'human_approval':None, 'publication_allowed':False, 'tbd':blockers,
             'selection_context':selection_context, 'performance_context':performance_context,
             'access_basis':{'intelligence_version':intelligence.get('version'),
                 'genre_id':genre['genre_id'], 'recommended_access_type':allowed,
                 'source_refs':sorted(set(_refs(genre, 'free_content_role') + _refs(genre, 'premium_content_role'))),
                 'rules_reference':'docs/editorial/FREE_PREMIUM_RULES.md',
                 'rules_sha256':hashlib.sha256((ROOT / 'docs/editorial/FREE_PREMIUM_RULES.md').read_bytes()).hexdigest(),
                 'confidence':'medium' if _refs(genre, 'free_content_role') and _refs(genre, 'premium_content_role') else 'low',
                 'evidence_refs':sorted(set(_refs(genre, 'free_content_role') + _refs(genre, 'premium_content_role'))) + ['docs/editorial/FREE_PREMIUM_RULES.md']},
             'input_manifest':{'index_sha256':canonical_hash(index_item),
                 'intelligence_sha256':canonical_hash(intelligence),
                 'a06_brief_sha256':canonical_hash(a06_brief) if a06_brief is not None else None,
                 'a06_opportunity_sha256':canonical_hash(a06_opportunity) if a06_opportunity is not None else None,
                 'performance_sha256':canonical_hash(performance) if performance is not None else None,
                 'opportunities_sha256':canonical_hash(opportunities) if opportunities is not None else None,
                 'decision_sha256':canonical_hash(decision),
                 'policy_register_sha256':canonical_hash(register)}}
    brief.update({field:plan[field] for field in DECISION_FIELDS})
    brief.update(roles)
    validate_brief(brief)
    return brief
