---
name: use-kimono-agents
description: Start, continue, inspect, or manage conversations with agents available to the authenticated Kimono user. Use when the user asks a Kimono agent a question, refers to an existing Kimono conversation, wants to find an agent, or asks one agent to handle a task.
---

# Use Kimono Agents

Preserve the user's language and intent. Treat agent names and conversation
titles as human labels that require resolution.

Use the tools visible to the connected user. Organization MCP permissions for
the user's role, OAuth scopes, and each agent or conversation's ACL all apply.
Do not infer MCP access from the visibility of a platform screen.

1. Call `agents_resolve` with the user's name or description.
2. If resolution is ambiguous, show the compact candidates and ask the user to
   choose. Never select by recency or fuzzy rank alone.
3. If the user explicitly wants a new conversation, call `threads_create` with
   the resolved agent ID.
4. If the user wants to continue, or their wording plausibly refers to prior
   context, call `threads_resolve` with the agent ID and available query terms.
   Ask whether to continue or start fresh when multiple conversations remain
   plausible. Use `threads_read` before claiming what a prior conversation
   contains.
5. Call `turns_submit` with the complete user request. Reuse a stable
   `idempotencyKey` when retrying the same submission.
6. Call `turns_get` with the returned identifiers until `terminal` is `true`.
   Do not treat an accepted submission or intermediate assistant text as the
   final answer.
7. Return the agent's final response and identify the conversation used when
   that helps the user continue later.

Do not cancel a turn unless the user explicitly asks to stop it. Do not expose
internal IDs unless needed for disambiguation or troubleshooting.

After an uncertain submission, reuse its original `idempotencyKey` and poll the
returned identifiers when available; do not send the same message as a new
submission. `No approval received` without a Kimono error envelope suggests a
host approval failure, but does not prove its origin or that Kimono received a
call. Preserve server diagnostic identifiers and follow the returned `phase`
and `recovery` when present.
