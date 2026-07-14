---
doc_id: runbook-integrations-github-sync
title: GitHub sync troubleshooting runbook
doc_type: runbook
topic: integrations
updated_at: 2026-03-25
source: internal://runbook/integrations/github-sync
---
# GitHub sync troubleshooting runbook

## Symptoms

The sync service is degraded when repository webhooks are delayed for more than ten minutes or the retry queue grows above one thousand jobs.

Customers may report missing pull request links, delayed deployment previews, or stale commit status in the dashboard. These symptoms usually indicate webhook delivery delay rather than data loss.

## Investigation

Check recent webhook delivery failures, worker queue depth, and the token validity for the GitHub app installation.

If the retry queue is above one thousand jobs, do not restart workers immediately. First check whether GitHub is returning rate limit responses, whether the database migration lock is active, and whether the app installation token expired.

## Recovery

Restart the sync worker only after validating that the database migration lock is not active.

After restart, confirm that the retry queue decreases for ten consecutive minutes. If the queue keeps growing, scale workers by one replica and notify integrations engineering.

## Escalation

Escalate to severity 2 when sync delay affects production deployments or more than ten enterprise workspaces. Escalate to severity 3 when only preview environment links are delayed.
