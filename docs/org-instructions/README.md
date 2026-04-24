# Recommended Claude Org Instructions

When your team has multiple MCP connectors — Octave, HubSpot, Salesforce, Gong, Granola, Clay, Google Drive, etc. — Claude needs explicit guidance to route GTM questions to Octave's synthesis layer rather than to raw-data tools. Without this, reps have to prefix every prompt with "Using Octave, …" to get the right output, which is fragile and doesn't scale across a team.

Setting **Organization preferences** in Claude tells every conversation in your workspace how to route. Pick one of the two versions below, customize for your stack, and paste into **Settings → Organization preferences** at [claude.ai](https://claude.ai) (requires admin or owner role).

Claude org preferences cap at **3,000 characters**.

## Pick a version

| Version | Size | Use when |
|---|---|---|
| **[short.md](./short.md)** | ~1,700 chars | You want headroom to layer workspace-specific rules (custom ICPs, named playbooks, vertical terms) on top. Covers core routing and the most common Octave intents. |
| **[long.md](./long.md)** | ~2,950 chars | Your team also has HubSpot, Salesforce, Gong, Granola, Fathom, or Clay connected. Adds explicit rules that demote raw-data tools to fallbacks, plus routing for LFGTM plugin skills and specialized agents. |

Click into either file, view **Raw** on GitHub, copy the full contents, and paste into Claude org preferences.

## How to install

1. Log in to [claude.ai](https://claude.ai) as an admin or owner.
2. Go to **Settings → Organization preferences**.
3. Paste the raw contents of [short.md](./short.md) or [long.md](./long.md). Customize as needed (see below).
4. Save. **Changes can take up to 1 hour** to take effect across Claude products (claude.ai, Desktop, Claude Code, mobile).

Individual Pro users who aren't in a Teams/Enterprise workspace can paste the same text into **Settings → Personal preferences** instead — it applies to all their own conversations.

## How to customize

Before saving, consider adding workspace-specific rules. A few useful patterns:

- **Named playbooks.** If your team has a standard playbook (e.g., "4-Step Cold Outbound Sequence"), reference it by name so Claude knows to look for it: *"When asked to run a cold outbound sequence, use the '4-Step Cold Outbound Sequence' playbook."*
- **ICP-specific framing.** *"We sell to mid-market B2B SaaS companies with 50–500 employees. Ignore fit signals outside this range."*
- **Vertical terminology.** If your industry uses specific terms (e.g., "ACV," "GRR," "PLG motion"), define them once so Claude uses them correctly.
- **Custom MCP tool names.** If you renamed your Octave connection (e.g., `octave-acme` vs. `octave-myWorkspace`), no change needed — tool names are server-scoped, not connection-scoped.

## How to test

> **Wait up to 1 hour before testing.** Claude org preferences can take up to an hour to propagate across products. If you test too early, old routing will win and you may incorrectly conclude the instructions aren't working. Come back later.

Once propagation is done, start a new Claude conversation (any surface) and run these prompts **without** mentioning Octave. Claude should route each one to the right tool:

| Prompt | Expected tool |
|---|---|
| *"What's the status of my deal with [company] and what should I be doing next?"* | `get_deal_deep_dive` or `/octave:pipeline` |
| *"Prep me for my discovery call with [name] at [company]."* | `generate_call_prep`, `/octave:research`, or `/octave:meeting-prep` |
| *"Qualify [name] at [company] against our ICP."* | `qualify_person` + `qualify_company` |
| *"Enrich [name] at [company] — I don't know much about them."* | `enrich_person` + `enrich_company` |
| *"Draft a 4-step outbound sequence for [name] at [company]."* | `generate_email` or `run_email_agent` |

If Claude still reaches for HubSpot, Salesforce, or Gong first after waiting the full hour, tighten the "Routing vs. other connectors" section for the specific tool that's winning the routing.

## Related

- [Claude support: Set organization preferences](https://support.claude.com/en/articles/14546867-set-organization-preferences)
- [LFGTM plugin setup](../../README.md#installation)
- [Octave MCP tool reference](https://docs.octavehq.com/mcp/available-tools)
