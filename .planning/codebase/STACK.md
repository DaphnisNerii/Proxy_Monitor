# Technology Stack

**Analysis Date:** 2026-04-11

## Languages

**Primary:**
- Python 3.10+ - All application logic, GUI, and background monitoring.

**Secondary:**
- None - Project is pure Python.

## Runtime

**Environment:**
- Python 3.10 (CPython)
- Windows-only (uses `winreg`, `socket` for instantiation, and `tkinter` for UI).

**Package Manager:**
- `pip` (standard Python package manager)
- No `requirements.txt` present; dependencies are managed dynamically in-script.

## Frameworks

**Core:**
- `Tkinter` - Used for the settings GUI.
- `pystray` - Used for the Windows system tray icon and menu.

**Testing:**
- None - No automated tests detected.

**Build/Dev:**
- None - Runs as a raw script (`.pyw` for windowless execution).

## Key Dependencies

**Critical:**
- `pystray` - Enables system tray interaction.
- `Pillow` (PIL) - Used for icon generation and UI image handling.
- `urllib` (built-in) - Handles network requests to subscription URLs and ServerChan.
- `winreg` (built-in) - Manages Windows registry for auto-start.

**Infrastructure:**
- `threading` - Manages background monitoring loop without blocking the UI.
- `socket` - Used for single-instance locking via port binding.

## Configuration

**Environment:**
- `config.json` - Persistent user settings.
- `traffic_state.json` - Persistent traffic tracking stats.

**Build:**
- None.

## Platform Requirements

**Development:**
- Windows 10/11
- Python 3.10+

**Production:**
- Windows 10/11
- Requires internet access for traffic monitoring and notifications.

---

*Stack analysis: 2026-04-11*
*Update after major dependency changes*
