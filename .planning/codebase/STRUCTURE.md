# Directory Structure

**Analysis Date:** 2026-04-11

## Overview

The project follows a flat structure typical of small Python utility applications.

## Key Locations

### Root Directory
- `proxy_monitor.pyw` - **The Monolith**. Contains all logic: UI, Monitoring, Tray, and Utils.
- `config.json` - User settings and preferences.
- `traffic_state.json` - Persistent counters for daily traffic usage.
- `monitor.log` - Application logs.
- `README.md` - Documentation and project overview.
- `.gitignore` - Standard Python and IDE ignore patterns.
- `LICENSE` - MIT License.

### `assets/`
Contains UI-related static assets.
- `tray_preview.png` - Visual representation of the system tray status.
- `settings_preview.png` - Visual representation of the settings interface.

### Logical Modules (Inside `proxy_monitor.pyw`)
While code is in one file, it is organized into logical sections:
- **Configuration (L35-97):** Config loading/saving and Registry management.
- **Monitoring (L121-221):** Network fetching, regex parsing, and polling logic.
- **UI & Icons (L222-258):** PIL-based dynamic icon generation.
- **Settings GUI (L259-417):** Tkinter window definition and event handlers.
- **Main (L418-444):** Single instance check and initialization.

## Naming Conventions
- **Files:** snake_case (e.g., `proxy_monitor.pyw`).
- **Functions:** snake_case (e.g., `get_traffic_info`).
- **GUI Styles:** UpperCamelCase with dot notation (e.g., `Primary.TButton`).
- **Constants:** SCREAMING_SNAKE_CASE (e.g., `CONFIG_FILE`).

---

*Structure map: 2026-04-11*
