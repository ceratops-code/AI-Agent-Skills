[CmdletBinding()]
param(
    [string]$RuntimeRepoRoot,
    [string]$MainBranch = "main",
    [string]$ReleaseBranch = "release/local",
    [string[]]$StagedBranches = @()
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($RuntimeRepoRoot)) {
    $RuntimeRepoRoot = Join-Path $PSScriptRoot "..\..\.."
}

$resolvedRuntimeRepoRoot = (Resolve-Path -LiteralPath $RuntimeRepoRoot).Path
$scriptPath = Join-Path $resolvedRuntimeRepoRoot "scripts\check-pending-release-work.ps1"
if (-not (Test-Path -LiteralPath $scriptPath)) {
    throw "Could not find centralized pending-work helper at '$scriptPath'."
}

& $scriptPath -RuntimeRepoRoot $resolvedRuntimeRepoRoot -MainBranch $MainBranch -ReleaseBranch $ReleaseBranch -StagedBranches $StagedBranches
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
