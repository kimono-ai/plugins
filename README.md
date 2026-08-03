# Kimono plugins

Official public plugin packages for ChatGPT and Codex. The packages in this
repository contain manifests, skills, and public assets. Kimono's hosted MCP
server and product implementation remain in the private Kimono platform.

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

## Available plugin

- [`kimono`](./plugins/kimono): interact with accessible agents, continue or
  start conversations, analyze organization activity with Brain, and operate
  the canonical agent Builder.

## Security and support

- [Privacy policy](https://usekimono.ai/privacy)
- [Terms of service](https://usekimono.ai/terms)
- Support: [support@usekimono.ai](mailto:support@usekimono.ai)

Non-secret preparation material for the OpenAI public directory is kept under
[`submission/`](./submission). Reviewer credentials are never stored in this
repository.

Licensed under the [Apache License 2.0](./LICENSE).
