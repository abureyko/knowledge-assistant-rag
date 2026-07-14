---
doc_id: guide-integrations-webhooks
title: Webhook integration guide
doc_type: guide
topic: integrations
updated_at: 2026-04-08
source: internal://guide/integrations/webhooks
---
# Webhook integration guide

## Setup

Workspace admins create webhook subscriptions from Settings -> Integrations -> Webhooks. Each subscription needs a target URL, event type filter, signing secret, and owner.

The target URL must use HTTPS. Localhost, private IP ranges, and URLs with embedded credentials are rejected.

## Event filters

Subscriptions can receive all events or a smaller set such as deployment updates, billing warnings, incident updates, or GitHub sync changes. Narrow filters reduce noise and make retries easier to inspect.

Changing filters does not rotate the signing secret. Secret rotation is a separate action.

## Security

Every webhook request includes a timestamp and signature header. Consumers must reject requests with an invalid signature or a timestamp older than five minutes.

Signing secrets rotate every one hundred eighty days. Legacy webhook tokens stop working after June 30, 2026, so customers should migrate before that date.

## Delivery behavior

Failed deliveries are retried three times with exponential backoff. After the third failure, the subscription is marked degraded and appears in the integrations dashboard.
