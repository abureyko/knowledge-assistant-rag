---
doc_id: guide-deploy-feature-flags
title: Feature flag rollout guide
doc_type: guide
topic: deployments
updated_at: 2026-04-09
source: internal://guide/deployments/feature-flags
---
# Feature flag rollout guide

## Purpose

Feature flags let teams release code separately from customer exposure. They are required for risky user-facing changes, billing behavior changes, and integrations that call external systems.

Small internal UI changes do not require a flag unless rollback would require a new deployment.

## Rollout stages

Start with internal users, then enable the flag for one pilot customer, then expand to five percent, twenty-five percent, and one hundred percent of eligible workspaces.

Each stage should run for at least one business day unless the change is a hotfix approved by the incident commander.

## Guardrails

Every production flag must have an owner, a rollback plan, and an expiry date. Flags older than ninety days are reviewed during deployment hygiene cleanup.

Monitor error rate, latency, billing events, and support tickets during rollout. If error rate increases by more than one percentage point over baseline, pause the rollout and notify the owning team.

## Cleanup

After a flag reaches one hundred percent for seven days without incidents, remove the dead code path and close the rollout ticket.
