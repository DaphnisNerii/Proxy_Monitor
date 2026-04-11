# Coding Conventions

**Analysis Date:** 2026-04-11

## Code Style

### Python Standards
- **Standard Library First:** Heavy reliance on Python built-ins (`urllib`, `re`, `json`, `tkinter`).
- **Shebang/Extension:** Uses `.pyw` to indicate to Windows that the script should run without a terminal window (using `pythonw.exe`).

### Formatting
- **Indentation:** 4 spaces (standard PEP8).
- **Line Length:** Generally follows standard limits, but some UI layout lines are long.
- **Commenting:** English comments for logic; Chinese comments for some UI strings and error messages.

## Patterns

### Error Handling
- **Permissive Failure:** Network modules (`get_traffic_info`) use retries and `try-except` blocks to prevent the background thread from crashing on intermittency.
- **Runtime Injection:** Automatically attempts to install missing dependencies (`pystray`, `pillow`) via `pip` at runtime if `ImportError` occurs.
- **Log Capture:** `sys.stdout/err` are redirected to a file to capture tracebacks in a windowless environment.

### State Management
- **Global Config:** A `config` global dictionary is updated via `load_config` and accessed via `get_config_val`.
- **Event-Based Refresh:** Uses `threading.Event` to interrupt the polling sleep timer when a user requests an immediate refresh.

### UI Styling
- **Custom Theme:** Does not use standard Tkinter grey. Instead, implements a modern "Dark Mode" using `ttk.Style` and custom RGB colors (`#0f172a`, `#818cf8`).
- **Dynamic Icons:** Icons are generated programmatically using PIL instead of loading numerous `.ico` files.

---

*Convention audit: 2026-04-11*
