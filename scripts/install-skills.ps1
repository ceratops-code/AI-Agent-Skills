[CmdletBinding()]
param(
    [string]$RepoRoot,
    [string]$RuntimeRoot,
    [string]$PythonCommand,
    [string[]]$Skill
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($RepoRoot)) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}

if ([string]::IsNullOrWhiteSpace($RuntimeRoot)) {
    $codexHome = $env:CODEX_HOME
    if ([string]::IsNullOrWhiteSpace($codexHome)) {
        $codexHome = Join-Path $env:USERPROFILE ".codex"
    }
    $RuntimeRoot = Join-Path $codexHome "skills"
}

function Resolve-PythonCommand {
    param([string]$Preferred)

    # Prefer an explicit interpreter path when the caller provides one, then
    # fall back to the normal launcher names. The installer avoids activating a
    # virtualenv because the Codex runtime skill install should be reproducible
    # from a plain shell.
    if (-not [string]::IsNullOrWhiteSpace($Preferred) -and (Test-Path -LiteralPath $Preferred)) {
        return (Resolve-Path -LiteralPath $Preferred).Path
    }

    foreach ($candidate in @($Preferred, "python", "py")) {
        if ([string]::IsNullOrWhiteSpace($candidate)) {
            continue
        }

        $command = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($null -ne $command) {
            if ($command.Source) {
                return $command.Source
            }
            if ($command.Path) {
                return $command.Path
            }
            return $command.Name
        }
    }

    throw "Could not find a usable Python command. Install Python or pass -PythonCommand."
}

function Is-ReparsePoint {
    param([System.IO.FileSystemInfo]$Item)

    return [bool]($Item.Attributes -band [System.IO.FileAttributes]::ReparsePoint)
}

function Remove-ReparsePoint {
    param([string]$Path)

    # Older installs used directory junctions. The new runtime model uses
    # managed copies, so it is safe to remove a reparse point but unsafe to
    # delete an ordinary directory that may contain user-managed files.
    $item = Get-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
    if ($null -eq $item) {
        return
    }

    $looksLikeBrokenDirectoryLink = $item.PSIsContainer -and $item.Exists -eq $false
    if (-not (Is-ReparsePoint $item) -and -not $looksLikeBrokenDirectoryLink) {
        throw "Path '$Path' exists and is not a reparse point."
    }

    if ($item.PSIsContainer) {
        [System.IO.Directory]::Delete($Path)
        return
    }

    [System.IO.File]::Delete($Path)
}

function Remove-ExistingRuntimeLinks {
    param(
        [string]$RuntimeRoot,
        [string[]]$SkillNames
    )

    # Migration path from the old install model: remove reparse points for the
    # skills being rebuilt, and remove stale helper skill links that were never
    # real user-facing skills. Ordinary directories are left for the Python
    # builder, which only replaces folders marked with its runtime manifest.
    foreach ($skillName in $SkillNames) {
        $runtimeSkill = Join-Path $RuntimeRoot $skillName
        $item = Get-Item -LiteralPath $runtimeSkill -Force -ErrorAction SilentlyContinue
        if ($null -ne $item -and (Is-ReparsePoint $item)) {
            Remove-ReparsePoint -Path $runtimeSkill
        }
    }

    foreach ($staleRuntimeSkillName in @("ceratops-gh-current-state", "ceratops-gh-runtime")) {
        $staleRuntimeSkill = Join-Path $RuntimeRoot $staleRuntimeSkillName
        $staleItem = Get-Item -LiteralPath $staleRuntimeSkill -Force -ErrorAction SilentlyContinue
        if ($null -ne $staleItem -and (Is-ReparsePoint $staleItem)) {
            Remove-ReparsePoint -Path $staleRuntimeSkill
        }
    }
}

$resolvedRepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
$skillsRoot = Join-Path $resolvedRepoRoot "skills"
$builder = Join-Path $resolvedRepoRoot "scripts\build-runtime-skills.py"
if (-not (Test-Path -LiteralPath $skillsRoot -PathType Container)) {
    throw "Missing skills directory: $skillsRoot"
}
if (-not (Test-Path -LiteralPath $builder -PathType Leaf)) {
    throw "Missing runtime skill builder: $builder"
}
if (-not (Test-Path -LiteralPath $RuntimeRoot)) {
    New-Item -ItemType Directory -Path $RuntimeRoot | Out-Null
}

$python = Resolve-PythonCommand $PythonCommand

$sourceSkillNames = Get-ChildItem -LiteralPath $skillsRoot -Directory |
    Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md") } |
    Sort-Object Name |
    ForEach-Object { $_.Name }

$buildSkillNames = @()
if ($null -ne $Skill -and $Skill.Count -gt 0) {
    $known = @{}
    foreach ($skillName in $sourceSkillNames) {
        $known[$skillName] = $true
    }
    foreach ($skillName in $Skill) {
        if (-not $known.ContainsKey($skillName)) {
            throw "Unknown skill: $skillName"
        }
        $buildSkillNames += $skillName
    }
} else {
    $buildSkillNames = $sourceSkillNames
}

Remove-ExistingRuntimeLinks -RuntimeRoot $RuntimeRoot -SkillNames $buildSkillNames

$builderArgs = @($builder, "--runtime-root", $RuntimeRoot)
foreach ($skillName in $buildSkillNames) {
    $builderArgs += @("--skill", $skillName)
}
if ($buildSkillNames.Count -eq $sourceSkillNames.Count) {
    # Only full installs remove stale managed skill folders. A targeted skill
    # install should not clean up unrelated managed skills that may belong to an
    # active preview workflow.
    $builderArgs += "--remove-stale"
}

$buildOutput = & $python @builderArgs 2>&1
if ($LASTEXITCODE -ne 0) {
    if ($buildOutput) {
        $buildOutput | ForEach-Object { Write-Error $_ }
    }
    throw "Runtime skill build failed."
}

Write-Output "installed"
