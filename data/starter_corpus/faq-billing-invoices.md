---
doc_id: faq-billing-invoices
title: Billing and invoices FAQ
doc_type: faq
topic: billing
updated_at: 2026-03-07
source: internal://faq/billing/invoices
---
# Billing and invoices FAQ

## When are invoices generated?

Invoices are generated on the first calendar day of each month for the previous billing period. The billing job starts at 03:00 UTC and usually finishes within two hours.

If usage data arrives late, finance can rerun invoice calculation until the third business day of the month. After invoices are sent to customers, corrections must follow the invoice correction runbook.

## Where can customers download invoices?

Customers can download invoices from the billing portal under Settings -> Billing -> Documents.

The portal shows the invoice PDF, line-item CSV, payment status, and account credit balance. Only workspace owners and billing administrators can download documents.

## How are refunds processed?

Approved refunds appear as account credits on the next invoice unless finance manually issues a bank transfer.

Refunds above five thousand dollars require approval from finance leadership. Support should not promise refund timing until finance confirms whether the refund will be a credit or a transfer.

## Missing invoice checklist

1. Confirm that the customer account is active.
2. Check whether the billing job completed for the account.
3. Verify that the requester has billing administrator permissions.
4. Escalate to finance if the document is still missing after the third business day.
