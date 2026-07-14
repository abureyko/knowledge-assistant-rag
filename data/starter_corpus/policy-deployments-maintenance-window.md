---
doc_id: policy-deployments-maintenance-window
title: Maintenance window policy
doc_type: policy
topic: deployments
updated_at: 2026-02-22
source: internal://policy/deployments/maintenance-window
---
# Maintenance window policy

## Standard window

Customer-visible maintenance is scheduled on Tuesdays between 02:00 and 04:00 UTC.

The standard window applies to database migrations, search index rebuilds, and network changes that may create visible latency or short read-only periods. Regular application deploys can happen outside this window if they are backward compatible and use progressive rollout.

## Exceptions

Emergency security patches may be deployed outside the standard window with approval from the incident commander.

Hotfixes for active severity 1 incidents may also bypass the standard window, but the hotfix runbook must be followed. Planned feature launches do not qualify as exceptions even when a customer is waiting for the feature.

## Notifications

Support must notify affected customers at least twenty-four hours before planned maintenance.

Notifications must include the expected impact, start time, end time, and rollback contact. If the maintenance affects only preview or sandbox environments, a public customer notification is not required.

## Change freeze

During billing close, production maintenance that affects invoice calculation is frozen from the last calendar day of the month until the third business day of the next month.
