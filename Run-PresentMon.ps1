Set-StrictMode -Version "Latest"
$ErrorActionPreference = "Stop"

$logFolderPath = "$env:UserProfile\Repository\SharedTools\MyLogOutput\$(Get-Date -Format "yyyy-MM-dd_HH-mm-ss")"
New-Item -ItemType "Directory" -Path $logFolderPath

$processName = "RelicCardinal.exe"

$presentMonPath = "$env:UserProfile\Program\PresentMon-2.5.1-x64.exe"
if (Test-Path $presentMonPath) {
    $presentMonLogFilePath  = "$($logFolderPath)\PresentMon.csv"
    Start-Process -FilePath $presentMonPath -ArgumentList "--process_name `"$($processName)`" --output_file `"$($presentMonLogFilePath)`"" -Verb "RunAs"
} else {
    throw "PresentMon executable not found at $($presentMonPath)"
}
