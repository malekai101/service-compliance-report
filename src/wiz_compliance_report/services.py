"""Fetches the service catalog from the Wiz GraphQL API."""

from __future__ import annotations

from wiz_compliance_report.client import execute_query
from wiz_compliance_report.config import WizConfig

PAGE_SIZE = 500

PROMOTED_SERVICES_QUERY = """
query PromotedServicesTable($after: String, $first: Int, $filterBy: ApplicationServiceFilters, $orderBy: ApplicationServiceOrder) {
  applicationServices(
    first: $first
    after: $after
    orderBy: $orderBy
    filterBy: $filterBy
  ) {
    nodes {
      id
      displayName
      ownersV2 {
        identity {
          id
          name
          primaryEmail
        }
      }
      sources
    }
    pageInfo {
      endCursor
      hasNextPage
    }
    totalCount
  }
}
"""


def list_services(config: WizConfig, access_token: str) -> dict[str, dict]:
    services: dict[str, dict] = {}
    after: str | None = None

    while True:
        variables = {
            "first": PAGE_SIZE,
            "after": after,
            "filterBy": {},
            "orderBy": {"field": "NAME", "direction": "ASC"},
        }

        data = execute_query(config, access_token, PROMOTED_SERVICES_QUERY, variables)
        connection = data["applicationServices"]

        for node in connection["nodes"]:
            owners = [
                owner["identity"]["name"]
                for owner in node.get("ownersV2") or []
                if owner.get("identity")
            ]
            services[node["id"]] = {
                "displayName": node["displayName"],
                "owners": owners,
            }

        page_info = connection["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        after = page_info["endCursor"]

    return services
