---
doc_id: runbook-deploy-hotfix
title: Production hotfix runbook
doc_type: runbook
topic: deployments
updated_at: 2026-04-11
source: internal://runbook/deployments/hotfix
---
# Production hotfix runbook

## When to use

Use the hotfix runbook for a production issue that cannot wait for the standard deployment train. Typical cases include severity 1 incidents, broken checkout flow, security patches, or a deployment blocker that affects multiple enterprise customers.

Do not use a hotfix for planned feature launches or cosmetic defects.

## Approval

The incident commander approves severity 1 hotfixes. For severity 2 issues, the engineering manager and on-call owner approve the hotfix. Security patches also require security engineering approval.

Hotfixes may run outside the Tuesday 02:00 to 04:00 UTC maintenance window when the incident commander approves the exception.

## Steps

1. Create a hotfix branch from the current production tag.
2. Apply the smallest safe change.
3. Run unit tests, smoke tests, and the affected integration test.
4. Deploy to one region.
5. Watch health checks for ten minutes.
6. Continue rollout or roll back using the rollback runbook.

## After rollout

Create a follow-up ticket to merge the hotfix back into the main branch. The owner must attach the incident link and test evidence.
