# Installed runtime and routing

Resolve `<plugin-root>` from this installed package, not the user's working directory or a maintainer's cache. `<skill-dir>` is the selected installed skill directory. Root helpers live at `<plugin-root>/scripts`; cross-skill resources resolve relative to the referring file. Downstream builds preserve these dependencies and provide `package-resources.json`.

Detect actual capabilities before choosing execution: shell, Python, Node, browser/rendering, exporters, connected workspace tools, analytics and asset permissions. Inspect current schemas; never invent an API, argument, entitlement, or tool result. Missing optional capabilities reduce what can be checked or delivered. State unavailable/not-run separately from failure and pass.

Use the user's explicit task and inherited choices to select one primary skill. Carry workspace/opportunity, offering/motion, sources, output purpose, brand, and resolved inputs through a handoff. Keep a visited-skill set and never route back into the same task indefinitely. Direct invocation retains applicable workspace methods, not just context loaded by an assistant agent.

## Reviewers on every host

Reviewer instructions ship at `<plugin-root>/agents/octave-editorial-reviewer.md` and `<plugin-root>/agents/octave-presentation-reviewer.md`. Claude's named Task syntax is one host adapter, not a universal API. Use supported delegation with these files as instructions when available. Otherwise perform the same checks sequentially. Both reviewers inspect the same immutable artifact version and return findings; one author applies edits and reruns affected checks.

No browser means visual review is not run. No exporter means no completed export. A labeled working draft or agreed text alternative may still complete the requested task; never fabricate a scorecard or tool success. Use bounded retries and resume verified progress after an interrupted call.
## Runtime dependencies

Core local helpers require Python 3.10+; asset HTTP scripts also require curl.
Builds require bash, Python and jq. Browser capture/regression uses the pinned
Playwright and Pillow versions in `requirements-validation.txt` plus Chromium:
`python3 -m pip install -r <package-root>/requirements-validation.txt`, then
`python3 -m playwright install chromium`. The Node render gate also needs the pinned root npm dependencies: run `npm ci --ignore-scripts` from the installed package root (or use a writable runtime cache with NODE_PATH configured). Install only dependencies needed for
the requested operation. PDF/PPTX conversion helpers document their own Node or
python-pptx requirements. Missing optional tools produce NOT RUN with a useful
fallback; no check passes merely because its runtime is unavailable.
