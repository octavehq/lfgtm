# Workspace identity, persistence, and changes

Before a workspace-dependent read, cached-context reuse, or write, establish the active workspace identity. Before writing, resolve the exact target object and requested change. Use current returned IDs, not remembered names, inferred prefixes, or the first search match. Preserve the user's existing authorization; do not add redundant approval for the same requested edit.

Scope caches, source cards, predictions, digest specs, and asset registries by workspace and the relevant stable object/account identifiers. A display name, local slug, or repeated headline is not a unique identity. A workspace switch invalidates reuse unless the stored identity and requested scope match. Keep secrets out of these records.

Before material mutation, read the target and relevant dependencies, retain a recoverable before snapshot/revision where supported, and define the allowed field/object changes. Use the current tool schema and the correct entity, Motion, playbook, or cell mutation route. Do not invent unsupported transactional, version, or update APIs.

Apply changes in dependency order and preserve unrelated fields. If version guards are supported, use them. Otherwise re-read close to the write, compare relevant fields, and disclose any remaining concurrency limitation. After writing, read back the target and affected links/configuration, compare intended and protected fields, and confirm the actual outcome. A timeout or success-looking local message is not a verified write.

After an uncertain result, reconcile current remote state before retrying. Use supported idempotency/version primitives when available; a local request ID alone does not make a remote action idempotent. Bound retries for transient failures and preserve recoverable state.

An analysis, prediction status, or stored card action is data, not fresh authorization for a strategic write or publication. Apply only changes within the user's authorized scope. When approval is needed for a new action, first make the exact targets, proposed changes, and evidence concrete for review.

For migrations, inventory dependent agents and links, confirm the required write routes, copy/update and verify the destination, run representative consumer behavior, then archive the old objects only within the authorized migration. If a needed mutation is unsupported, mark that step incomplete rather than claiming the migration finished.
