# Research: Pitfalls & Mitigation

## 1. Pystray Context Conflict
- **Pitfall**: Both Flet/PySide and pystray want to own the main thread.
- **Mitigation**: Run pystray in a dedicated daemon thread and use thread-safe queues or Signals to communicate.

## 2. Windows DPI Scaling
- **Pitfall**: High-DPI screens make traditional Tkinter look blurry.
- **Mitigation**: Flet and PySide handle DPI scaling natively.

## 3. SQLite Concurrent Access
- **Pitfall**: If monitoring thread writes and UI thread reads SQLite simultaneously.
- **Mitigation**: Use a simple Lock or queue-based writer for the database.
