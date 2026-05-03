# Restore the runtime checkout to main after a staged skill release is shipped.
# The script also reruns the copy-based installer so installed skills match the
# restored runtime checkout instead of an unpublished release branch.
param(
    [string]$MainBranch = "main",
    [string]$ReleaseBranch = "release/local",
    [switch]$DropReleaseBranch,
    [switch]$KeepReleaseBranch
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

$repoRoot = (Get-GitOutput "rev-parse" "--show-toplevel" | Select-Object -First 1).Trim()
Set-Location -LiteralPath $repoRoot

$status = Get-GitOutput "status" "--porcelain"
if ($status) {
    # A dirty runtime checkout could contain unpublished edits. Stop before
    # switching branches or deleting release-branch state.
    throw "Runtime checkout is dirty; commit, stash, or discard unrelated changes before restoring main."
}

Invoke-Git "fetch" "--prune" "origin"
Invoke-Git "switch" $MainBranch
Invoke-Git "merge" "--ff-only" "origin/$MainBranch"

if (($DropReleaseBranch -or -not $KeepReleaseBranch) -and (Test-BranchExists $ReleaseBranch)) {
    # A squash merge leaves the release branch not literally merged but often
    # tree-identical to main. In either case the local preview branch is stale
    # and can be removed unless the caller explicitly keeps it.
    & git merge-base --is-ancestor $ReleaseBranch $MainBranch
    $merged = $LASTEXITCODE -eq 0

    & git diff --quiet $MainBranch $ReleaseBranch
    $treeIdentical = $LASTEXITCODE -eq 0

    if ($merged -or $treeIdentical) {
        if ($merged) {
            Invoke-Git "branch" "-d" $ReleaseBranch
        } else {
            Invoke-Git "branch" "-D" $ReleaseBranch
        }
    }
}

$installer = Join-Path $repoRoot "scripts/install-skills.ps1"
if (-not (Test-Path -LiteralPath $installer)) {
    throw "Missing runtime installer: $installer"
}

& powershell -ExecutionPolicy Bypass -File $installer
if ($LASTEXITCODE -ne 0) {
    throw "runtime installer failed with exit code $LASTEXITCODE"
}

Invoke-Git "status" "--short" "--branch"
