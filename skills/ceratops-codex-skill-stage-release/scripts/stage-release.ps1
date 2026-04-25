[CmdletBinding()]
param(
    [string]$RuntimeRepoRoot,
    [string]$MainBranch = "main",
    [string]$ReleaseBranch = "release/local",
    [string[]]$MergeBranches = @(),
    [switch]$Reset,
    [switch]$KeepMergedBranches
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($RuntimeRepoRoot)) {
    $RuntimeRepoRoot = Join-Path $env:USERPROFILE "CodexProjects\CeratopsSkills\codex-skills"
}

$resolvedRuntimeRepoRoot = (Resolve-Path -LiteralPath $RuntimeRepoRoot).Path

function Invoke-Git {
    param([string[]]$Arguments)

    & git -C $resolvedRuntimeRepoRoot @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "git failed: $($Arguments -join ' ')"
    }
}

function Get-GitOutput {
    param([string[]]$Arguments)

    $output = & git -C $resolvedRuntimeRepoRoot @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "git failed: $($Arguments -join ' ')"
    }
    return ($output -join "`n").Trim()
}

function Test-LocalBranch {
    param([string]$BranchName)

    & git -C $resolvedRuntimeRepoRoot show-ref --verify --quiet "refs/heads/$BranchName"
    return ($LASTEXITCODE -eq 0)
}

function Get-WorktreePathForBranch {
    param([string]$BranchName)

    $branchRef = "refs/heads/$BranchName"
    $current = @{}
    $records = @()

    $lines = & git -C $resolvedRuntimeRepoRoot worktree list --porcelain
    if ($LASTEXITCODE -ne 0) {
        throw "git failed: worktree list --porcelain"
    }

    foreach ($line in $lines) {
        if ([string]::IsNullOrWhiteSpace($line)) {
            if ($current.ContainsKey("worktree")) {
                $records += [pscustomobject]$current
            }
            $current = @{}
            continue
        }

        $parts = $line.Split(" ", 2)
        if ($parts.Count -lt 2) {
            continue
        }
        $current[$parts[0]] = $parts[1]
    }

    if ($current.ContainsKey("worktree")) {
        $records += [pscustomobject]$current
    }

    foreach ($record in $records) {
        if ($record.PSObject.Properties.Name -contains "branch" -and $record.branch -eq $branchRef) {
            return $record.worktree
        }
    }

    return $null
}

function Test-IsUnderPath {
    param(
        [string]$Path,
        [string]$ParentPath
    )

    $resolvedPath = (Resolve-Path -LiteralPath $Path).Path.TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
    $resolvedParent = (Resolve-Path -LiteralPath $ParentPath).Path.TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
    $prefix = $resolvedParent + [IO.Path]::DirectorySeparatorChar
    return $resolvedPath.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)
}

$status = Get-GitOutput @("status", "--porcelain")
if (-not [string]::IsNullOrWhiteSpace($status)) {
    throw "Runtime checkout '$resolvedRuntimeRepoRoot' has uncommitted changes. Clean or commit them before staging a release branch."
}

& git -C $resolvedRuntimeRepoRoot remote get-url origin *> $null
if ($LASTEXITCODE -eq 0) {
    Invoke-Git @("fetch", "--prune", "origin")
}

Invoke-Git @("rev-parse", "--verify", $MainBranch)

& git -C $resolvedRuntimeRepoRoot show-ref --verify --quiet "refs/heads/$ReleaseBranch"
$releaseExists = ($LASTEXITCODE -eq 0)

if ($Reset) {
    Invoke-Git @("checkout", $MainBranch)
    Invoke-Git @("branch", "-f", $ReleaseBranch, $MainBranch)
    $releaseExists = $true
}

if (-not $releaseExists) {
    Invoke-Git @("checkout", "-b", $ReleaseBranch, $MainBranch)
}
else {
    Invoke-Git @("checkout", $ReleaseBranch)
}

$cleanupTargets = @()
foreach ($mergeBranch in $MergeBranches) {
    if ([string]::IsNullOrWhiteSpace($mergeBranch)) {
        continue
    }

    Invoke-Git @("rev-parse", "--verify", $mergeBranch)
    $isLocalBranch = Test-LocalBranch $mergeBranch
    $worktreePath = $null
    if ($isLocalBranch) {
        $worktreePath = Get-WorktreePathForBranch $mergeBranch
    }

    Invoke-Git @("merge", "--no-ff", "--no-edit", $mergeBranch)

    if ($isLocalBranch -and $mergeBranch -ne $MainBranch -and $mergeBranch -ne $ReleaseBranch) {
        $cleanupTargets += [pscustomobject]@{
            Branch = $mergeBranch
            WorktreePath = $worktreePath
        }
    }
}

if (-not $KeepMergedBranches) {
    $projectRoot = Split-Path -Parent $resolvedRuntimeRepoRoot
    $projectWorktreesRoot = Join-Path $projectRoot "worktrees"

    foreach ($target in $cleanupTargets) {
        if (-not [string]::IsNullOrWhiteSpace($target.WorktreePath)) {
            $resolvedWorktreePath = (Resolve-Path -LiteralPath $target.WorktreePath).Path
            if ($resolvedWorktreePath -ieq $resolvedRuntimeRepoRoot) {
                throw "Refusing to remove runtime checkout worktree for branch '$($target.Branch)'."
            }
            if (-not (Test-Path -LiteralPath $projectWorktreesRoot)) {
                throw "Expected project worktree root '$projectWorktreesRoot' before removing '$resolvedWorktreePath'."
            }
            if (-not (Test-IsUnderPath -Path $resolvedWorktreePath -ParentPath $projectWorktreesRoot)) {
                throw "Refusing to remove worktree outside '$projectWorktreesRoot': $resolvedWorktreePath"
            }
            Invoke-Git @("worktree", "remove", $resolvedWorktreePath)
        }

        Invoke-Git @("branch", "-d", $target.Branch)
    }
}

$activeBranch = Get-GitOutput @("branch", "--show-current")
$head = Get-GitOutput @("rev-parse", "HEAD")

Write-Host "Active release branch: $activeBranch"
Write-Host "HEAD: $head"
