[CmdletBinding()]
param(
    [string]$RuntimeRepoRoot,
    [string]$MainBranch = "main",
    [string]$ReleaseBranch = "release/local",
    [switch]$DropReleaseBranch
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

$status = Get-GitOutput @("status", "--porcelain")
if (-not [string]::IsNullOrWhiteSpace($status)) {
    throw "Runtime checkout '$resolvedRuntimeRepoRoot' has uncommitted changes. Clean or commit them before restoring main."
}

Invoke-Git @("checkout", $MainBranch)
Invoke-Git @("pull", "--ff-only", "origin", $MainBranch)

if ($DropReleaseBranch) {
    & git -C $resolvedRuntimeRepoRoot show-ref --verify --quiet "refs/heads/$ReleaseBranch"
    if ($LASTEXITCODE -eq 0) {
        & git -C $resolvedRuntimeRepoRoot merge-base --is-ancestor $ReleaseBranch $MainBranch
        $branchIsMerged = ($LASTEXITCODE -eq 0)
        $treesMatch = $false

        if (-not $branchIsMerged) {
            & git -C $resolvedRuntimeRepoRoot diff --quiet $MainBranch $ReleaseBranch
            $treesMatch = ($LASTEXITCODE -eq 0)
        }

        if ($branchIsMerged -or $treesMatch) {
            Invoke-Git @("branch", "-D", $ReleaseBranch)
        }
        else {
            throw "Release branch '$ReleaseBranch' is neither merged into '$MainBranch' nor tree-identical to it."
        }
    }
}

& powershell -ExecutionPolicy Bypass -File (Join-Path $resolvedRuntimeRepoRoot "scripts\install-skills.ps1") -RepoRoot $resolvedRuntimeRepoRoot
if ($LASTEXITCODE -ne 0) {
    throw "Runtime installer failed after restoring '$MainBranch'."
}

$activeBranch = Get-GitOutput @("branch", "--show-current")
$head = Get-GitOutput @("rev-parse", "HEAD")

Write-Host "Runtime checkout restored to: $activeBranch"
Write-Host "HEAD: $head"
