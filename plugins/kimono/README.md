# Kimono

The Kimono plugin connects ChatGPT and Codex to the hosted Kimono MCP endpoint
at `https://mcp.usekimono.ai/mcp`.

Authentication uses the Kimono OAuth flow. Every tool call re-enters Kimono's
canonical authorization boundaries, preserving the authenticated user's
organization, role, and resource ACLs.

The bundled skills cover three workflows:

- conversations with Kimono agents;
- organization analysis through Brain;
- agent creation, editing, testing, publication, and retirement.

Write and destructive actions require the matching OAuth scope. Publishing,
unpublishing, deletion, and cancellation also require explicit user intent.
