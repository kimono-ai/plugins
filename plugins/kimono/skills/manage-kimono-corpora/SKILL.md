---
name: manage-kimono-corpora
description: Create, edit, archive, and manage Kimono Corpora, their manual-upload or Google Drive sources, files, and Agente access through MCP. Use for Corpus administration and source-bound uploads; use Intelligence Layer tools for questions or information proposals and Builder for configuring or publishing Agentes.
---

# Manage Kimono Corpora

Use the hosted Kimono MCP tools available to the connected user. A Corpus
contains sources and documents. Intelligence Layer search and Agente use
operate on those same authorized resources; Brain handles operational analytics.
Never use private APIs, storage credentials, or another organization's identity.

## Access and discovery

- Resolve the Corpus with `corpus_list`, then read `corpus_get` before changing
  it. Keep its `id`, `spaceId`, `accessGeneration`, sources, and capabilities.
  Use `spaceId` to scope `knowledge_search`; it is not interchangeable with
  `corpusId`.
- Reads require the OAuth grant and **Consultar a Intelligence Layer** under
  **Configurações → MCP → Permissões** for the user's existing role. Management
  also requires **Gerenciar a Intelligence Layer** and the corresponding write
  scope. Custom roles work through the same policy. Resource ACLs and Agente
  authorization still apply; platform screen visibility does not grant access.
- Use returned capabilities and visible tools to establish the available
  operation. Missing permission is not a reason to switch accounts or invent
  another execution path. Refresh the catalog after a policy or server update;
  OAuth consent changes only when scopes are missing.

## Corpus and sources

- Create with `corpus_create`; change name or description with `corpus_update`.
  Updates and `corpus_archive` require the current `expectedAccessGeneration`.
  Archiving revokes the Corpus's accesses and retains its records; it is not
  permanent deletion.
- Create a source with `corpus_source_create`, using a stable UUID
  `idempotencyKey` for that creation inside the nested `source` input alongside
  `type`, optional `name`, and Drive `roots` when applicable. Supported types are
  `manual_upload` and `google_drive`. Do not offer S3 configuration.
- For Google Drive, discover selectable roots with `corpus_drive_roots` and
  browse folders with `corpus_drive_children`. The tools use the user's Google
  account already connected to Kimono. Do not request Google tokens, upload
  host credentials, or substitute a Drive connector from another account.
  Creating or changing roots requires access to the selected folders through
  that connected account. Follow the returned root selection schema.
  Folder discovery requires both read and management MCP permissions and
  scopes. Omit both `corpusId` and `sourceId` to discover roots before creating
  a source; provide both to browse an existing authorized source. For children,
  preserve the returned `rootId`, `rootType`, and `driveId` when supplied.
  Browsing a source's folders is restricted to the owner of its configured
  Google account, even when another Corpus manager can synchronize that source.
- Read the source's `syncGeneration` before `corpus_source_update`; supply it
  as `expectedSyncGeneration` when changing Drive roots. Browse existing source
  folders only when authorized; discovery and an already configured source's
  synchronization are separate operations. Changing roots starts a new
  publication generation; inspect source and file state before reporting
  the refreshed content as available.
- Use `corpus_source_sync` to request synchronization, and
  `corpus_source_disable` or `corpus_source_resume` for the specified source.
  Disabling a source initiates revocation of that source's content and stops
  its synchronization; archiving affects the Corpus. Describe that selected
  effect. A sync request accepted or a job queued
  does not prove all documents have been published.

## Upload and verify files

For a file that must belong to a Corpus's inventory, choose or create its
`manual_upload` source and use the source-bound flow:

1. Call `corpus_upload_prepare` with `corpusId`, `sourceId`, and file metadata.
   Keep `sourceEventId` and `attachmentKey` stable for that upload.
   Preserve the returned session, receipt, expiry, URL, and required headers.
2. PUT the bytes to that exact signed URL with the declared MIME type and
   required headers. Keep signed URLs and receipt tokens private; binary data
   does not belong in MCP JSON.
3. Call `corpus_upload_finalize` with the same `corpusId`, `sourceId`, and
   returned `uploadToken`, preserving `sourceEventId` when provided. The signed
   receipt binds the canonical session; do not add a `sessionId` input to this
   tool. Retain the resulting artifact and job identifiers.
4. Inspect `corpus_source_files_list` or `corpus_files_list`. Track each file's
   processing version and failure independently. When a failed file is eligible
   for a retry, use `corpus_file_retry` with its current
   `expectedProcessingVersion`; requesting a retry is not proof of completion.
5. Verify actual availability with `knowledge_search` in the default `current`
   view scoped to the Corpus's `spaceId`, then `knowledge_evidence_read`.
   Preserve evidence IDs, revisions, and processing versions when reporting.

A generic ingestion session's `targetSpaceId` does not, by itself, register a
file under a Corpus source. Use `ingest-kimono-sources` for source event streams
or project-file sessions, and use this source-bound flow for Corpus inventory.
An uploaded or queued file, persisted publication, and successful search prove
different stages. Later semantic interpretation is separate from document
publication; a query failure is not normal heartbeat lag.

## Agente access

- For Corpus administration, read `corpus_get` for the selected Corpus's
  visible grants and eligible published Agentes. To grant, revoke, or replace
  access, start from visible grants with `active: true` and send the intended
  complete active list to
  `corpus_agent_grants_replace`. This operation replaces that list; do not
  omit active grants the user wanted to retain or reactivate revoked grants
  without that request. The Core preserves
  grants hidden by Agente authorization. Supply the current
  `expectedAccessGeneration`.
- `corpus_agent_access_list` and `corpus_agent_access_grant` are the separate
  Agente-oriented Builder entrypoints. They additionally require the Builder
  MCP permission and `agents:write`, plus authorization to edit that Agente.
  Do not use them to bypass the authorized Corpus administration workflow.
- A grant permits the Agente to access a Corpus. Configuring the Agente's
  workflow to use it and publishing that workflow are separate Builder
  operations with their own permissions. Do not report a grant as a completed
  Agente configuration or publication.

## Intent and recovery

The user's explicit request for a target and effect authorizes that action;
do not request the same decision at every step. Use `confirm: true` only for
the already authorized effect when the tool requires it. Ask only for missing
information that changes the target or effect. Host tool approval is separate.

On a generation conflict, reload the Corpus, source, or file and reconcile the
requested change with its current version. On `reconcile_before_retry` or an
uncertain write result, inspect the affected resource before resending. After
an uncertain creation, find the resource first to avoid duplicates; retain the
original source idempotency key and upload receipt. Do not blindly repeat sync,
retry, archival, grant replacement, or upload finalization.

For `retry_read`, wait the returned `retryAfterSeconds` before repeating a read;
stop repeated failures and preserve diagnostic IDs. An approval message without
a Kimono error envelope does not prove the server received the call. Report
what was accepted, persisted, processed, and verified separately.
