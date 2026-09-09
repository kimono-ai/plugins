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

## Create or edit

- Use `agents_create` for a new agent and retain the returned agent and Builder
  thread IDs.
- Use `agents_draft_patch` for typed blueprint changes and
  `agents_workflow_patch` for workflow changes. Read the current draft first
  and send its `baseRevision`; these tools reject stale concurrent edits.
- Use `agents_validate` and `agents_diff` after an edit, then read the draft
  again to verify the resulting state. These operations do not publish it.

## Test

- Use `agents_preview` with a representative prompt and the intended
  `sourceKind` when the user wants to test a draft or published version.
- Poll `turns_get` with the returned identifiers until terminal and compare the
  final response with the user's acceptance criteria.
- Iterate through the structured draft patch tools when the preview does not
  satisfy the goal.

## Publish or retire

- Never publish, unpublish, or delete from an inferred intent.
- Before calling the tool, summarize the exact agent, current status, and
  effect, then obtain explicit confirmation.
- Use `agents_publish` with the current `expectedSourceHash`,
  `expectedPublishedVersionId`, and `confirm: true`.
- Use `agents_unpublish` with the current `expectedName` and `confirm: true`.
- Use `agents_delete` with the current `expectedName` and `confirm: true`;
  set `forceDeleteDefault: true` only when the user explicitly confirms
  deletion of a default agent.
- Treat deletion as irreversible.

Do not bypass the Builder by editing raw storage, prompts, workflows, or
versions through another integration.
