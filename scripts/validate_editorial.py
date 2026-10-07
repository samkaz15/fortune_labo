#!/usr/bin/env python3
"""Validate the checked-in editorial foundation with Python's standard library.

This implements only the Draft 2020-12 keywords used by this repository, rejects
unknown keywords, and performs cross-file checks. It is not a general-purpose
JSON Schema implementation. No network, production API, or file writes.
"""
import argparse
import datetime as dt
import json
import math
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / 'docs/editorial/schemas'
ANNOTATIONS = {'$schema', '$id', 'title', 'description', 'default'}
SUPPORTED = ANNOTATIONS | {'$ref', '$defs', 'type', 'const', 'enum', 'properties',
    'required', 'additionalProperties', 'items', 'minItems', 'maxItems',
    'uniqueItems', 'minimum', 'maximum', 'minLength', 'maxLength', 'pattern',
    'format', 'allOf', 'anyOf', 'if', 'then', 'else'}


class ValidationError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ValidationError(message)


def load(path):
    def reject_constant(value):
        raise ValidationError('Non-JSON number: ' + value)
    return json.loads(path.read_text(encoding='utf-8'), parse_constant=reject_constant)


def equal(left, right):
    if isinstance(left, bool) != isinstance(right, bool):
        return False
    return left == right


def matches_type(value, name):
    number = isinstance(value, (int, float)) and not isinstance(value, bool)
    return {'null': value is None, 'object': isinstance(value, dict),
        'array': isinstance(value, list), 'string': isinstance(value, str),
        'boolean': isinstance(value, bool), 'number': number,
        'integer': number and (isinstance(value, int) or (math.isfinite(value) and int(value) == value))}.get(name, False)


def audit_schema(schema):
    if isinstance(schema, bool):
        return
    require(isinstance(schema, dict), 'Schema must be object or boolean')
    require(not set(schema) - SUPPORTED, 'Unsupported schema keywords: ' + str(set(schema) - SUPPORTED))
    for key in ('properties', '$defs'):
        for child in schema.get(key, {}).values():
            audit_schema(child)
    for key in ('items', 'if', 'then', 'else'):
        if key in schema:
            audit_schema(schema[key])
    for key in ('allOf', 'anyOf'):
        for child in schema.get(key, []):
            audit_schema(child)
    if 'additionalProperties' in schema and isinstance(schema['additionalProperties'], dict):
        audit_schema(schema['additionalProperties'])
    if '$ref' in schema:
        require(schema['$ref'].startswith('#/'), 'Only local schema references are supported')
    if 'format' in schema:
        require(schema['format'] in ('date', 'date-time', 'uri', 'uri-reference'), 'Unsupported format')


def validate(value, schema, root=None, path='$'):
    root = schema if root is None else root
    if isinstance(schema, bool):
        require(schema, path + ': false schema')
        return
    if '$ref' in schema:
        target = root
        for part in schema['$ref'][2:].split('/'):
            target = target[part.replace('~1', '/').replace('~0', '~')]
        validate(value, target, root, path)
    if 'type' in schema:
        types = schema['type'] if isinstance(schema['type'], list) else [schema['type']]
        require(any(matches_type(value, name) for name in types), path + ': type must be ' + str(types))
    if 'const' in schema:
        require(equal(value, schema['const']), path + ': unexpected constant')
    if 'enum' in schema:
        require(any(equal(value, item) for item in schema['enum']), path + ': invalid enum value ' + repr(value))
    for child in schema.get('allOf', []):
        validate(value, child, root, path)
    if 'anyOf' in schema:
        errors = []
        for child in schema['anyOf']:
            try:
                validate(value, child, root, path)
                break
            except ValidationError as error:
                errors.append(str(error))
        else:
            raise ValidationError(path + ': no anyOf match (' + '; '.join(errors) + ')')
    if 'if' in schema:
        try:
            validate(value, schema['if'], root, path)
            branch = 'then'
        except ValidationError:
            branch = 'else'
        if branch in schema:
            validate(value, schema[branch], root, path)
    if isinstance(value, dict):
        require(set(schema.get('required', [])) <= set(value), path + ': missing required fields ' + str(set(schema.get('required', [])) - set(value)))
        properties = schema.get('properties', {})
        for key, item in value.items():
            if key in properties:
                validate(item, properties[key], root, path + '.' + key)
            elif schema.get('additionalProperties') is False:
                raise ValidationError(path + ': unknown field ' + key)
            elif isinstance(schema.get('additionalProperties'), dict):
                validate(item, schema['additionalProperties'], root, path + '.' + key)
    if isinstance(value, list):
        require(len(value) >= schema.get('minItems', 0), path + ': too few items')
        require(len(value) <= schema.get('maxItems', len(value)), path + ': too many items')
        if schema.get('uniqueItems'):
            require(len({json.dumps(x, sort_keys=True) for x in value}) == len(value), path + ': duplicate items')
        for index, item in enumerate(value):
            if 'items' in schema:
                validate(item, schema['items'], root, path + '[' + str(index) + ']')
    if isinstance(value, str):
        require(len(value) >= schema.get('minLength', 0), path + ': string too short')
        require(len(value) <= schema.get('maxLength', len(value)), path + ': string too long')
        if 'pattern' in schema:
            require(re.search(schema['pattern'], value) is not None, path + ': pattern mismatch')
        form = schema.get('format')
        try:
            if form == 'date':
                require(re.fullmatch(r'\d{4}-\d{2}-\d{2}', value), path + ': invalid date format')
                dt.date.fromisoformat(value)
            elif form == 'date-time':
                require(re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})', value), path + ': invalid timestamp format')
                dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
            elif form in ('uri', 'uri-reference'):
                parts = urlsplit(value)
                require(not re.search(r'\s', value), path + ': whitespace in URI')
                if form == 'uri':
                    require(bool(parts.scheme), path + ': absolute URI required')
                if parts.scheme in ('http', 'https'):
                    require(bool(parts.hostname), path + ': hostname required')
        except ValueError as error:
            raise ValidationError(path + ': invalid ' + str(form)) from error
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        require(isinstance(value, int) or math.isfinite(value), path + ': number must be finite')
        require(value >= schema.get('minimum', value), path + ': below minimum')
        require(value <= schema.get('maximum', value), path + ': above maximum')


def checked_path(reference, root=ROOT):
    path = (root / reference).resolve()
    require(path.is_relative_to(root.resolve()), 'Artifact escapes repository: ' + reference)
    require(path.is_file(), 'Missing artifact: ' + reference)
    return path


def validate_artifacts_and_metrics(item, ids, root):
    cid = item['content_id']
    stages = {
        'planned': [], 'briefed': ['brief'], 'drafting': ['brief', 'blueprint'],
        'qa_pending': ['brief', 'blueprint', 'draft'], 'archived': []}
    required = stages.get(item['status'], list(item['artifacts']))
    if item['release_gate'] == 'approved':
        required = list(item['artifacts'])
    for name, reference in item['artifacts'].items():
        if name in required:
            require(reference is not None, cid + ': missing stage artifact: ' + name)
        if reference is not None:
            checked_path(reference, root)
    for link in item['internal_links']:
        if link['target_content_id'] is not None:
            require(link['target_content_id'] in ids, cid + ': unknown internal target content_id')
    measurement = item['performance']['measurement']
    if measurement['window_start'] and measurement['window_end']:
        require(measurement['window_start'] <= measurement['window_end'], cid + ': reversed measurement window')
    for group in ('seo', 'engagement', 'conversion', 'retention'):
        measured = any(value is not None for value in item['performance'][group].values())
        if measured:
            require(all(measurement[key] is not None for key in ('window_start', 'window_end', 'collected_at', 'definition_version')), cid + ': metrics lack measurement provenance')
            require(measurement['source'][group] is not None, cid + ': metrics lack source')
        if item['status'] == 'test_draft':
            require(not measured, cid + ': offline test cannot contain measured performance')


def semantic_checks(index, briefs, root=ROOT):
    ids = [item['content_id'] for item in index['items']]
    require(len(ids) == len(set(ids)), 'Duplicate content_id')
    expected = {item['content_id'] for item in index['items'] if item['artifacts']['brief'] is not None}
    require(set(briefs) == expected, 'Index/brief IDs do not match')
    register = load(root / 'docs/seo/SEO_POLICY_REGISTER.json')
    policies = {policy['version']: policy for policy in register['policy_versions']}
    require(len(policies) == len(register['policy_versions']), 'Duplicate SEO policy version')
    current = register['current_approved_policy']
    if current is not None:
        require(current in policies and policies[current]['status'] == 'approved', 'Current policy is not approved')
    for policy in policies.values():
        approval_keys = ('approved_by', 'approved_at', 'approval_reference', 'effective_at')
        if policy['status'] in ('approved', 'superseded'):
            require(all(policy.get(key) for key in approval_keys), 'Approved policy lacks human approval evidence')
            require(not policy['version'].endswith('-draft'), 'Draft policy cannot be approved')
            for key in ('approved_at', 'effective_at'):
                validate(policy[key], {'type':'string', 'format':'date-time'}, path='policy.' + key)
        elif policy['status'] == 'pending_human_approval':
            require(all(policy.get(key) is None for key in approval_keys), 'Pending policy contains fabricated approval')
    taxonomy = load(root / 'docs/editorial/genre-taxonomy.json')
    genres = [genre['genre_id'] for genre in taxonomy['genres']]
    require(len(genres) == len(set(genres)), 'Duplicate taxonomy genre_id')
    for item in index['items']:
        cid = item['content_id']
        require(item['genre'] in genres, cid + ': unknown genre')
        require(item['seo_policy_version'] in policies, cid + ': unknown SEO policy version')
        policy = policies[item['seo_policy_version']]
        validate_artifacts_and_metrics(item, ids, root)
        brief = briefs.get(cid)
        if brief is None:
            require(item['status'] in ('planned', 'archived') and item['release_gate'] != 'approved', cid + ': current stage requires a brief')
            continue
        for index_key, brief_key in [('content_id', 'content_id'), ('title', 'title'), ('genre', 'genre'),
                ('primary_keyword', 'keyword'), ('secondary_keywords', 'secondary_keywords'),
                ('search_intent', 'search_intent'), ('explicit_need', 'explicit_need'), ('latent_need', 'latent_need'),
                ('persona', 'persona'), ('reader_stage', 'reader_stage'), ('access_type', 'access_type'),
                ('content_depth', 'content_depth'), ('article_type', 'article_type'), ('seo_policy_version', 'seo_policy_version')]:
            require(item[index_key] == brief[brief_key], cid + ': index/brief mismatch: ' + index_key)
        require(item['cta_type'] == brief['cta']['type'], cid + ': CTA type mismatch')
        require(item['cta_destination'] == brief['cta']['destination'], cid + ': CTA destination mismatch')
        require(item['internal_links'] == brief['internal_link_candidates'], cid + ': internal links mismatch')
        if brief['mode'] == 'offline_test':
            require(policy['permitted_scope'] == 'offline_test_articles_and_qa_only', cid + ': policy scope is not offline test')
        else:
            require(policy['status'] in ('approved', 'superseded'), cid + ': production handoff requires approved policy')
            require(policy['permitted_scope'] == 'editorial_production', cid + ': policy scope does not authorize editorial production')
        require(item['artifacts']['brief'] == 'docs/editorial/test-articles/' + cid + '/brief.json' or brief['mode'] != 'offline_test', cid + ': test brief path mismatch')
        if item['status'] in ('approved', 'published') or item['release_gate'] == 'approved':
            require(brief['mode'] == 'a06_handoff' and brief['handoff']['state'] == 'ready', cid + ': release blocked by brief')
        if brief['mode'] == 'offline_test':
            require(item['status'] == 'test_draft', cid + ': offline brief must remain test_draft')
            require(brief['strategy_assessment']['strategy_review_status'] == 'pending', cid + ': offline test cannot imply strategy approval')
        else:
            validate_a06_binding(brief, root)


def validate_a06_binding(brief, root=ROOT):
    source = brief['a06_source']
    a06_brief = load(checked_path(source['brief_ref'], root))
    opportunity = load(checked_path(source['opportunity_ref'], root))
    for value, name in [(a06_brief, 'content_brief'), (opportunity, 'seo_opportunity')]:
        schema = load(root / ('fortune_labo/agents/seo/schemas/' + name + '.schema.json'))
        audit_schema(schema)
        validate(value, schema)
    require(opportunity.get('status') == 'approved', 'A06 opportunity is not approved')
    require(opportunity['moat_alignment'] != 'conflicting', 'A06 moat conflict is unresolved')
    require(not opportunity.get('compliance_flags'), 'A06 compliance flags are unresolved')
    for key in ('tier', 'keyword', 'search_intent'):
        if opportunity.get(key) is not None:
            require(opportunity[key] == a06_brief[key], 'A06 opportunity/brief mismatch: ' + key)
    require(brief['strategy_assessment']['moat_alignment'] == opportunity['moat_alignment'], 'A06 moat assessment mismatch')
    require(source['brief_id'] == a06_brief['id'], 'A06 brief ID mismatch')
    require(source['opportunity_id'] == a06_brief['opportunity_id'] == opportunity['id'], 'A06 opportunity ID mismatch')
    for key in ('tier', 'content_path', 'visit_record_id'):
        require(source[key] == a06_brief.get(key), 'A06 binding mismatch: ' + key)
    for downstream, upstream in [('keyword','keyword'), ('secondary_keywords','secondary_keywords'),
            ('search_intent','search_intent'), ('persona','target_audience'), ('article_type','article_type'), ('title','working_title')]:
        require(brief[downstream] == a06_brief.get(upstream, [] if upstream == 'secondary_keywords' else None), 'A06 mapping mismatch: ' + upstream)
    require(len(brief['h2_h3_intent']) == len(a06_brief['outline']), 'A06 outline requires explicit re-briefing')
    for downstream, upstream in zip(brief['h2_h3_intent'], a06_brief['outline']):
        for key in ('heading_level', 'heading', 'purpose', 'source_requirement'):
            require(downstream[key] == upstream.get(key), 'A06 outline mapping mismatch: ' + key)
    for key in ('type', 'placement', 'copy_direction'):
        require(brief['cta'][key] == a06_brief['cta'].get(key), 'A06 CTA change requires re-briefing: ' + key)
    for upstream in a06_brief['internal_links']:
        require(any(all(candidate[key] == upstream[key] for key in ('target_url', 'anchor_text', 'rationale')) and ('direction' not in upstream or candidate['direction'] == upstream['direction']) for candidate in brief['internal_link_candidates']), 'A06 internal link requirement was dropped')
    if a06_brief['article_type'] in ('shrine_visit_report', 'annual_outlook', 'forecast_review'):
        require(source['content_path'] == 'path_1_firsthand', 'A06 shrine/forecast content requires completed human records')
    if source['content_path'] == 'path_1_firsthand':
        checked_path(brief['personal_experience_needed']['source_ref'], root)
    if brief['handoff']['state'] == 'ready':
        require(brief['strategy_assessment']['moat_alignment'] in ('required','neutral'), 'Ready handoff has unresolved moat conflict')
        if brief['personal_experience_needed']['required']:
            require(brief['personal_experience_needed']['status'] == 'verified', 'Ready handoff lacks personal experience')
            checked_path(brief['personal_experience_needed']['source_ref'], root)
        require(brief['strategy_assessment']['strategy_review_status'] in ('approved','not_required'), 'Strategy review unresolved')
        require(not brief['tbd'] and not source['binding_gaps'], 'Ready handoff contains unresolved requirements')
        require(all(item['status'] != 'pending' for item in brief['evidence_needed']), 'Ready handoff lacks evidence')


def run(root=ROOT, schemas_only=False):
    schema_dir = root / 'docs/editorial/schemas'
    schemas = {}
    paths = sorted(schema_dir.glob('*.schema.json'))
    if schemas_only:
        paths += sorted((root / 'fortune_labo/agents/content-strategy/schemas').glob('*.schema.json'))
        paths += sorted((root / 'fortune_labo/agents/content-production/schemas').glob('*.schema.json'))
        paths += sorted((root / 'fortune_labo/agents/creative/schemas').glob('*.schema.json'))
        paths += sorted((root / 'fortune_labo/agents/wordpress/schemas').glob('*.schema.json'))
    for path in paths:
        schema = load(path)
        audit_schema(schema)
        schemas[path.name] = schema
    if schemas_only:
        print('PASS: ' + str(len(paths)) + ' schema definitions; no private records loaded')
        return
    index = load(root / 'docs/editorial/content-index.json')
    validate(index, schemas['content_index.schema.json'])
    briefs = {}
    for item in index['items']:
        if item['artifacts']['brief'] is None:
            continue
        path = checked_path(item['artifacts']['brief'], root)
        brief = load(path)
        validate(brief, schemas['a07_a08_brief.schema.json'])
        require(brief['content_id'] not in briefs, 'Duplicate brief content_id')
        briefs[brief['content_id']] = brief
    semantic_checks(index, briefs, root)
    print('PASS: ' + str(len(schemas)) + ' schemas; ' + str(len(index['items'])) + ' index records and briefs; artifacts and release gates')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--schemas-only', action='store_true', help='Audit public contracts without private runtime data')
    arguments = parser.parse_args()
    try:
        run(arguments.root.resolve(), arguments.schemas_only)
    except (ValidationError, OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        sys.exit(1)
