# Kimono plugins

Official public plugin packages for ChatGPT, Codex, and Claude Code. The
packages in this repository contain host manifests, skills, MCP connection
metadata, and public assets. Kimono's hosted MCP server and product
implementation remain in the private Kimono platform.

## Install from ChatGPT or Codex

Add this Git marketplace:

- Source: `kimono-ai/plugins`
- Git ref: `main`
- Sparse paths: leave empty

From the Codex CLI:

```bash
codex plugin marketplace add kimono-ai/plugins --ref main
codex plugin add kimono@kimono
```

After installation, authenticate with your Kimono account. Kimono derives the
organization and effective permissions from that account; the plugin cannot
select or cross organization boundaries.

## Install from Claude Code

Add the public Kimono marketplace and install the plugin:

```bash
claude plugin marketplace add kimono-ai/plugins
claude plugin install kimono@kimono
```

Restart Claude Code or run `/reload-plugins`, then open `/mcp` and authenticate
the `kimono` server with your Kimono account. To distribute the package through
Anthropic's Claude plugin directory, use the current Claude.ai or Console
submission form. Approved third-party plugins enter the community marketplace;
Anthropic's curated official marketplace is separate.

## Available plugin

- [`kimono`](./plugins/kimono): interact with accessible agents, continue or
  start conversations, analyze organization activity with Brain, and operate
  the canonical agent Builder.

## Security and support

- [Privacy policy](https://usekimono.ai/privacy)
- [Terms of service](https://usekimono.ai/terms)
- Support: [support@usekimono.ai](mailto:support@usekimono.ai)

Non-secret preparation material for the OpenAI and Anthropic public directories
is kept under [`submission/`](./submission). Reviewer credentials are never
stored in this repository.

Licensed under the [Apache License 2.0](./LICENSE).
