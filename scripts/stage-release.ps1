param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string[]]$Branches,
    [string]$ReleaseBranch = "release/local",
    [switch]$Reset,
    [switch]$KeepMergedBranches
)

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
    throw "Runtime checkout is dirty; commit, stash, or discard unrelated changes before staging a release branch."
}

Invoke-Git "fetch" "--prune" "origin"

if (-not (Test-BranchExists "main")) {
    throw "Local main branch is required before staging $ReleaseBranch."
}

Invoke-Git "switch" "main"
Invoke-Git "merge" "--ff-only" "origin/main"

if ($Reset -and (Test-BranchExists $ReleaseBranch)) {
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
