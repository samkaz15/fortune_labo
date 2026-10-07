"""A25 draft packaging only. No credentials, transport, scheduling or publish API."""
from copy import deepcopy
from hashlib import sha256
from html import escape
from pathlib import PurePosixPath
import json
import re
from urllib.parse import urlsplit


def digest(value):
    return sha256(value.encode('utf-8')).hexdigest()


def canonical_hash(value):
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False))


def _https(value):
    parsed = urlsplit(value or '')
    return parsed.scheme == 'https' and bool(parsed.netloc) and not parsed.username and not parsed.password


def _inline(text):
    """Escape author text; render only explicit safe Markdown links and emphasis."""
    pattern = r'\[([^\]\n]+)\]\((https?://[^\s)]+)\)'
    pieces, cursor = [], 0
    for match in re.finditer(pattern, text):
        pieces.append(escape(text[cursor:match.start()]))
        href = match.group(2)
        parts = urlsplit(href)
        if parts.username or parts.password:
            raise ValueError('Article links cannot contain URL credentials')
        pieces.append('<a href="' + escape(href, quote=True) + '">' + escape(match.group(1)) + '</a>')
        cursor = match.end()
    pieces.append(escape(text[cursor:]))
    value = ''.join(pieces)
    value = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', value)
    value = re.sub(r'`([^`]+)`', r'<code>\1</code>', value)
    return value


def render_markdown(source, *, insertions=None, title=None):
    """Deterministic formatting projection; source article bytes remain unchanged.

    Supports the A08 fixture subset: headings, prose, simple lists, pipe tables,
    inline code/emphasis and explicit HTTP(S) links. Raw HTML is escaped. The
    source H1 supplies the official post title and is omitted from the body
    projection when it exactly matches title, avoiding a duplicated page H1.
    """
    insertions = insertions or {}
    lines, output, i = source.splitlines(), [], 0
    if title is not None:
        if not lines or lines[0] != '# ' + title:
            raise ValueError('Article title must match the immutable A08 H1')
        i = 1
    active_section = None
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        heading = re.fullmatch(r'(#{1,6})\s+(.+)', line)
        if heading:
            level, title = len(heading[1]), heading[2]
            if level == 2:
                if active_section:
                    output.extend(insertions.get(('after_section', active_section), []))
                active_section = title
            output.append(f'<h{level}>' + _inline(title) + f'</h{level}>')
            if level == 2:
                output.extend(insertions.get(('after_h2', title), []))
            i += 1
            continue
        if line.startswith('|') and i + 1 < len(lines) and re.fullmatch(r'[\s|:\-]+', lines[i + 1]):
            headers = [cell.strip() for cell in line.strip('|').split('|')]
            table = ['<table><thead><tr>' + ''.join('<th>' + _inline(cell) + '</th>' for cell in headers) + '</tr></thead><tbody>']
            i += 2
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [cell.strip() for cell in lines[i].strip().strip('|').split('|')]
                if len(cells) != len(headers):
                    raise ValueError('Table formatting requires a consistent column count')
                table.append('<tr>' + ''.join('<td>' + _inline(cell) + '</td>' for cell in cells) + '</tr>')
                i += 1
            table.append('</tbody></table>')
            output.append('\n'.join(table))
            continue
        unordered = bool(re.match(r'^[-*]\s+', line))
        ordered = bool(re.match(r'^\d+\.\s+', line))
        if unordered or ordered:
            tag, pattern = ('ul', r'^[-*]\s+') if unordered else ('ol', r'^\d+\.\s+')
            items = []
            while i < len(lines) and re.match(pattern, lines[i].strip()):
                items.append('<li>' + _inline(re.sub(pattern, '', lines[i].strip())) + '</li>')
                i += 1
            output.append('<' + tag + '>' + ''.join(items) + '</' + tag + '>')
            continue
        paragraph = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(?:#{1,6}\s|[-*]\s|\d+\.\s|\|)', lines[i].strip()):
            paragraph.append(lines[i].strip())
            i += 1
        output.append('<p>' + _inline('\n'.join(paragraph)) + '</p>')
    if active_section:
        output.extend(insertions.get(('after_section', active_section), []))
    return '\n\n'.join(output)


def _media_key(site_id, content_id, image_hash):
    return digest('|'.join([site_id or 'unconnected', content_id, image_hash]))


def _check_receipt(receipt, *, asset, content_id, site_id, fixture_mode):
    if receipt.get('state') not in ('uploaded', 'failed'):
        raise ValueError('A media receipt must record uploaded or failed state')
    for key, expected in [('content_id', content_id), ('image_sha256', asset['image_sha256']), ('asset_id', asset['asset_id']), ('site_id', site_id)]:
        if not expected or receipt.get(key) != expected:
            raise ValueError('Media receipt identity mismatch: ' + key)
    receipt_type = receipt.get('receipt_type')
    if receipt_type == 'test_fixture' and not fixture_mode:
        raise ValueError('Fabricated fixture attachment IDs cannot enter a normal runtime payload')
    if receipt_type not in ('wordpress_response', 'test_fixture'):
        raise ValueError('Attachment IDs require WordPress response provenance')
    if not receipt.get('response_reference'):
        raise ValueError('Media receipt lacks response provenance')
    if receipt['state'] == 'uploaded':
        mid = receipt.get('attachment_id')
        if not isinstance(mid, int) or isinstance(mid, bool) or mid <= 0 or not _https(receipt.get('source_url')):
            raise ValueError('Uploaded receipt requires a positive received ID and HTTPS source URL')
    elif receipt.get('attachment_id') is not None:
        raise ValueError('Failed upload cannot retain a successful attachment ID')


def _meta_payload(metadata, seo_meta, site_config):
    """Only explicitly mapped, REST-registered keys may enter WordPress meta."""
    source = dict(metadata)
    source.update({'seo.' + key: value for key, value in (seo_meta or {}).items()})
    result = {}
    registrations = site_config.get('registered_meta', {})
    for logical, wp_key in site_config.get('meta_mapping', {}).items():
        if logical not in source or wp_key not in registrations:
            raise ValueError('Unknown logical metadata or unverified REST registration: ' + logical)
        registration = registrations[wp_key]
        if not registration.get('registration_reference') or registration.get('rest_writable') is not True:
            raise ValueError('Meta mapping requires explicit writable REST registration evidence')
        if wp_key in result:
            raise ValueError('Multiple logical fields target the same WordPress meta key')
        value = source[logical]
        if value is None:
            continue
        types = {'string': str, 'integer': int, 'boolean': bool, 'object': dict, 'array': list}
        expected = types.get(registration.get('type'))
        if not expected or not isinstance(value, expected) or expected is int and isinstance(value, bool):
            raise ValueError('Meta value differs from its registered WordPress type: ' + wp_key)
        result[wp_key] = deepcopy(value)
    return result


def build_draft_payload(article, image_plan, qa, *, media_receipts=None, site_config=None,
                        requested_status='draft', fixture_mode=False):
    """Build a reviewable preview; inputs are never mutated and no network runs."""
    if requested_status != 'draft' or article.get('status', 'draft') != 'draft':
        raise ValueError('A25 accepts WordPress status draft only')
    site_config, media_receipts = deepcopy(site_config or {}), deepcopy(media_receipts or [])
    cid, content = article.get('content_id'), article.get('content')
    if not cid or not article.get('title') or not isinstance(content, str) or not content.strip():
        raise ValueError('Article ID, exact title and source content are required')
    if article.get('content_format', 'markdown') != 'markdown':
        raise ValueError('This adapter accepts the immutable A08 Markdown source format only')
    draft_hash = digest(content)
    if article.get('draft_sha256') != draft_hash or image_plan.get('draft_sha256') != draft_hash:
        raise ValueError('Article or creative source hash mismatch')
    if image_plan.get('content_id') != cid or qa.get('content_id') != cid:
        raise ValueError('Article, creative and QA must share the same content ID')
    if image_plan.get('article_version') != article.get('article_version') or not article.get('article_version'):
        raise ValueError('Article and visual plan versions differ')
    visual_version = image_plan.get('visual_style_version')
    if not visual_version:
        raise ValueError('Visual style version is required')
    plan_hash = canonical_hash(image_plan)
    if qa.get('draft_sha256') != draft_hash or qa.get('image_plan_sha256') != plan_hash:
        raise ValueError('QA is stale for the current article or image plan')
    gates = qa.get('gates', {})
    if set(gates) != {'A29', 'A32', 'A28'}:
        raise ValueError('Exactly A29, A32 and A28 QA gates are required')
    blockers = list(qa.get('blockers', []))
    for name, gate in gates.items():
        if gate.get('status') != 'passed' or not isinstance(gate.get('evidence_ref'), str) or not gate['evidence_ref'].strip() or gate.get('reviewer_kind') not in ('model_review', 'human_review'):
            blockers.append(name + '_not_passed_with_evidence')
    if qa.get('scope') not in ('offline_fixture', 'draft_preparation'):
        blockers.append('qa_scope_unverified')
    images = image_plan.get('images', [])
    featured = [image for image in images if image.get('placement') == 'featured']
    if len(featured) != 1:
        raise ValueError('Exactly one featured image plan is required')
    h2s = re.findall(r'^##\s+(.+?)\s*$', content, flags=re.MULTILINE)
    if len(h2s) != len(set(h2s)):
        raise ValueError('Duplicate H2 text requires distinct rendering anchors before A25')
    image_ids, asset_ids, receipts_used, media_by_key, insertions, inline_media = set(), {}, set(), {}, {}, []
    featured_media = None
    for image in images:
        image_id = image.get('image_id')
        if not image_id or image_id in image_ids or image.get('content_id') != cid:
            raise ValueError('Image IDs must be unique and bound to the article')
        image_ids.add(image_id)
        placement = image.get('placement')
        if placement == 'none':
            if image.get('generation_status') != 'not_applicable' or not image.get('no_image_reason'):
                raise ValueError('NO_IMAGE requires a reason and not_applicable status')
            continue
        if placement not in ('featured', 'after_h2', 'after_section'):
            raise ValueError('Unsupported explicit image placement')
        heading = image.get('section_heading')
        if placement != 'featured' and heading not in h2s:
            raise ValueError('Inline image heading is absent from the immutable article')
        asset = image.get('generated_asset_reference')
        receipt, attachment_id, source_url = None, None, None
        if image.get('generation_status') not in ('generated', 'supplied') or not asset:
            blockers.append('image_incomplete:' + image_id)
        else:
            if asset.get('state') not in ('generated', 'supplied') or not re.fullmatch(r'[0-9a-f]{64}', asset.get('image_sha256', '')) or not asset.get('asset_id'):
                raise ValueError('Generated asset requires identity, hash and state')
            asset_id = asset['asset_id']
            relative = PurePosixPath(asset.get('relative_path') or '')
            if not asset.get('relative_path') or relative.is_absolute() or '..' in relative.parts or '\\' in str(relative):
                raise ValueError('Asset path must be a safe relative path within the validated A11 asset root')
            format_supported = asset.get('mime_type') in ('image/png', 'image/jpeg', 'image/webp')
            if not format_supported:
                blockers.append('media_format_requires_conversion:' + image_id)
            if asset_id in asset_ids and asset_ids[asset_id] != asset['image_sha256']:
                raise ValueError('An asset ID cannot refer to multiple image hashes')
            asset_ids[asset_id] = asset['image_sha256']
            matches = [(index, row) for index, row in enumerate(media_receipts) if row.get('asset_id') == asset_id]
            if len(matches) > 1:
                raise ValueError('Select the latest reconciled media receipt; duplicates are ambiguous')
            if matches:
                receipt_index, receipt = matches[0]
                receipts_used.add(receipt_index)
                _check_receipt(receipt, asset=asset, content_id=cid, site_id=site_config.get('site_id'), fixture_mode=fixture_mode)
                if not format_supported:
                    raise ValueError('Unsupported media formats cannot receive automatic WordPress association')
                if receipt['state'] == 'uploaded':
                    attachment_id, source_url = receipt['attachment_id'], receipt['source_url']
            key = _media_key(site_config.get('site_id'), cid, asset['image_sha256'])
            media_metadata = {'title': image_id, 'alt_text': image.get('alt'), 'caption': image.get('caption')}
            if key not in media_by_key:
                media_by_key[key] = {'dedup_key': key, 'content_id': cid, 'asset_ids': [asset_id],
                    'image_sha256': asset['image_sha256'], 'relative_path': asset.get('relative_path'),
                    'mime_type': asset.get('mime_type'), 'metadata': media_metadata,
                    'action': 'requires_conversion' if not format_supported else 'reuse_attachment' if attachment_id else 'retry_upload' if receipt else 'upload',
                    'attachment_id': attachment_id, 'response_reference': receipt.get('response_reference') if receipt else None,
                    'association': {'post': None, 'state': 'after_draft_creation'}}
            else:
                row = media_by_key[key]
                if asset_id not in row['asset_ids']:
                    row['asset_ids'].append(asset_id)
                if row['attachment_id'] and attachment_id and row['attachment_id'] != attachment_id:
                    raise ValueError('Same image hash has conflicting uploaded attachments; reconcile before retry')
                if attachment_id and not row['attachment_id']:
                    row.update(action='reuse_attachment', attachment_id=attachment_id, response_reference=receipt['response_reference'])
                elif row['attachment_id']:
                    attachment_id = row['attachment_id']
                    previous = next(r for r in media_receipts if r.get('attachment_id') == attachment_id)
                    source_url = previous['source_url']
            if attachment_id is None:
                blockers.append('media_upload_required:' + image_id)
        if placement == 'featured':
            featured_media = attachment_id
        else:
            figure = '<!-- A25 pending image: ' + escape(image_id) + ' -->'
            if attachment_id and source_url:
                figure = '<figure class="wp-block-image"><img src="' + escape(source_url, quote=True) + '" alt="' + escape(image.get('alt') or '', quote=True) + '" class="wp-image-' + str(attachment_id) + '"/>'
                if image.get('caption'):
                    figure += '<figcaption>' + escape(image['caption']) + '</figcaption>'
                figure += '</figure>'
            insertions.setdefault((placement, heading), []).append(figure)
            inline_media.append({'image_id': image_id, 'attachment_id': attachment_id,
                                 'section_heading': heading, 'placement': placement,
                                 'alt_text': image.get('alt'), 'caption': image.get('caption')})
    if len(receipts_used) != len(media_receipts):
        raise ValueError('Media receipt references an asset outside this image plan')
    for key in ('categories', 'tags'):
        values = article.get(key)
        if values is not None and (not isinstance(values, list) or any(not isinstance(value, int) or isinstance(value, bool) or value <= 0 for value in values)):
            raise ValueError('WordPress taxonomy associations require actual positive term IDs: ' + key)
    metadata = {'content_id': cid, 'access_type': article.get('access_type'),
                'seo_policy_version': article.get('seo_policy_version'), 'article_version': article['article_version'],
                'visual_style_version': visual_version, 'draft_sha256': draft_hash, 'image_plan_sha256': plan_hash,
                'fact_check_status': gates['A29'].get('status'), 'qa_status': gates['A28'].get('status'),
                'internal_links': deepcopy(article.get('internal_links')), 'cta': deepcopy(article.get('cta'))}
    payload = {'status': 'draft', 'title': article['title'], 'content': render_markdown(content, insertions=insertions, title=article['title']),
               'excerpt': article.get('excerpt'), 'slug': article.get('slug'), 'categories': article.get('categories'),
               'tags': article.get('tags'), 'featured_media': featured_media,
               'meta': _meta_payload(metadata, article.get('seo_meta'), site_config)}
    blockers = sorted(set(blockers))
    ready = not blockers
    request_payload = {key: value for key, value in payload.items() if value is not None} if ready else None
    result = {'schema_version': '1.0.0', 'content_id': cid, 'site_id': site_config.get('site_id'), 'mode': 'test_fixture' if fixture_mode else 'dry_run',
            'state': 'payload_ready' if ready else 'preview_blocked', 'payload_ready': ready,
            'network_ready': False, 'publication_allowed': False, 'human_approval_required_before_publish': True,
            'proposed_payload': payload, 'request_payload': request_payload,
            'media_upload_plan': list(media_by_key.values()), 'inline_media': inline_media,
            'editorial_metadata': metadata, 'seo_metadata': deepcopy(article.get('seo_meta')),
            'qa_reference': canonical_hash(qa), 'blockers': blockers,
            'source_article_sha256': draft_hash, 'rendered_content_sha256': digest(payload['content']),
            'connection_status': 'not_connected', 'wordpress_post_id': None}
    result['package_sha256'] = canonical_hash(result)
    from .strategy import ROOT, _validator
    validator = _validator()
    schema = validator.load(ROOT / 'fortune_labo/agents/wordpress/schemas/draft_payload.schema.json')
    validator.audit_schema(schema)
    validator.validate(result, schema)
    return result


def association_plan(envelope, post_receipt):
    """Prepare media-to-post association after a received DRAFT response, never send."""
    if canonical_hash({key: value for key, value in envelope.items() if key != 'package_sha256'}) != envelope.get('package_sha256'):
        raise ValueError('Draft package changed after QA-bound preparation')
    if not envelope.get('payload_ready') or envelope['proposed_payload'].get('status') != 'draft':
        raise ValueError('Cannot associate media before the draft payload is ready')
    if not envelope.get('site_id') or post_receipt.get('site_id') != envelope['site_id']:
        raise ValueError('Draft response site identity differs from the prepared media package')
    post_id = post_receipt.get('id')
    if not isinstance(post_id, int) or isinstance(post_id, bool) or post_id <= 0 or post_receipt.get('status') != 'draft':
        raise ValueError('Association requires an actual WordPress DRAFT response ID')
    if post_receipt.get('content_id') != envelope['content_id'] or not post_receipt.get('response_reference'):
        raise ValueError('Draft response lacks content identity or response provenance')
    if post_receipt.get('receipt_type') == 'test_fixture' and envelope['mode'] != 'test_fixture':
        raise ValueError('Fixture post IDs cannot enter normal runtime')
    if post_receipt.get('receipt_type') not in ('wordpress_response', 'test_fixture'):
        raise ValueError('Post ID requires WordPress response provenance')
    return [{'endpoint': '/wp/v2/media/' + str(media['attachment_id']),
             'payload': {'post': post_id}, 'dedup_key': media['dedup_key'],
             'asset_ids': list(media['asset_ids']), 'content_id': envelope['content_id']}
            for media in envelope['media_upload_plan'] if media['attachment_id']]


def execute_draft(*args, **kwargs):
    """Deliberately unavailable; a future connection is a separate implementation."""
    raise RuntimeError('WordPress write transport is not connected; dry-run packaging only')
