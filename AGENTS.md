# AGENTS - Kimono plugins

This public repository is the distribution boundary for Kimono plugins used by
ChatGPT and Codex.

- Keep runtime implementation, infrastructure, credentials, customer data,
  internal endpoints, and operational runbooks out of this repository.
- Plugin packages may contain public manifests, MCP connection metadata,
  skills, documentation, and brand assets only.
- The hosted Kimono MCP server remains the sole execution boundary; skills
  must use its published tools instead of inventing direct API or storage
  access.
- Preserve OAuth least privilege and the authenticated Kimono organization
  boundary in every workflow.
- Increment the plugin semantic version for released package changes.
- Run `python scripts/validate.py` before commit.
