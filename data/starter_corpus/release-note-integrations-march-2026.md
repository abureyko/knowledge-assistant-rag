---
doc_id: release-note-integrations-march-2026
title: March 2026 integrations release notes
doc_type: release_note
topic: integrations
updated_at: 2026-03-30
source: internal://release-notes/integrations/2026-03
---
# March 2026 integrations release notes

## New features

Slack notifications now support incident severity tags and deployment environment labels.

Webhook subscriptions can now filter by event type. Existing subscriptions continue to receive all events until an owner chooses a narrower filter.

## Fixes

The GitHub sync job now retries failed webhook deliveries three times before marking the sync as degraded.

The retry delay now uses exponential backoff instead of a fixed one-minute delay. This reduces repeated failures when GitHub or a customer endpoint is temporarily unavailable.

## Deprecations

Legacy webhook tokens will stop working after June 30, 2026.

Customers should migrate to signed webhook secrets before the deadline. The integrations catalog shows a warning banner for any workspace that still has a legacy token after May 15, 2026.

## Operational notes

The GitHub sync runbook has been updated with a new retry queue threshold. Operators should check queue depth before restarting workers because restarts can hide the original delivery failure.
