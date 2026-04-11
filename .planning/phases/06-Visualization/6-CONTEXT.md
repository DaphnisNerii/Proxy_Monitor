# Phase 6 Context: Analytics & Visualization

## Goal
Enhance the Flet UI with a visual analytics dashboard, specifically a 24-hour speed chart and 7-day total usage summary.

## Decisions

### 1. Visualization Components
- **Top Card: 24h Speed LineChart**
  - Metric: `delta_bytes` per minute (formatted as MB/min or KB/min).
  - Visualization: `ft.LineChart` with cubic splines, gradient area fill, and a crosshair tooltip.
  - Data points: Last 24 hours (with intelligent downsampling if performance remains an issue).
- **Bottom Summary: 7d Usage BarChart/Sparkline**
  - Metric: `total_used` per day.
  - Visualization: Row of data cards or a simplified `ft.BarChart`.

### 2. Live Updates
- The dashboard will refresh its charts every time the `TrafficMonitor` pushes new data via the `UIBridge`.
- Incremental updates for the chart (appending new points) to ensure smooth performance.

### 3. Visual Style
- Theme: Material 3 Dark.
- Palette: Primary (Indigo/Blue) for the line, secondary accents for tooltips.
- Responsiveness: The chart will expand to fill available horizontal space.

## Canonical Refs
- `j:/Project/Proxy_Monitor/flet_ui.py` (Implementation target)
- `j:/Project/Proxy_Monitor/data_service.py` (Source of truth)
- `j:/Project/Proxy_Monitor/ui_bridge.py` (Broker for chart data)
