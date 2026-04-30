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

function Remove-ReparsePoint {
    param([string]$Path)

    $item = Get-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
    if ($null -eq $item) {
        return
    }

    $looksLikeBrokenDirectoryLink = $item.PSIsContainer -and $item.Exists -eq $false
    if (-not (Is-ReparsePoint $item) -and -not $looksLikeBrokenDirectoryLink) {
        throw "Path '$Path' exists and is not a junction."
    }

    if ($item.PSIsContainer) {
        [System.IO.Directory]::Delete($Path)
        return
    }

    [System.IO.File]::Delete($Path)
}

function Remove-GeneratedEggInfo {
    param([string]$RepoRoot)

    foreach ($searchRoot in @($RepoRoot, (Join-Path $RepoRoot "src"))) {
        if (-not (Test-Path -LiteralPath $searchRoot)) {
            continue
        }

        Get-ChildItem -LiteralPath $searchRoot -Directory -Filter *.egg-info -Force -ErrorAction SilentlyContinue |
            ForEach-Object {
                Remove-Item -LiteralPath $_.FullName -Recurse -Force
            }
    }
}

function Ensure-Junction {
    param(
        [string]$Path,
        [string]$Target
    )

    $resolvedTarget = (Resolve-Path -LiteralPath $Target).Path
    $item = Get-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
    if ($null -ne $item) {
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

        Remove-ReparsePoint -Path $Path
    }

    New-Item -ItemType Junction -Path $Path -Target $resolvedTarget | Out-Null
}

function Ensure-SkillIcon {
    param(
        [string]$RepoRoot,
        [string]$SkillRoot
    )

    $sourceIcon = Join-Path $RepoRoot "assets\ceratops-logo-500.png"
    if (-not (Test-Path -LiteralPath $sourceIcon -PathType Leaf)) {
        throw "Missing shared Ceratops icon: $sourceIcon"
    }

    $skillAssets = Join-Path $SkillRoot "assets"
    $assetsItem = Get-Item -LiteralPath $skillAssets -Force -ErrorAction SilentlyContinue
    if ($null -eq $assetsItem) {
        New-Item -ItemType Directory -Path $skillAssets | Out-Null
    } elseif (-not $assetsItem.PSIsContainer) {
        throw "Skill assets path '$skillAssets' exists and is not a directory."
    }

    $targetIcon = Join-Path $skillAssets "ceratops-logo-500.png"
    $shouldCopy = -not (Test-Path -LiteralPath $targetIcon -PathType Leaf)
    if (-not $shouldCopy) {
        $sourceHash = (Get-FileHash -LiteralPath $sourceIcon -Algorithm SHA256).Hash
        $targetHash = (Get-FileHash -LiteralPath $targetIcon -Algorithm SHA256).Hash
        $shouldCopy = $sourceHash -ne $targetHash
    }

    if ($shouldCopy) {
        Copy-Item -LiteralPath $sourceIcon -Destination $targetIcon -Force
    }
}

$resolvedRepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
if (-not (Test-Path -LiteralPath $RuntimeRoot)) {
    New-Item -ItemType Directory -Path $RuntimeRoot | Out-Null
}

$python = Resolve-PythonCommand $PythonCommand
$previousPipDisableVersionCheck = $env:PIP_DISABLE_PIP_VERSION_CHECK
$env:PIP_DISABLE_PIP_VERSION_CHECK = "1"
$helperPackageNames = @("ceratops-gh-current-state", "ceratops-gh-runtime")
try {
    $installedPackagesJson = & $python -m pip list --format=json 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Could not list currently installed Python packages."
    }
    $installedPackages = $installedPackagesJson | ConvertFrom-Json
    $installedPackageNames = @{}
    foreach ($package in $installedPackages) {
        if ($null -ne $package.name) {
            $installedPackageNames[[string]$package.name] = $true
        }
    }
    foreach ($helperPackage in $helperPackageNames) {
        if ($installedPackageNames.ContainsKey($helperPackage)) {
            & $python -m pip uninstall --yes $helperPackage *> $null
        }
    }
    $installOutput = & $python -m pip install --editable $resolvedRepoRoot 2>&1
    if ($LASTEXITCODE -ne 0) {
        if ($installOutput) {
            $installOutput | ForEach-Object { Write-Error $_ }
        }
        throw "Editable helper-package install failed."
    }

    $editablePackageShow = & $python -m pip show ceratops-gh-current-state 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Could not inspect the installed GH helper package."
    }
    $editableProjectLocationLine = $editablePackageShow | Where-Object { $_ -like "Editable project location:*" } | Select-Object -First 1
    if ([string]::IsNullOrWhiteSpace($editableProjectLocationLine)) {
        throw "Installed GH helper package is not registered as editable."
    }
    $editableProjectLocation = $editableProjectLocationLine.Substring("Editable project location:".Length).Trim()
    if ($editableProjectLocation -ne $resolvedRepoRoot) {
        throw "Installed GH helper package does not point at the requested checkout."
    }
}
finally {
    if ($null -eq $previousPipDisableVersionCheck) {
        Remove-Item Env:\PIP_DISABLE_PIP_VERSION_CHECK -ErrorAction SilentlyContinue
    } else {
        $env:PIP_DISABLE_PIP_VERSION_CHECK = $previousPipDisableVersionCheck
    }
    Remove-GeneratedEggInfo -RepoRoot $resolvedRepoRoot
}

foreach ($staleRuntimeSkillName in @("ceratops-gh-current-state", "ceratops-gh-runtime")) {
    $staleRuntimeSkill = Join-Path $RuntimeRoot $staleRuntimeSkillName
    $staleItem = Get-Item -LiteralPath $staleRuntimeSkill -Force -ErrorAction SilentlyContinue
    if ($null -ne $staleItem) {
        $looksLikeBrokenDirectoryLink = $staleItem.PSIsContainer -and $staleItem.Exists -eq $false
        if (-not (Is-ReparsePoint $staleItem)) {
            if (-not $looksLikeBrokenDirectoryLink) {
                throw "Stale runtime skill path '$staleRuntimeSkill' exists and is not a junction."
            }
        }
        Remove-ReparsePoint -Path $staleRuntimeSkill
    }
}

$skillsRoot = Join-Path $resolvedRepoRoot "skills"
$skills = Get-ChildItem -LiteralPath $skillsRoot -Directory | Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md") } | Sort-Object Name
$expectedSkillNames = @{}
foreach ($skill in $skills) {
    $expectedSkillNames[$skill.Name] = $true
    Ensure-SkillIcon -RepoRoot $resolvedRepoRoot -SkillRoot $skill.FullName
    $link = Join-Path $RuntimeRoot $skill.Name
    Ensure-Junction -Path $link -Target $skill.FullName
}

$installedItems = Get-ChildItem -LiteralPath $RuntimeRoot -Force -ErrorAction SilentlyContinue |
    Where-Object { $_.PSIsContainer -and $_.Name -like "ceratops-*" }
foreach ($item in $installedItems) {
    if ($expectedSkillNames.ContainsKey($item.Name)) {
        continue
    }

    $looksLikeBrokenDirectoryLink = $item.PSIsContainer -and $item.Exists -eq $false
    if (-not (Is-ReparsePoint $item) -and -not $looksLikeBrokenDirectoryLink) {
        continue
    }

    $rawTarget = Resolve-LinkTarget $item
    $repoManagedTarget = $false
    if (-not [string]::IsNullOrWhiteSpace($rawTarget)) {
        try {
            $resolvedTarget = (Resolve-Path -LiteralPath $rawTarget).Path
            if ($resolvedTarget.StartsWith($skillsRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
                $repoManagedTarget = $true
            }
        } catch {
            if ($rawTarget.StartsWith($skillsRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
                $repoManagedTarget = $true
            }
        }
    }

    if ($repoManagedTarget) {
        Remove-ReparsePoint -Path $item.FullName
    }
}

Write-Output "installed"
