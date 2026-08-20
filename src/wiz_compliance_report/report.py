"""Builds and writes the JSON compliance report."""

from __future__ import annotations

import getpass
import json
from datetime import datetime, timezone
from typing import Any


def build_report(compliance_id: str, services: dict[str, dict]) -> dict[str, Any]:
    return {
        "generatedBy": getpass.getuser(),
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "complianceFrameworkId": compliance_id,
        "services": [
            {
                "id": service_id,
                "name": service["displayName"],
                "owners": service["owners"],
                "complianceScore": service["averageCompliancePosture"],
            }
            for service_id, service in services.items()
        ],
    }


def write_report(report: dict[str, Any], output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
