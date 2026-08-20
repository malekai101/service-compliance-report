"""Fetches per-service compliance scores for a security framework from the Wiz GraphQL API."""

from __future__ import annotations

from wiz_compliance_report.client import execute_query
from wiz_compliance_report.config import WizConfig

COMPLIANCE_PAGE_QUERY = """
query CompliancePageTable($id: ID!, $analyticsSelection: SecurityFrameworkComplianceAnalyticsSelection, $orderBy: SecurityFrameworkSelectionOrder) {
  securityFramework(id: $id) {
    id
    name
    complianceAnalytics(selection: $analyticsSelection, orderBy: $orderBy) {
      averageCompliancePosture
    }
  }
}
"""


def get_compliance_score(
    config: WizConfig, access_token: str, framework_id: str, service_id: str
) -> float | None:
    variables = {
        "id": framework_id,
        "analyticsSelection": {"owningApplicationService": {"equals": [service_id]}},
    }

    data = execute_query(config, access_token, COMPLIANCE_PAGE_QUERY, variables)
    return data["securityFramework"]["complianceAnalytics"]["averageCompliancePosture"]
