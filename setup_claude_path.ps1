# Add Claude Code to PATH if not already present
$claudePath = "C:\Users\Sagar\.local\bin"
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")

if (-not ($currentPath -like "*$claudePath*")) {
    $newPath = "$currentPath;$claudePath"
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
    Write-Host "Added Claude Code to PATH. Please restart your terminal/command prompt."
} else {
    Write-Host "Claude Code is already in PATH."
}

# Verify Claude Code is accessible
try {
    $claudeVersion = claude "--version"
    Write-Host "Claude Code is accessible: $claudeVersion"
} catch {
    Write-Host "Claude Code is not accessible. You may need to restart your terminal."
}