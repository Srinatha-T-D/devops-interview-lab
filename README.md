# DevOps Interview Lab — Order API

This is a compact production-style service designed for hands-on interview preparation. It contains an API, PostgreSQL dependency, Docker build, CI examples, Kubernetes manifests, and intentional incident scenarios.

## Architecture

```text
client -> order-api (FastAPI) -> PostgreSQL
              |        |
              |        +-> /metrics (Prometheus format)
              +-> structured request logs
```

The API exposes:

| Endpoint | Purpose | Expected result |
| --- | --- | --- |
| `/livez` | Process liveness only | `200` while the app process runs |
| `/readyz` | Readiness, including a real database query | `200` only when PostgreSQL is usable |
| `/api/v1/orders` | Application endpoint | Returns seeded orders |
| `/metrics` | Basic HTTP metrics | Prometheus-compatible text |

## Local prerequisites

Required for the first lab:

- Docker Desktop 4.x running, with Docker Compose v2.
- Git and a terminal (PowerShell is fine).
- VS Code is strongly recommended.

Useful later:

- Python 3.12 for running and testing outside Docker.
- `kubectl` plus `kind` or `minikube` for Kubernetes labs.
- Postman, Bruno, or `curl` for API checks.

You **do not need an AWS/Azure account** for the first two labs. We will use a local Kubernetes cluster first. For the cloud phase, use a personal sandbox AWS account with MFA, a budget alert, AWS CLI v2, and no long-lived root credentials. Never paste cloud keys into the repository, Compose file, Jenkinsfile, or chat.

## Start the healthy baseline

Run these commands from this directory:

```powershell
docker compose up --build -d
docker compose ps
curl.exe -i http://localhost:8080/livez
curl.exe -i http://localhost:8080/readyz
curl.exe http://localhost:8080/api/v1/orders
docker compose logs --tail=100 api
```

Expected: both probes return `200`, and `orders` returns two rows. Stop the stack with `docker compose down`.

## First incident: broken production deployment

This is intentionally a configuration incident, not a code rewrite. Start it only after you have captured the healthy baseline outputs:

```powershell
docker compose --profile incident-db-url up --build -d
docker compose ps
curl.exe -i http://localhost:8081/livez
curl.exe -i http://localhost:8081/readyz
curl.exe -i http://localhost:8081/api/v1/orders
docker compose logs --tail=100 incident-api
```

Your task is to diagnose the incident and propose the smallest safe remediation. Do **not** edit the application code yet. Capture the exact command output and explain:

1. Which component is unhealthy?
2. Why liveness and readiness disagree (if they do)?
3. What evidence supports the root cause?
4. What one-line configuration change safely resolves it?
5. What regression guard would prevent recurrence?

When you can answer those, share the results and we will validate the fix before progressing to the next incident.

## Enterprise troubleshooting loop

Use this order in every production incident:

1. **Scope impact:** identify users, environment, start time, SLO/error-rate impact.
2. **Stabilize:** rollback, stop further rollout, or reduce traffic before experimenting.
3. **Collect evidence:** deployment diff, logs with request IDs, metrics, events, and dependency health.
4. **Form a falsifiable hypothesis:** state what observation would prove it wrong.
5. **Apply the smallest reversible change:** prefer config rollback or canary over broad edits.
6. **Validate recovery:** user path, readiness, error rate, latency, and a time window of stable metrics.
7. **Prevent recurrence:** test, alert, immutable config review, runbook, and post-incident action.

## Interview talking points represented here

- Liveness means the process can run; readiness means it can safely receive traffic. Do not make liveness depend on transient downstream services.
- Config is a release artifact: validate it in CI and expose it through an auditable deployment mechanism.
- Logs should be structured and correlated; metrics should describe rate, errors, and latency; traces explain a single request path.
- CI builds and tests an immutable image. CD promotes that *same image digest* through environments, with approvals and rollback.
- Kubernetes should use resource requests/limits, probes, non-root execution, a rolling-update strategy, and Secret references—not embedded credentials.

See `docs/INTERVIEW_PREP.md` for the preparation plan and `docs/RUNBOOK.md` for a corporate-style incident template.
