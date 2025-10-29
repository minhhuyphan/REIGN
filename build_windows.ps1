<#
PowerShell build helper for packaging the game on Windows using PyInstaller.
Usage:
  .\build_windows.ps1            # default: onefile, console visible
  .\build_windows.ps1 -OneFile:$false   # build --onedir (recommended for reliability)
  .\build_windows.ps1 -Windowed:$true  # hide console

Notes:
- This script installs pyinstaller in the active Python environment if needed.
- It includes the `tai_nguyen` and `tai_lieu` folders as data so assets are bundled.
- Entry point is `ma_nguon/main.py` (adjust if your real entry differs).
- If you prefer an installer or further customizations (icons, version info), I can add them.
#>
param(
    [switch]$OneFile = $true,
    [switch]$Windowed = $false
)

Write-Host "Starting build (OneFile=$OneFile, Windowed=$Windowed)"

# Ensure pip and pyinstaller
try {
    python -m pip --version > $null 2>&1
} catch {
    Write-Error "Python/pip not found in PATH. Ensure Python 3.8+ is installed and available as 'python'."
    exit 1
}

try {
    python -c "import PyInstaller" > $null 2>&1
} catch {
    Write-Host "PyInstaller not found. Installing PyInstaller and pygame..."
    python -m pip install --upgrade pip
    python -m pip install pyinstaller pygame
}

# Files/folders to include as data. Format: src;dest (Windows)
$adds = @(
    "tai_nguyen;tai_nguyen",
    "tai_lieu;tai_lieu"
)

$extraArgs = @()
if ($OneFile) { $extraArgs += "--onefile" } else { $extraArgs += "--onedir" }
if ($Windowed) { $extraArgs += "--noconsole" }
# You can add an icon file like: $extraArgs += "--icon=path\to\icon.ico"

foreach ($d in $adds) {
    $extraArgs += "--add-data"
    $extraArgs += $d
}

# Entry script: adjust if necessary
$entry = "ma_nguon\\main.py"

# Ensure working dir is repository root
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

# Run pyinstaller
$cmd = "pyinstaller " + ($extraArgs -join ' ') + " " + $entry
Write-Host "Running: $cmd"

& pyinstaller @extraArgs $entry

if ($LASTEXITCODE -ne 0) {
    Write-Error "PyInstaller failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

# Output path
if ($OneFile) {
    $exe = Join-Path -Path (Join-Path $root 'dist') -ChildPath (Split-Path $entry -LeafBase) + '.exe'
    Write-Host "Build finished. Onefile exe should be at: $exe"
} else {
    $dir = Join-Path $root 'dist' (Split-Path $entry -LeafBase)
    Write-Host "Build finished. Bundle folder is: $dir"
}

Write-Host "Tip: test the built executable on a clean Windows machine or VM. Antivirus can flag single-file EXEs."