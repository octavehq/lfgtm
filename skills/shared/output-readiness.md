# Deliverable purpose and readiness

Resolve the requested artifact, audience, format, and purpose. A seller draft, buyer proposal, internal coaching brief, and collaborative POC worksheet have different completion requirements.

Use these working states when useful:
- seller_draft: supported content with explicit open inputs or assumptions; a valid final deliverable when the user asks for a draft/scaffold.
- ready_for_review: the requested content has been assembled and is ready for the applicable checks or chosen review.
- buyer_ready: suitable for its intended reader and decision, with the necessary facts, usable structure, and no accidental missing seller inputs. A planned future-measurement or buyer-input field can remain when its purpose, owner, and timing are clear.
- published_verified: the intended artifact/version and intended access have been confirmed after an authorized publication.

An artifact need not pass through every state. Readiness does not require a zero-question first turn. Use evidence-and-inputs.md to collect material gaps, then validate after incorporating the answers.

## Check the final deliverable

For every format, including plain text and saved-agent output, check the requested scope, strategy fit, evidence fidelity, and customer voice, plus a practical next step when requested or intrinsic to the task. Preserve quoted evidence, exact names, and necessary domain terms. Apply style preferences to authored prose in context; do not corrupt a quote or technical meaning to satisfy a word ban.

For HTML or exported artifacts, also check the requested format, links/CTAs, images, typography, responsive/print behavior, and necessary interactions. Use deterministic scripts where available and actual rendering for visual claims. A one-page print deliverable must have one readable printed page; a working CTA must reach its intended destination. A slide or lesson must expose its content and navigation in the promised modes.

Use the customer's explicit brand choice, then the relevant workspace brand, then a clear neutral fallback. Recipient branding requires a relevant user choice. Mandatory Octave branding is not a universal customer requirement.

Run available checks honestly. If a required renderer or exporter is unavailable, use a supported alternative or label exactly what remains unverified. Do not report an unperformed check as PASS. A useful draft or alternative format can still be delivered when it matches the user's intent.

Reviewers inspect an immutable copy and return findings. One author applies changes, then repeats affected checks on the final artifact. Parallel review is acceptable; concurrent edits to the same artifact are not the default. Use the current host's supported delegation and packaged reviewer instructions; when delegation is unavailable, perform the same relevant checks sequentially.

Limit optional polishing rounds, but do not relabel an unresolved fabricated claim, missing required section, broken primary action, or wrong-audience content as ready because a cycle cap was reached. Continue a concrete fix, collect the needed input, or report the useful draft and its limitation.

Keep private source notes and internal account strategy out of external publish bundles. Use a declared file manifest. Publication follows the user's authorized scope and intended audience; content generation alone does not authorize a new distribution action. Report verified destination and access only after the relevant readback.

## Source-lint policy

Pass a JSON policy to `shared/scripts/lint.sh --policy`: `audience` is `internal`, `restricted_external`, or `public`; `readiness` is one of the states above; `assets` is `embedded`, `bundled`, or `hosted`. Optional string lists: `remoteHosts` (exact permitted hosts for hosted assets), `intentionalPlaceholders` (exact agreed planning fields), and `allowedTerms` (customer/domain terms). Unknown keys/values fail validation. Without a policy, the conservative default is internal, ready_for_review, bundled, with no remote hosts. A source pass is never a visual pass.
