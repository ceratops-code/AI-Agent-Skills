# Naming And Workflow Research

## Short Answer

There is no single universal industry label that cleanly covers the whole activity you described. In practice, teams split it across several adjacent labels:

- `post-merge validation` or `merged-results validation` for checking the combined result against the latest target branch
- `integration testing` and `end-to-end testing` for making sure components still work together
- `regression testing` and `smoke testing` for catching behavior drift quickly and then more broadly
- `release-readiness review` for checking whether the release is actually complete rather than merely merged
- `documentation drift` checks for docs, README, and examples that no longer match behavior
- `architectural fitness functions` for continuously enforcing important consistency constraints

For this skill, `post-merge consistency audit` is the clearest composite label because it covers behavior, docs, config, tests, and merged-only interactions without implying a pure style review or a narrow test-suite run.

## What Current Sources Suggest

### Post-merge and merged-result validation

- GitHub documents `merge queues` as ensuring queued pull requests still pass checks when applied to the latest target branch and queued changes, specifically to prevent incompatible changes.
- GitLab documents `merged results pipelines` as testing a temporary merged commit to catch integration issues before merging and to ensure changes in different files work together.

These sources support the `post-merge validation` and `merged-result validation` part of the activity.

### Release readiness

- Atlassian describes `release readiness` as aggregating deployment information such as unreviewed code, open reviews, unmerged pull requests, and failing builds so the team can judge whether the release is truly complete.

This supports the operational side of the activity: not only "does it compile," but "is the repo actually coherent enough to release."

### Regression and smoke testing

- Microsoft recommends fast smoke tests on every commit and broader regression tests nightly or before release.
- Microsoft also stresses that test assets and test cases must stay in sync with intended behavior.

This supports the practical testing layer: use quick checks for drift detection and broader checks before release or after large merges.

### Architectural conformance

- Thoughtworks describes `architectural fitness functions` as tests that measure alignment to architectural goals and provide continuous feedback for architectural conformance.
- Thoughtworks also frames them as a way to avoid architectural drift and to keep important qualities explicit and testable.

This supports the deeper consistency angle: when multiple valid changes combine into a result that no longer matches the repo's intended structure or operational model.

## Recommended Practical Workflow

1. Start from declared behavior, not from code style.
2. Identify the repo's sources of truth: README, docs, examples, configs, manifests, tests, automation, and control files.
3. Inspect the merged interaction surfaces where separate changes can conflict semantically.
4. Run fast smoke and regression checks where the repo already has them.
5. Compare declared behavior against actual behavior and flag contradictions.
6. Look explicitly for merged-only edge cases, partial renames, stale references, duplicate logic drift, and follow-through gaps.
7. Report only concrete inconsistencies, risks, and the smallest credible fixes.

## Source Links

- GitHub merge queue docs: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request-with-a-merge-queue?tool=webui
- GitLab merged results pipelines: https://docs.gitlab.com/ci/pipelines/merged_results_pipelines/
- Atlassian release readiness article: https://www.atlassian.com/blog/2015/04/jira-6-4-release-confidence-sanity
- Microsoft testing guidance: https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/testing
- Thoughtworks fitness function-driven development: https://www.thoughtworks.com/en-cl/insights/articles/fitness-function-driven-development
