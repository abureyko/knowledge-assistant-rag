---
doc_id: runbook-deploy-rollback
title: Deployment rollback runbook
doc_type: runbook
topic: deployments
updated_at: 2026-03-19
source: internal://runbook/deployments/rollback
---
# Deployment rollback runbook

## Trigger conditions

Start the rollback procedure if the error rate exceeds two percent for five consecutive minutes or the checkout flow fails in production.

Rollback is also required when a database migration creates irreversible data corruption, when the incident commander declares a severity 1 customer impact, or when the deployment controller reports a failed health gate in two regions.

## Rollback steps

1. Pause the rollout in the deployment controller.
2. Promote the previous stable image tag.
3. Run the smoke test suite against the restored version.
4. Announce the rollback in the incident channel.

If the deployment included a database migration, stop after step 1 and contact the database owner before promoting the previous image. Some migrations require a forward fix instead of a rollback.

## After rollback

Create a post-incident ticket and attach the failing build identifier.

The ticket should include the rollback start time, restored version, smoke test result, and customer impact summary. If feature flags were involved, record which flags were disabled and who approved the change.

## Communication

Support should wait for the incident commander before sending customer-facing updates. Internal updates go to the incident channel every fifteen minutes until the rollback is complete.
