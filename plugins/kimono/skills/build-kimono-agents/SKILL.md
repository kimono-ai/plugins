---
name: build-kimono-agents
description: Create, inspect, edit, test, publish, unpublish, or delete Kimono agents through the canonical Builder. Use when the user wants to change an agent's behavior, build a new agent, test a draft, publish a verified draft, retire an agent, or inspect how an agent is configured.
---

# Build Kimono Agents

Resolve the exact agent before making changes. Use `agents.inspect` to establish
the current definition and effective permissions.

## Create or edit

- Use `agents.create` for a new agent and retain the returned agent and Builder
  thread IDs.
- Use `agents.edit` for an existing agent. State the intended outcome and
  constraints, not an unreviewed replacement prompt.
- Poll `turns.get` until the Builder turn is terminal, then inspect the agent
  again to verify the resulting draft.

## Test

- Use `agents.preview` with a representative prompt.
- Poll `turns.get` until terminal and compare the final response with the
  user's acceptance criteria.
- Iterate through `agents.edit` when the preview does not satisfy the goal.

## Publish or retire

- Never publish, unpublish, or delete from an inferred intent.
- Before calling the tool, summarize the exact agent, current status, and
  effect, then obtain explicit confirmation.
- Supply the current exact agent name and required confirmation fields.
- Treat deletion as irreversible. Do not set `forceDeleteDefault` unless the
  user explicitly confirms deletion of a default agent.

Do not bypass the Builder by editing raw storage, prompts, workflows, or
versions through another integration.
