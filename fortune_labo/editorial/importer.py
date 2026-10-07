"""Read-only WordPress inventory. Real imports belong in .private/, never Git."""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit, urlencode
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

SCHEMA_VERSION = "1.0.0"
EDITORIAL_FIELDS = (
    "genre", "subgenre", "topic_cluster", "access_type", "primary_keyword",
    "secondary_keywords", "search_intent", "explicit_need", "latent_need",
    "article_type", "content_depth", "cta_type", "cta_destination", "seo_policy_version",
)
NS = {"wp": "http://wordpress.org/export/1.2/", "content": "http://purl.org/rss/1.0/modules/content/"}


class TextParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.links, self.hidden = [], [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.hidden += 1
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)
        if tag in ("p", "div", "br", "li", "h1", "h2", "h3", "h4", "td"):
            self.parts.append(" ")

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.hidden:
            self.hidden -= 1
        if tag in ("p", "div", "li", "h1", "h2", "h3", "h4", "td"):
            self.parts.append(" ")

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)

    @property
    def text(self):
        return " ".join("".join(self.parts).split())


def parse_html(value):
    parser = TextParser()
    parser.feed(value or "")
    return parser


def rendered(value):
    if isinstance(value, dict):
        return value.get("raw", value.get("rendered"))
    return value if isinstance(value, str) else None


def date_value(value, *, gmt=False):
    if not value or value.startswith("0000-"):
        return None
    value = value.replace(" ", "T")
    return value + "Z" if gmt and not re.search(r"Z|[+-]\d\d:\d\d$", value) else value


def content_id(site_id, post_id):
    if not site_id or not isinstance(site_id, str):
        raise ValueError("site_id is a required stable site namespace")
    if not isinstance(post_id, int) or isinstance(post_id, bool) or post_id <= 0:
        raise ValueError("WordPress post ID must be a positive integer")
    return f"wp-{sha256(site_id.encode()).hexdigest()[:16]}-{post_id}"


def _terms(post, name):
    values = post.get(name)
    if values is None:
        return None
    taxonomy = "category" if name == "categories" else "post_tag"
    lookup = {}
    for group in post.get("_embedded", {}).get("wp:term", []):
        for term in group:
            if isinstance(term, dict) and term.get("taxonomy") == taxonomy:
                lookup[term.get("id")] = term
    result = []
    for value in values:
        term = value if isinstance(value, dict) else lookup.get(value, {"id": value})
        result.append({"id": term.get("id"), "name": parse_html(term.get("name")).text or None,
                       "slug": term.get("slug")})
    return result


def _meta_field(post, source):
    value = post
    for part in source.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def normalize_rest_post(post, site_id, *, site_url=None, field_map=None):
    post_id = post.get("id")
    cid = content_id(site_id, post_id)
    title = rendered(post.get("title"))
    body = rendered(post.get("content"))
    protected = isinstance(post.get("content"), dict) and post["content"].get("protected")
    body = None if protected else body
    parsed = parse_html(body) if body is not None else None
    url = post.get("link")
    origin = urlsplit(site_url or url or "")
    links = None
    if parsed is not None and origin.netloc:
        links = []
        for href in parsed.links:
            target = urljoin(url or site_url, href)
            parts = urlsplit(target)
            if parts.scheme in ("http", "https") and parts.netloc.lower() == origin.netloc.lower():
                target = parts._replace(fragment="").geturl()
                if target not in links:
                    links.append(target)
    media_id = post.get("featured_media")
    media = next((v for v in post.get("_embedded", {}).get("wp:featuredmedia", [])
                  if isinstance(v, dict) and v.get("id") == media_id), {})
    item = {
        "content_id": cid, "wordpress_post_id": post_id,
        "title": parse_html(title).text if title is not None else None,
        "slug": post.get("slug"), "url": url, "status": post.get("status"),
        "publish_date": date_value(post.get("date_gmt"), gmt=True) or date_value(post.get("date")),
        "modified_date": date_value(post.get("modified_gmt"), gmt=True) or date_value(post.get("modified")),
        "date_basis": "utc" if post.get("date_gmt") and not post["date_gmt"].startswith("0000-") else "site_timezone_unknown",
        "post_type": post.get("type"), "category": _terms(post, "categories"), "tags": _terms(post, "tags"),
        "internal_links": links,
        "featured_image": {"wordpress_media_id": media_id, "url": media.get("source_url"), "alt_text": media.get("alt_text")} if media_id else None,
        "word_count": len(re.findall(r"[\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff]|[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*", parsed.text)) if parsed is not None else None,
        "word_count_method": "cjk_character_plus_latin_number_token_v1" if parsed is not None else None,
        "body_available": body is not None,
        "field_provenance": {},
    }
    for field in EDITORIAL_FIELDS:
        item[field] = None
    for field, source in (field_map or {}).items():
        if field not in EDITORIAL_FIELDS or not isinstance(source, str):
            raise ValueError(f"Unsupported explicit metadata mapping: {field}")
        value = _meta_field(post, source)
        if field == "access_type" and value not in (None, "FREE", "PREMIUM"):
            value = None
        if value is not None:
            valid = isinstance(value, list) and all(isinstance(v, str) for v in value) if field == "secondary_keywords" else isinstance(value, str)
            if not valid:
                raise ValueError(f"Invalid mapped metadata type: {field}")
            item[field] = value
            item["field_provenance"][field] = f"wordpress_metadata:{source}"
    return item


def _inventory(records, site_id, source_type, *, completeness="unknown", statuses_requested=None,
               coverage_complete=False, expected_count=None, source_ref=None):
    if completeness not in ("complete", "partial", "unknown"):
        raise ValueError("Unknown completeness")
    unique, duplicates = {}, []
    for record in records:
        cid = record["content_id"]
        if cid in unique:
            conflict = unique[cid] != record
            duplicates.append({"content_id": cid, "conflict": conflict})
            # Keep the newest modified record; retain first on equal timestamps.
            if (record.get("modified_date") or "") > (unique[cid].get("modified_date") or ""):
                unique[cid] = record
        else:
            unique[cid] = record
    if any(v["conflict"] for v in duplicates):
        completeness, coverage_complete = "partial", False
    if expected_count is not None and len(unique) != expected_count:
        completeness, coverage_complete = "partial", False
    items = sorted(unique.values(), key=lambda value: value["wordpress_post_id"])
    return {"schema_version": SCHEMA_VERSION,
            "scope": {"site_id": site_id, "source_type": source_type,
                      "source_ref": source_ref, "completeness": completeness,
                      "coverage_complete": coverage_complete,
                      "statuses_requested": list(statuses_requested or []),
                      "statuses_observed": sorted({i["status"] for i in items if i["status"]}),
                      "expected_count": expected_count, "imported_count": len(items),
                      "imported_at": datetime.now(timezone.utc).isoformat(),
                      "limitations": []},
            "items": items, "duplicates": duplicates}


def import_rest(payload, site_id, *, site_url=None, completeness="unknown", statuses_requested=None,
                field_map=None, coverage_complete=False, expected_count=None, source_ref=None):
    posts = payload.get("posts", payload.get("items")) if isinstance(payload, dict) else payload
    if not isinstance(posts, list):
        raise ValueError("Expected REST posts array or {posts: [...]} export")
    records = [normalize_rest_post(post, site_id, site_url=site_url, field_map=field_map) for post in posts]
    inventory = _inventory(records, site_id, "wordpress_rest_export", completeness=completeness,
                           statuses_requested=statuses_requested, coverage_complete=coverage_complete,
                           expected_count=expected_count, source_ref=source_ref)
    if completeness != "complete":
        inventory["scope"]["limitations"].append("Export scope not verified as all article statuses and post types.")
    return inventory


def import_wxr(xml_data, site_id, *, site_url=None, complete_export=False, post_types=("post", "page"),
               field_map=None, source_ref=None):
    data = xml_data.encode() if isinstance(xml_data, str) else xml_data
    if b"<!DOCTYPE" in data.upper() or b"<!ENTITY" in data.upper():
        raise ValueError("DTD/entity declarations are not accepted")
    root = ET.fromstring(data)
    channel = root.find("channel")
    if channel is None:
        raise ValueError("Missing WXR channel")
    # Handle WXR 1.0/1.1/1.2 namespaces without accepting arbitrary XML structures.
    namespaces = dict(NS)
    for node in channel.iter():
        if node.tag.endswith("}wxr_version"):
            namespaces["wp"] = node.tag.split("}")[0][1:]
            break
    def value(node, key):
        return node.findtext(key, default=None, namespaces=namespaces)
    site_url = site_url or value(channel, "link")
    attachments = {int(value(n, "wp:post_id")): value(n, "wp:attachment_url") for n in channel.findall("item")
                   if value(n, "wp:post_type") == "attachment" and value(n, "wp:post_id")}
    term_lookup = {}
    for tag, taxonomy, id_key, slug_key, name_key in (
        ("wp:category", "category", "wp:term_id", "wp:category_nicename", "wp:cat_name"),
        ("wp:tag", "post_tag", "wp:term_id", "wp:tag_slug", "wp:tag_name"),
    ):
        for term in channel.findall(tag, namespaces):
            term_id = value(term, id_key)
            slug = value(term, slug_key)
            term_lookup[(taxonomy, slug)] = {"id": int(term_id) if term_id else None,
                                              "slug": slug, "name": value(term, name_key)}
    posts = []
    for node in channel.findall("item"):
        post_type = value(node, "wp:post_type")
        if post_type not in post_types:
            continue
        meta = {value(n, "wp:meta_key"): value(n, "wp:meta_value") for n in node.findall("wp:postmeta", namespaces)}
        media_id = int(meta["_thumbnail_id"]) if str(meta.get("_thumbnail_id", "")).isdigit() else None
        post = {"id": int(value(node, "wp:post_id")), "title": value(node, "title"),
                "slug": value(node, "wp:post_name"), "link": value(node, "link"),
                "status": value(node, "wp:status"), "type": post_type,
                "date": value(node, "wp:post_date"), "date_gmt": value(node, "wp:post_date_gmt"),
                "modified": value(node, "wp:post_modified"), "modified_gmt": value(node, "wp:post_modified_gmt"),
                "content": value(node, "content:encoded"), "meta": meta,
                "categories": [], "tags": [], "featured_media": media_id,
                "_embedded": {"wp:featuredmedia": [{"id": media_id, "source_url": attachments.get(media_id)}]}}
        for term in node.findall("category"):
            taxonomy, slug = term.get("domain"), term.get("nicename")
            if taxonomy in ("category", "post_tag"):
                post["categories" if taxonomy == "category" else "tags"].append(
                    term_lookup.get((taxonomy, slug), {"id": None, "slug": slug, "name": term.text}))
        posts.append(post)
    inventory = import_rest(posts, site_id, site_url=site_url,
                            completeness="complete" if complete_export else "unknown",
                            statuses_requested=["all"] if complete_export else [],
                            field_map=field_map, coverage_complete=complete_export, source_ref=source_ref)
    inventory["scope"]["source_type"] = "wordpress_wxr"
    inventory["scope"]["limitations"].append("Includes selected post types only: " + ", ".join(post_types))
    return inventory


def fetch_public_rest(site_url, site_id, *, opener=None, max_pages=10000):
    """GET-only public posts adapter. All-site completeness remains partial."""
    parts = urlsplit(site_url)
    if parts.scheme != "https" or not parts.netloc or parts.username or parts.query or parts.fragment:
        raise ValueError("Use an HTTPS site URL without credentials, query or fragment")
    opener = opener or urlopen
    endpoint = site_url.rstrip("/") + "/wp-json/wp/v2/posts"
    posts, expected_total, expected_pages, stable = [], None, None, True
    page = 1
    while page <= max_pages:
        query = urlencode({"per_page": 100, "page": page, "status": "publish", "orderby": "id", "order": "asc", "_embed": "1"})
        request = Request(endpoint + "?" + query, headers={"Accept": "application/json", "User-Agent": "FortuneLabo-ReadOnlyInventory/1.0"}, method="GET")
        with opener(request, timeout=30) as response:
            batch = json.load(response)
            total = int(response.headers["X-WP-Total"])
            pages = int(response.headers["X-WP-TotalPages"])
        if not isinstance(batch, list):
            raise ValueError("REST endpoint did not return a posts array")
        if expected_total is None:
            expected_total, expected_pages = total, pages
        elif (total, pages) != (expected_total, expected_pages):
            stable = False
        posts.extend(batch)
        if page >= pages or not batch:
            break
        page += 1
    coverage = stable and expected_pages is not None and page >= expected_pages
    inventory = import_rest(posts, site_id, site_url=site_url, completeness="partial",
                            statuses_requested=["publish"], coverage_complete=coverage,
                            expected_count=expected_total)
    inventory["scope"]["source_type"] = "wordpress_rest_public"
    inventory["scope"]["limitations"].append("Unauthenticated public posts only; draft/private/future/custom types and membership access are not proven.")
    if not coverage:
        inventory["scope"]["limitations"].append("Pagination changed or page limit reached; repeat a stable export.")
    return inventory


def inventory_view(existing_inventory, test_index):
    """Read both stores without representing an unpublished test as an existing post.

    All requested metadata fields are present. Unobserved links/counts stay null;
    candidate links are retained separately from observed WordPress links.
    """
    records = [{"record_type": "existing_wordpress", "source_index": "existing-content-index",
                "metadata": deepcopy(item), "candidate_internal_links": []}
               for item in existing_inventory["items"]]
    for fixture in test_index.get("items", []):
        metadata = {key: None for key in (
            "content_id", "wordpress_post_id", "title", "slug", "url", "status", "publish_date", "modified_date",
            "post_type", "category", "tags", "internal_links", "featured_image", "word_count", "word_count_method", *EDITORIAL_FIELDS)}
        metadata.update({"date_basis": "site_timezone_unknown", "body_available": False, "field_provenance": {}})
        for key in metadata:
            if key not in ("internal_links", "field_provenance") and key in fixture:
                metadata[key] = deepcopy(fixture[key])
        metadata["wordpress_post_id"] = None
        metadata["field_provenance"] = {key: "test_fixture:" + fixture["content_id"] for key in EDITORIAL_FIELDS if metadata[key] is not None}
        links = fixture.get("internal_links") or []
        candidates = [deepcopy(link) for link in links if isinstance(link, dict)]
        observed = [link for link in links if isinstance(link, str)]
        observed += [link["target_url"] for link in candidates if link.get("status") == "verified" and link.get("target_url")]
        metadata["internal_links"] = observed or None
        records.append({"record_type": "test_fixture", "source_index": "test-content-index", "metadata": metadata,
                        "candidate_internal_links": candidates})
    identifiers = [record["metadata"]["content_id"] for record in records]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("Content ID collision between existing and test indexes")
    return {"schema_version": "1.0.0", "counts": {"existing": len(existing_inventory["items"]),
            "test_fixtures": len(test_index.get("items", [])), "total_records": len(records)}, "records": records}


def write_private_json(value, output, *, repository=None):
    """Fail closed for output paths inside the repo except its ignored .private/."""
    repository = Path(repository or Path(__file__).resolve().parents[2]).resolve()
    output = Path(output).resolve()
    if output == repository or repository in output.parents:
        private = repository / ".private"
        if private not in output.parents:
            raise ValueError("Real inventories must be outside the repository or inside ignored .private/")
    output.parent.mkdir(parents=True, exist_ok=True)
    # Atomic file replace avoids following an existing file symlink and leaves 0600.
    temporary = output.with_name(output.name + ".tmp")
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        temporary.replace(output)
    finally:
        if temporary.exists():
            temporary.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--rest-json", type=Path)
    source.add_argument("--wxr", type=Path)
    source.add_argument("--public-site")
    parser.add_argument("--site-id", required=True, help="Stable operator-assigned site namespace")
    parser.add_argument("--output", type=Path, default=Path(".private/editorial/existing-content-index.json"))
    parser.add_argument("--field-map", type=Path)
    parser.add_argument("--complete-export", action="store_true", help="Operator attests full article export across all statuses")
    parser.add_argument("--post-types", nargs="+", default=["post", "page"])
    args = parser.parse_args()
    mapping = json.loads(args.field_map.read_text()) if args.field_map else None
    if args.public_site:
        if args.complete_export:
            parser.error("Public REST cannot prove all-site completeness")
        inventory = fetch_public_rest(args.public_site, args.site_id)
    elif args.wxr:
        inventory = import_wxr(args.wxr.read_bytes(), args.site_id, complete_export=args.complete_export,
                               post_types=args.post_types, field_map=mapping)
    else:
        inventory = import_rest(json.loads(args.rest_json.read_text()), args.site_id,
                                completeness="complete" if args.complete_export else "unknown",
                                statuses_requested=["all"] if args.complete_export else [],
                                coverage_complete=args.complete_export, field_map=mapping)
    write_private_json(inventory, args.output)
    print(json.dumps({"imported_count": len(inventory["items"]), "completeness": inventory["scope"]["completeness"],
                      "duplicates": len(inventory["duplicates"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
