# Stage committed task branches into the runtime checkout's local release branch.
# This script is intentionally limited to git worktree/branch mechanics; skill
# rendering still belongs to scripts/install-skills.ps1 after staging completes.
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string[]]$Branches,
    [string]$ReleaseBranch = "release/local",
    [switch]$Reset,
    [switch]$KeepMergedBranches
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-Git {
    param(
        [Parameter(Mandatory = $true, ValueFromRemainingArguments = $true)]
        [string[]]$Arguments
    )

    & git @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "git $($Arguments -join ' ') failed with exit code $LASTEXITCODE"
    }
}

function Get-GitOutput {
    param(
        [Parameter(Mandatory = $true, ValueFromRemainingArguments = $true)]
        [string[]]$Arguments
    )

    $output = & git @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "git $($Arguments -join ' ') failed with exit code $LASTEXITCODE"
    }
    return $output
}

function Test-BranchExists {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Branch
    )

    & git show-ref --verify --quiet "refs/heads/$Branch"
    return $LASTEXITCODE -eq 0
}

function Get-WorktreePathForBranch {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Branch
    )

    # `git worktree list --porcelain` emits records split across lines. Track
    # the current record's path so the matching branch can be removed after a
    # successful merge without guessing from folder names.
    $targetRef = "refs/heads/$Branch"
    $currentPath = $null
    foreach ($line in Get-GitOutput "worktree" "list" "--porcelain") {
        if ($line.StartsWith("worktree ")) {
            $currentPath = $line.Substring("worktree ".Length)
            continue
        }
        if ($line -eq "branch $targetRef") {
            return $currentPath
        }
    }

    return $null
}

$repoRoot = (Get-GitOutput "rev-parse" "--show-toplevel" | Select-Object -First 1).Trim()
Set-Location -LiteralPath $repoRoot

$status = Get-GitOutput "status" "--porcelain"
if ($status) {
    # Refuse to merge task branches into a dirty runtime checkout because the
    # release branch is supposed to represent only committed source branches.
    throw "Runtime checkout is dirty; commit, stash, or discard unrelated changes before staging a release branch."
}

Invoke-Git "fetch" "--prune" "origin"

if (-not (Test-BranchExists "main")) {
    throw "Local main branch is required before staging $ReleaseBranch."
}

Invoke-Git "switch" "main"
Invoke-Git "merge" "--ff-only" "origin/main"

if ($Reset -and (Test-BranchExists $ReleaseBranch)) {
    # `-Reset` is the explicit escape hatch for rebuilding the local preview
    # branch from main instead of trying to untangle partial staged state.
    Invoke-Git "branch" "-D" $ReleaseBranch
}

if (Test-BranchExists $ReleaseBranch) {
    Invoke-Git "switch" $ReleaseBranch
    Invoke-Git "merge" "--ff-only" "main"
} else {
    Invoke-Git "switch" "-c" $ReleaseBranch "main"
}

foreach ($branch in $Branches) {
    if (-not (Test-BranchExists $branch)) {
        throw "Task branch '$branch' does not exist."
    }

    Invoke-Git "merge" "--no-edit" $branch

    if (-not $KeepMergedBranches) {
        # After a successful merge, remove the source task worktree and branch
        # so stale local state cannot be mistaken for work still outside the
        # staged release batch.
        $worktreePath = Get-WorktreePathForBranch $branch
        if ($worktreePath) {
            $resolvedRepo = (Resolve-Path -LiteralPath $repoRoot).Path
            $resolvedWorktree = (Resolve-Path -LiteralPath $worktreePath).Path
            if ($resolvedWorktree -eq $resolvedRepo) {
                throw "Refusing to remove runtime checkout while cleaning task branch '$branch'."
            }
            Invoke-Git "worktree" "remove" $worktreePath
        }
        Invoke-Git "branch" "-d" $branch
    }
}

Invoke-Git "status" "--short" "--branch"
