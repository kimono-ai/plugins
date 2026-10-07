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

For installation and authorization instructions for other MCP hosts, use the
[Kimono installation guide](https://app.usekimono.ai/install.md).

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

- [`kimono`](./plugins/kimono): use and build Agentes, analyze operational
  organization data with Brain, search Corpora and the Intelligence Layer,
  and ingest source events and documents with processing verification.

## Update an installed plugin

The hosted MCP catalog and bundled skills update separately. A newer server
can expose tools while an older installed plugin still has outdated guidance.

In Codex, refresh the Git marketplace with
`codex plugin marketplace upgrade kimono`, then apply the available plugin
update in your host and start a new conversation to load the updated skills.
For Claude Code:

```bash
claude plugin update kimono@kimono
```

Run `/reload-plugins` in the active Claude session or restart it. Third-party
marketplaces do not auto-update by default; see
[Claude's update instructions](https://code.claude.com/docs/en/discover-plugins#keep-plugins-updated).

Refresh or reconnect the MCP catalog when published tool schemas change.
Additional OAuth consent is needed only for missing scopes; reconnecting does
not grant organization MCP permissions or resource access. See the
[plugin's access and recovery guidance](./plugins/kimono/README.md).

## Security and support

- [Privacy policy](https://usekimono.ai/privacy)
- [Terms of service](https://usekimono.ai/terms)
- Support: [support@usekimono.ai](mailto:support@usekimono.ai)

Non-secret preparation material for the OpenAI and Anthropic public directories
is kept under [`submission/`](./submission). Reviewer credentials are never
stored in this repository.

Licensed under the [Apache License 2.0](./LICENSE).
