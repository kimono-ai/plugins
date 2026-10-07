---
name: analyze-with-kimono-brain
description: Analyze authorized operational organization data with Kimono Brain, including usage, users, agents, conversations, adoption, and recent activity. Use for organizational metrics and investigations; use the Intelligence Layer skill for Corpus sources and institutional information.
---

# Analyze with Kimono Brain

Use Brain as the analyst; do not invent organizational facts from plugin
metadata or prior chat context.

Brain analyzes operational organization data. Corpus and the Intelligence
Layer have their own published tools; do not route source ingestion, source
search, or information governance through Brain. Use only tools exposed to the
connected user; OAuth consent does not override the organization's MCP
permissions for the user's role or resource ACLs.

1. Resolve `Brain` with `agents_resolve`, preferring a published agent that the
   user can start a chat with. Inspect the returned status and ask the user to
   choose if multiple candidates remain; never pick by rank alone.
2. Continue a Brain conversation only when the user refers to prior analysis or
   context. Use `threads_resolve` with the resolved agent ID and ask the user
   when more than one thread is plausible. Otherwise use `threads_create` for a
   new private conversation with a specific title.
3. Submit the full analytical request with `turns_submit`, preserving dates,
   timezone, comparison windows, filters, and requested output format. Reuse a
   stable `idempotencyKey` only when retrying the same submission. Ask Brain to
   state data gaps rather than estimate unavailable values.
4. Poll `turns_get` with the returned `threadId`, `submissionId`, and
   `userMessageId` until `terminal` is `true`. Do not treat an accepted run or
   intermediate text as the final answer.
5. Present Brain's final answer faithfully. Keep caveats, coverage windows, and
   ambiguity explicit.

The authenticated Kimono account fixes the organization boundary. Never ask
for or supply another organization ID. If Brain reports denied or unavailable
data, explain the limitation instead of attempting another data path.
