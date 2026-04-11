# Technical Concerns & Debt

**Analysis Date:** 2026-04-11

## Technical Debt

### 1. Monolithic Structure
- **Issue:** All logic (networking, UI, OS interaction) resides in a single 440+ line file (`proxy_monitor.pyw`).
- **Impact:** Harder to maintain, test, and refactor as features grow.

### 2. Runtime Dependency Installation
- **Issue:** The script runs `pip install` during import failure.
- **Impact:** Can be slow on first run, may fail in restricted environments, and is generally considered an anti-pattern for distributed software.

### 3. Hardcoded Assumptions
- **Issue:** Regex for traffic info expects a specific `subscription-userinfo` format.
- **Impact:** Fragile if a provider uses a different header format or non-standard key-value pairs.

## Risks

### 1. Security
- **Sensitive Data:** `serverchan_sendkey` and `sub_url` are stored in plain text JSON.
- **Exposure:** If the log file is shared, it might contain sensitive info if not carefully managed (though current logging seems safe).

### 2. Stability
- **Single Thread for UI:** Although the monitor is threaded, the settings window creation (`_create_window`) uses `threading.Thread` to wrap a `tk.Tk().mainloop()`. Running `Tk` in a non-main thread can be unstable on some platforms/versions.
- **Resource Leaks:** Ensure `_instance_lock_socket` and other resources are properly handled if the app crashes.

## Fragile Areas

- **Registry Access:** Registry operations might require higher privileges in some Windows configurations.
- **Regex Extraction:** Reliance on `re.search(r'upload=(\d+)', ...)` without handling variations in whitespace or order.

---

*Concerns audit: 2026-04-11*
