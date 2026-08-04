# Recommended setup for Unity and Godot games

System setup:

* Earlier experiments seemed to indicate that enabling hardware accelerated graphics scheduling, using more than one monitor, and/or playing a youtube video or other streaming video on the second monitor caused problems.
  * Currently, I haven't reproduced these issues when doing any of those things, so I no longer recommend avoiding those.
* Keep the laptop lid open even if you're using external monitor/keyboard/mouse instead of using the laptop's built-in screen/keyboard/trackpad
  * It's possible that closing the laptop lid triggers some odd firmware/software states
  * I speculate that some display issues awhile back were caused by using the laptop with the lid closed
  * Also, having an open lid supposedly helps with heat dissipation
* Setup PA278QGV like this:
  * Connect to laptop's Thunderbolt 5 ports using DisplayPort (monitor side) to USB-C (laptop side) cable
  * OSD > Menu > Settings > All Reset = YES
  * After reset, disable energy saving mode
  * OSD > Menu > Settings > Dynamic Dimming = OFF
  * OSD > Menu > Settings > OSD Setup > OSD Timeout = Max
  * OSD > Menu > Settings > OSD Setup > DDC/CI = OFF
  * OSD > Menu > Settings > OSD Setup > Transparency  = 0
  * OSD > Menu > Settings > Sound > Volume = 0
  * OSD > Menu > Settings > Sound > Mute = ON
  * OSD > Menu > Settings > ASUS Power Sync = OFF
  * OSD > Menu > Image > Trace Free = 0
  * OSD > Menu > Palette > Brightness = 150
  * OSD > Menu > Settings > MediaSync = ON
* Setup U2717D like this:
  * Connect to laptop's Thunderbolt 5 ports using DisplayPort (monitor side) to USB-C (laptop side) cable
  * OSD > Others > Reset Others
  * OSD > Others > Factory Reset
  * OSD > Menu > Timer = 60 s
  * OSD > Menu > Transparency = 0
  * OSD > Brightness/Contrast > Brightness = 20
  * OSD > Others > DDC/CI = Disable
* Do a "Ctrl + Shift + Win + B"
* Do a clean reinstall of the graphics driver
  * Or: use Nvidia Profile Inspector to reset global settings and delete per-program profiles
  * Or: Ctrl + Shift + Win + B
* Open Nvidia App and disable "Battery Boost" in global settings
* Open Nvidia control panel (NVCP) and enable gsync
  * Make sure that you check the box to enable PA278QGV even though nvidia complains that it is not verified compatible
  * Turn gsync on/off/on or off/on/off/on to make sure it fully applies
  * Turn on gsync indicator
* Do a "Ctrl + Shift + Win + B"
* In windows display settings:
  * Arrange all three screens (including laptop screen)
  * Set PA278QGV to main display
  * Set PA278QGV to 120 hz
  * Set U2717D to 59.95 hz
  * Disconnect the laptop screen
* Open nvcp
  * Set "global settings > power management mode = prefer maximum performance" 
  * Ensure that "global settings > monitor technology" is already set to "g-sync, g-sync compatible"
* legion space
  * toggle it between performance and balance a few times and then set to performance

Per program setup:

* Create an nvcp profile for the exe
* Set the following in the nvcp profile
  * low latency mode = ultra
  * max frame rate = off, or anything from 60 to 110
  * vertical sync = on
* Setting low latency mode to on or ultra forces a frame rate cap of 116 fps (slightly below the monitor refresh rate of 120 hz)
* You can get a locked 120 fps with vsync=on and gsync=on if you set low latency mode to off, but this will lead to higher input latency in godot games
  * Interestingly, LLM doesn't seem to affect the Unity ZoomTracks game
  * I suspect it is because ZoomTracks sets maxQueuedFrames to 1, which may be what LLM=Ultra does.
  * Last time I investigated, Godot doesn't have an equivalent to maxQueuedFrames=1
* Launch the game with a cmd+PowerShell launcher that sets process priority to "High"
* On the secondary monitor (U2717D) you should be able to play a fullscreen Youtube video in Edge browser that hardware accel enabled, and the game should still run smoothly on the primary monitor

Tested with:

* Windows 11 Pro 25H2 26200.8875
* Nvidia Game Ready Driver 596.49
* Primary monitor: Asus ProArt PA278QGV
* Secondary monitor: Dell UltraSharp U2717D
* Cable Matters 54Gbps Unidirectional USB C to DisplayPort 2.1 Cable
  * Cable Matters Product ID = 201456
* 2025 Lenovo Legion 9i 18IAX10
  * Intel Core Ultra 9 275HX
  * NVIDIA GeForce RTX 5090 Laptop GPU
  * Screen variant: 2D-only, non-3D WQUXGA (3840x2400)
  * 1x HDMI port
  * 2x Thunderbolt 5 ports

Example sessions:
* "C:\Users\k\Repository\SharedTools\SavedLogOutput\2026-08-03_18-14-29 godot VsyncStutterTest"
* "C:\Users\k\Repository\SharedTools\SavedLogOutput\2026-08-03_19-11-14 unity ZoomTracks"

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
