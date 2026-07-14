---
doc_id: runbook-billing-invoice-correction
title: Invoice correction runbook
doc_type: runbook
topic: billing
updated_at: 2026-04-04
source: internal://runbook/billing/invoice-correction
---
# Invoice correction runbook

## When to use

Use this runbook when an invoice was already generated and the customer reports incorrect usage, missing credits, wrong tax details, or a duplicate charge.

If the invoice has not been sent yet, rerun the monthly billing job instead of issuing a correction. Corrections are only for documents that customers can already see in the billing portal.

## Required information

Collect the invoice number, customer account id, disputed line item, expected amount, and the support ticket link. Finance cannot approve a correction without the original invoice number.

For usage corrections, attach the usage export that explains the difference. For tax corrections, attach the updated billing address or tax exemption certificate.

## Correction steps

1. Mark the invoice as under review in the billing portal.
2. Create a correction draft with the changed line items.
3. Ask finance to approve the draft.
4. Send the corrected invoice to the customer.
5. Record whether the customer receives a credit or a replacement invoice.

## Deadline

Standard corrections should be completed within five business days. High-value enterprise corrections above ten thousand dollars require finance leadership approval.
