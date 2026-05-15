# billing-api

Internal billing service. Currently runs on EC2 via systemd; being migrated to the internal Kubernetes platform per the [K8s Migration Runbook](runbook.md).

## Layout

- `src/` — Flask app, request handlers, DB layer
- `requirements.txt` — Python deps
- `systemd/billing-api.service` — current VM deployment unit
- `runbook.md` — team-wide K8s migration runbook (source of truth)
- `k8s/` — manifests added during the migration (one PR per resource)

## Migration status

| Artifact | PR | Runbook section |
| --- | --- | --- |
| Dockerfile | #1 | §1 |
| Deployment | #2 | §3.2, §4.1, §5 |
| Service + Ingress | #3 | §6 |
| ExternalSecret | #4 | §7 |
| HPA + PodDisruptionBudget | #5 | §8 |
