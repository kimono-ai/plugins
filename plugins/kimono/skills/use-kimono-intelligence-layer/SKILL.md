---
name: use-kimono-intelligence-layer
description: Search authorized Kimono Projetos, Corpora, and other Intelligence Layer contexts, read source evidence, and work with available governed proposals or discussions. Use for shared information and its evidence; use Brain for operational organization metrics and the relevant management skill for sharing files or configuring sources.
---

# Use Kimono Intelligence Layer

The Intelligence Layer is the common query surface across authorized Projetos,
Corpora, and other contexts. Projeto organizes collaboration and participants;
Corpus organizes curated sources reused by Agentes. Keep these same product
terms throughout the platform and MCP. Internal graph/space names are not
additional user-facing products.

Use the connected server's actual tools. Access requires compatible OAuth
scopes, organization MCP permissions for dynamic roles, and resource ACLs.
An OAuth grant limited to Projetos does not authorize unrelated institutional
content. Do not select another account or bypass a denied destination.

## Find and read evidence

- For a Projeto, discover it with `project_list`/`project_get`, then use
  `knowledge_search` or `knowledge_list` with `focus: "project"` and
  `projectRef` set to its UUID or `project:UUID`. `current_project` is a runtime
  shortcut; an MCP host must not assume a current Projeto exists.
- For a Corpus, discover it with `corpus_list`/`corpus_get`, then use
  `focus: "corpus"` and `corpusRefs` with the returned Corpus references/IDs.
- The default search focus is `relevant`; `personal` and `accessible` are
  available when appropriate to the request. Keep a question about a selected
  Projeto or Corpus scoped to it. Apply `types` and `time` when relevant.
- Read results by their `ref` with `knowledge_read`. Preserve returned source
  references and `revisionId` for attribution. Documents are evidence; an
  uploaded document does not automatically become an accepted fact.
- `knowledge_traverse` handles neighbors, paths, and relationship types using
  discovered references. `knowledge_timeline` explores supported timelines.
  Follow `nextCursor` and inspect coverage before describing results as
  exhaustive; a truncated page is not the complete context.

A search error is not an empty result. Follow `recovery: "retry_read"` and
`retryAfterSeconds` for a capacity delay; stop repeated failures and retain
its code and diagnostic IDs. Query failure is not normal ingestion heartbeat
lag and does not prove the document upload failed.

## Share and govern information

For “share this proposal with a colleague”, use `manage-kimono-projects` to
resolve the person, create/reuse an appropriately scoped Projeto, and upload
the selected file. Do not use an organizational Corpus as a private sharing
shortcut. `context_share` records a governed sharing intention; it is not a
file upload or, by itself, a grant of human access.

For Corpus lifecycle, source configuration, source-bound uploads or Agente
grants, use `manage-kimono-corpora`. Agent configuration/publication remains
in Builder; operational analytics remains in Brain.

For an explicitly requested institutional sharing intention, discover a
publication destination with `context_spaces_search` and `action: "publish"`.
Read `knowledge_ontology_describe` before proposing an ontology change through
`knowledge_ontology_propose`. Use only proposal and workroom operations
actually present in the catalog; do not invent a generic remember/correct API.
Explicit Native/CLI memory writes require their own human proof and are not
exposed by this MCP gateway.

Read each proposal and its evidence before `knowledge_proposal_review`.
Review individually, with `confirm: true` only for the decision already
authorized by the user. Use the published `knowledge_workroom_*` tools for
requested discussions and evidence-backed resolutions; do not approve in bulk.
Existing authorization for the same target and effect does not need repeated
conversational confirmation. Host tool approval may still be required.

After an ambiguous mutation, read the affected resource before retrying.
`No approval received` without a Kimono error envelope suggests host approval,
not proof of where execution stopped. Preserve `phase`, `recovery`, and
correlation IDs instead of inventing a cause.
