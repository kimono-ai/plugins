# OpenAI directory submission

The non-secret submission material lives in
[`openai-directory.json`](./openai-directory.json). It keeps the five positive
cases, three negative cases, release notes, and tool-annotation justifications
reviewable alongside the public plugin package.

Before submitting a release through the OpenAI plugin portal:

1. deploy the matching MCP server version to `https://mcp.usekimono.ai/mcp`;
2. configure the portal-generated domain token as
   `OPENAI_APPS_CHALLENGE_TOKEN` and verify
   `/.well-known/openai-apps-challenge`;
3. scan the production tools and confirm the advertised annotations;
4. test all eight cases in both ChatGPT and Codex;
5. record a short HTTPS-hosted demo covering Brain, conversations, and Builder;
6. enter reviewer credentials only in the portal—never commit them here;
7. after the MCP connection is registered, add its `asdk_app...` identifier in
   `plugins/kimono/.app.json` and reference it from the plugin manifest.

The reviewer account must be isolated demo data, require no MFA or email/SMS
verification, and have only the minimum Kimono permissions needed by the test
cases.
