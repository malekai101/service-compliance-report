"""Authenticates against the Wiz API using the OAuth2 client-credentials grant."""

from __future__ import annotations

import requests

from wiz_compliance_report.config import WizConfig


class WizAuthError(RuntimeError):
    pass


def get_access_token(config: WizConfig) -> str:
    response = requests.post(
        config.auth_url,
        data={
            "grant_type": "client_credentials",
            "client_id": config.client_id,
            "client_secret": config.client_secret,
            "audience": "wiz-api",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )

    if not response.ok:
        body = response.text.replace(config.client_secret, "[REDACTED]")
        raise WizAuthError(f"Wiz authentication failed ({response.status_code}): {body}")

    token = response.json().get("access_token")
    if not token:
        raise WizAuthError("Wiz authentication response did not contain an access_token")

    return token
