---
doc_id: faq-access-mfa
title: Multi-factor authentication FAQ
doc_type: faq
topic: access
updated_at: 2026-03-11
source: internal://faq/access/mfa
---
# Multi-factor authentication FAQ

## Who must enable MFA?

All employees, contractors, and temporary support partners with dashboard access must enable multi-factor authentication before receiving production permissions. MFA is also required for sandbox access when the account can create API tokens, view customer metadata, or trigger deployment actions.

New hires have a seven-day grace period for non-production systems, but production dashboards are blocked until MFA is active. Managers cannot approve an exception without security engineering review.

## Which methods are supported?

The identity provider supports authenticator apps, platform passkeys, and hardware security keys. Hardware security keys are recommended for production operators, incident commanders, and finance administrators.

SMS codes are allowed only as a temporary recovery method. They must not be used as the primary factor for accounts with billing, deployment, or security incident permissions.

## What happens if MFA is not enabled?

Accounts without MFA lose access to the admin dashboard after the seven-day grace period.

If access is blocked, the user should complete enrollment in the identity provider and then sign out and sign in again. If the account is needed for an active incident, follow the emergency admin runbook instead of asking support to bypass MFA.

## Recovery notes

Lost devices are handled through the access portal. The user must provide the related ticket number and confirm their manager. Security engineering can issue a temporary recovery code that expires after eight hours.
