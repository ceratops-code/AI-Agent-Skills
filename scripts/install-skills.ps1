[CmdletBinding()]
param(
    [string]$RepoRoot,
    [string]$RuntimeRoot,
    [string]$PythonCommand
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($RepoRoot)) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}

if ([string]::IsNullOrWhiteSpace($RuntimeRoot)) {
    $RuntimeRoot = Join-Path $env:USERPROFILE ".codex\skills"
}

function Resolve-PythonCommand {
    param([string]$Preferred)

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

function Resolve-LinkTarget {
    param([System.IO.FileSystemInfo]$Item)

    $target = $Item.Target
    if ($target -is [System.Array]) {
        return [string]$target[0]
    }
    return [string]$target
}

function Ensure-Junction {
    param(
        [string]$Path,
        [string]$Target
    )

    $resolvedTarget = (Resolve-Path -LiteralPath $Target).Path
    if (Test-Path -LiteralPath $Path) {
        $item = Get-Item -LiteralPath $Path -Force
        if (-not (Is-ReparsePoint $item)) {
            throw "Install path '$Path' already exists and is not a junction."
        }

        $existingTarget = Resolve-LinkTarget $item
        if ($existingTarget) {
            try {
                $resolvedExistingTarget = (Resolve-Path -LiteralPath $existingTarget).Path
                if ($resolvedExistingTarget -eq $resolvedTarget) {
                    return
                }
            } catch {
            }
        }

        Remove-Item -LiteralPath $Path -Force
    }

    New-Item -ItemType Junction -Path $Path -Target $resolvedTarget | Out-Null
}

$resolvedRepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
if (-not (Test-Path -LiteralPath $RuntimeRoot)) {
    New-Item -ItemType Directory -Path $RuntimeRoot | Out-Null
}

$python = Resolve-PythonCommand $PythonCommand
& $python -m pip uninstall --yes ceratops-gh-runtime | Out-Null
& $python -m pip install --editable $resolvedRepoRoot
if ($LASTEXITCODE -ne 0) {
    throw "Editable helper-package install failed."
}

$editablePackages = (& $python -m pip list --editable --format=json | ConvertFrom-Json)
if ($LASTEXITCODE -ne 0) {
    throw "Could not verify the installed GH helper package mode."
}
$editablePackage = $editablePackages | Where-Object { $_.name -eq "ceratops-gh-runtime" } | Select-Object -First 1
if ($null -eq $editablePackage) {
    throw "Installed GH helper package is not registered as editable."
}
if ($editablePackage.editable_project_location -ne $resolvedRepoRoot) {
    throw "Installed GH helper package does not point at the requested checkout."
}

$staleRuntimeSkill = Join-Path $RuntimeRoot "ceratops-gh-runtime"
if (Test-Path -LiteralPath $staleRuntimeSkill) {
    $staleItem = Get-Item -LiteralPath $staleRuntimeSkill -Force
    if (-not (Is-ReparsePoint $staleItem)) {
        throw "Stale runtime skill path '$staleRuntimeSkill' exists and is not a junction."
    }
    Remove-Item -LiteralPath $staleRuntimeSkill -Force
}

$skillsRoot = Join-Path $resolvedRepoRoot "skills"
$skills = Get-ChildItem -LiteralPath $skillsRoot -Directory | Sort-Object Name
foreach ($skill in $skills) {
    $link = Join-Path $RuntimeRoot $skill.Name
    Ensure-Junction -Path $link -Target $skill.FullName
}

Write-Host "Installed Ceratops skills and local GH helper package."
