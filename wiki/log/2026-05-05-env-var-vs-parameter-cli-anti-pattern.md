---
date: 2026-05-05
slug: env-var-vs-parameter-cli-anti-pattern
type: cross-project-lesson
for: second-brain
tags: [cli-ux, anti-pattern, operator-tool, cross-project, lesson]
---

# CLI design lesson — env-var vs parameter (operator-tool anti-pattern)

## Operator's verbatim (2026-05-05, cycle 70)

> "WHOS THE FUCKING RETARD WHO USE ENV VAR WHEN ITS SUPPOSED TO BE PARAMETERS..."

Plus earlier:
> "I cannot setup all that... I should be plain simple.. why would it be made so fucking complex..."

## Context

The publish script `/tmp/publish-root-ghostproxy.sh` (authored by the /opt second-brain agent for the operator's first-MVP-alpha publish workflow) exposed configuration via environment variables ONLY:

```
VISIBILITY=public bash /tmp/publish-root-ghostproxy.sh --execute
LICENSE_TYPE=mit bash /tmp/publish-root-ghostproxy.sh --execute
```

When operator tried `--visibility public` (the natural attempt), the script rejected it with `unknown arg`.

## The anti-pattern

**Env-var-only config for one-shot operator-tool CLIs.**

This is wrong because:

1. **Operator's prior CLI knowledge is parameter-based.** Every common CLI (`ls -la`, `gh repo create --public`, `git commit -m "..."`, `curl -X POST`) takes flags. Operator's muscle memory is `--<flag> <value>`, not `<VAR>=<value> bash <script>`.

2. **Env-vars conflate config with environment.** `VISIBILITY=public` looks like an environment variable for export, not a one-shot config override. It also silently persists if exported (unlike a flag which is per-invocation by design).

3. **Discovery via `--help` doesn't surface env-vars cleanly.** Flags appear in `--help` output as expected; env-var docs end up buried in script header comments. Operator can't reach for `--help` and find what they need.

4. **No tab completion.** Modern shells autocomplete `--<flag>` but not `<VAR>=<value>` prefixes.

5. **Fragile under composition.** `bash script --execute && bash script --execute` works; `VISIBILITY=public bash script --execute && bash script --execute` only sets visibility on the first call (the second has no env var) — silent failure mode.

## The right pattern

For one-shot operator-tool CLIs, **parameters/flags are the default**:

```
bash script --execute --public
bash script --execute --visibility=public  # if value-with-name preferred
bash script --execute --name=my-repo --license=mit
```

Env vars MAY be supported as fallback for non-interactive automation (CI, scripts), but the **flag form must be the documented primary**.

## Cross-project applicability

This applies to ANY operator-facing tool the second-brain authors:

- Publish scripts
- Setup scripts
- Migration tools
- One-off utility tools
- Anything that an operator runs interactively from a shell

The second-brain agent should default to flag-based CLI for operator tools; env-vars only for genuinely-environmental things (PATH, HOME, project-root resolution).

## Fix applied (cycle 70)

`/tmp/publish-root-ghostproxy.sh` now accepts:
- `--public` / `--private` (mapped to VISIBILITY)
- `--name=<repo-name>` (mapped to REPO_NAME)
- `--license=<type>` (mapped to LICENSE_TYPE)
- `--description=<text>` (mapped to DESCRIPTION)

Env-var fallbacks preserved for CI compatibility. Flag form is now primary.

## Recommended back to second-brain

This lesson belongs in the second-brain's CLI-authoring patterns. Suggest:
- Wiki entry under `wiki/lessons/03_validated/cli-ux/` — "CLI parameter-vs-env-var anti-pattern: parameters are default for operator tools"
- Future operator-tool scripts authored by second-brain agent: default to flag-based; env-vars only as supplementary fallback for automation contexts.

Cross-project channel: this log + (when M007 connect lands) `tools.gateway contribute` for the lesson back to second-brain's `wiki/lessons/`.
