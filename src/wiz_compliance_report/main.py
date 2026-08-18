"""CLI entry point for the Wiz service compliance report tool."""

from __future__ import annotations

import argparse
import os
import sys

from wiz_compliance_report.auth import WizAuthError, get_access_token
from wiz_compliance_report.client import WizAPIError
from wiz_compliance_report.compliance import get_compliance_score
from wiz_compliance_report.config import load_config
from wiz_compliance_report.report import build_report, write_report
from wiz_compliance_report.services import list_services

DEFAULT_COMPLIANCE_ID = "wf-id-1"
PROGRESS_INTERVAL = 20


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a Wiz service compliance report.")
    parser.add_argument(
        "--compliance-id",
        default=DEFAULT_COMPLIANCE_ID,
        help=f"Security framework ID to score services against (default: {DEFAULT_COMPLIANCE_ID}).",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Path to write the JSON report to. If omitted, results are only printed to stdout.",
    )
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args()

    try:
        config = load_config()
        access_token = get_access_token(config)
        services = list_services(config, access_token)
        print(f"Discovered {len(services)} service(s).")

        print(f"Pulling compliance scores for framework '{args.compliance_id}'...")
        total = len(services)
        for count, (service_id, service) in enumerate(services.items(), start=1):
            service["averageCompliancePosture"] = get_compliance_score(
                config, access_token, args.compliance_id, service_id
            )
            if count % PROGRESS_INTERVAL == 0 or count == total:
                print(f"{count} of {total} services processed")
    except (RuntimeError, WizAuthError, WizAPIError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Found {len(services)} service(s):")
    for service_id, service in services.items():
        print(
            f"  {service_id}: {service['displayName']} "
            f"(compliance: {service['averageCompliancePosture']})"
        )

    if args.output:
        report = build_report(args.compliance_id, services)
        write_report(report, args.output)
        print(f"Report written to {os.path.abspath(args.output)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
