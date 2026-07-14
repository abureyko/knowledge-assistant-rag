---
doc_id: policy-security-data-retention
title: Security data retention policy
doc_type: policy
topic: security
updated_at: 2026-04-06
source: internal://policy/security/data-retention
---
# Security data retention policy

## Audit logs

Production audit logs are retained for four hundred days. Security incident audit exports are retained for seven years because they may be needed for legal review.

Sandbox audit logs are retained for ninety days unless they are attached to an incident record.

## Secrets and evidence

Leaked secrets should be revoked immediately, but evidence of the leak must be preserved until the incident commander approves cleanup. Evidence can include commit hashes, ticket links, screenshots, and provider audit events.

Do not paste raw secrets into incident notes. Use redacted values and attach provider evidence when possible.

## Customer data

Customer data must not be copied into tickets, chat messages, or local files during investigation. If a reproduction requires customer data, create a sanitized fixture and store it in the approved evidence bucket.

## Deletion requests

Legal deletion requests are handled by privacy operations. Engineering teams should not manually delete audit logs or billing records without written approval from privacy operations.
