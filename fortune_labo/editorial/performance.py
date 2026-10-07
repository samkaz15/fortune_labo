"""Raw observations only. No scores, blended rates or fabricated zero values."""
from datetime import date
import math

METRICS = {
    "impressions": ("count", "integer"), "clicks": ("count", "integer"),
    "ctr": ("ratio", "number"), "average_position": ("position", "number"),
    "users": ("count", "integer"), "sessions": ("count", "integer"),
    "engaged_sessions": ("count", "integer"), "engagement_rate": ("ratio", "number"),
    "average_engagement_time": ("seconds", "number"), "scroll_depth": ("percent", "number"),
    "fortune_cta_clicks": ("count", "integer"), "fortune_start": ("count", "integer"),
    "fortune_complete": ("count", "integer"), "member_registration": ("count", "integer"),
    "premium_conversion": ("count", "integer"), "returning_users": ("count", "integer"),
    "repeat_article_views": ("count", "integer"),
}
SOURCES = {"Search Console", "GA4", "WordPress", "SNS"}


def empty_observation(content_id, source, period_start, period_end, *, timezone="UTC",
                      source_reference=None, definition_version="raw-metrics-1.0.0"):
    if source not in SOURCES:
        raise ValueError("Unknown performance source")
    return {"schema_version": "1.0.0", "content_id": content_id, "source": source,
            "period_start": period_start, "period_end": period_end, "timezone": timezone,
            "collected_at": None, "definition_version": definition_version,
            "source_reference": source_reference, "filters": {}, "dimensions": {},
            "metrics": {key: None for key in METRICS},
            "metric_metadata": {key: {"unit": unit, "source_metric": None, "definition": None,
                                      "aggregation": None, "numerator": None, "denominator": None}
                                for key, (unit, _) in METRICS.items()},
            "data_quality": {"sampling": "unknown", "thresholding": "unknown", "notes": []}}


def validate_observation(record):
    # Use the same strict, dependency-free contract validator as A07/A08.
    import importlib.util
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    spec = importlib.util.spec_from_file_location("_performance_contract_validator", root / "scripts/validate_editorial.py")
    validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator)
    schema = validator.load(root / "docs/editorial/schemas/performance_observation.schema.json")
    validator.audit_schema(schema)
    validator.validate(record, schema)
    if record.get("source") not in SOURCES:
        raise ValueError("Unknown performance source")
    if date.fromisoformat(record["period_start"]) > date.fromisoformat(record["period_end"]):
        raise ValueError("Performance period is reversed")
    if not record.get("timezone") or not record.get("definition_version"):
        raise ValueError("Timezone and metric definition version are required")
    if set(record["metrics"]) != set(METRICS):
        raise ValueError("Store exactly the raw metric contract; scores are unsupported")
    for key, (unit, kind) in METRICS.items():
        value = record["metrics"][key]
        meta = record["metric_metadata"][key]
        if meta["unit"] != unit:
            raise ValueError(f"Wrong metric unit: {key}")
        if value is None:
            continue
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
            raise ValueError(f"Invalid metric value: {key}")
        if kind == "integer" and not isinstance(value, int):
            raise ValueError(f"Count must be integer: {key}")
        if unit == "ratio" and value > 1 or unit == "percent" and value > 100:
            raise ValueError(f"Metric outside its scale: {key}")
        if not record.get("collected_at") or not record.get("source_reference"):
            raise ValueError("Observed metrics require collection time and source reference")
        if not meta.get("source_metric") or not meta.get("definition") or not meta.get("aggregation"):
            raise ValueError(f"Observed metric requires a traceable source definition: {key}")
    return record


METRIC_GROUPS = {
    "seo": ("impressions", "clicks", "ctr", "average_position"),
    "engagement": ("users", "sessions", "engaged_sessions", "engagement_rate", "average_engagement_time", "scroll_depth"),
    "conversion": ("fortune_cta_clicks", "fortune_start", "fortune_complete", "member_registration", "premium_conversion"),
    "retention": ("returning_users", "repeat_article_views"),
}


def performance_context(observations, *, content_id, period_start, period_end, timezone,
                        filters=None, dimensions=None):
    """Project one explicitly selected reporting scope into A07's metric groups.

    No metric is averaged, scored or recalculated. Reject mixed content IDs,
    periods, reporting timezones, filters, dimensions, definition versions and
    duplicate metric ownership. Full immutable-copy source observations travel
    with the projection so A07/A08 cannot lose units or provider provenance.
    """
    from copy import deepcopy
    if not isinstance(observations, list):
        raise ValueError("Performance observations must be a list")
    if not content_id or not timezone:
        raise ValueError("Explicit content ID and reporting timezone are required")
    if date.fromisoformat(period_start) > date.fromisoformat(period_end):
        raise ValueError("Selected performance period is reversed")
    selected_filters = {} if filters is None else filters
    selected_dimensions = {} if dimensions is None else dimensions
    if not isinstance(selected_filters, dict) or not isinstance(selected_dimensions, dict):
        raise ValueError("Performance filters and dimensions must be objects")
    selected = {"content_id": content_id, "period_start": period_start, "period_end": period_end,
                "timezone": timezone, "filters": selected_filters, "dimensions": selected_dimensions}
    groups = {group: {key: None for key in keys} for group, keys in METRIC_GROUPS.items()}
    owners, refs, definitions = {}, set(), set()
    for observation in observations:
        validate_observation(observation)
        for key, value in selected.items():
            if observation[key] != value:
                raise ValueError(f"Observation differs from the selected reporting scope: {key}")
        definitions.add(observation["definition_version"])
        if len(definitions) > 1:
            raise ValueError("Do not mix performance definition versions in one A07 context")
        for group, metric_names in METRIC_GROUPS.items():
            for key in metric_names:
                value = observation["metrics"][key]
                if value is None:
                    continue
                if key in owners:
                    raise ValueError(f"Multiple observations supply the same metric; select one source/scope explicitly: {key}")
                owners[key] = observation["source_reference"]
                groups[group][key] = value
                refs.add(observation["source_reference"])
    observed = [group for group, values in groups.items() if any(value is not None for value in values.values())]
    return {"status": "supplied_not_independently_verified" if observed else "unmeasured",
            "metric_groups": groups, "observed_groups": observed, "evidence_refs": sorted(refs),
            "raw_observations": deepcopy(observations)}
