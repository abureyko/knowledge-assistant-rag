---
doc_id: policy-access-service-accounts
title: Service account access policy
doc_type: policy
topic: access
updated_at: 2026-04-02
source: internal://policy/access/service-accounts
---
# Service account access policy

## Scope

Service accounts are non-human identities used by automation, integrations, and scheduled jobs. They must have a named owner, a business reason, and the narrowest permission set that allows the job to run.

Service accounts may bypass SSO only when security engineering approves the exception. They must still use scoped tokens or workload identity where supported.

## Ownership

Every service account must have one engineering owner and one backup owner. The owner is responsible for credential rotation, incident response, and quarterly access review.

If the owner leaves the company or changes teams, the account is disabled until a new owner is assigned. Shared ownership by a team name is not enough for production service accounts.

## Review and rotation

Production service account credentials rotate every ninety days. Sandbox service accounts rotate every one hundred eighty days.

Managers must confirm service account ownership during the quarterly access review. Accounts without confirmation are disabled within five business days.

## Prohibited use

Service accounts must not be used for interactive dashboard access, manual billing exports, or emergency admin actions. Human operators should use their own SSO account so audit logs stay attributable.
