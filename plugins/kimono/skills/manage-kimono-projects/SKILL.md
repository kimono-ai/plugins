---
name: manage-kimono-projects
description: Create and manage Kimono Projetos, participants, and selected shared files through MCP. Use when a user wants to share a proposal or document with colleagues, create a collaboration context, or manage an existing Projeto. Use Corpus management for curated organizational sources reused by Agentes.
---

# Manage Kimono Projetos

A Projeto is the existing collaboration context for people, files, and
explicitly shared conversations. It can be as small as one proposal and two
people. Corpus is a curated source collection; do not create a Corpus mirror
of a Projeto or introduce a new user-facing space entity. Both use the
Intelligence Layer with their own authorization boundaries.

Use only the published tools visible to the connected account. Access combines
`projects:read`/`projects:write`, the organization's MCP project permissions for
its dynamic roles, and resource ACLs. Platform screen visibility is separate.
A missing permission is not a reason to use an organizational destination.

## Share a selected document with a colleague

Treat “share this proposal with Marco” as authorization to share that selected
file with that resolved person, including creating the appropriate Projeto
when needed. Proceed through the authorized operation without asking the same
question at each stage. Ask only when identity, document, or intended audience
is materially ambiguous. Host tool approval requirements still apply.

1. Resolve the colleague with `project_members_search`. Use the returned
   organization member ID; a person mentioned in document evidence is not
   necessarily an eligible project participant. Resolve ambiguous identities
   before granting access.
2. Find candidate Projetos with `project_list`. Read the selected one with
   `project_get` and `project_members_list`. Reuse it only when its purpose and
   current audience fit the requested sharing; a similarly named Projeto with
   additional people would disclose the file more broadly. Direct membership
   is not necessarily an exhaustive view of inherited ACLs. If the available
   resource data cannot establish the effective audience, create a fresh
   Projeto with the explicit intended participants.
3. Otherwise, use `project_create` with a meaningful name and the intended
   participants. Choose the minimum role needed by the request: viewing a
   proposal does not imply editing or ownership. The creator's membership is
   managed by the server. Do not add people inferred from the proposal text.
4. Upload only the selected document through `ingest-kimono-sources`, opening
   the session with explicit `targetProjectId`. Omitting that destination can
   publish to the organization. Keep source IDs, event IDs and idempotency keys
   stable for the same upload.
5. Read `project_files_list` for processing state. Verify search with
   `knowledge_search({ focus: "project", projectRef: "project:<uuid>", ... })`,
   then open the returned reference with `knowledge_read`. Return the Projeto
   link when supplied or known from an observed platform resource, participants,
   and the actual file state. If no verified URL is available, return the
   Projeto name and ID. Do not invent routes or claim delivery from HTTP 200.

Membership changes use `project_member_upsert` and `project_member_remove`.
Adding a participant grants access to the Projeto's current and future shared
files. If sharing one document would expose unrelated files, create a separate
Projeto with the intended participants instead of adding them to that one.
A new participant can receive files without receiving private conversations;
retain the explicit thread selection and do not share the source conversation
just to share one file. Changing a role, removing a member, or broadening access
must match the user's requested effect. Read the current members before a
change and preserve unrelated access.

`project_update` changes the Projeto's metadata. `project_files_remove`
removes the selected project file only when requested. Read the current file
inventory and respect any required confirmation fields for the already
authorized target and effect.

## Evidence and recovery

Project creation, membership persisted, sharing notification, upload accepted,
document published, successful search, and recipient opened/read are separate
states. An own-account search plus a member list does not prove execution in
the recipient's account. Report the strongest stage actually observed.

The original file uses Kimono's canonical storage, and extraction publishes
document/pages/segments into the Projeto's authorized Intelligence Layer
context. Agente access also requires its configured project context and the
person's authorization; adding a participant does not grant every Agente access.

For an uncertain write, inspect the affected Projeto, member list, session, or
file before retrying. Find an uncertain creation before making a duplicate.
Follow `recovery` and retain diagnostic IDs. A denied scope requires OAuth
consent; denied organization permission or resource ACL requires that access
change, not repeated login or an alternate integration.
