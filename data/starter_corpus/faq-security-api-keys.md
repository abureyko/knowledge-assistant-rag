---
doc_id: faq-security-api-keys
title: API key security FAQ
doc_type: faq
topic: security
updated_at: 2026-03-16
source: internal://faq/security/api-keys
---
# API key security FAQ

## Where should API keys be stored?

API keys must be stored in the approved secrets manager. Keys must never be committed to Git repositories or pasted into tickets.

Local `.env` files are allowed for development only when they are ignored by Git. Shared demo keys must be distributed through a private channel and rotated after the access window closes.

## How often should keys be rotated?

Production API keys are rotated every ninety days or immediately after a suspected exposure.

Integration-specific webhook signing secrets rotate every one hundred eighty days unless the integration policy defines a shorter period. Service account credentials follow the service account access policy.

## What if a key leaks?

Revoke the key, rotate dependent credentials, and open a severity 2 security incident if the leak touched a production integration.

If the leak was limited to a sandbox key, create a security ticket, rotate the key, and record the repository or ticket where the exposure happened. Do not delete evidence until the incident commander confirms that audit logs were preserved.

## What counts as a secret?

API keys, refresh tokens, webhook signing secrets, database URLs with passwords, and LangSmith or LLM provider keys are treated as secrets. Masked examples such as `your_key_here` are allowed in documentation.
