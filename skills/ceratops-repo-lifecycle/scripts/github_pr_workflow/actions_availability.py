"""Detect a confirmed GitHub Actions outage from one bounded status snapshot.

The ship workflow uses this module only as a pre-mutation circuit breaker.
Unavailable, malformed, oversized, or non-outage status evidence is not enough
to block shipping; ordinary exact-head gates remain authoritative in that case.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from collections.abc import Callable
from typing import Any

STATUS_SUMMARY_URL = "https://www.githubstatus.com/api/v2/summary.json"
ACTIONS_COMPONENT_ID = "br0l2tvcx85d"
OUTAGE_STATES = frozenset({"partial_outage", "major_outage"})
ACTIVE_INCIDENT_STATES = frozenset({"investigating", "identified", "monitoring"})
MAX_STATUS_BYTES = 256 * 1024
DEFAULT_TIMEOUT_SECONDS = 5.0


def _bounded_string(value: object, *, limit: int = 512) -> str | None:
    """Return one bounded string field from untrusted status-page JSON."""

    if not isinstance(value, str) or not value:
        return None
    return value if len(value) <= limit else value[:limit]


def _is_actions_component(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    component_id = value.get("id") or value.get("code")
    name = value.get("name")
    return component_id == ACTIONS_COMPONENT_ID or (
        isinstance(name, str) and name.casefold() == "actions"
    )


def _incident_evidence(raw_incidents: object) -> dict[str, Any] | None:
    """Return bounded evidence for the first active Actions incident."""

    if not isinstance(raw_incidents, list):
        return None
    for incident in raw_incidents[:25]:
        if not isinstance(incident, dict):
            continue
        status = incident.get("status")
        affected = incident.get("components")
        if status not in ACTIVE_INCIDENT_STATES or not isinstance(affected, list):
            continue
        if not any(_is_actions_component(component) for component in affected[:25]):
            continue
        url = _bounded_string(incident.get("shortlink"), limit=300)
        return {
            "id": _bounded_string(incident.get("id"), limit=100),
            "name": _bounded_string(incident.get("name")),
            "status": _bounded_string(status, limit=40),
            "impact": _bounded_string(incident.get("impact"), limit=40),
            "url": url if url and url.startswith("https://") else None,
            "updated_at": _bounded_string(incident.get("updated_at"), limit=80),
        }
    return None


def confirmed_actions_outage(
    *,
    opener: Callable[..., Any] | None = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
) -> dict[str, Any] | None:
    """Return bounded outage evidence, or ``None`` without a confirmation.

    Exactly one Statuspage summary request is made. Network and payload failures
    deliberately fall through to the existing GitHub gate workflow instead of
    turning the status service itself into a shipping blocker.
    """

    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")
    request = urllib.request.Request(
        STATUS_SUMMARY_URL,
        headers={
            "Accept": "application/json",
            "User-Agent": "ceratops-repo-lifecycle",
        },
    )
    open_request = opener or urllib.request.urlopen
    try:
        with open_request(request, timeout=timeout_seconds) as response:
            raw = response.read(MAX_STATUS_BYTES + 1)
        if len(raw) > MAX_STATUS_BYTES:
            return None
        payload = json.loads(raw.decode("utf-8"))
    except (
        OSError,
        UnicodeDecodeError,
        ValueError,
        json.JSONDecodeError,
        urllib.error.URLError,
    ):
        return None
    if not isinstance(payload, dict):
        return None
    components = payload.get("components")
    if not isinstance(components, list):
        return None
    component = next(
        (value for value in components[:50] if _is_actions_component(value)),
        None,
    )
    if not isinstance(component, dict) or component.get("status") not in OUTAGE_STATES:
        return None
    page = payload.get("page")
    page_updated_at = (
        _bounded_string(page.get("updated_at"), limit=80)
        if isinstance(page, dict)
        else None
    )
    return {
        "source": STATUS_SUMMARY_URL,
        "page_updated_at": page_updated_at,
        "component": {
            "id": _bounded_string(component.get("id"), limit=100),
            "name": _bounded_string(component.get("name"), limit=100),
            "status": _bounded_string(component.get("status"), limit=40),
            "updated_at": _bounded_string(component.get("updated_at"), limit=80),
        },
        "incident": _incident_evidence(payload.get("incidents")),
    }
