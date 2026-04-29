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

if ($MainBranch -ne "main") {
    throw "The centralized stage-release helper supports only the main branch."
}

if ([string]::IsNullOrWhiteSpace($RuntimeRepoRoot)) {
    $RuntimeRepoRoot = Join-Path $PSScriptRoot "..\..\.."
}

$resolvedRuntimeRepoRoot = (Resolve-Path -LiteralPath $RuntimeRepoRoot).Path
$scriptPath = Join-Path $resolvedRuntimeRepoRoot "scripts\stage-release.ps1"
if (-not (Test-Path -LiteralPath $scriptPath)) {
    throw "Could not find centralized staging helper at '$scriptPath'."
}

$arguments = @()
$arguments += $MergeBranches
$arguments += @("-ReleaseBranch", $ReleaseBranch)
if ($Reset) {
    $arguments += "-Reset"
}
if ($KeepMergedBranches) {
    $arguments += "-KeepMergedBranches"
}

Push-Location -LiteralPath $resolvedRuntimeRepoRoot
try {
    & $scriptPath @arguments
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}
finally {
    Pop-Location
}
