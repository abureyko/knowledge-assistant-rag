---
doc_id: guide-deploy-preview
title: Preview environments guide
doc_type: guide
topic: deployments
updated_at: 2026-03-04
source: internal://guide/deployments/preview-environments
---
# Preview environments guide

## Purpose

Every pull request can request a preview environment for product review and QA validation.

Preview environments are intended for short-lived review. They should mirror production configuration where practical, but they must not connect to production databases, payment processors, or customer notification channels.

## Lifecycle

Preview environments are created automatically after CI succeeds and are deleted after the pull request is closed.

If a pull request stays open for more than fourteen days, the environment is paused overnight to reduce cost. The author can resume it from the deployment controller when review continues.

## Ownership

The author of the pull request owns the preview environment and is responsible for cleaning up extra data fixtures.

QA may add test fixtures, but ownership still stays with the pull request author. If the author leaves the project, the engineering manager must either assign a new owner or close the environment.

## Good review habits

- Use feature flags for risky behavior.
- Put test data in the preview database only.
- Link the preview URL in the pull request description.
- Delete manual fixtures before requesting final approval.
