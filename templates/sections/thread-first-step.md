<!-- INTERNAL: include in thread-handoff skills -->

## First-Step State Refresh

- Reuse fresh state already established in the current thread by default.
- Refresh only facts whose staleness would change or misdirect the first step in the new thread.
- Keep refs exact but limited to the entities the next thread is likely to open first.
