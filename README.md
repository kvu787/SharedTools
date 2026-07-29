```powershell
python "C:\Users\kevin\Repository\SharedTools\presentmon_input_latency.py" "C:\Users\kevin\Repository\Unity\ZoomTracks\ZoomTracks\MyLogOutput\2026-07-23_03-54-26\PresentMon.csv"
python "C:\Users\kevin\Repository\SharedTools\presentmon_input_latency.py" "C:\Users\kevin\Repository\Unity\ZoomTracks\ZoomTracks\MyLogOutput\2026-07-23_03-54-26\PresentMon.csv" --ignore-start 10 --ignore-end 10

& "C:\Users\k\Repository\SharedTools\Split-File.ps1" -FilePath "C:\Users\k\Repository\Godot\VsyncStutterTest\SavedLogOutput\2026-07-29_10-38-48 limiter disabled\PresentMon.csv" -NumParts 25 -PadLength 2
& "C:\Users\k\Repository\SharedTools\Split-File.ps1" -FilePath "C:\Users\k\Repository\Godot\VsyncStutterTest\SavedLogOutput\2026-07-29_11-42-44 limiter enabled\PresentMon.csv" -NumParts 25 -PadLength 2
```

