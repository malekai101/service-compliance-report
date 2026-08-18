"""Thin client for issuing queries against the Wiz GraphQL API."""

from __future__ import annotations

from typing import Any

import requests

from wiz_compliance_report.config import WizConfig


class WizAPIError(RuntimeError):
    pass


def execute_query(
    config: WizConfig,
    access_token: str,
    query: str,
    variables: dict[str, Any] | None = None,
) -> dict[str, Any]:
    response = requests.post(
        config.api_url,
        json={"query": query, "variables": variables or {}},
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        timeout=60,
    )

    if not response.ok:
        body = response.text.replace(access_token, "[REDACTED]")
        raise WizAPIError(f"Wiz API request failed ({response.status_code}): {body}")

    payload = response.json()
    if "errors" in payload and payload["errors"]:
        raise WizAPIError(f"Wiz API returned errors: {payload['errors']}")

    return payload["data"]
