# DevOps Engineer preparation plan (3–5 years)

## Preparation cadence before the interview

### Day 1 — delivery foundations

Build this lab, explain its Dockerfile line-by-line, and trace a request from port 8080 to PostgreSQL. Practise `git diff`, a pull-request review mindset, semantic versioning, and identifying an image by immutable digest rather than `latest`.

### Day 2 — CI/CD ownership

Explain Jenkins controller/agent design, credentials binding, shared libraries, declarative versus scripted pipelines, artifact promotion, gates, parallel stages, and rollback. Explain GitHub Actions events, reusable workflows, OIDC, least-privilege `permissions`, protected environments, and dependency pinning. Be ready to design: commit -> test -> SAST/SCA -> build -> image scan -> sign/SBOM -> registry -> staging -> smoke test -> approval -> production canary -> promotion.

### Day 3 — container and Kubernetes operations

Know image layers, multi-stage builds, non-root images, `.dockerignore`, registry auth, tag versus digest, and container resource constraints. For Kubernetes: Pods, Deployments, ReplicaSets, Services, Ingress, ConfigMaps, Secrets, probes, requests/limits, HPA, PDB, namespaces, RBAC, NetworkPolicies, StatefulSets, Jobs/CronJobs, and rollout/rollback commands. Explain why `readiness` removes a Pod from endpoints while `liveness` causes a restart.

### Day 4 — cloud and reliability

For AWS, cover IAM roles, VPC/subnets/routes/NAT/security groups, ALB, ECR, EKS/ECS, RDS, S3, CloudWatch, KMS, Secrets Manager, autoscaling, multi-AZ resilience, tagging, budgets, CloudTrail, and IaC with Terraform. State Azure equivalents: Entra ID/managed identity, VNet/NSG, ACR, AKS, Azure Database, Key Vault, Monitor, and Bicep/Terraform. For reliability, articulate SLIs/SLOs/error budgets, the four golden signals, alert fatigue, load testing, backups/restore tests, capacity planning, RTO/RPO, and disaster recovery.

### Day 5 — automation and interview simulation

Use Python for an idempotent API/cloud automation: command-line arguments, environment validation, retry with exponential backoff and jitter, structured logs, typed error handling, unit tests, and a `--dry-run` mode. Review the Makefile: explain targets, variables, phony targets, and why builds must be reproducible. Then practise a 45-minute design/troubleshooting round using the incident labs.

## Senior-quality answers

### “How do you design a production CI/CD pipeline?”

“I separate build from deployment and produce one immutable, scanned image identified by digest. Pull requests run unit tests, linting, SAST and dependency scanning. Main builds, creates an SBOM, signs and publishes the artifact. CD promotes that exact digest through environments using declarative manifests and environment-specific configuration from a secret manager. Production uses canary or blue/green delivery, health and SLO-based gates, auditable approval where required, and a fast tested rollback. Credentials use workload identity/OIDC with least privilege.”

### “A Kubernetes deployment is unhealthy after release. What do you do?”

“First I measure customer impact and stop the rollout or rollback if needed. I compare the release’s image, config and dependency changes with the last good version. I inspect pod status, events, probe failures, container logs and service endpoints, then correlate a failing request using its request ID. I form a testable hypothesis, perform the smallest reversible remediation, and validate user-path success, error rate and latency before closing. I finish with a prevention item such as a configuration contract test or pre-deploy smoke test.”

### “How would you use AI responsibly in DevOps?”

“I use it to accelerate low-risk work—summarizing logs, drafting runbooks, detecting anomalous patterns, and suggesting remediation—but its output stays reviewable. I do not give an agent unrestricted production credentials or allow autonomous destructive changes. Inputs are redacted, actions are policy-gated, and every recommendation has evidence, human approval, and an audit trail.”

## Questions to ask Mirafra

1. Which delivery platform is the source of truth: Jenkins, GitHub Actions, or both—and why?
2. What are the current deployment frequency, change-failure rate, and mean time to restore?
3. Is the main workload Kubernetes, VMs, or managed containers? Which cloud is primary?
4. How are Terraform/IaC changes reviewed, state protected, and secrets delivered to workloads?
5. What would success in the first 90 days look like for this role?
