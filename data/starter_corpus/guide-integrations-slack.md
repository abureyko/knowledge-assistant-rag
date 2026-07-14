---
doc_id: guide-integrations-slack
title: Slack integration guide
doc_type: guide
topic: integrations
updated_at: 2026-03-09
source: internal://guide/integrations/slack
---
# Slack integration guide

## Installation

Workspace admins install the Slack app from the integrations catalog and approve requested scopes.

The installer must choose the default notification channel and confirm whether deployment events, billing warnings, and security incidents should be enabled. Security incident notifications should go only to restricted channels.

## Supported notifications

The integration can send deployment updates, billing warnings, and incident notifications to selected channels.

Deployment updates include environment name, rollout status, and rollback links. Billing warnings include usage thresholds and invoice links. Incident notifications include severity, incident commander, and bridge status.

## Re-authentication

If the Slack token expires, the integration owner must reconnect it from Settings -> Integrations.

Re-authentication does not change channel routing. If notifications stop after reconnecting, check whether the Slack app was removed from the target channel or whether workspace admins restricted the requested scopes.

## Common mistakes

- Installing the app from a personal workspace instead of the company workspace.
- Sending production incident alerts to a public channel.
- Reconnecting with a user who does not have workspace admin permissions.
