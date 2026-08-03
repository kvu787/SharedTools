# VSync input latency

Based on the PresentMon captures in `C:\Users\k\Repository\SharedTools\SavedLogOutput\aoe4 input latency testing`, it seems like using VSync without VRR introduces 2 frames of input latency for a total upper bound of 4 frames of input latency.
I tried various configurations, but I couldn't eliminate that extra input latency.

Using VRR results in an upper bound of 2 frames of input latency, which is pretty good.

## More tests

After another barrage of tests with AOE4, ZoomTracks, and VsyncStutterTests, I still couldn't get a 2-frame input latency bound without GSync. So it still seems like GSync is required to get that ideal input latency.

# Misc

```powershell
python "C:\Users\kevin\Repository\SharedTools\presentmon_input_latency.py" "C:\Users\kevin\Repository\Unity\ZoomTracks\ZoomTracks\MyLogOutput\2026-07-23_03-54-26\PresentMon.csv"
python "C:\Users\kevin\Repository\SharedTools\presentmon_input_latency.py" "C:\Users\kevin\Repository\Unity\ZoomTracks\ZoomTracks\MyLogOutput\2026-07-23_03-54-26\PresentMon.csv" --ignore-start 10 --ignore-end 10

& "C:\Users\k\Repository\SharedTools\Split-File.ps1" -FilePath "C:\Users\k\Repository\Godot\VsyncStutterTest\SavedLogOutput\2026-07-29_10-38-48 limiter disabled\PresentMon.csv" -NumParts 25 -PadLength 2
& "C:\Users\k\Repository\SharedTools\Split-File.ps1" -FilePath "C:\Users\k\Repository\Godot\VsyncStutterTest\SavedLogOutput\2026-07-29_11-42-44 limiter enabled\PresentMon.csv" -NumParts 25 -PadLength 2
& "C:\Users\k\Repository\SharedTools\Split-File.ps1" -FilePath "C:\Users\k\Repository\SharedTools\MyLogOutput\2026-08-02_07-31-09\PresentMon combined.csv" -NumParts 43 -PadLength 2
```

