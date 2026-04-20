# Reusable Prompt Templates

## Full Prompt

```text
Run a post-merge consistency audit on this repository.

This is not a style review or generic code-quality pass. Focus on repository coherence after combined changes, large refactors, branch merges, or parallel agent threads.

Start from declared behavior and sources of truth such as README files, docs, examples, configs, manifests, tests, automation, control files, and naming. Compare those expectations against the actual implementation and against each other.

Look for:
- contradictions between code, docs, tests, examples, configs, and control files
- files whose actual behavior no longer matches their stated purpose
- merged changes that are individually reasonable but inconsistent when combined
- duplicate or parallel logic that drifted
- partial renames, stale references, orphaned options, dead paths, or missing follow-through updates
- merged-only edge cases and interaction bugs
- tests or examples that still reflect pre-refactor behavior

Work in this order:
1. Identify the intended behavior from the repo's sources of truth.
2. Map the highest-risk interaction surfaces between separately changed areas.
3. Check the merged result for contradictions and stale state.
4. Report only concrete inconsistencies and verification gaps.

Output only:
1. Findings ordered by severity.
2. For each finding: conflicting artifacts, the exact inconsistency, why it matters, and the smallest credible fix.
3. Important areas checked and found consistent.
4. Anything important you could not verify.
```

## Short Prompt

```text
Run a post-merge consistency audit. Ignore style. Find contradictions, docs-to-code drift, stale assumptions, partial follow-through, duplicate logic drift, and merged-only edge cases by comparing declared behavior against actual behavior.
```

## Audit-And-Fix Variant

```text
Run a post-merge consistency audit, then apply only the smallest safe fixes for confirmed contradictions that are clearly in scope. Ignore style. Re-run the relevant checks after each fix and report only real findings, fixes, and anything important not verified.
```
