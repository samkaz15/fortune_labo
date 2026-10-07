#!/usr/bin/env python3
"""Verify three article-bound creative jobs without network or publication."""
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from fortune_labo.editorial.content_job import build_job
from fortune_labo.editorial.creative import validate_image_plan
from fortune_labo.editorial.wordpress_draft import build_draft_payload
from scripts.validate_editorial import load,validate,audit_schema


def article_descriptor(letter,root=ROOT):
    cid='FL-TEST-'+letter
    original=root/'docs/editorial/test-articles'/cid
    creative=root/'docs/editorial/creative-fixtures'/cid
    brief=load(original/'brief.json')
    package=load(creative/'wordpress-draft-payload.json')
    content=(original/'article.md').read_text(encoding='utf-8')
    article={'content_id':cid,'title':brief['title'],'content':content,'content_format':'markdown',
        'draft_sha256':hashlib.sha256(content.encode()).hexdigest(),'article_version':'article-1.0.0',
        'access_type':brief['access_type'],'seo_policy_version':brief['seo_policy_version'],
        'internal_links':brief['internal_link_candidates'],'cta':brief['cta'],'seo_meta':package['seo_metadata']}
    article.update({key:package['proposed_payload'][key] for key in ['excerpt','slug','categories','tags']})
    return article


def verify(root=ROOT):
    counts={'jobs':0,'featured':0,'inline':0,'no_image':0,'actual_wordpress_drafts':0}
    for letter in 'ABC':
        cid='FL-TEST-'+letter
        original=root/'docs/editorial/test-articles'/cid
        creative=root/'docs/editorial/creative-fixtures'/cid
        plan,qa,package,job=[load(creative/name) for name in ['image-plan.json','qa.json','wordpress-draft-payload.json','job.json']]
        validate_image_plan(plan,original/'article.md',original/'blueprint.json',asset_root=creative)
        for artifact,name in [(job,'content_job')]:
            schema=load(root/('docs/editorial/schemas/'+name+'.schema.json'))
            audit_schema(schema);validate(artifact,schema)
        expected=build_draft_payload(article_descriptor(letter,root),plan,qa)
        if package!=expected:
            raise ValueError('Stored WordPress package differs from its immutable inputs')
        rebuilt=build_job(original/'article.md',original/'blueprint.json',plan,qa,package,
                          asset_root=creative,artifact_references=job['artifacts'])
        if job!=rebuilt:
            raise ValueError('Stored job state differs from derived stage outcomes')
        if any(row['attachment_id'] is not None for row in package['media_upload_plan']):
            raise ValueError('Offline public fixtures must not invent attachment IDs')
        if package['request_payload'] is not None or package['network_ready'] or package['proposed_payload']['status']!='draft':
            raise ValueError('Unconnected previews cannot claim a ready WordPress request')
        for reference in job['artifacts'].values():
            path=(root/reference).resolve()
            if root.resolve() not in path.parents or not path.is_file():
                raise ValueError('Missing or unsafe job artifact')
        counts['jobs']+=1
        for row in plan['images']:
            counts['no_image' if row['visual_type']=='NO_IMAGE' else 'featured' if row['image_role']=='featured' else 'inline']+=1
    return counts


if __name__=='__main__':
    print('PASS: '+json.dumps(verify()))
