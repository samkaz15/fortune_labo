"""Build a blocked QA envelope; this is not an A29/A32/A28 implementation."""
import hashlib
import re
from .strategy import canonical_hash


def extract_claim_candidates(text):
    """Extract review candidates, including plain assertions without numbers.

    No source verification or truth verdict is inferred. Questions and headings
    are omitted; a human/model fact review must still inspect the whole draft.
    """
    claims = []
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.startswith(('#', '|', '>')):
            continue
        for sentence in re.findall(r'[^。！？!?]+[。！？!?]?', line):
            sentence = sentence.strip()
            if not sentence or sentence.endswith(('?', '？')):
                continue
            claims.append({'claim_id': 'CLAIM-%03d' % (len(claims) + 1),
                'line': line_number, 'text': sentence,
                'claim_kind': 'unclassified', 'status': 'requires_fact_review',
                'evidence_refs': [],
                'numeric_or_absolute_signal': bool(re.search(r'\d|必ず|絶対|保証|科学的', sentence))})
    return {'method': 'sentence_candidates_not_verified_claims',
            'requires_full_draft_review': True, 'claims': claims}


def build_qa_handoff(brief, draft_text, *, artifact_ids=None, findings=None):
    if brief.get('publication_allowed') is not False:
        raise ValueError('This contract accepts unpublished work only')
    return {
        'schema_version': '1.0.0', 'content_id': brief['content_id'],
        'brief_sha256': canonical_hash(brief),
        'draft_sha256': hashlib.sha256(draft_text.encode('utf-8')).hexdigest(),
        'seo_policy_version': brief['seo_policy_version'],
        'artifact_ids': list(artifact_ids or []),
        'stages': [{'agent': name, 'status': 'contract_pending'} for name in ['A29', 'A32', 'A28']],
        'findings': list(findings or []),
        'blockers': ['QA agent implementations are absent', 'Human article approval is absent',
                     'Operational SEO policy and A06 acceptance require verification'],
        'human_approval': None, 'wordpress_handoff_allowed': False,
        'publication_allowed': False,
    }
