---
doc_id: policy-access-sso
title: Single sign-on policy
doc_type: policy
topic: access
updated_at: 2026-02-28
source: internal://policy/access/sso
---
# Single sign-on policy

## Scope

All full-time employees must authenticate through the corporate SSO provider. Shared credentials are prohibited.

Contractors with access to internal dashboards must also use corporate SSO unless a vendor agreement requires a separate identity provider. In that case, the vendor identity provider must still enforce MFA.

## Exception process

Service accounts may bypass SSO only after approval from security engineering and must be documented in the quarterly access review.

Human users cannot bypass SSO for convenience, travel, or local development. If SSO is unavailable during an incident, use the emergency admin runbook and record the reason in the incident timeline.

## Session duration

Interactive sessions expire after twelve hours and require re-authentication.

Privileged actions such as production deployment, billing export, and incident severity changes require step-up authentication if the previous MFA challenge is older than two hours.

## Access review

Managers review SSO group membership every quarter. Access that does not have a named owner, active ticket, or business reason is removed during the review.
