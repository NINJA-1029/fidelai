param (
    [string]$Version = ""
)

$pubspecPath = "$PSScriptRoot\pubspec.yaml"
$pubspecContent = Get-Content $pubspecPath -Raw

if ($Version -eq "") {
    # Extract current version
    if ($pubspecContent -match 'version:\s*([0-9]+)\.([0-9]+)\.([0-9]+)\+([0-9]+)') {
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        $patch = [int]$Matches[3] + 1
        $build = [int]$Matches[4] + 1
        $Version = "$major.$minor.$patch"
        $newVersionLine = "version: $major.$minor.$patch+$build"
    } else {
        $Version = "1.0.1"
        $newVersionLine = "version: 1.0.1+2"
    }
} else {
    $cleanVer = $Version.TrimStart('v')
    $build = 1
    if ($pubspecContent -match 'version:.*\+([0-9]+)') {
        $build = [int]$Matches[1] + 1
    }
    $newVersionLine = "version: $cleanVer+$build"
    $Version = $cleanVer
}

Write-Host "Updating version in pubspec.yaml to $newVersionLine..." -ForegroundColor Cyan
$updatedContent = $pubspecContent -replace 'version:.*', $newVersionLine
Set-Content -Path $pubspecPath -Value $updatedContent -NoNewline

Write-Host "Building release APK for version v$Version..." -ForegroundColor Green
flutter build apk --release

$outputDir = "$PSScriptRoot\build_outputs"
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

$sourceApk = "$PSScriptRoot\build\app\outputs\flutter-apk\app-release.apk"
$destApk = "$outputDir\fidel-v$Version.apk"

if (Test-Path $sourceApk) {
    Copy-Item $sourceApk -Destination $destApk -Force
    Write-Host "SUCCESS: Saved build artifact to $destApk" -ForegroundColor Green
} else {
    Write-Host "ERROR: Release APK not found at $sourceApk" -ForegroundColor Red
}
