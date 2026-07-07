# Generation Modes

Content-producing skills use Octave's `generate_content` and `generate_email` tools by default. Two alternatives are always available:

- **Saved agents** — Check for matching agents with `list_agents` when relevant, and offer to run one for consistency and team standards. See `/octave:explore-agents` to browse and manage saved agents.
- **Claude-direct** — Skip the `generate_*` calls: gather the same Octave context (persona, Motion ICP narrative, proof points, brand voice), then Claude writes the content directly. Offer this when the user wants more control over structure, length, or format.

For the full interactive mode selector (saved agent / Octave default / Claude direct), use `/octave:generate`.

When generating with Claude-direct, label the output with the sources used (persona, Motion ICP cell, proof points, brand voice) so the user can evaluate grounding.
