---
name: ceratops-consistency-audit
description: Audit a repository after large refactors, branch merges, or parallel agent threads for contradictions between implementation, docs, configs, tests, examples, and control files. Use when the goal is post-merge validation, release-readiness consistency checking, documentation-drift detection, or merged-only edge-case hunting rather than style review.
---

# Ceratops Consistency Audit

Audit repository coherence after combined changes. Across teams this work is usually split across post-merge validation, integration and regression testing, release-readiness review, documentation-drift checks, and architectural fitness functions. Use this skill to run the cross-cutting consistency pass those labels only partially cover.

Use these references when helpful:

- Reusable prompt templates: `references/prompt-template.md`

<!-- CERATOPS_COMMON_CORE_START -->
## Core Rules

- Everything in this skill is mandatory unless explicitly marked optional or inapplicable.
- Before completion, re-open this `SKILL.md` and verify the work line by line against `Core Rules`, `Inputs To Capture`, `Boundaries`, `Workflow`, `Credential Handling`, `Completion Gate`, and `Output Contract`.
- Use local state, local files, installed tools, and other direct evidence first. Check current official docs or other live official sources only when the task depends on unstable external behavior and the available direct evidence still leaves a concrete task-blocking ambiguity or material conflict.
- Do not do generalized best-practice refresh, reference-repo comparison, or skill-maintenance work during routine runs.
- Do not update this `SKILL.md` during routine runs unless the user explicitly asked for skill maintenance or the current task cannot be completed safely without a narrow in-scope fix.
- Inspect local state and local auth before asking for credentials or making assumptions.
- When editing an existing text file, preserve its current line-ending convention unless intentional normalization is part of the task.
- Classify each touched artifact, external entity, and side effect as active, intentionally retained with reason, stale and removed, not applicable, or blocked.
- For every open security, code-scanning, maturity, or process alert you inspect, decide whether it is safe, fix low-risk items directly, and for every alert not fixed report its name or id, whether it is blocking, why it is not being fixed now, and the concrete work needed to clear it. Do not collapse retained alerts into a generic healthy result.
- In user-facing answers, keep routine success reporting implicit. Omit PR metadata, commit IDs, check lists, cleanup logs, and exact local paths unless they materially change the user's next action, explain a blocker, or were explicitly requested.
- If any required item is unmet or unverifiable, report the blocker instead of claiming completion.
<!-- CERATOPS_COMMON_CORE_END -->

## Skill-Specific Rules

- Treat repository coherence as the goal. Do not turn the task into a generic style or code-quality review.
- Start from declared behavior and sources of truth before judging implementation details.
- Treat conflicts between two declared sources of truth as findings even when the code still happens to work.
- Prefer concrete contradictions, stale follow-through, and merged-only interaction bugs over speculative architecture advice.
- When git history or recent merge context is available, judge the current merged result against the latest target-branch state, not each branch in isolation.

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

## Credential Handling

- Do not ask for credentials for normal local repo audits.
- If external systems are genuinely needed, first exhaust local repo state, local git history, and no-auth metadata.
- If credentials are still required, ask only for the missing credential, why it is needed now, where it will be stored, and the exact command or setting required.

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

`Use $ceratops-consistency-audit on this repo. Ignore style. Find post-merge contradictions, docs-to-code drift, stale assumptions, and merged-only edge cases.`
