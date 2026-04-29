[CmdletBinding()]
param(
    [string]$RuntimeRepoRoot,
    [string]$MainBranch = "main",
    [string]$ReleaseBranch = "release/local",
    [switch]$DropReleaseBranch,
    [switch]$KeepReleaseBranch
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ($MainBranch -ne "main") {
    throw "The centralized restore-runtime-main helper supports only the main branch."
}

if ([string]::IsNullOrWhiteSpace($RuntimeRepoRoot)) {
    $RuntimeRepoRoot = Join-Path $PSScriptRoot "..\..\.."
}

$resolvedRuntimeRepoRoot = (Resolve-Path -LiteralPath $RuntimeRepoRoot).Path
$scriptPath = Join-Path $resolvedRuntimeRepoRoot "scripts\restore-runtime-main.ps1"
if (-not (Test-Path -LiteralPath $scriptPath)) {
    throw "Could not find centralized runtime restore helper at '$scriptPath'."
}

$arguments = @("-MainBranch", $MainBranch, "-ReleaseBranch", $ReleaseBranch)
if ($DropReleaseBranch) {
    $arguments += "-DropReleaseBranch"
}
if ($KeepReleaseBranch) {
    $arguments += "-KeepReleaseBranch"
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
