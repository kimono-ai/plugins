---
name: build-kimono-agents
description: Create, inspect, edit, test, publish, unpublish, or delete Kimono agents through the canonical Builder. Use when the user wants to change an agent's behavior, build a new agent, test a draft, publish a verified draft, retire an agent, or inspect how an agent is configured.
---

# Build Kimono Agents

Resolve the exact agent before making changes with `agents_resolve`. Use
`agents_capabilities` to establish the current runtime identity, effective
permissions, and blockers. When the write scope is available, use
`agents_draft_get` to read the structured draft. These are the current MCP tool
names; use the names returned by the server's catalog exactly.

The user's current platform permissions, matching OAuth scopes, and resource
access govern execution. Tool discovery alone does not establish permission;
reconnecting cannot override a denied platform permission.

## Create or edit

- Use `agents_create` for a new agent and retain the returned agent and Builder
  thread IDs.
- To work conversationally on an existing agent, call `agents_builder_open`
  with its ID, then use the returned Builder thread with `turns_submit` and
  poll `turns_get` until terminal. This opens a new session and requires the
  current OAuth scope and edit access to that agent; continue with the returned
  thread instead of opening another session for each message.
- Use `agents_draft_patch` for typed blueprint changes and
  `agents_workflow_patch` for workflow changes. Read the current draft first
  and send its `baseRevision`; these tools reject stale concurrent edits.
- Use `agents_validate` and `agents_diff` after an edit, then read the draft
  again to verify the resulting state. These operations do not publish it.

When the requested change uses a Corpus, check authorized access separately
from the Agente's workflow configuration. `corpus_agent_access_list` and
`corpus_agent_access_grant` use the Agente-oriented Builder entrypoint and its
extra permissions. A grant alone does not add a Corpus to the workflow or
publish the Agente. Use `manage-kimono-corpora` for Corpus lifecycle, source
administration, source-bound file uploads, and the visible Corpus grant set.

## Test

- Use `agents_preview` with a representative prompt and the intended
  `sourceKind` when the user wants to test a draft or published version.
- Poll `turns_get` with the returned identifiers until terminal and compare the
  final response with the user's acceptance criteria.
- Iterate through the structured draft patch tools when the preview does not
  satisfy the goal.

## Publish or retire

- Never publish, unpublish, or delete from an inferred intent.
- Proceed when the user has already explicitly authorized the exact agent and
  effect. Summarize the concrete change before execution; ask for confirmation
  only when the target or effect is not authorized. A host's mandatory tool
  approval remains separate from conversational authorization.
- Use `agents_publish` with the current `expectedSourceHash`,
  `expectedPublishedVersionId`, and `confirm: true`.
- Use `agents_unpublish` with the current `expectedName` and `confirm: true`.
- Use `agents_delete` with the current `expectedName` and `confirm: true`;
  set `forceDeleteDefault: true` only when the user explicitly confirms
  deletion of a default agent.
- Treat deletion as irreversible.

Do not bypass the Builder by editing raw storage, prompts, workflows, or
versions through another integration.

## Recover a failed edit

- `No approval received` without a Kimono error envelope suggests a host
  approval failure; the wording alone does not prove its origin or that Kimono
  received a call. Check the host's approval state and use any server diagnostic
  IDs to establish execution before claiming a rejection or applied edit.
- On transport failure, response-contract failure, or an error with unknown
  mutation outcome, read `agents_draft_get` and `agents_diff` before retrying.
  Compare the current draft and revision with the intended patch. If it was
  applied, verify it; otherwise use the current `baseRevision` for any remaining
  change. Never blindly resend a non-idempotent patch.
- Preserve the returned `code`, `requestId`, `operationId`, and `deploymentId`
  for troubleshooting. Follow `recovery` and `phase` when present; wait
  `retryAfterSeconds` for a retryable read. `reconcile_before_retry` requires
  reading the affected state before resubmission. A generic failure is not
  evidence of a size limit or rate limit.
