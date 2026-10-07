"""Evidence-linked coverage candidates without numeric priority scores."""
from hashlib import sha256
from .classification import norm


def topics_from_intelligence(intelligence):
    """Only explicitly registered topic candidates; do not fabricate keyword demand."""
    topics = []
    for genre in intelligence.get("genres", []):
        for item in genre.get("topic_candidates", []):
            if not isinstance(item, dict):
                raise ValueError("topic_candidates must contain structured objects")
            topic = dict(item)
            topic.setdefault("genre", genre["genre_id"])
            topics.append(topic)
    return topics


def generate_opportunities(inventory, topics, *, draft_index=None, reviewed_overlaps=None):
    if reviewed_overlaps is not None and not isinstance(reviewed_overlaps, list):
        raise ValueError("Reviewed overlaps must be a list")
    completeness = inventory.get("scope", {}).get("completeness", "unknown")
    opportunities, suppressed, seen = [], [], set()
    content = list(inventory["items"]) + list((draft_index or {}).get("items", []))
    content_by_id = {item["content_id"]: item for item in content}
    if len(content_by_id) != len(content):
        raise ValueError("Duplicate content ID across existing and draft indexes")
    reviews = {}
    for review in reviewed_overlaps or []:
        if not isinstance(review, dict):
            raise ValueError("Reviewed overlaps must contain objects")
        oid = review.get("opportunity_id")
        if not oid or oid in reviews:
            raise ValueError("Reviewed overlaps require unique opportunity IDs")
        if any(not isinstance(review.get(key), list) or not review[key] or
               any(not isinstance(value, str) or not value.strip() for value in review[key])
               for key in ("content_ids", "evidence_refs")) or not isinstance(review.get("reason"), str) or not review["reason"].strip():
            raise ValueError("Reviewed overlaps require content IDs, evidence references and a reason")
        if any(cid not in content_by_id for cid in review["content_ids"]):
            raise ValueError("Reviewed overlap references content absent from the compared indexes")
        reviews[oid] = review
    matched_reviews = set()
    for topic in topics:
        if not topic.get("genre") or not topic.get("topic") or not isinstance(topic.get("evidence_refs"), list) or not topic["evidence_refs"] or any(not isinstance(ref, str) or not ref.strip() for ref in topic["evidence_refs"]):
            raise ValueError("Opportunity topic requires genre, topic and evidence_refs")
        key = "|".join([topic["genre"], norm(topic["topic"]), norm(topic.get("keyword")), norm(topic.get("search_intent"))])
        if key in seen:
            continue
        seen.add(key)
        overlaps = []
        for item in content:
            reasons = []
            if topic.get("topic_cluster") and item.get("topic_cluster") == topic["topic_cluster"]:
                reasons.append("same_topic_cluster")
            if topic.get("keyword") and norm(topic["keyword"]) in {
                norm(item.get("primary_keyword")), *[norm(k) for k in item.get("secondary_keywords") or []]
            }:
                reasons.append("same_registered_keyword")
            if norm(topic["topic"]) == norm(item.get("title")):
                reasons.append("same_title")
            # Literal phrase/title overlap is evidence for human review, not semantic identity.
            if topic.get("keyword") and norm(topic["keyword"]) in norm(item.get("title")):
                reasons.append("keyword_in_title")
            if reasons:
                overlaps.append({"content_id": item["content_id"], "reasons": reasons,
                                 "search_intent_match": item.get("search_intent") == topic.get("search_intent") if item.get("search_intent") and topic.get("search_intent") else None})
        oid = "opp-" + sha256(key.encode()).hexdigest()[:16]
        review = reviews.get(oid)
        if review:
            matched_reviews.add(oid)
            for cid in review["content_ids"]:
                existing = next((row for row in overlaps if row["content_id"] == cid), None)
                if existing is not None:
                    existing["reasons"].append("reviewed_editorial_overlap")
                else:
                    item = content_by_id[cid]
                    overlaps.append({"content_id": cid, "reasons": ["reviewed_editorial_overlap"],
                                     "search_intent_match": item.get("search_intent") == topic.get("search_intent") if item.get("search_intent") and topic.get("search_intent") else None})
        strong_overlap = any(set(m["reasons"]) & {"same_topic_cluster", "same_registered_keyword", "same_title", "reviewed_editorial_overlap"} for m in overlaps)
        opportunity = {"opportunity_id": oid, "genre": topic["genre"], "topic": topic["topic"],
                       "keyword": topic.get("keyword"), "search_intent": topic.get("search_intent"),
                       "reader_need": topic.get("reader_need"), "existing_content_overlap": overlaps,
                       "free_premium_candidate": topic.get("free_premium_candidate"),
                       "reason": "No matching registered topic/title/keyword in existing and supplied draft indexes; semantic coverage requires human review." if not overlaps else "Potential overlap requires consolidation or distinct-intent review.",
                       "evidence_refs": list(dict.fromkeys(list(topic["evidence_refs"]) + (list(review["evidence_refs"]) if review else []))),
                       "priority_candidate": topic.get("priority_candidate"),
                       "inventory_completeness": completeness,
                       "coverage_status": "overlap_review" if overlaps else "no_index_match" if completeness == "complete" else "potential_gap",
                       "human_review_required": True}
        if review:
            opportunity["reason"] = review["reason"]
        if opportunity["free_premium_candidate"] not in (None, "FREE", "PREMIUM"):
            raise ValueError("Invalid FREE/PREMIUM candidate")
        if opportunity["priority_candidate"] not in (None, "review", "consider", "defer"):
            raise ValueError("Priority candidate is an ordinal review label, never a score")
        if strong_overlap:
            suppressed.append(opportunity)
        else:
            opportunities.append(opportunity)
    if set(reviews) != matched_reviews:
        raise ValueError("Reviewed overlap references an opportunity absent from the topic catalog")
    return {"schema_version": "1.0.0", "inventory_completeness": completeness,
            "opportunities": opportunities, "suppressed": suppressed}
