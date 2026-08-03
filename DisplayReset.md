# List of nvidia things to set after reset

* ctrl shift win B = driver reboot
* battery boost
* power management mode
* gsync

---------

Your suspicion fits today’s evidence: demotions vanished after resets/reapplications, while app code didn’t change. Here’s a tiered reset procedure tuned to your setup (Legion + NVIDIA + G-SYNC + PresentMon).

---

## When to use this

Treat a capture as pathological if steady PresentMon shows any of:
- Displayed Hz ≪ present FPS (e.g. ~70–80 vs 100)
- Display ~2× gaps ≳ 5–10%
- Frequent HC:IF ↔ H:IF / HNX intercalation
- Mixed `sync=1` demotions while you expect a G-SYNC/MFR path

---

## Tier 0 — Soft reset (2–5 min)

Do this first whenever behavior looks “weird” after changing NVCP / refresh / GPU mode.

1. **Fully quit the game** (and Unity Editor / Godot if open).
2. **Kill leftovers**
   ```powershell
   Get-Process ZoomTracks, VsyncStutterTest, Unity, Godot* -ErrorAction SilentlyContinue | Stop-Process -Force
   ```
3. **Restart NVIDIA user stack**
   ```powershell
   # Admin PowerShell recommended
   Get-Process nvcontainer, NVDisplay.Container -ErrorAction SilentlyContinue | Stop-Process -Force
   Restart-Service NVDisplay.ContainerLocalSystem -ErrorAction SilentlyContinue
   ```
   If service restart fails, reboot instead.
4. **Cycle the panel**
   - Unplug DP/HDMI → wait 5 s → replug  
   - Or monitor OSD: power off → on  
   - Confirm Windows shows the intended refresh (e.g. 120 Hz) under **Settings → System → Display → Advanced display**
5. **Cold launch** only the test exe (not from a dirty editor play-mode session).
6. Capture ≥20 s PresentMon and check the health gates below.

---

## Tier 1 — Clean NVCP / profile reset (10–15 min)

Use when Tier 0 fails, or after hybrid↔dGPU switches, driver updates, or “I changed a bunch of NVCP stuff.”

### A. Wipe per-app profiles
In **NVIDIA Control Panel** (or NVIDIA App → Graphics):

1. **Manage 3D settings → Program Settings**
2. Delete profiles for:
   - `ZoomTracks.exe`
   - `VsyncStutterTest.exe`
   - any stale Unity/Godot editor profiles you don’t want
3. **Apply**

### B. Restore NVCP defaults (both places)
1. **Manage 3D settings → Global Settings → Restore**
2. **Display → Set up G-SYNC** — note current value, then re-apply intentionally after restore
3. **Change resolution** — confirm target refresh is selected (don’t leave a stale 59.95/120 mix)
4. **Adjust desktop size and position** — Scaling = your normal choice; Apply

### C. Optional: export/import safety
Before nuking, export current 3D settings if the UI allows, so you can diff later.

### D. Re-apply a known-good baseline (example for MFR100 tests)
**Global / Display**
- G-SYNC: Enable for fullscreen (or fullscreen+windowed if that’s your known-good)
- Preferred refresh = intended panel rate (document it)
- HAGS / Optimizations for windowed games / Windows VRR: leave at your known-good (your README: defaults/on)

**Per-app profile** (`ZoomTracks.exe` / `VsyncStutterTest.exe`)
| Setting | Baseline for MFR100 G-SYNC tests |
|---|---|
| Monitor Technology | G-SYNC |
| Max Frame Rate | 100 (or your test value) |
| Vertical Sync | Off *or* On — pick one and document; both were healthy once state was clean |
| Low Latency Mode | Off *or* Ultra — document; not the demotion switch in isolation |
| Power management | Prefer maximum performance |

### E. Reboot once after profile recreate
Don’t skip this after a big NVCP reset.

### F. Verify with a short Godot capture first
Godot is the cheaper canary. If Godot is pathological, don’t bother debugging Unity yet.

---

## Tier 2 — Windows display / DWM reset (15–20 min)

Use if Tier 1 fails or Windows Advanced Display / HDR / multi-monitor state looks wrong.

1. **Single-monitor mode** for the test (disable other displays temporarily).
2. **Settings → System → Display**
   - Correct GPU / display selected
   - Refresh rate = intended
   - HDR off for A/B unless HDR is part of the test
3. **Graphics settings**
   - Remove custom per-app Windows graphics preferences for the test exes
   - Don’t change HAGS mid-experiment
4. **Restart DWM/explorer** (mild)
   ```powershell
   Stop-Process -Name explorer -Force; Start-Process explorer
   ```
5. **Sign out / sign in** (stronger than explorer restart).
6. Reboot, then Tier 0 soft launch + PresentMon.

Also avoid mid-session:
- switching hybrid ↔ dGPU
- lid open/close changes
- overnight sleep/wake with different refresh topologies  

Those are your README’s known bad-state triggers.

---

## Tier 3 — Clean NVIDIA driver reinstall (nuclear, most reliable)

Use when profiles/resets don’t restore PresentMon health, especially after GPU-mode switches.

1. Download the exact driver you trust (your notes: **596.49** or current known-good).
2. Install with **Custom → Perform a clean installation**.
3. Reboot.
4. Re-apply Tier 1 baseline from scratch (don’t restore an old NVCP backup yet).
5. Validate Godot, then ZoomTracks.

This is the only method that reliably wipes latent NVCP/driver state.

Optional stronger variant: DDU in Safe Mode → install driver clean. Only if clean install alone isn’t enough.

---

## PresentMon health gates (pass/fail)

After any tier, run ~20–30 s and require **steady** (+3 s warmup):

| Gate | Healthy | Pathological |
|---|---|---|
| PresentMode | ~100% HC:IF | Frequent H:IF intercalation |
| AllowsTearing / SyncInterval | Stable (e.g. tear=1,sync=0 for G-SYNC+MFR) | Flip-flopping / mixed sync demotions |
| Displayed Hz vs present FPS | Within ~1–2 Hz | Gap of 15–30+ Hz |
| Display ~2× % | ~0% | ≳10% |
| HNX count | 0–few | Hundreds |
| Mode+tear transitions | ~0–2 | Hundreds |

Quick mental model from this session:
- Healthy MFR100: present≈100, displayed≈100, Until≈10 ms, I2P≈15 ms, HNX≈0  
- Pathological MFR100: present≈100, displayed≈73–80, 2×≈20–37%, HNX hundreds  

---

## Recommended “it happened again” checklist

1. Note what changed (GPU mode, sleep, driver, refresh, NVCP tweak).
2. Tier 0 → capture canary (Godot).
3. Fail → Tier 1 (delete app profiles + restore + re-apply + reboot) → canary.
4. Fail → Tier 2 (single display + Windows graphics cleanup + reboot) → canary.
5. Fail → Tier 3 clean driver install.
6. Only after Godot is healthy, retest ZoomTracks with the same NVCP recipe.
7. Keep a short log: date, tier used, refresh, MFR, VSync, LLM, G-SYNC, PresentMon folder name, pass/fail.

---

## What not to chase first

From this session’s A/Bs, these were **not** sufficient alone to explain demotions once state was clean:
- SC=2 vs SC=3 (secondary at best)
- NVCP VSync on vs off
- LLM Ultra vs Off
- Deleting one app profile without a fuller reset/reboot

If pathology returns, assume **driver/NVCP latch / display topology state** first; run the tiers above before digging into engine present code.