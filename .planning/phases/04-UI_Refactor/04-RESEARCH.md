# Phase 4 Research: UI Framework Migration & System Integration

## Overview
This phase involves migrating from Tkinter to Flet and ensuring the system tray (pystray) and background monitor service work harmoniously.

## Flet + Pystray Integration
### Strategy
- **Threading**: Run `pystray.Icon.run()` in a separate daemon thread.
- **Main Loop**: Run `flet.app()` on the main thread for optimal performance and compatibility.
- **Lifecycle**: Use `page.window.prevent_close = True` to intercept the close event and hide the window instead of exiting. The app only exits when the tray's "Exit" menu is clicked.

### Communication (UI Bridge)
- **Singleton Pattern**: Implement `UIBridge` in `ui_bridge.py`.
- **Decoupling**: Bridge exposes methods for UI (Flet) to trigger logic (e.g., `bridge.save_config()`, `bridge.request_refresh()`).
- **Events**: Use `threading.Event` or `queue.Queue` to signal the monitor thread. Monitor thread remains agnostic of the UI framework.

## Modern UI Patterns (Flet)
- **Theme**: Material Design 3 (Dark Mode).
- **Navigation**: `ft.NavigationRail` for sidebar implementation.
- **Components**:
  - `ft.Card` for grouping sections.
  - `ft.LineChart` for future traffic visualization (Phase 6).
  - `ft.TextField` with validation feedback.

## Implementation Details
1. **Bridge Class**:
   ```python
   class UIBridge:
       def __init__(self, monitor, config_mgr):
           self.monitor = monitor
           self.config_mgr = config_mgr
           self.refresh_event = threading.Event()
       
       def save_config(self, new_data):
           success = self.config_mgr.save_config(new_data)
           if success:
               self.refresh_event.set()
           return success
   ```
2. **Main Entry Update**:
   ```python
   # main.pyw
   bridge = UIBridge(monitor, config_mgr)
   tray = ProxyTrayIcon(bridge) # Update Tray to take bridge
   threading.Thread(target=tray.run, daemon=True).start()
   ft.app(target=lambda page: start_flet_ui(page, bridge))
   ```

## Dependencies
- `flet`: Core UI framework.
- `requirements.txt`: Add `flet`.

## Potential Pitfalls
- **Recursive Updates**: Ensure `page.update()` is called safely from other threads if needed.
- **Asset Paths**: Flet's asset management might differ from standard file paths; use absolute paths or relative to script.
- **System Tray Icons**: Ensure the icon image is compatible with Windows (ICO/PNG/PIL).

---
## RESEARCH COMPLETE
