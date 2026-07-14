# ruff: noqa: F401,F841
from __future__ import annotations

from typing import Any

from qdrant_client.http.models import FieldCondition, Filter, MatchAny, MatchValue


def build_payload_filter(filters: dict[str, Any] | None) -> Filter | None:
    if not filters:
        return None
    conditions: list[FieldCondition] = []
    for key, value in filters.items():
        if value is None:
            continue
        if isinstance(value, list | tuple | set):
            values = [item for item in value if item is not None]
            if values:
                conditions.append(FieldCondition(key=key, match=MatchAny(any=values)))
        else:
            conditions.append(FieldCondition(key=key, match=MatchValue(value=value)))
    return Filter(must=conditions) if conditions else None
