---
name: ingest-kimono-sources
description: Send authorized source events and document attachments to the Kimono Intelligence Layer or a specified project through Context Ingestion Sessions, and verify processing and search availability. Use Corpus management for source-bound Corpus file uploads and Drive configuration; use Intelligence Layer tools for queries and Brain for operational analytics.
---

# Ingest Kimono Sources

Use the hosted MCP ingestion tools. The host adapts the source to CloudEvents;
it does not access Kimono storage or private APIs. Resolve an authorized
destination and use only the catalog and schemas available to the connected
user. OAuth scopes, dynamic organization role MCP permissions, and destination
ACLs all apply. Do not derive write access from platform screen visibility.

For files that must appear in a Corpus's source inventory, use
`manage-kimono-corpora` and the `corpus_upload_prepare` → PUT →
`corpus_upload_finalize` flow with the selected `corpusId` and `sourceId`.
A generic session aimed at a Corpus's `targetSpaceId` publishes to that space;
it does not, by itself, register a file under one of the Corpus's sources.
Keep this skill for source event streams and project-file sessions.

## Send source events and attachments

1. Open a session with `context_ingest_session_open`, retaining its session ID
   and a stable `idempotencyKey` for the same operation. Use the returned Corpus
   or destination ID as `targetSpaceId`, or the explicitly requested project
   as `targetProjectId`; omission uses the organization destination.
2. Append JSON CloudEvents with `context_ingest_session_append` in batches of
   at most 100. Preserve `source`, event `id`, and original `time`; reusing the
   source and event ID deduplicates retries. Include at least one source event
   before closing an institutional session. Project sessions require
   `ai.kimono.source.file.snapshot` events, with `source` matching the session,
   `subject` as the source file ID, and `data: {name, revision}`. Follow returned
   `fileDecisions`: upload files requiring an add or update, and avoid duplicate
   uploads for unchanged or pending files.
3. For each document, call `context_ingest_attachment_prepare` with metadata.
   Upload bytes with a PUT to the exact returned signed URL: institutional
   attachments return `uploadUrl` and `requiredHeaders`; project files return
   `url` and a workspace receipt. Use required headers when provided and the
   declared file MIME type. Keep URLs and receipt tokens private; do not place
   binary content in MCP JSON. Respect expiry and do not forward credentials to
   an unrelated endpoint.
4. After a successful upload, call `context_ingest_attachment_finalize` with
   the returned receipt and source event ID. Retain each institutional
   `artifactId` and `deterministicJobId` independently; they are not the
   session's JSONL artifact. For project files retain the returned `fileId`,
   `documentId`, `jobId`, and `workflowId` instead of fabricating artifact IDs.
5. Close the session with `context_ingest_session_close`. An institutional
   session seals its event artifact and queues processing. A project-targeted
   session uses the project-file flow and may return null artifact and job IDs
   on close; preserve each attachment's project-file result.

Existing user authorization for the specified source and destination is
enough; ask only for a materially missing destination or effect. Host approval
requirements are separate.

## Verify the effect

Accepted events, an upload HTTP 200, a queued job, and a sealed session prove
different stages. Use `context_ingest_session_status` to inspect the session;
it does not prove every independently finalized attachment was processed.
Use `context_ingest_artifact_status` with its `sessionId` and `artifactId` for
each institutional attachment and the separate JSONL artifact returned on
close. It reports the artifact, processing job, and semantic interpretation
separately. `publicationRecorded` is a persisted publication receipt, not proof
that a current search succeeds. Retain failure codes and the artifact/job
diagnostic IDs rather than waiting indefinitely or uploading duplicates. If
the tool is absent, refresh the catalog and check the connected user's MCP
permissions; do not invent an endpoint or claim processing verification.

Document extraction and publication make document evidence searchable. Later
semantic interpretation through the organization's heartbeat is a separate
stage; it is not required before checking published document evidence with
`knowledge_search`'s default `current` view. Search within the authorized
destination and read the returned evidence. A 500 or capacity error is a failed
query, not normal heartbeat delay or proof that the upload failed.

Retry an idempotent operation with the original event IDs, keys, and receipt
when appropriate. For `recovery: "retry_read"`, wait `retryAfterSeconds` before
retrying a read. For `reconcile_before_retry` or an unknown mutation outcome,
read the session and artifact status before resending. `No approval received`
without a Kimono error envelope suggests a host approval failure; it does not
prove origin or server execution. Preserve `phase` and server diagnostic IDs
when present.
