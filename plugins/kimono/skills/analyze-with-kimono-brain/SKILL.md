---
name: analyze-with-kimono-brain
description: Ask the Kimono Brain to analyze organization-authorized usage, users, agents, conversations, adoption, or recent activity. Use when the user requests organizational metrics, investigation, comparisons, trends, or evidence that an administrator could obtain through the Kimono Brain.
---

# Analyze with Kimono Brain

Use Brain as the analyst; do not invent organizational facts from plugin
metadata or prior chat context.

1. Resolve `Brain` with `agents.resolve`, preferring a published agent that the
   user can start a chat with. Ask the user to choose if multiple candidates
   remain.
2. Continue a Brain conversation only when the user refers to prior analysis or
   context. Otherwise create a new private conversation with a specific title.
3. Submit the full analytical request, preserving dates, timezone, comparison
   windows, filters, and requested output format. Ask Brain to state data gaps
   rather than estimate unavailable values.
4. Poll `turns.get` until the logical turn is terminal.
5. Present Brain's final answer faithfully. Keep caveats, coverage windows, and
   ambiguity explicit.

The authenticated Kimono account fixes the organization boundary. Never ask
for or supply another organization ID. If Brain reports denied or unavailable
data, explain the limitation instead of attempting another data path.
