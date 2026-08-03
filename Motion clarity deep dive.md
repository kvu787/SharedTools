# NOTE

This used to be a Google Doc. On Aug 3, 2026, exported it to this Markdown file and saved it here so I don't forget about it.

It serves as an archived reference file that I'll use to update authoritative files. It shouldn't be edited.

# Perfect frame delivery

***Perfect frame delivery conformance (PFDC)*** is the extent to which a system delivers one distinct frame for every interval at a specified frequency.

* Each interval presents exactly one newly rendered frame.  
* Frames are presented in their intended order, with no dropped, duplicated, or reordered frames.  
* No frame misses its intended interval.  
* No screen tearing occurs.

# Best tested setup

On the PC side, the most important thing is to maximize PFDC.  
Do this:

* Install lenovo vantage  
* Install all updates from vantage  
* Install legion space  
* Set profile to "Performance \+ enable GPU OC" in legion space

On the display side, the most important thing is well-tuned motion clarity.  
Do this:

* Asus ROG Strix Pulsar XG27AQNGV  
* 54Gbps Unidirectional USB C to DisplayPort 2.1 Cable, Supports DP54, 8K@165Hz / 4K@480Hz  
  * Cable Matters Product ID \= 201456  
* Use either Pulsar or ULMB 2 on the monitor

Use this per-program setup in Nvidia Control Panel:  
1. Low Latency Mode \= Ultra  
2. Max Frame Rate \=  
   * 240 FPS if internal limiter is disabled  
   * Off if internal limiter is enabled  
3. Monitor Technology \= G-SYNC  
4. Power management mode \= Prefer maximum performance  
5. Preferred refresh rate \= Application-controlled  
6. Vertical sync \= On  
All other settings should remain on defaults

Use these repos and these specific commits as test scenes:

* [https://github.com/kvu787/VsyncStutterTest/commit/2a249aeba8673a0e69881e13077ad55566af5ea1](https://github.com/kvu787/VsyncStutterTest/commit/2a249aeba8673a0e69881e13077ad55566af5ea1)  
* [https://github.com/kvu787/ZoomTracks/commit/07c9479a19973324f53785de9f50cb9e434ec1cf](https://github.com/kvu787/ZoomTracks/commit/07c9479a19973324f53785de9f50cb9e434ec1cf) 

# Detailed setup instructions

Reset procedure

* Disconnect power cable  
* Hold power button until laptop turns off  
* Reset BIOS defaults  
* Hold power button for about 15 seconds to reset EC  
  * The power button should light up briefly, then turn off  
  * As soon as the power light turns off, release the power button, or else it will continue to another EC reset  
* Access BIOs by spamming F2 when Legion logo appears  
* Reset BIOS defaults  
* In BIOS, do "Security Erase (NVMe SSD) 1 Data"  
* Reset BIOS defaults  
  * After restarting, it could take up to 10 minutes to boot  
* configure bios  
  * disable wireless lan  
  * disable fool proof fn ctrl  
  * disable battery level protection  
  * disable always on usb  
  * disable pxe boot to lan  
* Plug in a mouse via wired usb  
* Boot from win11 usb

If BIOS graphics setting is "dynamic" (aka hybrid, aka both dgpu and igpu):

* nvcp vsync won't work  
* you need to change the display mode to dgpu only in nvcp

***DON'T*** change the monitor resolution or refresh rate in NVCP. Only do that in Windows display settings.

oobe setup  
plug in ethernet cable  
install windows updates  
install microsoft store updates  
configure edge  
switch to dgpu  
configure 1password

* disable startup  
* disable hardware accel  
* disable hotkeys  
* disable submit auto with auto-type

install nvdia driver 596.49  
disable smart app control  
install vc 14 redist 32 and 64 bit

Test setup

* update winget  
* winget install powershell  
* winget install git  
* install intel presentmon  
* download gamedevtech/presentmon to program folder  
* clone vsyncstutter repo  
* export vsyncstutter  
* setup nvcp profile  
* run.cmd

laptop drivers:  
[https://pcsupport.lenovo.com/us/en/products/laptops-and-netbooks/legion-series/legion-9-18iax10/downloads/driver-list](https://pcsupport.lenovo.com/us/en/products/laptops-and-netbooks/legion-series/legion-9-18iax10/downloads/driver-list) 

# Settings to try

* windows version  
* nvidia driver version:  
  * 610.88  
  * 596.49  
  * lenovo nvidia driver 32.0.15.9611 / 596.11  
    * This can only be found on lenovo drivers site  
* hybrid, dgpu-only, igpu-only  
* legion space profiles: quiet, balance, performance, custom  
* lenovo legion toolkit  
* hardware accelerated gpu scheduling  
* windows vrr toggle  
* full screen optimizations  
* optimizations for windowed games  
* laptop lid open vs closed  
* monitor topology  
  * laptop built-in screen only  
  * primary monitor only  
  * primary and secondary monitory  
  * primary, secondary, and laptop monitor  
* Monitor connection: displayport, usb-c, hdmi  
* pulsar, ulmb, strobing off  
* g-sync on or off  
* \-force-gfx-direct  
* \-force-d3d11-flip-model  
* graphics api:  
  * directx 11  
  * directx 12  
  * vulkan  
  * opengl  
* window mode  
  * exclusive fullscreen  
  * true exclusive fullscreen  
  * borderless fullscreen  
  * borderless non-fullscreen  
  * windowed  
* using nvidia control panel vs nvidia app  
* nvidia battery boost  
  * can only be set in nvidia app  
* nvidia per-program settings:  
  1. Low Latency Mode \= Ultra  
  2. Max Frame Rate \=  
     * 240 FPS if internal limiter is disabled  
     * Off if internal limiter is enabled  
  3. Monitor Technology \= G-SYNC  
  4. Power management mode \= Prefer maximum performance  
  5. Preferred refresh rate \= Application-controlled  
  6. Vertical sync \= On  
* Set monitor to different refresh rates in windows advanced display settings  
* Intel PresentMon on or off  
* PresentMon capture on or off  
* Different system software setups:  
  * Lenovo Vantage \+ Legion Space  
  * Lenovo Vantage only  
  * Legion Space only  
  * No vantage or space, but manually install drivers from Lenovo site  
  * None of the above, do offline install of win11pro, and just do all windows updates  
* Lenovo Vantage battery conservation (80% charge limit) on or off  
* Razer Synapse: Not installed, installed but not opened, opened  
* mouse and controller connections: wired vs wireless  
* wlan (wifi hardware) enabled or disabled in BIOS  
* changing display settings (resolution, refresh rate, arrangement, enablement) in NVCP vs nvidia app vs windows settings  
* laptop power cable plugged in vs not  
* windows power usage settings  
  * This is not the same as windows power plan  
* Windows power plan  
  * This is not the same as windows power usage settings  
  * Hidden built-in ultimate performance power plan  
* Elevate process priority  
* Isolate game threads with core affinity  
* Enable/disable e-cores in BIOS  
  * The BIOS calls these atom cores  
* Unity settings  
  * maxQueuedFrames  
  * Vsync on/off  
* Godot settings  
  * Engine.max\_fps  
  * Custom limiter on/off  
  * Vsync on/off  
* 1000 hz vs 8000 hz polling rate for mouse and controller  
* unity engine version  
* godot engine version  
* windows/xbox game mode on/off

# Hardware

Monitors tested

* Lenovo ThinkVision T27hv-20  
  * Bad viewing angle  
* Dell UltraSharp U2717D  
  * Good except for default color calibration  
* Asus ProArt PA278QV  
  * Haven't tried yet  
* Asus ProArt PA278CV  
  * Works well, except for some fade-out at the left and right edges  
* Asus ProArt PA278QGV  
* Asus ProArt PA278CGRV  
  * FreeSync has some issues  
* Asus ROG Strix XG27ACMES  
  * Bad viewing angle  
* Asus ROG Strix Pulsar XG27AQNGV  
  * Best motion clarity out of all tested  
  * Too hot  
  * Back panel connectors force cables to bend severely  
  * Fullscreen-only gsync doesn't seem to work  
    * I had to add per-program profiles for unity editor and godot editor to disable gsync for them  
    * PA278CV, PA278QGV, PA278CGRV didn't seem to have this issue  
* Dell Alienware AW2725DM  
  * Has banding/interlacing every other row at 180 hz  
* LG UltraGear 32GX870A-B  
  * Too hot  
* Legion 9i built-in screen  
  * All-around excellent

Peripherals  
razer deathadder v4 pro, connected via wireless  
razer wolverine v3 pro 8k pc, connected via wireless  
kinesis advantage 360 (non-wireless version)

PC specifications  
2025 Lenovo Legion 9i 18IAX10  
Intel Core Ultra 9 275HX  
NVIDIA GeForce RTX 5090 Laptop GPU  
2D-only, non-3D WQUXGA (3840x2400)  
1x HDMI port  
2x Thunderbolt 5 ports

# Capture tools

* PresentMon  
* Windows Performance Recorder  
* Windows Performance Analyzer  
* GPUView  
* LatencyMon  
* [https://testufo.com/animation-time-graph](https://testufo.com/animation-time-graph) 
