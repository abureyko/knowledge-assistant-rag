---
doc_id: guide-access-sandbox
title: Sandbox access guide
doc_type: guide
topic: access
updated_at: 2026-03-13
source: internal://guide/access/sandbox
---
# Sandbox access guide

## Request flow

Developers request sandbox access through the internal access portal and must attach the related ticket number.

The request should include the environment name, expected duration, and a short reason. Requests without a ticket number are returned automatically because the access review cannot connect them to project work.

## Approval

The engineering manager approves requests for up to thirty days. Longer access requires security review.

Security review is also required when the sandbox can create API tokens, connect to external webhooks, or store customer-like test fixtures. The reviewer may reduce the requested duration if the work can be completed with narrower access.

## Limits

Sandbox environments do not contain production data and are reset every night.

Developers should not use sandbox systems for load testing, billing experiments, or long-running demos. Preview environments are a better fit for pull request review, while sandbox access is meant for development and integration testing.

## Revocation

Access expires automatically at the approved date. If the related ticket is closed earlier, the requester should remove their own access or ask the manager to revoke it from the access portal.
