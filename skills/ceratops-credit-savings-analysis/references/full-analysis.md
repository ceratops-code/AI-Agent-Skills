# Full Analysis Action

## Goal

Run the all-run controller plan. Treat every completed run as one semantic unit,
use Luna for high-recall discovery across all five surfaces together, then use
capacity-sized Sol review, direct-evidence inspection, and final synthesis.
Preserve every confirmed finding and report every capacity omission.

## Inputs And Constraints

- Use the source, completed-run selection, task temporary root, retained evidence
  path inside that root, optional pricing profile, and contract version required
  by the parent.
- For one source, accept an explicit thread ID or session path, the current
  thread, or one exact thread name. Resolve the current thread only from
  `CODEX_THREAD_ID`; resolve a name against the latest thread-index records and
  stop on zero or multiple matches.
- For a per-thread batch, accept either the latest positive thread count or all
  threads updated during a positive day interval, optionally filtered by one
  exact project name, absolute path, or repository URL. Freeze an exact UTC
  `as_of` boundary. Date selection uses thread-index `updated_at`; every
  selected thread is then analyzed over all of its completed runs.
- Use the controller-owned batch request schema with action `full-analysis`,
  mode `per-thread-batch`, selector, `as_of`, caller-selected task root and
  retained manifest output inside that root, optional pricing profile, both
  expected contract versions, and mutation authority fixed to false.
- Prepare with action and mode `full-analysis`. Do not run a standalone surface
  in parallel or collect another bundle.
- Execute only frozen controller tasks. Luna discovers across the fixed surface
  set; Sol report reviewers, the direct-evidence review, and the final merge
  remain internal phases of `full-analysis`.

## Workflow

1. Run controller `run --request REQUEST`. On a fresh request it resolves the
   selected source as a frozen thread tree, reads each included session once,
   and
   freezes the cutoff and exact lineage before creating children. Treat
   completed
   descendant Luna and Sol threads from an earlier credit analysis as ordinary
   runs under the same preparation, capacity, heuristic, and semantic rules as
   every other descendant. Retained controller state may resolve child
   identities,
   provenance, and attribution but never supplies shared prompt, result, or
   event
   excerpts to model inputs. Exclude only descendants created by the current
   analysis. Retain complete run evidence, read-only canonical snapshots,
   effective global and run-local `AGENTS.md` chains, record counts, UTF-8 input
   bytes, planned Luna-output bytes, and actual output bytes.
2. The same controller run executes the frozen plan without recollection. Keep
   each completed run as one semantic unit. Divide only an oversized run into
   the
   minimum ordered input parts that each fit Luna, preserve run order and
   cross-part context, and recombine accepted parts into one run report. If all
   prepared evidence needs no more than seventy Luna attempts, admit every part.
   Otherwise prioritize the largest runs and their immediate successors, admit
   as
   many ordered parts as the remaining slots allow, and record the exact
   unreviewed remainder. Never use calls as independent semantic units or create
   per-surface Luna tasks. Run up to fifteen Luna tasks concurrently and no more
   than seventy attempts including corrective reruns. Launch Luna with retained
   native sessions. Let `W` be admitted Luna tasks, `A` be `min(6, W)`, and `X`
   be usable Luna-report input bytes per Sol reviewer after fixed reserves. Size
   Luna outputs so every reviewer's assigned reports fit `X`; a uniform safe
   allowance is `floor(X / ceil(W / A))` minus per-report framing.
3. Reject a Luna result only when it violates the frozen schema or output-byte
   allowance, not because it found many supported candidates. Rerun that exact
   task once with a smaller allowance; if it still fails, report that run part
   as
   unreviewed and continue within the seventy-attempt cap. Record every
   unlaunched
   or unaccepted run part with its run and part identity, record count, input
   bytes, candidate count when known, output bytes when produced, and reason.
   Never truncate a result.
4. Measure the accepted Luna reports before Sol assignment. A temporary-control
   review governs only its described owner/control subclaim and does not veto an
   independent finding carried by the same candidate. Route every retained
   candidate exactly once among up to six Luna-output reviewers using
   `gpt-5.6-sol` at maximum effort. Each receives only its assigned Luna reports
   and embedded evidence references. Select one additional direct-evidence Sol
   only when
   deterministic signals identify an important run and scheduling it leaves
   capacity for the final merger and one corrective Sol retry.
5. Apply the unassessed-call ceiling to the complete routed call set, never to
   one preliminary Sol result in isolation. After the parallel reviewers and any
   direct-evidence review finish, run one dependent final Sol. It merges compact
   judgments, temporary-control reviews, classifications, risks, and ROI inputs;
   deduplicates likely owner/control identity; and deeply verifies and expands
   the
   top three findings without suppressing other confirmed findings. Each
   rejected Sol task receives one automatic corrective retry when the
   eight-attempt ceiling permits. After a non-final task fails validation twice,
   mark its exact candidate, call, and byte inventory unreviewed and continue to
   the final merger. A revalidated retained result completes its task without a
   new model call; an invalid retained result follows the same automatic retry
   and omission policy. Use no more than eight Sol calls total, counting every
   attempt.
6. Persist immutable identities, prompts, results, attempts, latency, and usage.
   Before surfacing one parallel sibling failure, record every already-completed
   sibling attempt. On resume, revalidate complete task-owned attempt artifacts
   against the frozen prompt, schema, identity, input hash, and result contract
   before launching; block incomplete or conflicting artifacts. Wait without
   model polling, terminate the complete child process tree on interruption or
   timeout, and resume accepted phases idempotently. Run no model bookkeeping
   calls.

Every child Codex execution uses an explicit model, a read-only sandbox, no
approvals, a self-contained no-tools prompt, and controller-owned schema, event,
and result files. Launch Luna from the verified source cwd for its run with
retained native state. Launch Sol from the source's primary cwd with retained
native state, and include retained effective-rule hashes plus the text of any differing
run-local rules in its handoff. Bind the applicable rule-chain hash to every task
and attempt. The controller waits internally and emits periodic
non-model progress. Resume the exact request. Alternatively use
`execute --state STATE`; never recollect prepared evidence or overwrite an
accepted result. Use `plan` only for planning-only inspection.

For a batch, run `prepare-batch` once; it freezes selection and plans one
ordinary holistic child per selected thread. For the pending child returned by
`status-batch`, run `execute --state CHILD_STATE`, then pass its retained final
result to `advance-batch`. Repeat until the batch-summary phase, satisfy that
existing summary contract, advance it, and run `finalize-batch`. This preserves
the existing batch manifest and summary contracts and does not expose Luna
input parts, Sol review, direct-evidence inspection, or merge as public actions.
Never collect a child through a parallel controller or create a temporary
discovery script.

## Completion Gate

Complete only when controller status reports `complete: true` and retained
evidence contains the frozen manifest; the identity, byte accounting, and result
of every admitted Luna part and Sol task; one disposition for every retained
Luna candidate; every confirmed finding, plausible risk, temporary-control
review and merge, call classification, producer group, and ROI input; and the
exact inventory of every capacity omission. Label semantic coverage incomplete
when any omission exists.
For a batch, every selected child must also be finalized and indexed exactly
once before batch finalization succeeds.

## Output Contract

Start with coverage: completed runs and semantic run units; planned, reviewed,
and omitted run parts; evidence bytes reviewed and total; coverage percentage;
actual Luna and Sol calls; and one row per part with records, input bytes,
output allowance, actual output bytes, and status. For every omission, show
`Run | Part | Records | Evidence bytes | Candidate count | Output bytes |
Reason`. Do not render a capacity omission as zero findings or zero avoidable
calls.

First show this exact run table:

`Completed run | Total model calls | Avoidable calls - Fix Implemented |
Avoidable calls - Fix Unimplemented | Token usage (total; input % of total/cached
% of input/output % of total/reasoning output % of output)`.

Use each run's `started_at`, not its turn ID, and include a totals row. Show total
tokens as an integer and percentages to two decimal places; do not show raw
category token counts. Use numeric classification values only for reviewed
calls. When a run is wholly or partly omitted, state `not reviewed` or the
reviewed and capacity-omitted call counts in the affected cells rather than
zero.

For every still-unimplemented control, show this exact control table:

`Proposed control | Calls saved per affected run | Est. Percent of Affected
Similar Runs | Additional Calls per Affected Run for Implemented Fix | Est.
Calls Saving by Fix per Similar Run | New Complexity Introduced by Fix |
One-time implementation cost (model calls) | Recommendation`.

Retain every confirmed finding in machine evidence. Present every verified
unimplemented Minimal finding whose durable correction is one or two lines,
regardless of count, and every other unimplemented finding whose low-end
expected saving exceeds one model call per similar run. Follow the parent
plain-language `Problem` and `Fix` format. Present remaining confirmed controls
in the control table and counts without claiming they received deep review.

Before selecting the top three for extra verification, deduplicate by likely
owner/control. Rank deterministically by recurrence across runs, affected-call
count, evidence bytes, direct error/retry/user-correction sequence, identifiable
owner, then stable finding ID. Deeply verify and expand the top three, but do not
suppress any other qualifying finding.

Report confirmed input/output-volume waste even when it saves zero model calls,
but exclude it from call-savings arithmetic. For every such finding, report its
aggregate input, cached-input, output, tool-argument, and tool-result evidence;
state when none was confirmed.

Explain plausible risks under the parent contract. Also report necessary,
protocol-overhead, reviewed-no-confirmed-waste, and unassessed totals;
outstanding avoidable calls versus total calls; priced cost only when
available; and the retained analysis-result path.

For a batch, group similar findings across threads under plain-language problem
titles, apply the same ordering, identify affected threads, report per-thread
totals, and provide the retained batch result.
