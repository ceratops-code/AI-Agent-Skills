[CmdletBinding()]
param(
    [string]$RuntimeRepoRoot,
    [string]$MainBranch = "main",
    [string]$ReleaseBranch = "release/local",
    [string[]]$MergeBranches = @(),
    [switch]$Reset
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
    throw "Runtime checkout '$resolvedRuntimeRepoRoot' has uncommitted changes. Clean or commit them before staging a release branch."
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

foreach ($mergeBranch in $MergeBranches) {
    if ([string]::IsNullOrWhiteSpace($mergeBranch)) {
        continue
    }

    Invoke-Git @("rev-parse", "--verify", $mergeBranch)
    Invoke-Git @("merge", "--no-ff", "--no-edit", $mergeBranch)
}

$activeBranch = Get-GitOutput @("branch", "--show-current")
$head = Get-GitOutput @("rev-parse", "HEAD")

Write-Host "Active release branch: $activeBranch"
Write-Host "HEAD: $head"
