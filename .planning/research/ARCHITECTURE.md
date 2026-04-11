# Research: Architecture Integration

## Decoupling UI
- Current `app.py` combines UI and lifecycle. 
- **Plan**: Create `ui_bridge.py` as an interface. The UI will only call methods from `ui_bridge`, which delegates to `monitor.py`.
- **Thread Control**: Use a management class for `pystray` and the UI framework threads to prevent deadlocks.

## Data Persistence for Charts
- Need a small local DB (SQLite) or structured JSON to store historical traffic points.
