"""A08 offline orchestration: immutable brief, blueprint, draft acceptance, review.

The caller supplies model/human prose. This module never calls an LLM or claims
that deterministic templating is autonomous article generation or human QA.
"""
import copy
import hashlib
import json
import re
from pathlib import Path
from .strategy import ROOT, canonical_hash, validate_brief, _validator

REVIEW_CHECKS = (
    'search_intent', 'explicit_need', 'latent_need', 'paragraph_flow',
    'sentence_variation', 'ending_variation', 'heading_density', 'list_density',
    'non_uniform_structure', 'concrete_examples', 'claim_separation',
    'no_fabricated_experience', 'free_completeness', 'premium_difference',
    'natural_cta', 'internal_link_candidates', 'seo_policy_trace')
RULES = ROOT / 'docs/editorial/ARTICLE_PRODUCTION_RULES.md'
POLICY_REGISTER = ROOT / 'docs/seo/SEO_POLICY_REGISTER.json'


def _sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def _private_path(path, private_root):
    path, private_root, public_root = Path(path).resolve(), Path(private_root).resolve(), ROOT.resolve()
    if private_root == public_root or private_root in public_root.parents or public_root in private_root.parents:
        raise ValueError('private_root must be separate from the public repository')
    if path != private_root and private_root not in path.parents:
        raise ValueError('Run output must remain inside private_root')
    return path


def _write_json(path, value, exclusive=False):
    with path.open('x' if exclusive else 'w', encoding='utf-8') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write('\n')


def _load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def _validate_artifact(value, name):
    validator = _validator()
    schema = validator.load(ROOT / ('fortune_labo/agents/content-production/schemas/' + name + '.schema.json'))
    validator.audit_schema(schema)
    validator.validate(value, schema)


def _require_registered_offline_policy(version):
    """Check this exact stored version; never substitute the newest policy.

    A register may gain other versions without invalidating a historical run.
    The selected record must still permit the offline operation. A caller's
    input-manifest hash is provenance, not authority to bypass this boundary.
    """
    register = _load(POLICY_REGISTER)
    matches = [row for row in register.get('policy_versions', []) if row.get('version') == version]
    if len(matches) != 1:
        raise ValueError('A08 requires an exactly registered SEO policy version')
    policy = matches[0]
    if policy.get('permitted_scope') != 'offline_test_articles_and_qa_only':
        raise ValueError('Registered policy scope does not permit this offline run')
    if policy.get('status') != 'pending_human_approval' or not version.endswith('-draft'):
        raise ValueError('Registered policy state does not permit this offline run')
    approval_fields = ('approved_by', 'approved_at', 'approval_reference', 'effective_at')
    if any(key not in policy or policy[key] is not None for key in approval_fields):
        raise ValueError('Registered draft policy has inconsistent approval state')
    if policy.get('external_write_authorized') is not False or register.get('current_approved_policy') == version:
        raise ValueError('Registered draft policy has inconsistent publication authority')


def self_review_template():
    return {'reviewer_kind':'model_self_review', 'checks':[
        {'check_id':check, 'status':'needs_review', 'evidence':'TBD', 'notes':'TBD'}
        for check in REVIEW_CHECKS], 'known_gaps':[], 'human_approval':None}


def build_blueprint(brief):
    validate_brief(brief)
    return {'schema_version':'1.0.0', 'content_id':brief['content_id'],
        'brief_sha256':canonical_hash(brief), 'seo_policy_version':brief['seo_policy_version'],
        'core_answer':brief['core_answer'], 'access_type':brief['access_type'],
        'access_rationale':brief['access_rationale'],
        'sections':copy.deepcopy(brief['h2_h3_intent']),
        'evidence_needed':copy.deepcopy(brief['evidence_needed']),
        'personal_experience_needed':copy.deepcopy(brief['personal_experience_needed']),
        'internal_link_candidates':copy.deepcopy(brief['internal_link_candidates']),
        'cta':copy.deepcopy(brief['cta']),
        'writing_rules_reference':'docs/editorial/ARTICLE_PRODUCTION_RULES.md',
        'publication_allowed':False, 'human_approval':None}


def prepare_run(brief, output_dir, *, private_root, rules_path=None):
    """Create a new private run. Refuses reuse/overwrite of an existing run."""
    validate_brief(brief)
    _require_registered_offline_policy(brief['seo_policy_version'])
    run = _private_path(output_dir, private_root)
    rules_path = Path(rules_path or RULES).resolve()
    if rules_path != RULES.resolve():
        raise ValueError('ARTICLE_PRODUCTION_RULES.md is the only writing source of truth')
    rules_text = rules_path.read_text(encoding='utf-8')
    blueprint = build_blueprint(brief)
    blueprint['writing_rules_sha256'] = _sha(rules_text)
    _validate_artifact(blueprint, 'blueprint')
    run.mkdir(parents=True, exist_ok=False)
    _write_json(run / 'brief.json', brief, exclusive=True)
    _write_json(run / 'blueprint.json', blueprint, exclusive=True)
    (run / 'writing-rules.md').write_text(rules_text, encoding='utf-8')
    prompt = (ROOT / 'fortune_labo/agents/content-production/prompts/draft.md').read_text(encoding='utf-8')
    prompt += '\n\n## Immutable brief\n\n```json\n' + json.dumps(brief, ensure_ascii=False, indent=2) + '\n```\n'
    prompt += '\n## Writing rules snapshot\n\n' + rules_text
    (run / 'draft-prompt.md').write_text(prompt, encoding='utf-8')
    _write_json(run / 'self-review-template.json', self_review_template(), exclusive=True)
    manifest = {'schema_version':'1.0.0', 'content_id':brief['content_id'],
        'state':'awaiting_external_draft', 'brief_sha256':canonical_hash(brief),
        'blueprint_sha256':canonical_hash(blueprint), 'rules_sha256':_sha(rules_text),
        'prompt_sha256':_sha(prompt), 'draft_sha256':None, 'self_review_sha256':None,
        'seo_policy_version':brief['seo_policy_version'], 'publication_allowed':False,
        'human_approval':None, 'next_stage':'A08_external_writer'}
    _write_json(run / 'run.json', manifest, exclusive=True)
    return copy.deepcopy(manifest)


def writing_findings(text):
    """Conservative structural indicators, never proof of natural Japanese."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError('Non-empty externally authored draft text is required')
    lines = text.splitlines()
    prose = [line.strip() for line in lines if line.strip() and not line.lstrip().startswith(('#', '-', '*', '>', '|', '```'))]
    blocks = [part.strip() for part in re.split(r'\n\s*\n', text) if part.strip()]
    paragraphs = [block for block in blocks if not block.startswith(('#', '-', '*', '>', '|', '```'))]
    fragmented = [index + 1 for index, block in enumerate(paragraphs)
                  if len(block) < 45 and len(re.findall(r'[。！？.!?](?:\s|$)', block)) <= 1]
    sentence_lines = sum(1 for line in prose if re.search(r'[。！？.!?]$', line) and len(re.findall(r'[。！？.!?]', line)) == 1)
    findings = []
    if len(fragmented) >= 3:
        findings.append({'code':'short_paragraph_run', 'severity':'review', 'paragraph_numbers':fragmented})
    if len(prose) >= 5 and sentence_lines / len(prose) >= 0.8:
        findings.append({'code':'one_sentence_per_line', 'severity':'review', 'line_count':sentence_lines})
    if not re.search(r'^##\s+\S', text, re.MULTILINE):
        findings.append({'code':'missing_h2_structure', 'severity':'review'})
    if len(re.findall(r'^###?\s+', text, re.MULTILINE)) > max(3, len(text) // 160):
        findings.append({'code':'dense_headings', 'severity':'review'})
    if re.search(r'\bTBD\b|https?://[^\s)]+(?:TBD|placeholder)', text):
        findings.append({'code':'unresolved_reader_facing_placeholder', 'severity':'review'})
    return {'schema_version':'1.0.0', 'method':'structural_heuristic_not_quality_verdict',
            'findings':findings, 'paragraph_count':len(paragraphs),
            'requires_editorial_review':True}


def _check_review(review):
    if review.get('reviewer_kind') not in ('model_self_review', 'human_editorial_review'):
        raise ValueError('Review must identify the real reviewer type')
    if review.get('human_approval') is not None:
        raise ValueError('A08 self review never creates human publication approval')
    checks = review.get('checks', [])
    if len(checks) != len(REVIEW_CHECKS) or {row.get('check_id') for row in checks} != set(REVIEW_CHECKS):
        raise ValueError('Every self-review criterion is required exactly once')
    for check in checks:
        if check.get('status') not in ('passed', 'needs_revision', 'not_applicable'):
            raise ValueError('Self review must resolve needs_review before acceptance')
        if not check.get('evidence') or check['evidence'] == 'TBD' or not isinstance(check.get('notes'), str):
            raise ValueError('Self review requires concrete evidence and notes')
    if not isinstance(review.get('known_gaps'), list):
        raise ValueError('Self review must preserve known gaps')


def accept_draft(run_dir, draft_text, self_review, *, private_root):
    """Store caller-authored prose and evidence-backed self review once."""
    run = _private_path(run_dir, private_root)
    before = verify_run(run, private_root=private_root)
    if before['state'] != 'awaiting_external_draft':
        raise ValueError('A completed run is immutable; prepare a new run for revisions')
    _check_review(self_review)
    findings = writing_findings(draft_text)
    brief = _load(run / 'brief.json')
    if draft_text.lstrip().splitlines()[0] != '# ' + brief['title']:
        raise ValueError('Draft H1 must retain the exact A07 working title for this run')
    missing_headings = [row['heading'] for row in brief['h2_h3_intent']
                        if not re.search(r'^' + re.escape('## ' if row['heading_level'] == 'h2' else '### ') + re.escape(row['heading']) + r'\s*$', draft_text, re.MULTILINE)]
    actual_headings = re.findall(r'^(#{2,3})\s+(.+?)\s*$', draft_text, re.MULTILINE)
    expected_headings = [('##' if row['heading_level'] == 'h2' else '###', row['heading']) for row in brief['h2_h3_intent']]
    if missing_headings or actual_headings != expected_headings:
        raise ValueError('A08 cannot silently change the Brief outline: ' + ', '.join(missing_headings))
    review = copy.deepcopy(self_review)
    review['content_id'] = brief['content_id']
    review['brief_sha256'] = canonical_hash(brief)
    review['draft_sha256'] = _sha(draft_text)
    review['seo_policy_version'] = brief['seo_policy_version']
    _validate_artifact(review, 'self_review')
    (run / 'article.md').write_text(draft_text, encoding='utf-8')
    _write_json(run / 'self-review.json', review, exclusive=True)
    _write_json(run / 'writing-findings.json', findings, exclusive=True)
    manifest = _load(run / 'run.json')
    manifest.update(state='draft_and_self_review_recorded', draft_sha256=_sha(draft_text),
                    self_review_sha256=canonical_hash(review), next_stage='A29_contract_only')
    _write_json(run / 'run.json', manifest)
    return {'manifest':copy.deepcopy(manifest), 'writing_findings':findings,
            'release_gate':'blocked', 'quality_verdict':'requires_A29_A32_A28_and_human_approval'}


def verify_run(run_dir, *, private_root):
    run = _private_path(run_dir, private_root)
    manifest = _load(run / 'run.json')
    brief = _load(run / 'brief.json')
    blueprint = _load(run / 'blueprint.json')
    validate_brief(brief)
    _require_registered_offline_policy(brief['seo_policy_version'])
    _validate_artifact(manifest, 'run')
    _validate_artifact(blueprint, 'blueprint')
    checks = [('brief_sha256', canonical_hash(brief)), ('blueprint_sha256', canonical_hash(blueprint)),
              ('rules_sha256', _sha((run / 'writing-rules.md').read_text(encoding='utf-8'))),
              ('prompt_sha256', _sha((run / 'draft-prompt.md').read_text(encoding='utf-8')))]
    if manifest.get('state') == 'draft_and_self_review_recorded':
        article = (run / 'article.md').read_text(encoding='utf-8')
        review = _load(run / 'self-review.json')
        _check_review(review)
        _validate_artifact(review, 'self_review')
        checks.extend([('draft_sha256', _sha(article)), ('self_review_sha256', canonical_hash(review))])
        if review['brief_sha256'] != manifest['brief_sha256'] or review['draft_sha256'] != _sha(article):
            raise ValueError('Review is not bound to this exact brief and draft')
        if review['seo_policy_version'] != brief['seo_policy_version']:
            raise ValueError('Self review SEO policy trace mismatch')
    elif manifest.get('state') != 'awaiting_external_draft':
        raise ValueError('Unknown run state')
    for key, actual in checks:
        if manifest.get(key) != actual:
            raise ValueError('Immutable input or output changed: ' + key)
    if manifest['seo_policy_version'] != brief['seo_policy_version'] or blueprint['seo_policy_version'] != brief['seo_policy_version']:
        raise ValueError('SEO policy trace mismatch')
    if blueprint['brief_sha256'] != manifest['brief_sha256']:
        raise ValueError('Blueprint does not reference immutable brief')
    if manifest.get('publication_allowed') is not False or manifest.get('human_approval') is not None:
        raise ValueError('A08 run cannot grant publication authority')
    return copy.deepcopy(manifest)
