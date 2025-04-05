# AMD-Optimized Lunar Aimbot

A modified version of [Lunar AI Aimbot](https://github.com/xxreflextheone/AI-Aimbot) optimized for AMD systems.

## Requirements
- Python 3.10.5
- AMD GPU with ROCm support (RX 5000/6000/7000 series)
- Latest AMD drivers (Adrenalin 23.x or newer)

## Installation
1. Install Python 3.10.5 and add it to PATH
2. Install ROCm (follow AMD's official installation guide)
3. Clone this repository
4. Run: `pip install -r requirements.txt`

## Basic Troubleshooting
- If Python is not recognized:
  - Reinstall Python and check "Add Python to PATH" during installation
  - Restart your computer after installation
- ROCm detection issues:
  - Verify ROCm installation with `rocminfo`
  - Check HIP is properly configured
  - Reinstall latest AMD drivers if needed
- Performance issues:
  - Set environment variable: `export HIP_VISIBLE_DEVICES=0`
  - Ensure system is using dedicated GPU

## Usage
Run: `start.bat`
Alternative: `python lunarAMD.py`

Hotkeys:
- F1: Toggle aimbot
- F2: Exit program

## Notes
- AMD hardware only (no NVIDIA/Intel support)
- No anti-cheat guarantees
- Original credits to xxreflextheone

Create a new issue at [https://github.com/eteb/LunarAMD/issues](https://github.com/eteb/Lunar-AMD/issues) for any problems.
