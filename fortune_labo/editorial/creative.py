"""A11: version-bound image planning and verified local assets; no generation API."""
import copy
import hashlib
import json
import re
import struct
import zlib
import xml.etree.ElementTree as ET
from pathlib import Path
from .strategy import ROOT, canonical_hash, _validator

VISUAL_IDENTITY = ROOT / 'docs/editorial/VISUAL_IDENTITY.md'
VISUAL_STYLE_VERSION = 'visual-style-0.1.0'
IMAGE_ROLES = ('featured', 'section', 'diagram', 'explanation', 'atmosphere', 'example')
VISUAL_TYPES = ('PHOTO', 'ILLUSTRATION', 'DIAGRAM', 'INFOGRAPHIC', 'ABSTRACT', 'NO_IMAGE')


def _hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _local_file(path, root):
    root, path = Path(root).resolve(), Path(path).resolve()
    if root not in path.parents or not path.is_file():
        raise ValueError('Asset must be an existing file inside asset_root')
    return path


def _source_ref(path):
    path = Path(path).resolve()
    try:
        return path.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return 'private-local-source'


def article_sections(article_path, blueprint_path):
    article = Path(article_path).read_text(encoding='utf-8')
    blueprint = json.loads(Path(blueprint_path).read_text(encoding='utf-8'))
    headings = re.findall(r'^##[ \t]+(.+?)[ \t]*$', article, re.MULTILINE)
    expected = [row['heading'] for row in blueprint['sections'] if row['heading_level'] == 'h2']
    if headings != expected:
        raise ValueError('Article H2 headings differ from the immutable Blueprint')
    return [{'section_id':'h2-' + str(index + 1).zfill(2), 'section_heading':heading}
            for index, heading in enumerate(headings)]


def image_template(content_id, image_id, *, section_id, section_heading=None,
                   image_role='section', visual_type='NO_IMAGE', no_image_reason=None):
    """Return a complete template; actual visual decisions remain with A11's caller."""
    no_image = visual_type == 'NO_IMAGE'
    return {'image_id':image_id, 'content_id':content_id, 'image_role':image_role,
        'visual_type':visual_type, 'section_id':section_id, 'section_heading':section_heading,
        'purpose':no_image_reason or 'TBD', 'visual_subject':None if no_image else 'TBD',
        'composition':None if no_image else 'TBD', 'environment':None if no_image else 'TBD',
        'lighting':None if no_image else 'TBD', 'mood':None if no_image else 'TBD',
        'aspect_ratio':None if no_image else '16:9', 'recommended_width':None if no_image else 1536,
        'recommended_height':None if no_image else 864, 'alt':None if no_image else 'TBD',
        'alt_text':None if no_image else 'TBD',
        'caption':None, 'generation_prompt':None if no_image else 'TBD',
        'negative_requirements':[] if no_image else ['no_long_japanese_text_in_raster', 'no_fabricated_firsthand_evidence', 'no_cosmic_or_occult_cliches'],
        'required':not no_image, 'placement':'none' if no_image else ('featured' if image_role == 'featured' else 'after_h2'),
        'render_method':'none' if no_image else 'raster', 'text_policy':'none', 'text_labels':[],
        'no_image_reason':no_image_reason if no_image else None,
        'generation_status':'not_applicable' if no_image else 'planned', 'generation_error':None,
        'generated_asset_reference':None, 'factual_subject_kind':'none',
        'factual_reference_required':False, 'factual_source_reference':None,
        'requires_actual_photo':False, 'illustrative_disclosure':None}


def _status(images):
    active = [row for row in images if row['visual_type'] != 'NO_IMAGE']
    if not active:
        return 'no_images_required'
    states = [row['generation_status'] for row in active]
    if 'failed' in states:
        return 'needs_attention'
    if all(state in ('generated', 'supplied') for state in states):
        return 'assets_ready_for_qa'
    return 'partially_generated' if any(state in ('generated', 'supplied') for state in states) else 'planned'


def _validate_structure(plan):
    validator = _validator()
    schema = validator.load(ROOT / 'fortune_labo/agents/creative/schemas/article_image_plan.schema.json')
    validator.audit_schema(schema)
    validator.validate(plan, schema)
    if plan['visual_style_version'] != VISUAL_STYLE_VERSION:
        raise ValueError('Unknown visual style version; do not silently use another version')
    if plan['visual_identity_sha256'] != _hash(VISUAL_IDENTITY):
        raise ValueError('Visual identity changed; version and plan need explicit review')
    ids = [row['image_id'] for row in plan['images']]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate image_id')
    featured = [row for row in plan['images'] if row['image_role'] == 'featured' and row['visual_type'] != 'NO_IMAGE']
    if len(featured) > 1 or (not featured and not plan['featured_exception_reason']):
        raise ValueError('Exactly one featured image is expected, or document why none is needed')
    if plan['status'] != _status(plan['images']):
        raise ValueError('Plan status differs from actual asset states')
    for row in plan['images']:
        if row.get('factual_subject_kind', 'none') != 'none' and not row.get('factual_reference_required', False):
            raise ValueError('Real places, people and traditional objects require factual reference review')
        if row.get('requires_actual_photo') and row['visual_type'] != 'PHOTO':
            raise ValueError('Actual-photo requirements must use PHOTO visual type')
        if row['alt_text'] != row['alt']:
            raise ValueError('alt_text and alt compatibility alias must match')
        if row['content_id'] != plan['content_id']:
            raise ValueError('Image content_id differs from its article')
        if row['visual_type'] == 'NO_IMAGE':
            if row['required'] or not row['no_image_reason'] or row['generated_asset_reference'] is not None or row['generation_status'] != 'not_applicable':
                raise ValueError('NO_IMAGE requires an explicit reason and cannot claim an asset')
            if row['render_method'] != 'none' or row['placement'] != 'none':
                raise ValueError('NO_IMAGE has no rendering or placement')
            continue
        for key in ('purpose','visual_subject','composition','environment','lighting','mood','alt','generation_prompt'):
            if row[key] in (None, '', 'TBD'):
                raise ValueError('Planned image requires a concrete ' + key)
        if row['render_method'] == 'none' or row['placement'] == 'none':
            raise ValueError('An image requires a rendering method and placement')
        if row['render_method'] == 'raster':
            if 'no_long_japanese_text_in_raster' not in row['negative_requirements']:
                raise ValueError('Raster generation must forbid embedded long Japanese text')
            if row['text_policy'] == 'native_text_layer':
                raise ValueError('Native text layers cannot be mislabeled as raster generation')
            if any(len(re.findall(r'[\u3040-\u30ff\u3400-\u9fff]', label)) > 12 or len(label) > 24 for label in row['text_labels']):
                raise ValueError('Long Japanese copy belongs in native text, not an AI raster image')
        if row['text_policy'] == 'none' and row['text_labels']:
            raise ValueError('No-text images cannot request text labels')
        ratio = [int(value) for value in row['aspect_ratio'].split(':')]
        if abs(row['recommended_width'] / row['recommended_height'] - ratio[0] / ratio[1]) > 0.01:
            raise ValueError('Recommended dimensions contradict the requested aspect ratio')
        asset = row['generated_asset_reference']
        if row['generation_status'] in ('generated', 'supplied'):
            if asset is None or asset['state'] != row['generation_status']:
                raise ValueError('Completed image requires a matching verified asset reference')
            _validate_factual_asset(row, asset['provenance'])
        elif asset is not None:
            raise ValueError('Pending or failed generation cannot claim a completed asset')
        if row['generation_status'] == 'failed' and not row['generation_error']:
            raise ValueError('Failed generation requires a recorded error')
        if row['generation_status'] != 'failed' and row['generation_error'] is not None:
            raise ValueError('Only failed generation may contain a generation error')
    return True


def create_image_plan(article_path, blueprint_path, *, content_id, article_version,
                      images, visual_style_version=VISUAL_STYLE_VERSION,
                      featured_exception_reason=None):
    blueprint = json.loads(Path(blueprint_path).read_text(encoding='utf-8'))
    images = copy.deepcopy(images)
    for row in images:
        for key, value in {'factual_subject_kind':'none','factual_reference_required':False,
                'factual_source_reference':None,'requires_actual_photo':False,'illustrative_disclosure':None}.items():
            row.setdefault(key, value)
        if row.get('alt_text') in (None, '', 'TBD') and row.get('alt') not in (None, '', 'TBD'):
            row['alt_text'] = row['alt']
        elif row.get('alt') in (None, '', 'TBD') and row.get('alt_text') not in (None, '', 'TBD'):
            row['alt'] = row['alt_text']
        elif 'alt_text' not in row:
            row['alt_text'] = row.get('alt')
    if blueprint['content_id'] != content_id:
        raise ValueError('Blueprint content_id does not match requested article')
    plan = {'schema_version':'1.0.0', 'content_id':content_id, 'article_version':article_version,
        'source_article_reference':_source_ref(article_path), 'source_blueprint_reference':_source_ref(blueprint_path),
        'draft_sha256':_hash(article_path), 'blueprint_sha256':canonical_hash(blueprint),
        'visual_style_version':visual_style_version, 'visual_identity_sha256':_hash(VISUAL_IDENTITY),
        'featured_exception_reason':featured_exception_reason, 'images':copy.deepcopy(images),
        'status':_status(images), 'human_approval':None, 'publication_allowed':False}
    validate_image_plan(plan, article_path, blueprint_path)
    return plan


def validate_image_plan(plan, article_path, blueprint_path, *, asset_root=None):
    _validate_structure(plan)
    blueprint = json.loads(Path(blueprint_path).read_text(encoding='utf-8'))
    if _hash(article_path) != plan['draft_sha256'] or canonical_hash(blueprint) != plan['blueprint_sha256']:
        raise ValueError('Image plan is stale: Article or Blueprint hash changed')
    if blueprint['content_id'] != plan['content_id']:
        raise ValueError('Image plan belongs to another Blueprint')
    sections = article_sections(article_path, blueprint_path)
    expected = {row['section_id']:row['section_heading'] for row in sections}
    covered = set()
    for row in plan['images']:
        if row['image_role'] == 'featured':
            if row['section_id'] != 'featured' or row['section_heading'] is not None or row['placement'] not in ('featured','none'):
                raise ValueError('Featured image must bind to the article, not an arbitrary H2')
        else:
            if row['section_id'] not in expected or row['section_heading'] != expected[row['section_id']]:
                raise ValueError('Image section must match the exact immutable H2')
            if row['placement'] == 'featured':
                raise ValueError('Section image cannot use featured placement')
            covered.add(row['section_id'])
        if row['generated_asset_reference'] is not None:
            if asset_root is None:
                raise ValueError('asset_root is required to verify completed assets')
            verify_asset(row['generated_asset_reference'], asset_root=asset_root)
    if covered != set(expected):
        raise ValueError('Every H2 needs an image decision or a reasoned NO_IMAGE decision')
    return True


def _png_dimensions(data):
    if not data.startswith(b'\x89PNG\r\n\x1a\n'):
        raise ValueError('Not a PNG image')
    pos, header, compressed, ended = 8, None, bytearray(), False
    while pos + 12 <= len(data):
        length = struct.unpack('>I', data[pos:pos+4])[0]
        kind = data[pos+4:pos+8]
        if pos + 12 + length > len(data):
            raise ValueError('Truncated PNG chunk')
        chunk = data[pos+8:pos+8+length]
        crc = struct.unpack('>I', data[pos+8+length:pos+12+length])[0]
        if zlib.crc32(kind + chunk) & 0xffffffff != crc:
            raise ValueError('Corrupt PNG chunk checksum')
        if kind == b'IHDR':
            if header is not None or pos != 8 or length != 13:
                raise ValueError('Invalid PNG header')
            header = struct.unpack('>IIBBBBB', chunk)
        elif kind == b'IDAT':
            compressed.extend(chunk)
        elif kind == b'IEND':
            ended = True
            if length or pos + 12 != len(data):
                raise ValueError('Invalid PNG end')
            break
        pos += 12 + length
    if not ended or header is None or not compressed:
        raise ValueError('PNG lacks complete image data')
    width, height, depth, color, compression, filtering, interlace = header
    channels = {0:1, 2:3, 3:1, 4:2, 6:4}.get(color)
    allowed_depth = {0:(1,2,4,8,16), 2:(8,16), 3:(1,2,4,8), 4:(8,16), 6:(8,16)}
    if channels is None or depth not in allowed_depth[color] or compression or filtering or interlace:
        raise ValueError('Only valid non-interlaced PNG is supported by this verifier')
    if not 1 <= width <= 8192 or not 1 <= height <= 8192:
        raise ValueError('Image dimensions are outside the supported range')
    stride = (width * channels * depth + 7) // 8 + 1
    expected = stride * height
    if expected > 128 * 1024 * 1024:
        raise ValueError('PNG decoded data exceeds the supported memory bound')
    decoder = zlib.decompressobj()
    pixels = decoder.decompress(bytes(compressed), expected + 1)
    if len(pixels) != expected or not decoder.eof or decoder.unused_data:
        raise ValueError('PNG pixel data does not match its dimensions')
    if any(pixels[offset] > 4 for offset in range(0, len(pixels), stride)):
        raise ValueError('Invalid PNG row filter')
    return width, height


def _svg_dimensions(data):
    text = data.decode('utf-8')
    if '<!DOCTYPE' in text.upper() or '<!ENTITY' in text.upper():
        raise ValueError('SVG entities and external document types are forbidden')
    try:
        svg = ET.fromstring(text)
    except ET.ParseError as error:
        raise ValueError('Invalid SVG') from error
    if svg.tag.split('}')[-1] != 'svg':
        raise ValueError('Asset is not SVG')
    forbidden = {'script','foreignObject','image','iframe','audio','video','style'}
    for element in svg.iter():
        if element.tag.split('}')[-1] in forbidden:
            raise ValueError('SVG contains executable or external content')
        for key, value in element.attrib.items():
            local = key.split('}')[-1].lower()
            if local.startswith('on') or local in ('href','src') or re.search(r'url\s*\(|javascript:|https?://', value, re.I):
                raise ValueError('SVG contains external or active references')
    dimensions = []
    for key in ('width','height'):
        value = svg.get(key, '')
        if not re.fullmatch(r'[0-9]+(?:px)?', value):
            raise ValueError('SVG requires explicit integer width and height')
        dimensions.append(int(value.removesuffix('px')))
    if not all(1 <= value <= 8192 for value in dimensions):
        raise ValueError('SVG dimensions are outside the supported range')
    return tuple(dimensions)


def inspect_asset(path):
    data = Path(path).read_bytes()
    if len(data) > 50 * 1024 * 1024:
        raise ValueError('Asset is too large for this offline verifier')
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        width, height = _png_dimensions(data)
        mime = 'image/png'
    elif data.lstrip().startswith((b'<svg', b'<?xml')):
        width, height = _svg_dimensions(data)
        mime = 'image/svg+xml'
    else:
        raise ValueError('Use a verified PNG or native SVG; unsupported formats are not accepted as complete')
    return {'image_sha256':hashlib.sha256(data).hexdigest(), 'mime_type':mime, 'width':width, 'height':height}


def _validate_provenance(provenance, mime_type):
    origin = provenance['origin']
    if origin == 'generated':
        if not provenance['generator'] or provenance['license_status'] != 'generated_original' or provenance['human_capture_confirmed']:
            raise ValueError('Generated imagery must identify its generator and cannot claim human capture')
    elif origin == 'native_vector':
        if provenance['license_status'] != 'original_code' or provenance['human_capture_confirmed']:
            raise ValueError('Native vector provenance requires original SVG code')
        if mime_type == 'image/png' and provenance['generator'] != 'native_svg_renderer':
            raise ValueError('Native vector PNG requires an identified SVG renderer')
        if mime_type not in ('image/svg+xml', 'image/png'):
            raise ValueError('Native vector supports only SVG master or rendered PNG')
    elif origin in ('original_photo', 'user_provided_photo'):
        if not provenance['human_capture_confirmed'] or provenance['license_status'] != 'confirmed' or not provenance['rights_reference']:
            raise ValueError('Original photography requires human capture and confirmed usage rights')
    elif origin == 'licensed_asset':
        if provenance['license_status'] != 'confirmed' or not provenance['rights_reference']:
            raise ValueError('Licensed assets require confirmed rights and a reference')
    else:
        raise ValueError('Unknown asset origin')


def _validate_factual_asset(row, provenance):
    origin = provenance['origin']
    if row.get('factual_reference_required') and not row.get('factual_source_reference'):
        raise ValueError('Factual imagery requires a verified subject reference before asset completion')
    if row.get('requires_actual_photo'):
        if origin not in ('original_photo','licensed_asset','user_provided_photo') or not provenance['human_capture_confirmed']:
            raise ValueError('Required actual photography cannot be replaced by generated or native vector imagery')
    if origin == 'generated':
        caption = row.get('caption') or ''
        if not any(term in caption.lower() for term in ('ai生成','生成画像','生成イラスト','generated illustration','ai-generated','ai generated')):
            raise ValueError('Generated images require an explicit illustrative disclosure in the caption')
        disclosure = row.get('illustrative_disclosure')
        if disclosure is not None and disclosure not in caption:
            raise ValueError('Illustrative disclosure must remain visible in the caption')


def add_asset(plan, image_id, asset_path, *, asset_root, provenance):
    """Return a new plan after inspecting a real local file; never fabricate success."""
    _validate_structure(plan)
    result = copy.deepcopy(plan)
    matches = [row for row in result['images'] if row['image_id'] == image_id]
    if len(matches) != 1 or matches[0]['visual_type'] == 'NO_IMAGE':
        raise ValueError('Asset must correspond to a planned non-NO_IMAGE decision')
    row = matches[0]
    if row['generated_asset_reference'] is not None:
        raise ValueError('Do not silently replace an accepted asset; revise the image plan')
    path = _local_file(asset_path, asset_root)
    details = inspect_asset(path)
    _validate_provenance(provenance, details['mime_type'])
    _validate_factual_asset(row, provenance)
    if provenance['origin'] == 'generated':
        row['illustrative_disclosure'] = row['caption']
    if details['mime_type'] == 'image/svg+xml' and row['render_method'] != 'html_svg_overlay':
        raise ValueError('Native SVG requires an explicit overlay rendering plan')
    if details['mime_type'] == 'image/png' and row['render_method'] not in ('raster','native_svg_render'):
        raise ValueError('PNG assets require raster or native SVG rendering')
    source_asset = None
    if provenance['origin'] == 'native_vector' and details['mime_type'] == 'image/png':
        if row['render_method'] != 'native_svg_render' or row['text_policy'] != 'native_text_layer':
            raise ValueError('Rendered SVG PNG requires an explicit native text rendering plan')
        source_path = _local_file(Path(asset_root) / provenance['source_reference'], asset_root)
        source_details = inspect_asset(source_path)
        if source_details['mime_type'] != 'image/svg+xml':
            raise ValueError('Native renderer source must be a verified SVG master')
        if (source_details['width'], source_details['height']) != (details['width'], details['height']):
            raise ValueError('SVG master and rendered PNG dimensions differ')
        source_asset = {'relative_path':source_path.relative_to(Path(asset_root).resolve()).as_posix(), **source_details}
    elif row['render_method'] == 'native_svg_render':
        raise ValueError('Native SVG rendering cannot be used for unrelated raster assets')
    if row['visual_type'] == 'PHOTO' and provenance['origin'] == 'generated':
        disclosure = (row['alt'] + ' ' + (row['caption'] or '')).lower()
        if not any(term in disclosure for term in ('生成','イメージ','illustration','generated')):
            raise ValueError('Synthetic photo-like imagery must disclose its illustrative nature')
    ratio = [int(value) for value in row['aspect_ratio'].split(':')]
    if abs(details['width'] / details['height'] - ratio[0] / ratio[1]) > 0.03:
        raise ValueError('Actual asset aspect ratio differs from the plan')
    state = 'generated' if provenance['origin'] == 'generated' else 'supplied'
    asset = {'asset_id':image_id + '-asset-01', 'relative_path':path.relative_to(Path(asset_root).resolve()).as_posix(),
             **details, 'state':state, 'provenance':copy.deepcopy(provenance),
             'source_asset_reference':source_asset}
    row.update(generated_asset_reference=asset, generation_status=state, generation_error=None)
    result['status'] = _status(result['images'])
    _validate_structure(result)
    return result


def record_generation_failure(plan, image_id, error):
    _validate_structure(plan)
    if not isinstance(error, str) or not error.strip():
        raise ValueError('Generation failure requires an actual error description')
    result = copy.deepcopy(plan)
    rows = [row for row in result['images'] if row['image_id'] == image_id]
    if len(rows) != 1 or rows[0]['visual_type'] == 'NO_IMAGE' or rows[0]['generated_asset_reference'] is not None:
        raise ValueError('Only a pending image can record generation failure')
    rows[0].update(generation_status='failed', generation_error=error)
    result['status'] = _status(result['images'])
    _validate_structure(result)
    return result


def verify_asset(asset, *, asset_root):
    validator = _validator()
    schema = validator.load(ROOT / 'fortune_labo/agents/creative/schemas/generated_asset_reference.schema.json')
    validator.audit_schema(schema); validator.validate(asset, schema)
    path = _local_file(Path(asset_root) / asset['relative_path'], asset_root)
    actual = inspect_asset(path)
    for key in ('image_sha256','mime_type','width','height'):
        if asset[key] != actual[key]:
            raise ValueError('Asset changed or metadata was fabricated: ' + key)
    _validate_provenance(asset['provenance'], asset['mime_type'])
    source = asset['source_asset_reference']
    native_png = asset['provenance']['origin'] == 'native_vector' and asset['mime_type'] == 'image/png'
    if native_png:
        if source is None or source['relative_path'] != asset['provenance']['source_reference']:
            raise ValueError('Rendered PNG lost its SVG master reference')
        source_path = _local_file(Path(asset_root) / source['relative_path'], asset_root)
        actual_source = inspect_asset(source_path)
        if actual_source['mime_type'] != 'image/svg+xml':
            raise ValueError('Native renderer master is not SVG')
        for key in ('image_sha256','mime_type','width','height'):
            if source[key] != actual_source[key]:
                raise ValueError('Native SVG master changed: ' + key)
        if (asset['width'], asset['height']) != (source['width'], source['height']):
            raise ValueError('Native SVG and PNG dimensions differ')
    elif source is not None:
        raise ValueError('Only native rendered PNG may carry an SVG master reference')
    expected = 'generated' if asset['provenance']['origin'] == 'generated' else 'supplied'
    if asset['state'] != expected:
        raise ValueError('Asset state does not match provenance')
    return True
