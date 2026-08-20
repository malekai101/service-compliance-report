"""Loads Wiz API configuration from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

_REQUIRED_VARS = ("WIZ_CLIENT_ID", "WIZ_CLIENT_SECRET", "WIZ_AUTH_URL", "WIZ_API_URL")


@dataclass(frozen=True)
class WizConfig:
    client_id: str
    client_secret: str
    auth_url: str
    api_url: str


def load_config() -> WizConfig:
    load_dotenv()

    values = {name: os.environ.get(name) for name in _REQUIRED_VARS}
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise RuntimeError(
            "Missing required environment variable(s): "
            f"{', '.join(missing)}. See .env.example."
        )

    return WizConfig(
        client_id=values["WIZ_CLIENT_ID"],
        client_secret=values["WIZ_CLIENT_SECRET"],
        auth_url=values["WIZ_AUTH_URL"],
        api_url=values["WIZ_API_URL"],
    )
