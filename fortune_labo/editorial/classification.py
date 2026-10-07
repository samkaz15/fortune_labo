"""Conservative candidates derived from metadata, taxonomy and explicit mappings."""
from copy import deepcopy
import re
import unicodedata

CANDIDATE_FIELDS = ("genre", "subgenre", "access_type", "search_intent", "reader_need", "cta_role")
CONFIDENCE_ORDER = {"low": 0, "medium": 1, "high": 2}


def norm(value):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", value or "")).casefold()


def candidate(value=None, confidence="low", evidence_refs=None, reason="No supported evidence; human review required."):
    return {"value": value, "confidence": confidence, "evidence_refs": list(evidence_refs or []), "reason": reason}


def classify_article(record, intelligence, taxonomy, *, text=None, mappings=None):
    """Return a sidecar; never rewrite the article or promote candidates to facts.

    mappings: {category_genres:{category_id_or_name:genre_id},
               title_genres:{literal_phrase:genre_id},
               intent_terms:{literal_phrase:search_intent},
               cta_roles:{exact_cta_type:role}}.
    Mappings are operator-reviewed configuration. Body text is transient and is
    never copied to the result. Body text alone does not establish access rights.
    """
    mappings = mappings or {}
    genres = {g["genre_id"]: g for g in taxonomy.get("genres", [])}
    insights = {g["genre_id"]: g for g in intelligence.get("genres", [])}
    results = {key: candidate() for key in CANDIDATE_FIELDS}
    cid = record["content_id"]
    direct = record.get("genre")
    evidence = {}
    if direct in genres and direct in insights:
        evidence[direct] = ["index:genre", f"taxonomy:{direct}", f"intelligence:{direct}"]
        results["genre"] = candidate(direct, "high", evidence[direct], "Explicit editorial metadata matches taxonomy and intelligence.")
    else:
        for term in record.get("category") or []:
            for key in (str(term.get("id")), term.get("name"), term.get("slug")):
                mapped = mappings.get("category_genres", {}).get(key)
                if mapped in genres and mapped in insights:
                    evidence.setdefault(mapped, []).append("mapping:category_genres:" + str(key))
            # Exact full taxonomy display names are useful evidence without inventing synonyms.
            for genre_id, genre in genres.items():
                if genre_id in insights and term.get("name") and norm(term["name"]) == norm(genre.get("genre_name")):
                    evidence.setdefault(genre_id, []).append("taxonomy:exact_category_name:" + genre_id)
        for phrase, mapped in mappings.get("title_genres", {}).items():
            if phrase and norm(phrase) in norm(record.get("title")) and mapped in genres and mapped in insights:
                evidence.setdefault(mapped, []).append("mapping:title_genres:" + phrase)
        if len(evidence) == 1:
            genre_id = next(iter(evidence))
            results["genre"] = candidate(genre_id, "medium", evidence[genre_id] + [f"intelligence:{genre_id}"],
                                          "One supported category/title mapping; candidate requires editorial confirmation.")
        elif len(evidence) > 1:
            results["genre"] = candidate(reason="Conflicting supported genres; primary genre is unclassified.",
                                          evidence_refs=[f"taxonomy:{g}" for g in sorted(evidence)])
    genre_id = results["genre"]["value"]
    insight = insights.get(genre_id, {})
    if genre_id:
        approved_subgenres = genres[genre_id].get("subgenres", [])
        subgenre_ids = {s.get("subgenre_id") if isinstance(s, dict) else s for s in approved_subgenres}
        if record.get("subgenre") in subgenre_ids and record.get("subgenre"):
            results["subgenre"] = candidate(record["subgenre"], "high", ["index:subgenre", f"taxonomy:{genre_id}:subgenres"],
                                             "Existing subgenre is present in the approved taxonomy.")
    access = record.get("access_type")
    if access in ("FREE", "PREMIUM") and genre_id:
        role_key = "free_content_role" if access == "FREE" else "premium_content_role"
        role = insight.get(role_key)
        if role and role != "TBD":
            results["access_type"] = candidate(access, "high", ["index:access_type", f"intelligence:{genre_id}:{role_key}",
                                                                  "FREE_PREMIUM_RULES"],
                                                 "Explicit access metadata is retained; editorial suitability remains separately reviewable.")
    intent = record.get("search_intent")
    allowed_intents = {"informational", "navigational", "commercial", "transactional", "local"}
    if intent in allowed_intents:
        results["search_intent"] = candidate(intent, "high", ["index:search_intent"], "Explicit editorial intent metadata.")
    else:
        matching_intents = {value for phrase, value in mappings.get("intent_terms", {}).items()
                            if phrase and norm(phrase) in norm(record.get("title")) and value in allowed_intents}
        if len(matching_intents) == 1:
            results["search_intent"] = candidate(next(iter(matching_intents)), "medium", ["mapping:intent_terms"],
                                                  "Explicit reviewed title mapping; search behavior remains unmeasured.")
    if record.get("explicit_need"):
        results["reader_need"] = candidate(record["explicit_need"], "high", ["index:explicit_need"], "Explicit editorial reader-need metadata.")
    # Genre-wide audience needs are not automatically claims about a particular article.
    cta_type = record.get("cta_type")
    if cta_type in mappings.get("cta_roles", {}):
        results["cta_role"] = candidate(mappings["cta_roles"][cta_type], "medium", ["index:cta_type", "mapping:cta_roles"],
                                         "Reviewed CTA-role mapping; destination and conversion effect require separate verification.")
    elif cta_type == "none":
        results["cta_role"] = candidate("none", "high", ["index:cta_type"], "Explicitly no CTA.")
    confidence = min((v["confidence"] for v in results.values()), key=CONFIDENCE_ORDER.get)
    return {"schema_version": "1.0.0", "content_id": cid, "candidates": results,
            "confidence": confidence, "human_review_required": confidence == "low",
            "status": "candidate" if genre_id else "unclassified",
            "access_reason": {"acquisition_role": insight.get("seo_role"),
                              "engagement_role": insight.get("engagement_role"),
                              "conversion_role": insight.get("conversion_role"),
                              "retention_role": insight.get("retention_role"),
                              "premium_value": insight.get("premium_content_role") if access == "PREMIUM" else None},
            "taxonomy_version": taxonomy.get("version"), "intelligence_version": intelligence.get("version"),
            "canonical_metadata_changed": False}


def classify_inventory(inventory, intelligence, taxonomy, *, mappings=None):
    items = [classify_article(item, intelligence, taxonomy, mappings=mappings) for item in inventory["items"]]
    classified = sum(item["status"] == "candidate" for item in items)
    return {"schema_version": "1.0.0", "scope": deepcopy(inventory["scope"]), "items": items,
            "counts": {"total": len(items), "classified": classified, "unclassified": len(items) - classified,
                       "human_review": sum(item["human_review_required"] for item in items)}}
