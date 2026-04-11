# Research Summary: v1.1 UX & Analytics

## Key Findings

1.  **Framework Selection**: **Flet** is highly recommended for its extreme aesthetic modularity and ease of building modern, animated dashboards. It creates a "wow" factor that is hard to achieve with pure Python logic in PyQt or Tkinter.
2.  **Dashboard Integration**: Flet's built-in `LineChart` and `BarChart` components cater perfectly to our traffic data needs.
3.  **Architecture**: The core logic is already modular but needs a clearer "Bridge/Presenter" layer to facilitate the framework swap without rewriting the monitor logic.

## Recommended Stack
- **UI**: Flet (Python library based on Flutter)
- **Status Tray**: Pystray (Keep existing)
- **Charts**: Flet LineChart
- **Database**: SQLite (for historical traffic logs)

## Watch Out For
- Ensure the `pystray` icon remains responsive when the Flet window is closed/reopened.
- Threading issues between UI and Monitoring loop.
