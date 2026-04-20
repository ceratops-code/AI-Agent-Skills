Repo-specific rules for this repo:

- The primary runtime checkout that installed Ceratops skill junctions resolve to must stay on local `main` tracking `origin/main`.
- Do not develop or patch skills directly in the runtime checkout. For any task that modifies skills, create a separate git worktree in a different folder outside the runtime checkout, preferably in a sibling worktree root dedicated to `codex-skills` tasks.
- Temporary local skill junctions or other development-only runtime paths may point at a worktree during the task, but they must be switched back to the runtime checkout and cleaned up before completion.
- Before closing any skill-modifying task, merge the result into `main`, update the runtime checkout to local `main` and `origin/main`, verify installed skills resolve to the runtime checkout, and remove the temporary worktree and branch unless there is an explicit reason to keep them.
