# Testing Strategy

**Analysis Date:** 2026-04-11

## Current State

The project currently has **no automated test suite** (no `unittest`, `pytest`, or integration tests).

## Manual Verification Process

Currently, verification is performed manually:
1. **Startup Test:** Confirm tray icon appears and tooltip shows initial data.
2. **Settings Test:** Open settings, change the polling interval, and save; verify `config.json` updates.
3. **Notification Test:** Temporarily set `daily_limit_gb` to 0.0001 and trigger a refresh to verify ServerChan delivery.
4. **Single Instance Test:** Attempt to launch the script while an instance is already running; verify the new process exits silently.

## Recommended Testing Roadmap

### 1. Unit Tests
- **Config Logic:** Verify `load_config` handles missing keys and invalid JSON.
- **Bytes Formatting:** Test `format_bytes` with various edge cases (0B, 1024B, 1GB+).
- **Header Parsing:** Mock `urllib` responses to test the regex extraction of traffic info.

### 2. Integration Tests
- **Windows Registry:** Verify `handle_auto_start` correctly adds/removes registry keys.
- **Persistence:** Verify `traffic_state.json` updates correctly after a mock poll.

---

*Testing audit: 2026-04-11*
