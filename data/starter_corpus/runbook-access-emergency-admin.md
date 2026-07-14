---
doc_id: runbook-access-emergency-admin
title: Emergency admin access runbook
doc_type: runbook
topic: access
updated_at: 2026-04-05
source: internal://runbook/access/emergency-admin
---
# Emergency admin access runbook

## When to use

Use emergency admin access only when a severity 1 or severity 2 incident requires immediate privileged action and the normal SSO or MFA flow is unavailable.

The runbook is not a shortcut for forgotten passwords, travel issues, onboarding delays, or routine permission requests. Those cases stay in the access portal.

## Approval

The incident commander and the on-call security engineer must approve emergency admin access. The approval is recorded in the incident timeline before access is granted.

Emergency access expires after four hours. A longer period requires a new approval entry and a reason from the incident commander.

## Steps

1. Confirm the incident severity and bridge link.
2. Create an emergency access ticket.
3. Grant the smallest required admin role.
4. Record the operator, role, start time, and expiry time.
5. Revoke access when the action is complete.

## After the incident

Security reviews the audit log within one business day. Any action outside the approved scope is treated as a separate access incident.
