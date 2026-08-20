# Wiz Service Compliance Report

> **⚠️ Test code — not production-ready.** This project was built incrementally as a
> proof of concept for pulling service-level compliance scores from the Wiz GraphQL
> API. It has not been security reviewed, load tested, or hardened for production
> use. Review it thoroughly (auth handling, error handling, rate limiting, logging
> of sensitive data, etc.) before relying on it for anything beyond local testing.

## What it does

1. Authenticates to the Wiz API using a service account (OAuth2 client-credentials
   grant).
2. Queries the Wiz service catalog (`applicationServices`) for every service,
   paginating with cursors as needed.
3. For each service, queries its average compliance posture
   (`securityFramework.complianceAnalytics`) against a given compliance framework ID.
4. Prints progress and results to stdout, and optionally writes a JSON report.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Copy `.env.example` to `.env` and fill in your Wiz service account credentials and
tenant-specific URLs:

```bash
cp .env.example .env
```

| Variable            | Description                                                        |
| ------------------- | -------------------------------------------------------------------|
| `WIZ_CLIENT_ID`     | Wiz service account client ID                                      |
| `WIZ_CLIENT_SECRET` | Wiz service account client secret                                  |
| `WIZ_AUTH_URL`      | Tenant-specific OAuth token endpoint                                |
| `WIZ_API_URL`       | Tenant-specific GraphQL API endpoint (e.g. `https://api.us1.app.wiz.io/graphql`) |

`.env` is git-ignored — never commit real credentials.

## Usage

```bash
wiz-compliance-report
```

By default this scores every discovered service against compliance framework
`wf-id-1` and prints results to stdout only.

### Options

| Flag                       | Default    | Description                                              |
| -------------------------- | ---------- | --------------------------------------------------------- |
| `--compliance-id`          | `wf-id-1`  | Security framework ID to score services against            |
| `--output` / `-o`          | *(none)*   | Path to write a JSON report to. If omitted, no file is written. |

Example:

```bash
wiz-compliance-report --compliance-id wf-id-1 --output report.json
```

## JSON report format

When `--output` is given, a report like this is written:

```json
{
  "generatedBy": "jsmith",
  "generatedAt": "2026-08-18T20:15:00.123456+00:00",
  "complianceFrameworkId": "wf-id-1",
  "services": [
    {
      "id": "abc-123",
      "name": "checkout-service",
      "owners": ["Jane Doe"],
      "complianceScore": 87.5
    }
  ]
}
```

- `generatedBy` — the OS user who ran the report (`getpass.getuser()`)
- `generatedAt` — UTC timestamp the report was generated
- `complianceFrameworkId` — the framework ID passed to `--compliance-id`
- `services` — one entry per discovered service, with its name, owner(s), and
  compliance score

## Known limitations

- One compliance-score API call is made per service (no batching/parallelism), so
  runtime scales linearly with catalog size and may hit rate limits on large
  tenants.
- Minimal error handling/retry logic around transient API failures.
- No automated test suite yet.
