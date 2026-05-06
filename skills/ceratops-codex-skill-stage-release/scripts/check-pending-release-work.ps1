[CmdletBinding()]
param(
    [string]$SkillsRepoRoot,
    [string]$MainBranch = "main",
    [string]$ReleaseBranch = "release/local",
    [string[]]$StagedBranches = @()
)

# Skill-local helper called only by ceratops-codex-skill-stage-release before a
# staged skills repo release is treated as ready to ship. It is intentionally
# read-only: it reports dirty worktrees or local branches that have commits not
# reachable from the release branch, but it never cleans them up or changes Git
# state.

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($SkillsRepoRoot)) {
    # The installed skill copy lives outside the skills repo checkout, so the safest
    # default is the caller's current checkout. The skill tells agents to run
    # this from the skills repo checkout or pass -SkillsRepoRoot explicitly.
    $SkillsRepoRoot = (Get-Location).Path
}

$resolvedSkillsRepoRoot = (Resolve-Path -LiteralPath $SkillsRepoRoot).Path

function Invoke-Git {
    param([string[]]$Arguments)

    $null = & git -C $resolvedSkillsRepoRoot @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "git failed: $($Arguments -join ' ')"
    }
}

function Get-GitLines {
    param([string[]]$Arguments)

    $output = & git -C $resolvedSkillsRepoRoot @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "git failed: $($Arguments -join ' ')"
    }
    return @($output)
}

function Get-WorktreeRecords {
    # Parse porcelain output into records so the staged-release skill can detect
    # other local worktrees that still carry dirty or unstaged work.
    $records = @()
    $current = @{}

    foreach ($line in Get-GitLines @("worktree", "list", "--porcelain")) {
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

    return $records
}

function Convert-BranchRefToName {
    param([string]$BranchRef)

    $prefix = "refs/heads/"
    if ($BranchRef.StartsWith($prefix, [StringComparison]::Ordinal)) {
        return $BranchRef.Substring($prefix.Length)
    }
    return $BranchRef
}

function Test-IsExcludedBranch {
    param([string]$BranchName)

    if ([string]::IsNullOrWhiteSpace($BranchName)) {
        return $false
    }
    # Main, the active release branch, and the branches explicitly staged into
    # that release are expected. Every other branch is suspicious if it has
    # commits that are not reachable from the release branch.
    if ($BranchName -eq $MainBranch -or $BranchName -eq $ReleaseBranch) {
        return $true
    }
    return $StagedBranches -contains $BranchName
}

Invoke-Git @("rev-parse", "--verify", $ReleaseBranch)

$findings = @()
$skillsRepoPath = $resolvedSkillsRepoRoot.TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)

foreach ($record in Get-WorktreeRecords) {
    $worktreePath = (Resolve-Path -LiteralPath $record.worktree).Path
    $normalizedWorktreePath = $worktreePath.TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
    if ($normalizedWorktreePath -ieq $skillsRepoPath) {
        continue
    }

    $branchName = "(detached)"
    if ($record.PSObject.Properties.Name -contains "branch") {
        $branchName = Convert-BranchRefToName $record.branch
    }

    # Dirty worktrees outside the skills repo checkout are reported before shipping
    # so they are either staged, intentionally retained, or cleaned up.
    $status = @(& git -C $worktreePath status --porcelain)
    if ($LASTEXITCODE -ne 0) {
        throw "git failed: status --porcelain in $worktreePath"
    }
    if ($status.Count -gt 0) {
        $findings += [pscustomobject]@{
            Kind = "dirty_worktree"
            Branch = $branchName
            Path = $worktreePath
            Detail = "$($status.Count) status entr$(if ($status.Count -eq 1) { 'y' } else { 'ies' })"
        }
    }
}

foreach ($branchName in Get-GitLines @("for-each-ref", "--format=%(refname:short)", "refs/heads")) {
    if (Test-IsExcludedBranch $branchName) {
        continue
    }

    # Count commits that would be left behind if the release branch shipped now.
    $aheadText = (Get-GitLines @("rev-list", "--count", "$ReleaseBranch..$branchName") | Select-Object -First 1).Trim()
    $aheadCount = [int]$aheadText
    if ($aheadCount -gt 0) {
        $findings += [pscustomobject]@{
            Kind = "unmerged_branch_commits"
            Branch = $branchName
            Path = ""
            Detail = "$aheadCount commit$(if ($aheadCount -eq 1) { '' } else { 's' }) not in $ReleaseBranch"
        }
    }
}

if ($findings.Count -eq 0) {
    Write-Host "No pending local work outside '$ReleaseBranch' was found."
    exit 0
}

Write-Host "Pending local work outside '$ReleaseBranch' was found:"
$findings | Sort-Object Kind, Branch, Path | Format-Table -AutoSize
exit 2
