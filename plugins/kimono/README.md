# Kimono

The Kimono plugin connects ChatGPT, Codex, and Claude Code to the hosted Kimono
MCP endpoint at `https://mcp.usekimono.ai/mcp`.

Authentication uses the Kimono OAuth flow. Every tool call re-enters Kimono's
canonical authorization boundaries, preserving the authenticated user's
organization, role, and resource ACLs.

## Product terms and workflows

| Product surface | Bundled skill | Use |
| --- | --- | --- |
| Agente | `use-kimono-agents` | Start, continue, and inspect conversations. |
| Agente Builder | `build-kimono-agents` | Create, edit, test, publish, and retire agents. |
| Brain | `analyze-with-kimono-brain` | Analyze operational organization data: usage, people, conversations, and adoption. |
| Corpus and Intelligence Layer | `use-kimono-intelligence-layer` | Search authorized sources and institutional information; manage explicit proposals and discussions. |
| Corpus | `manage-kimono-corpora` | Create, edit, archive, manage manual-upload or Google Drive sources and files, and grant or revoke Agente access. |
| Intelligence Layer and project sources | `ingest-kimono-sources` | Send events and documents and verify their processing and search availability. |

Corpus, Intelligence Layer, and Agente are the same product concepts in the
platform and MCP. A Corpus contains sources; an Agente can use an attached
Corpus, and an authorized MCP host can query it directly. Brain's operational
analytics workflow does not own source ingestion or Intelligence Layer
governance.

## Corpus management

Version **0.4.0** uses the matching server's `corpus_*` tools for Corpus
administration. Read access uses **Consultar a Intelligence Layer**; management
also uses **Gerenciar a Intelligence Layer**, the corresponding OAuth scopes,
and resource authorization. These are permissions for the organization's
existing roles, including custom roles; access does not require platform screens.

Corpus administration includes creating, renaming, describing, and archiving;
manual-upload and Google Drive source management; per-file inventory and
processing retry; and Agente grants. Archival revokes the Corpus's accesses
and retains its records. Disabling a source starts revoking its content and
stops its synchronization.
An Agente grant and configuring or publishing that Agente's workflow are
separate operations; Builder permissions continue to govern configuration.

Google Drive selection uses the Google account already connected to Kimono.
Folder discovery and new or changed roots require live authorization; existing
source synchronization follows its configured connection. Only that connection's
owner can browse the existing source's folders. MCP does not import
host Drive credentials or expose S3 configuration.

Upload Corpus files through a `manual_upload` source with
`corpus_upload_prepare` → signed PUT → `corpus_upload_finalize`. Supplying
`targetSpaceId` to a generic ingestion session does not, by itself, register
the upload in a Corpus source's file inventory. Read the inventory and verify
current search and evidence before reporting availability.

Use the returned `accessGeneration`, `syncGeneration`, or `processingVersion`
for the corresponding mutation. On conflicts or unknown outcomes, read the
current resource and reconcile the request before retrying. Agent grant
replacement submits the intended complete active visible grant list; preserve
active grants the user did not ask to revoke and keep revoked grants inactive
unless reactivation was requested. Existing explicit user authorization for the
target and effect is sufficient for required confirmation fields.

Update the local plugin and refresh the remote catalog independently. These
workflows become available when the matching Core and MCP release is deployed;
an installed skill alone does not prove server availability or authorization.

## Access and authorization

Every operation must satisfy three boundaries:

1. the OAuth scopes granted to this MCP connection;
2. organization MCP permissions configured under **Configurações → MCP →
   Permissões** for the user's existing role, including custom roles;
3. the ACL of the specific agent, conversation, Corpus, or destination.

The server filters the catalog by organization MCP permissions. The catalog
size is a server maximum, not a promise that every user receives every tool.
`identity_whoami` reports the connection's identity and scopes; it does not
prove access to every operation. Platform screen visibility is independent of
headless MCP access.

`KIMONO_MCP_INSUFFICIENT_SCOPE` calls for additional OAuth consent.
`MCP_PERMISSION_DENIED` requires an organization permission change by an
authorized administrator. A resource access denial requires the matching ACL;
reconnecting does not bypass either permission boundary.

Publishing, unpublishing, deletion, cancellation, source revocation, and
proposal decisions require explicit user intent for the target and effect.
An existing explicit request for that same action is sufficient; do not ask
for repetitive conversational confirmation. A host may still require tool
approval independently.

## Search and ingestion

`knowledge_search` defaults to `current`: published document evidence and
accepted current semantic information. `knowledge` searches accepted semantic
nodes only; `sources` is for explicit historical evidence investigations.
Documents are evidence and do not automatically become accepted facts. Retain
returned IDs, revisions, and processing versions when citing sources.

An accepted event, successful signed upload, finalized attachment, and sealed
session represent separate stages. `context_ingest_session_status` reports the
session. `context_ingest_artifact_status` takes `sessionId` and `artifactId` and
reports each institutional artifact's state, processing job, and semantic
interpretation separately. Check every attachment independently from the JSONL
artifact produced when an institutional session is closed.

`publicationRecorded` is a persisted receipt; verify actual availability with
a `current` search and evidence read. Document extraction and publication
precede optional later semantic interpretation by the organization's heartbeat.
A search error is not normal heartbeat lag. Project-targeted sessions use the
project-file destination and can return null artifact and job IDs on close;
preserve their individual file results.

## Error recovery

Kimono errors retain `code`, `message`, and correlation IDs when available.
The newer contract also exposes `phase` and `recovery`, with
`retryAfterSeconds` for capacity delays:

| Recovery | Action |
| --- | --- |
| `retry_read` | Wait the reported delay before retrying the read. Stop repeated failures and retain diagnostic IDs. |
| `reconcile_before_retry` | Read the affected resource and establish whether the mutation took effect before resending. |
| `reauthorize` | Complete the required OAuth authorization for the connection. |
| `check_permissions` | Check organization MCP permissions and the resource ACL. |
| `refresh_state` | Read the current resource revision before applying the intended change. |
| `investigate` | Preserve the error and diagnostic IDs instead of inventing a cause or repeating blindly. |

For an uncertain `agents_draft_patch`, read `agents_draft_get` and
`agents_diff`. Verify an already applied change or submit the remaining change
with the current `baseRevision`; never blindly resend the old patch.

`No approval received` without a Kimono error envelope suggests the host's
approval flow. Its wording alone does not prove where the failure occurred or
whether Kimono received a call. Check host approval and retain any returned
`requestId`, `operationId`, and `deploymentId` for execution tracing. Do not
label an unexplained error as a payload size limit or rate limit.

## Host manifests

- `.codex-plugin/plugin.json` packages the plugin for ChatGPT and Codex.
- `.claude-plugin/plugin.json` packages the same skills and MCP connection for
  Claude Code.

Both manifests intentionally point at the same `skills/` and `.mcp.json`
boundaries so behavior and authorization cannot drift between hosts. The
Claude directory submission is maintained separately from the curated official
marketplace; follow the current Anthropic submission form when listing the
plugin.
