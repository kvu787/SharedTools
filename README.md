# Abbreviations

* NVCP = Nvidia Control Panel
* NApp = Nvidia App
* NPI = Nvidia Profile Inspector
* GSync = Nvidia G-Sync (configured in nvcp)
* NVSync = VSync set to "On" in nvcp
* NMFR = Max frame rate setting in nvcp
* LoLM = Low latency mode setting in nvcp
* PMM = Power management mode setting in nvcp
* IVsync = Vsync set by the game or engine code ("I" stands for internal)
* IMFR = frame rate limiter implemented by the game or engine code ("I" stands for internal)
* WRR = Windows refresh rate = The refresh rate in Hz set by "Windows 11 > Settings > System > Display > Advanced display > Choose a refresh rate"
  * This is distinct from the refresh rate derived from VRR behavior
  * A single display can have different max WRRs for different resolutions
  * A single display can have different WRR options (such as 59.95, 74.97 100, 120) for a single resolution

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
  * Set one of the PA278QGV to main display
  * Set both PA278QGV to 120 hz
  * Disconnect the laptop screen
* Open nvcp
  * Set "global settings > power management mode = prefer maximum performance" 
  * Ensure that "global settings > monitor technology" is already set to "g-sync, g-sync compatible"
* legion space
  * toggle it between performance and balance a few times and then set to performance

Exception for Unity engine games (such as ZoomTracks):

* Unity engine exposes a setting called `QualitySettings.maxQueuedFrames`
  * I think that the equivalent setting in Godot is `rendering/rendering_device/vsync/frame_queue_size`
* Unity allows this to be set to 1, while Godot enforces a minimum of 2
* When QualitySettings.maxQueuedFrames=1, it is unnecessary to set LoLM=Ultra
* You can set LoLM=Off and still achieve 2-interval input latency
* By setting LoLM=Off, you also turn off the Nvidia imposed fps limiter, allowing you to achieve synced max refresh rate *and* minimum input latency
* I specifically demonstrated this with the session in `C:\Users\k\Repository\SharedTools\SavedLogOutput\2026-08-06_20-51-39 -- ZoomTracks -- max refresh rate -- 2-interval input latency`
  * That session uses these settings: GSync=on, NVSync=on, NMFR=off, LoLM=off, PMM=max, IVSync=off, IMFR=off
  * You can see that it runs at a synced 120 hz *and* has an upper bound of 2 intervals for input latency
  * If you ran with the following settings, you could achieve a locked 120 hz, but I don't think it would be "synced": GSync=on, NVSync=off, NMFR=120, LoLM=off, PMM=max, IVSync=off, IMFR=off

Recommended Intel PresentMon settings:

* This is for Intel PresentMon from https://game.intel.com/us/intel-presentmon/ not the PresentMon from https://github.com/gametechdev/presentmon
* Settings > Overlay > Windowed Mode = On
  * This is very important; using the monitor in overlay mode can mess with the display pipeline.
  * Move the monitor window away from the game screen onto a secondary screen.
* Settings > Overlay > Width = 400
* Settings > Overlay > Time Scale = 2.0
* Settings > Overlay > Draw Rate = 10
* Settings > Overlay > Background Color = opaque black
* Settings > Data > Polling Rate = 240 (or whatever the maximum is)

Fps cap imposed by ultra low latency mode
* These notes assume that ivsync=off and imfr=off
* gsync=on & lolm=ultra is required to get minimal input latency in some games, such as Godot engine games (see VsyncStutterTest)
* The weird thing is that doing gsync=on & nvsync=on|off & lolm=ultra & nmfr=off results in a frame rate limiter being added
  * If nvsync is off, the fps is capped to 1250
  * If nvsync is on, the fps is capped to 1 to 20 fps below the current refresh rate of the monitor
* I've observed this behavior on at least two different monitors (PA278QGV and XG27AQNGV)
* However, if you do gsync=on & nvsync=on|off & lolm=off & nmfr=off, you get the expected behavior:
  * If nvsync is off, the fps is uncapped
  * If nvsync is on, the fps is capped to the current refresh rate of the monitor

Per program setup:

* Create an nvcp profile for the exe
* Set the following in the nvcp profile
  * low latency mode = ultra
  * max frame rate = off, or anything from 60 to 110
  * vertical sync = on
* Setting low latency mode to ultra forces a frame rate cap of 116 fps (slightly below the monitor refresh rate of 120 hz)
* You can get a locked 120 fps with vsync=on and gsync=on if you set low latency mode to off, but this will lead to higher input latency in godot games
  * Interestingly, LoLM doesn't seem to affect the Unity ZoomTracks game
  * I suspect it is because ZoomTracks sets maxQueuedFrames to 1, which may be what LoLM=Ultra does.
  * Last time I investigated, Godot doesn't have an equivalent to maxQueuedFrames=1
* Launch the game with a cmd+PowerShell launcher that sets process priority to "High"
* On the secondary monitor you should be able to play a fullscreen Youtube video in Edge browser that hardware accel enabled, and the game should still run smoothly on the primary monitor

Tested with:

* Windows 11 Pro 25H2 26200.8875
* Nvidia Game Ready Driver 596.49
* Primary and secondary monitor: Asus ProArt PA278QGV
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

# NVSync input latency

Based on the PresentMon captures in `C:\Users\k\Repository\SharedTools\SavedLogOutput\aoe4 input latency testing`, it seems like using NVSync without VRR introduces 2 frames of input latency for a total upper bound of 4 frames of input latency.
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
