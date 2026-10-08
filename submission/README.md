# Public directory submissions

The non-secret submission material lives in
[`openai-directory.json`](./openai-directory.json) and
[`anthropic-directory.json`](./anthropic-directory.json). These files keep the
directory listings, test cases, and review notes versioned alongside the public
plugin package.

## OpenAI

Before submitting a release through the OpenAI plugin portal:

1. deploy the matching MCP server version to `https://mcp.usekimono.ai/mcp`;
2. configure the portal-generated domain token as
   `OPENAI_APPS_CHALLENGE_TOKEN` and verify
   `/.well-known/openai-apps-challenge`;
3. scan the production tools and confirm the advertised annotations;
4. test all versioned cases in both ChatGPT and Codex;
5. record a short HTTPS-hosted demo covering the advertised agent, Brain,
   Corpus, Intelligence Layer, and ingestion workflows;
6. enter reviewer credentials only in the portal—never commit them here;
7. after the MCP connection is registered, add its `asdk_app...` identifier in
   `plugins/kimono/.app.json` and reference it from the plugin manifest.

The reviewer account must be isolated demo data, require no MFA or email/SMS
verification, and have only the minimum Kimono permissions needed by the test
cases.

## Anthropic Claude plugin directory

Before selecting **Submit for review** in Anthropic's current Claude plugin
directory form:

1. run `claude plugin validate . --strict` from the repository root;
2. add the local marketplace and install `kimono@kimono`;
3. confirm all six namespaced skills are discoverable;
4. authenticate the plugin-provided `kimono` MCP server through `/mcp`;
5. exercise a conversation, Brain request, and Corpus search with a restricted
   test user, then validate explicitly authorized Builder, Corpus management,
   and ingestion writes;
6. confirm the listing still matches `anthropic-directory.json`.

Third-party approvals are reviewed for the community marketplace; the curated
official marketplace is a separate Anthropic program. Do not submit when
manifest validation, MCP OAuth, tool discovery, or the representative
functional checks are incomplete.
