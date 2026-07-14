---
doc_id: runbook-security-incident
title: Security incident runbook
doc_type: runbook
topic: security
updated_at: 2026-03-21
source: internal://runbook/security/incidents
---
# Security incident runbook

## Severity assignment

Use severity 1 for active data exposure, severity 2 for unauthorized access without confirmed exfiltration, and severity 3 for suspicious but unconfirmed events.

If the incident involves leaked production API keys, start at severity 2 until investigation proves that the key was never used. If customer data is confirmed exposed, raise the incident to severity 1.

## Immediate actions

Page the on-call security engineer, open the incident bridge, and preserve relevant audit logs before rotating credentials.

The incident commander owns timeline updates. Engineering owners can rotate credentials, disable integrations, and block accounts, but they should not delete logs or close tickets until security approves.

## External communication

Only the incident commander or legal representative may approve customer-facing updates.

Support can acknowledge that an investigation is in progress, but must not share root cause, affected accounts, or remediation details before legal review.

## Evidence checklist

- Relevant audit logs are exported.
- Exposed credentials are revoked.
- Dependent credentials are rotated.
- Related Git commits, tickets, and screenshots are attached to the incident record.
