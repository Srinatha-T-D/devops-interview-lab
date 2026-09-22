# Order API incident runbook

## First five minutes

1. Confirm severity: affected environment, users, error percentage, and start time.
2. Freeze the blast radius: pause rollout or rollback if this follows a release.
3. Compare the last known-good deployment: image digest, environment variables, Secret/ConfigMap revision, and infrastructure changes.
4. Read one failing request end-to-end using `X-Request-ID`; do not infer the cause from a dashboard alone.

## Docker evidence commands

```powershell
docker compose ps
docker compose logs --tail=100 api
docker compose exec api env | Select-String DATABASE_URL
docker compose exec api getent hosts db
docker inspect --format '{{json .State.Health}}' <container-name>
```

## Kubernetes evidence commands

```bash
kubectl -n <namespace> get pods,deploy,rs
kubectl -n <namespace> describe pod <pod>
kubectl -n <namespace> logs deploy/order-api --since=15m
kubectl -n <namespace> get events --sort-by=.lastTimestamp
kubectl -n <namespace> rollout history deploy/order-api
kubectl -n <namespace> get configmap order-api-config -o yaml
```

## Recovery decision

Rollback is the safe first response when a release or config change correlates with a customer-impacting failure and the cause is not immediately certain. Forward-fix only when the change is small, tested, reversible, and lower risk than rollback. Record the exact change and validation evidence.

## Post-incident record

- Timeline in UTC, impact, and detection method.
- Technical root cause and contributing conditions.
- Why existing monitoring or release controls did not prevent it.
- Remediations with owners and due dates: test, alert, deployment guardrail, documentation.
