---
doc_id: release-note-billing-april-2026
title: April 2026 billing release notes
doc_type: release_note
topic: billing
updated_at: 2026-04-18
source: internal://release-notes/billing/2026-04
---
# April 2026 billing release notes

## New features

Billing administrators can now export invoice line items as CSV directly from the billing portal. The export includes product area, usage unit, quantity, unit price, credits, and tax amount.

Enterprise accounts can also enable proactive usage warnings at sixty percent when the order form requests customer success outreach.

## Fixes

The invoice PDF now shows account credits before tax calculation. Previously, some customers saw credits only in the CSV export, which created confusion during dispute review.

The monthly billing job now records a separate status for late usage imports. This helps finance decide whether to rerun invoice calculation before invoices are sent.

## Operational notes

Support should use the invoice correction runbook when a customer reports a generated invoice with missing credits. If the invoice is not generated yet, ask finance whether the billing job should be rerun.
