---
name: ceratops-code-consistency-audit
description: Audit a repository after large refactors, branch merges, or parallel agent threads for contradictions between implementation, docs, configs, tests, examples, and control files. Use when the goal is post-merge validation, release-readiness consistency checking, documentation-drift detection, or merged-only edge-case hunting rather than style review.
---

# Ceratops Code Consistency Audit

Audit repository coherence after combined changes. Across teams this work is usually split across post-merge validation, integration and regression testing, release-readiness review, documentation-drift checks, and architectural fitness functions. Use this skill to run the cross-cutting consistency pass those labels only partially cover.

Use these references when helpful:

- Reusable prompt templates: `references/prompt-template.md`

<!-- CERATOPS_SHARED_SECTIONS_START -->
<!-- SECTION SOURCE: templates/sections/minimal.md -->

## Core Rules

- Mandatory: Everything in this section is part of the skill contract unless explicitly inapplicable to the current task.
- Blocking: When this skill is invoked, follow this `SKILL.md` as the workflow contract for the task; if a higher-precedence instruction conflicts with a required skill step, report the conflict instead of silently skipping the step.
- Blocking: Do not claim completion unless this skill's completion gate is satisfied, intentionally inapplicable, or reported as a blocker.
- Blocking: Scope completion, current-state, root-cause, no-fix, unsupported, and durable-resolution claims to evidence actually checked, or to fresh same-task evidence that still applies.
- Blocking: Reuse fresh sufficient same-run evidence unless state is uncertain, plausibly changed, materially broadened, externally mutable for the decision, or this skill explicitly requires a fresh check.
- Blocking: Prefer direct local evidence and targeted diagnostics for the next skill decision; use current official sources only when local evidence leaves a concrete ambiguity or the task depends on unstable external behavior.
- Blocking: Do not do generalized best-practice refresh, reference-repo comparison, or skill-maintenance work during routine skill runs unless the user explicitly asks or a required decision remains ambiguous after targeted evidence.
- Blocking: Ask before risky, destructive, irreversible, credential-dependent, externally mutating, complex, invasive, nonstandard, or high-maintenance steps unless the user already explicitly requested that tradeoff.
- Blocking: Do not update this `SKILL.md` or other skill/control files during a routine run unless the user explicitly asked for skill maintenance or the task cannot be completed safely without a narrow in-scope fix.
- Mandatory: When editing an existing text file, preserve its current line-ending convention unless intentional normalization is part of the task.
- Mandatory: Follow this skill's output contract when present; otherwise report only the outcome, unresolved blockers, retained state with reasons, and important unverified items.

<!-- SECTION SOURCE: templates/sections/credentials.md -->

## Credential Handling

- Do not ask for credentials unless they are truly required after local checks.
- If credentials are truly required after local checks, report only:

1. which credential or login is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, keyring, CI secret, registry setting, connector, or another exact target
<!-- CERATOPS_SHARED_SECTIONS_END -->

## Skill-Specific Rules

- Treat repository coherence as the goal. Do not turn the task into a generic style or code-quality review.
- Start from declared behavior and sources of truth before judging implementation details.
- Treat conflicts between two declared sources of truth as findings even when the code still happens to work.
- Prefer concrete contradictions, stale follow-through, and merged-only interaction bugs over speculative architecture advice.
- When git history or recent merge context is available, judge the current merged result against the latest target-branch state, not each branch in isolation.
- Do not ask for credentials for normal local repo audits.
- If external systems are genuinely needed, first exhaust local repo state, local git history, and no-auth metadata.

## Inputs To Capture

- Repo or subtree under audit and whether the task is audit-only or audit-and-fix.
- Recent refactors, branches, PRs, or agent-thread outputs most likely to have interacted.
- Expected sources of truth such as README files, docs, examples, configs, tests, manifests, generated metadata, automation, or control files.
- High-risk surfaces such as public APIs, migrations, feature flags, rename waves, packaging, install flows, or generated artifacts.

Infer missing inputs from repo state before asking.

## Boundaries

- Use this skill when a repo may have semantic drift after merges, refactors, migrations, or parallel agent work and the user wants a consistency audit rather than style feedback.
- If the user wants only a code review for bugs or regressions inside a bounded patch, use normal review flow instead of this whole-repo audit.
- If the task is only diagnosing and fixing one current breakage, stop and use `$ceratops-task-execute-in-stages`.
- If the task is only documentation maintenance without broader repository coherence concerns, narrow the work to documentation drift rather than running the full audit.

## Workflow

### 1. Define intended behavior first

- Identify declared behavior from the highest-signal local sources: README files, docs, examples, tests, configs, manifests, automation, control files, naming, and contracts.
- For skill repos or agent repos, treat `SKILL.md`, `agents/openai.yaml`, README tables, bundled resources, and any install metadata as first-class sources of truth.
- If multiple artifacts disagree about the intended behavior, record that conflict explicitly instead of guessing which one is correct.

### 2. Map merged interaction surfaces

- Inspect adjacent modules, flags, configs, scripts, templates, tests, and examples that were likely touched by separate refactors or threads.
- Use git history, diff context, or merge context when available to find where independently reasonable changes now interact.
- Prioritize hidden coupling, duplicated logic that drifted, partial renames, stale options, orphaned files, and follow-through gaps.

### 3. Run consistency passes

Check as many of these as the repo justifies:

- implementation vs README and docs
- implementation vs examples, scripts, and run instructions
- file names and stated purpose vs actual behavior
- tests vs current intended behavior
- configs, manifests, automation, and control files vs implementation
- public interfaces vs internal assumptions
- merged-only edge cases that appear when features or refactors combine
- stale artifacts, dead references, partial migrations, and unused compatibility shims

### 4. Validate findings before reporting

- Prefer findings that point to exact conflicting artifacts, exact inconsistency, actual risk, and the smallest credible fix.
- Avoid style nits, naming preferences, or refactor suggestions unless they are needed to resolve a real contradiction.
- Distinguish confirmed findings from plausible but unverified risk areas.

### 5. Fix only when asked or clearly justified

- Default to audit and report.
- If the user asked to repair the repo or the smallest safe fix is already in scope, apply the narrowest credible correction and rerun the relevant checks.
- Escalate before risky deletions, broad rewrites, or behavior-changing interpretation choices.

### 6. Close with explicit coverage

- Classify important checked surfaces as consistent, conflicting, blocked, or not verified.
- If no findings remain, say so explicitly and note the residual coverage limits instead of implying exhaustive certainty.

## Completion Gate

- Verify the audit inspected the repo's declared sources of truth, not only the implementation files.
- Verify merged interaction surfaces and likely cross-thread integration seams were checked where evidence existed.
- Verify every reported finding ties back to concrete conflicting artifacts or an explicitly stated verification gap.
- Verify the final answer reports findings, important consistent areas, and important verification limits without drifting into generic review commentary.

## Output Contract

Report only:

- findings ordered by severity
- for each finding: conflicting artifacts, exact inconsistency, risk, and the smallest credible fix
- important areas checked and found consistent
- anything important not verified

If no findings remain, say so explicitly and mention the main residual risk areas or coverage limits.

## Example Invocation

`Use $ceratops-code-consistency-audit on this repo. Ignore style. Find post-merge contradictions, docs-to-code drift, stale assumptions, and merged-only edge cases.`
