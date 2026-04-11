# Phase 4 Context: UI Framework Migration

## Goal
Migrate from legacy Tkinter to **Flet** for a modern, high-aesthetic experience. Implement a robust bridge architecture to decouple UI from monitoring logic.

## Decisions

### 1. UI Strategy: Flet (Material 3)
- **Framework**: Flet (Python + Flutter).
- **Launch Mode**: On-demand window. The main loop runs headless; Flet window spawns and closes as needed.
- **Visuals**: Dark Theme, Sidebar navigation, modern controls (Cards, Switches, Progress Rings).

### 2. Architecture: UI Bridge Pattern
- **Component**: `UIBridge` class in a new file `ui_bridge.py`.
- **Flow**: UI -> Bridge -> Config/Monitor.
- **Communication**: Use `threading.Event` to signal the monitor thread when config changes.

### 3. Service Orchestration
- **Main Thread**: Controls overall lifecycle and Pystray.
- **Background Thread**: `MonitorService` loop.
- **UI Thread**: Spawned by Flet when user opens settings/dashboard.

### 4. Codebase Reuse
- `monitor_service.py`: Keep as is, but ensure its update callback is thread-safe for Flet components.
- `config_manager.py`: Internal logic remains unchanged.

## Specifics
- Flet will be installed via `requirements.txt`.
- Dashboard (Phase 6) placeholders will be added to the Sidebar in this phase.
- Ensure the `NamedMutex` logic in `main.pyw` is preserved to prevent duplicate Flet instances.

## Canonical Refs
- `j:/Project/Proxy_Monitor/main.pyw` (Existing entry point)
- `j:/Project/Proxy_Monitor/monitor_service.py` (Core logic)
- `j:/Project/Proxy_Monitor/.planning/research/SUMMARY.md` (Research findings)
