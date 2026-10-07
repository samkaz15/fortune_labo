"""Synthetic A11 fixtures only; no private research or generated production art."""
import copy
import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fortune_labo.editorial.creative import (
    image_template, create_image_plan, validate_image_plan, add_asset,
    verify_asset, record_generation_failure, inspect_asset)


def png_bytes(width=16, height=9):
    def chunk(kind, payload):
        return struct.pack('>I',len(payload))+kind+payload+struct.pack('>I',zlib.crc32(kind+payload)&0xffffffff)
    raw=b''.join(b'\x00'+bytes([210,220,210])*width for _ in range(height))
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',width,height,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b'')


def provenance(origin='generated'):
    return {'origin':origin,'source_reference':'synthetic-generation-receipt',
        'generator':'synthetic-fixture-generator','created_at':'2026-10-07T00:00:00Z',
        'license_status':'generated_original','rights_reference':None,'human_capture_confirmed':False}


class CreativeTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name); self.article=self.root/'article.md'; self.blueprint=self.root/'blueprint.json'
        self.article.write_text('# 合成記事\n\n本文です。\n\n## 条件を分ける\n\n説明文です。\n\n## 一つ確かめる\n\n説明文です。\n',encoding='utf-8')
        self.blueprint.write_text(json.dumps({'content_id':'FL-SYNTH-CREATIVE','sections':[
            {'heading_level':'h2','heading':'条件を分ける'}, {'heading_level':'h2','heading':'一つ確かめる'}]},ensure_ascii=False),encoding='utf-8')
        featured=image_template('FL-SYNTH-CREATIVE','SYNTH-featured',section_id='featured',image_role='featured',visual_type='ILLUSTRATION')
        featured.update(purpose='Illustrate an orderly thinking space',visual_subject='Notebook and two neutral cards',
            composition='Wide tabletop with open space',environment='Quiet generic room',lighting='Natural side light',
            mood='Calm',alt='ノートとカードの説明用イラスト',caption='AI生成のイメージ画像です。実際の体験を撮影した写真ではありません。',generation_prompt='Calm editorial illustration of a notebook and two cards, no text.',
            recommended_width=16,recommended_height=9)
        self.images=[featured]
        for number,heading in enumerate(('条件を分ける','一つ確かめる'),1):
            self.images.append(image_template('FL-SYNTH-CREATIVE','SYNTH-h2-'+str(number),section_id='h2-'+str(number).zfill(2),
                section_heading=heading,no_image_reason='The paragraph already explains this step; an image would repeat it.'))
        self.plan=create_image_plan(self.article,self.blueprint,content_id='FL-SYNTH-CREATIVE',article_version='article-1.0.0',images=self.images)
        self.png=self.root/'featured.png'; self.png.write_bytes(png_bytes())

    def test_complete_plan_covers_every_h2_and_does_not_mutate_sources(self):
        original=self.article.read_bytes(),self.blueprint.read_bytes()
        self.assertTrue(validate_image_plan(self.plan,self.article,self.blueprint))
        self.assertEqual((self.article.read_bytes(),self.blueprint.read_bytes()),original)
        self.assertEqual(self.plan['images'][0]['alt'],self.plan['images'][0]['alt_text'])

    def test_real_asset_hash_dimensions_and_state(self):
        original=copy.deepcopy(self.plan)
        plan=add_asset(self.plan,'SYNTH-featured',self.png,asset_root=self.root,provenance=provenance())
        self.assertEqual(self.plan,original)
        self.assertEqual(plan['status'],'assets_ready_for_qa')
        self.assertEqual(plan['images'][0]['generated_asset_reference']['width'],16)
        self.assertTrue(validate_image_plan(plan,self.article,self.blueprint,asset_root=self.root))

    def test_missing_h2_decision_rejected(self):
        with self.assertRaisesRegex(ValueError,'Every H2'):
            create_image_plan(self.article,self.blueprint,content_id='FL-SYNTH-CREATIVE',article_version='article-1.0.0',images=self.images[:-1])

    def test_missing_no_image_reason_rejected(self):
        images=copy.deepcopy(self.images); images[1]['no_image_reason']=None
        with self.assertRaises(ValueError):
            create_image_plan(self.article,self.blueprint,content_id='FL-SYNTH-CREATIVE',article_version='article-1.0.0',images=images)

    def test_changed_article_rejects_stale_plan(self):
        self.article.write_text(self.article.read_text()+'追加文です。\n')
        with self.assertRaisesRegex(ValueError,'stale'):
            validate_image_plan(self.plan,self.article,self.blueprint)

    def test_inexact_h2_rejected(self):
        images=copy.deepcopy(self.images); images[1]['section_heading']='別の節'
        with self.assertRaisesRegex(ValueError,'exact immutable H2'):
            create_image_plan(self.article,self.blueprint,content_id='FL-SYNTH-CREATIVE',article_version='article-1.0.0',images=images)

    def test_missing_file_cannot_be_success(self):
        with self.assertRaisesRegex(ValueError,'existing file'):
            add_asset(self.plan,'SYNTH-featured',self.root/'missing.png',asset_root=self.root,provenance=provenance())

    def test_header_without_pixels_rejected(self):
        self.png.write_bytes(png_bytes()[:33])
        with self.assertRaisesRegex(ValueError,'complete image data'):
            add_asset(self.plan,'SYNTH-featured',self.png,asset_root=self.root,provenance=provenance())

    def test_asset_mutation_rejected(self):
        plan=add_asset(self.plan,'SYNTH-featured',self.png,asset_root=self.root,provenance=provenance())
        self.png.write_bytes(png_bytes(32,18))
        with self.assertRaisesRegex(ValueError,'changed or metadata'):
            verify_asset(plan['images'][0]['generated_asset_reference'],asset_root=self.root)

    def test_failed_generation_does_not_create_asset(self):
        plan=record_generation_failure(self.plan,'SYNTH-featured','Synthetic tool failure')
        self.assertEqual(plan['status'],'needs_attention')
        self.assertIsNone(plan['images'][0]['generated_asset_reference'])

    def test_original_photo_without_human_rights_rejected(self):
        source=provenance('original_photo');source['license_status']='pending'
        with self.assertRaisesRegex(ValueError,'human capture'):
            add_asset(self.plan,'SYNTH-featured',self.png,asset_root=self.root,provenance=source)

    def test_generated_image_cannot_claim_human_capture(self):
        source=provenance();source['human_capture_confirmed']=True
        with self.assertRaisesRegex(ValueError,'human capture'):
            add_asset(self.plan,'SYNTH-featured',self.png,asset_root=self.root,provenance=source)

    def test_long_japanese_in_ai_raster_rejected(self):
        images=copy.deepcopy(self.images);images[0].update(text_policy='short_labels_only',text_labels=['長い日本語の本文をこの画像にそのまま全部書き込む'])
        with self.assertRaisesRegex(ValueError,'Long Japanese'):
            create_image_plan(self.article,self.blueprint,content_id='FL-SYNTH-CREATIVE',article_version='article-1.0.0',images=images)

    def test_generated_image_without_visible_disclosure_rejected(self):
        images=copy.deepcopy(self.images);images[0]['caption']=None
        plan=create_image_plan(self.article,self.blueprint,content_id='FL-SYNTH-CREATIVE',article_version='article-1.0.0',images=images)
        with self.assertRaisesRegex(ValueError,'illustrative disclosure'):
            add_asset(plan,'SYNTH-featured',self.png,asset_root=self.root,provenance=provenance())

    def test_real_place_requiring_photo_rejects_generated_even_with_disclosure(self):
        images=copy.deepcopy(self.images);images[0].update(visual_type='PHOTO',factual_subject_kind='real_place',
            factual_reference_required=True,factual_source_reference='SYNTHETIC-VERIFIED-PLACE',requires_actual_photo=True)
        plan=create_image_plan(self.article,self.blueprint,content_id='FL-SYNTH-CREATIVE',article_version='article-1.0.0',images=images)
        with self.assertRaisesRegex(ValueError,'actual photography'):
            add_asset(plan,'SYNTH-featured',self.png,asset_root=self.root,provenance=provenance())

    def test_factual_subject_without_reference_cannot_complete(self):
        images=copy.deepcopy(self.images);images[0].update(factual_subject_kind='traditional_object',factual_reference_required=True)
        plan=create_image_plan(self.article,self.blueprint,content_id='FL-SYNTH-CREATIVE',article_version='article-1.0.0',images=images)
        with self.assertRaisesRegex(ValueError,'subject reference'):
            add_asset(plan,'SYNTH-featured',self.png,asset_root=self.root,provenance=provenance())

    def test_svg_active_content_rejected(self):
        path=self.root/'bad.svg';path.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="9"><script>alert(1)</script></svg>')
        with self.assertRaisesRegex(ValueError,'executable'):
            inspect_asset(path)

    def test_native_svg_render_preserves_master_and_png_hashes(self):
        images=copy.deepcopy(self.images);images[0].update(visual_type='DIAGRAM',render_method='native_svg_render',text_policy='native_text_layer',text_labels=['確認済み','まだ不明'])
        plan=create_image_plan(self.article,self.blueprint,content_id='FL-SYNTH-CREATIVE',article_version='article-1.0.0',images=images)
        master=self.root/'master.svg';master.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="9"><text x="0" y="8">確認済み</text></svg>',encoding='utf-8')
        source=provenance('native_vector');source.update(source_reference='master.svg',generator='native_svg_renderer',license_status='original_code')
        plan=add_asset(plan,'SYNTH-featured',self.png,asset_root=self.root,provenance=source)
        asset=plan['images'][0]['generated_asset_reference']
        self.assertEqual(asset['state'],'supplied');self.assertEqual(asset['source_asset_reference']['mime_type'],'image/svg+xml')
        self.assertTrue(verify_asset(asset,asset_root=self.root))
        master.write_text(master.read_text().replace('確認済み','別内容'))
        with self.assertRaisesRegex(ValueError,'master changed'):
            verify_asset(asset,asset_root=self.root)

    def test_native_png_without_master_rejected(self):
        images=copy.deepcopy(self.images);images[0].update(visual_type='DIAGRAM',render_method='native_svg_render',text_policy='native_text_layer')
        plan=create_image_plan(self.article,self.blueprint,content_id='FL-SYNTH-CREATIVE',article_version='article-1.0.0',images=images)
        source=provenance('native_vector');source.update(source_reference='missing.svg',generator='native_svg_renderer',license_status='original_code')
        with self.assertRaisesRegex(ValueError,'existing file'):
            add_asset(plan,'SYNTH-featured',self.png,asset_root=self.root,provenance=source)


if __name__=='__main__':
    unittest.main()
