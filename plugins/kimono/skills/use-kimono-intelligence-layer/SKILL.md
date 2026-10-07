---
name: use-kimono-intelligence-layer
description: Search accessible Corpora and the Kimono Intelligence Layer, read source evidence, and manage explicit proposals or discussions. Use for institutional information and its governance; use Brain for operational organization metrics and the ingestion skill for uploading sources.
---

# Use Kimono Intelligence Layer

A Corpus contains sources. The Intelligence Layer exposes institutional
information and its evidence across authorized destinations. An Agente can use
an attached Corpus, and an MCP host can query an accessible Corpus directly.
Use those product terms instead of introducing Context Graph as another
user-facing feature.

Use only the tools in the connected server's catalog. Access requires OAuth
scopes, organization MCP permissions configured for the user's existing role,
and resource ACLs. Never supply another organization ID or bypass a denied
destination.

## Search and evidence

- Resolve the user's Corpus with `context_spaces_search`. Use returned IDs in
  `knowledge_search`'s `spaceIds` to keep a Corpus-specific question scoped.
- Prefer the default `view: "current"`: current accepted semantic information
  and published documents. `knowledge` limits results to accepted semantic
  nodes; `sources` is an explicit historical evidence investigation, not the
  default check for a newly uploaded document.
- Read relevant results with `knowledge_get` and `knowledge_evidence_read`.
  Preserve returned node and artifact IDs, `revisionId`, and
  `processingVersion` when attributing evidence. Documents are sources and do
  not automatically become accepted facts.
- Deepen the requested investigation with the available relationship, path,
  timeline, or directory tools. A search failure is not an empty result. For a
  capacity error with `recovery: "retry_read"`, wait `retryAfterSeconds` before
  retrying the read. Stop repeated retries if the same failure persists and
  report its diagnostic identifiers.

## Proposals and discussions

- Locate a sharing destination with `context_spaces_search` and
  `action: "publish"` before `context_share`. Use `knowledge_propose` or
  `knowledge_correct` for an explicitly requested addition or correction with
  evidence; accepting the request does not prove an applied information change.
- Read `knowledge_ontology_describe` before proposing a new information type
  or relationship with `knowledge_ontology_propose`.
- Read proposals and their evidence before `knowledge_proposal_review`.
  Review one proposal at a time. Use `confirm: true` only when the user has
  explicitly authorized that proposal's decision; do not approve in bulk.
- Use the published `knowledge_workroom_*` tools for durable discussions.
  Read a discussion before assigning people or posting; conclude it only with
  an authorized, evidence-backed resolution.
- Revoking a source requires an explicit request for that source and effect.
  Existing authorization for the same target and effect does not require a
  repeated conversational confirmation. Host approval prompts may still apply.

On an ambiguous mutation failure, inspect the affected proposal, discussion,
or source before retrying, following `recovery: "reconcile_before_retry"` when
returned. `No approval received` without a Kimono error envelope suggests a
host approval failure; its wording alone does not prove origin or execution.
Keep returned error codes, `phase`, and diagnostic IDs; do not invent a cause
or use another integration to bypass authorization.
