"""Join immutable article, A11 assets, QA and draft packaging in one retryable job."""
import copy
import hashlib
import json
from pathlib import Path
from .creative import validate_image_plan
from .strategy import canonical_hash

FAILURE_STATES = {'images': 'image_incomplete', 'A29': 'fact_review_required',
                  'A32': 'editorial_revision_required', 'A28': 'qa_failed',
                  'wordpress': 'draft_sync_failed'}


def build_job(article_path, blueprint_path, image_plan, qa, draft_package, *,
              asset_root, artifact_references, previous_job=None):
    """Validate shared identity; a disconnected dry run never implies a WP draft."""
    validate_image_plan(image_plan, article_path, blueprint_path, asset_root=asset_root)
    blueprint = json.loads(Path(blueprint_path).read_text(encoding='utf-8'))
    cid, article_hash = image_plan['content_id'], image_plan['draft_sha256']
    if hashlib.sha256(Path(article_path).read_bytes()).hexdigest() != article_hash:
        raise ValueError('Article changed during the job')
    for value in (qa, draft_package):
        if value.get('content_id') != cid:
            raise ValueError('Job components belong to different articles')
    if qa.get('draft_sha256') != article_hash or qa.get('image_plan_sha256') != canonical_hash(image_plan):
        raise ValueError('QA belongs to another article or image plan')
    if draft_package.get('source_article_sha256') != article_hash or draft_package.get('qa_reference') != canonical_hash(qa):
        raise ValueError('Draft packaging does not reference this QA and article')
    if draft_package.get('editorial_metadata', {}).get('image_plan_sha256') != canonical_hash(image_plan):
        raise ValueError('Draft packaging uses another image plan')
    metadata = draft_package['editorial_metadata']
    for key in ('seo_policy_version', 'access_type'):
        if metadata.get(key) != blueprint[key]:
            raise ValueError('Draft metadata differs from the source Blueprint: ' + key)
    if metadata.get('article_version') != image_plan['article_version'] or metadata.get('visual_style_version') != image_plan['visual_style_version']:
        raise ValueError('Draft metadata version differs from the source image plan')
    if draft_package['proposed_payload'].get('status') != 'draft':
        raise ValueError('Only a draft payload may enter the job')
    unhashed = {key: value for key, value in draft_package.items() if key != 'package_sha256'}
    if canonical_hash(unhashed) != draft_package.get('package_sha256'):
        raise ValueError('Draft package changed after its review')
    job_id = 'job-' + cid + '-' + article_hash[:12]
    if previous_job and (previous_job.get('job_id') != job_id or previous_job.get('draft_sha256') != article_hash):
        raise ValueError('Retry cannot replace the source article; start a new versioned job')
    active = [row for row in image_plan['images'] if row['visual_type'] != 'NO_IMAGE']
    image_status = 'images_ready'
    if any(row['generation_status'] == 'failed' for row in active):
        image_status = 'image_incomplete'
    elif any(row['generation_status'] not in ('generated', 'supplied') for row in active):
        image_status = 'image_generation_pending'
    states = {'article': 'article_ready', 'images': image_status}
    for stage in ('A29', 'A32', 'A28'):
        gate = qa['gates'][stage]
        status = gate['status']
        evidence = gate.get('evidence_ref')
        reviewed = isinstance(evidence, str) and bool(evidence.strip()) and gate.get('reviewer_kind') in ('model_review', 'human_review')
        states[stage] = 'passed' if status == 'passed' and reviewed else FAILURE_STATES[stage] if status == 'failed' else 'pending'
    states['wordpress'] = 'draft_sync_pending'
    statuses = ['article_ready']
    if image_status != 'images_ready':
        statuses.extend(['image_incomplete', image_status])
    statuses += [value for value in states.values() if value in FAILURE_STATES.values()]
    statuses.append('draft_sync_pending')
    return {'schema_version': '1.0.0', 'job_id': job_id, 'content_id': cid,
            'pipeline_version': 'article-creative-1.0.0',
            'routing': ['A06', 'A07', 'A08', 'A11', 'A29', 'A32', 'A28', 'A25_draft', 'human_approval', 'human_publish'],
            'article_version': image_plan['article_version'], 'draft_sha256': article_hash,
            'blueprint_sha256': image_plan['blueprint_sha256'],
            'seo_policy_version': blueprint['seo_policy_version'],
            'visual_style_version': image_plan['visual_style_version'],
            'image_plan_sha256': canonical_hash(image_plan), 'qa_sha256': canonical_hash(qa),
            'draft_package_sha256': draft_package['package_sha256'],
            'access_type': blueprint['access_type'], 'stage_status': states,
            'statuses': list(dict.fromkeys(statuses)), 'article_preserved': True,
            'artifacts': copy.deepcopy(artifact_references),
            'assets': [{'image_id': row['image_id'], 'section_id': row['section_id'],
                        'asset_id': row['generated_asset_reference']['asset_id'],
                        'image_sha256': row['generated_asset_reference']['image_sha256']}
                       for row in active if row['generated_asset_reference']],
            'attempts': copy.deepcopy(previous_job.get('attempts', [])) if previous_job else [],
            'connection_status': 'not_connected', 'wordpress_post_id': None,
            'draft_payload_ready': draft_package['payload_ready'], 'execution_allowed': False,
            'publication_allowed': False, 'human_approval': None,
            'human_approval_required_before_publish': True}


def record_failure(job, stage, error):
    """Record a retryable stage failure without deleting the completed article."""
    if stage not in FAILURE_STATES or not isinstance(error, str) or not error.strip():
        raise ValueError('Record a known stage and an actual error')
    result = copy.deepcopy(job)
    state = FAILURE_STATES[stage]
    result['stage_status'][stage] = state
    result['statuses'] = list(dict.fromkeys(['article_ready', *result['statuses'], state]))
    result['attempts'].append({'attempt': len(result['attempts']) + 1,
                              'stage': stage, 'result': state, 'error': error,
                              'draft_sha256': result['draft_sha256'], 'retryable': True})
    result['article_preserved'] = True
    result['draft_payload_ready'] = False
    result['publication_allowed'] = False
    return result
