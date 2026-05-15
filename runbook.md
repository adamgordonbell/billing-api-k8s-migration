# Kubernetes Migration Runbook

How we move VM-based services onto the internal Kubernetes platform. This is the source of truth. Every migration PR cites the section it implements.

## 1. Containerization

- Base image: `python:3.12-slim` (or distroless for compiled services)
- Multi-stage builds for any compiled dependencies
- Non-root user (`appuser`, UID 10001)
- `.dockerignore` to keep the image lean (exclude `tests/`, `.venv`, `.git`)
- One process per container; no init system

## 2. Image registry

- Push to internal ECR (`<account>.dkr.ecr.us-east-1.amazonaws.com`)
- Tag with the git SHA, never `latest`
- Sign with cosign on the release branch

## 3. Deployment manifest

### 3.1 Naming

- `app.kubernetes.io/name` — the service (`billing-api`)
- `app.kubernetes.io/instance` — `<service>-<env>`
- `app.kubernetes.io/version` — image tag (git SHA)

### 3.2 Labels

- `team` — owning team handle (e.g., `payments`)
- `env` — `dev` / `staging` / `prod`
- `cost-center` — finance code

Network policies and Datadog routing key off these. Skipping them breaks both.

## 4. Resources

### 4.1 Baselines

- CPU: request `100m`, limit `500m`
- Memory: request `128Mi`, limit `512Mi`

Tune from p95 production metrics after one week. Document the change in the service's stack README.

## 5. Probes

- **Readiness**: `GET /health` — initial delay 5s, period 10s
- **Liveness**: `GET /health` — initial delay 30s, period 30s
- **Startup**: only add for services with boot >15s

## 6. Networking

### 6.1 Service

- `ClusterIP` unless explicitly external
- Port matches the container port; no rename

### 6.2 Ingress

- `nginx-ingress` class
- TLS via cert-manager `Issuer: letsencrypt-prod`
- Host: `<service>.<env>.internal`

## 7. Secrets

- External Secrets Operator (ESO)
- `ExternalSecret` references AWS Secrets Manager paths (`prod/<service>/*`)
- ESO renders into a `Secret`, consumed by the Deployment via `envFrom`
- Never bake secrets into env vars in the manifest

## 8. Autoscaling and resilience

### 8.1 HPA

- Target 60% CPU
- `minReplicas: 2`, `maxReplicas: 8` (raise if the service is fronted by a queue)

### 8.2 PodDisruptionBudget

- `minAvailable: 1` for every service
- Required before any node drain; without it, drains fail closed
