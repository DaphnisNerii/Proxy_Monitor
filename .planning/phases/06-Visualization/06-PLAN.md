# Plan: Phase 6 - Analytics & Visualization

## Goal
Implement a visual analytics dashboard in the Flet UI showing 24h speed trends and 7d usage summaries.

## Wave 1: Data Access Layer
<task id="06-W1-01" read_first="data_service.py" autonomous="true">
<action>
Add `get_recent_history(hours=24)` to `DataService` to return speed/delta points.
</action>
<acceptance_criteria>
Method returns a list of (timestamp, delta_bytes) tuples.
</acceptance_criteria>
</task>

<task id="06-W1-02" read_first="data_service.py" autonomous="true">
<action>
Add `get_stats_summary(days=7)` to `DataService` to return daily total usage.
</action>
<acceptance_criteria>
Method returns a list of (date, total_used) tuples.
</acceptance_criteria>
</task>

## Wave 2: Dashboard Implementation
<task id="06-W2-01" read_first="flet_ui.py" autonomous="true">
<action>
Refactor `_show_dashboard` in `FletUI` to include a `ft.LineChart` for the 24h speed view.
</action>
<acceptance_criteria>
Dashboard shows a functional (even if empty) line chart with theme-aligned colors.
</acceptance_criteria>
</task>

<task id="06-W2-02" read_first="flet_ui.py" autonomous="true">
<action>
Update the dashboard to show 7d usage cards or a small bar chart.
</action>
<acceptance_criteria>
Usage summary for the week is visible.
</acceptance_criteria>
</task>

## Wave 3: Real-time Integration
<task id="06-W3-01" read_first="ui_bridge.py, flet_ui.py" autonomous="true">
<action>
Update `UIBridge` to fetch and push chart data periodically or on demand.
</action>
<acceptance_criteria>
Charts update their data points when the monitor service completes a cycle.
</acceptance_criteria>
</task>

## Wave 4: Polish & Refinement
<task id="06-W4-01" read_first="flet_ui.py" autonomous="true">
<action>
Add axis labels, tooltips, and smooth bezier curves to the LineChart.
</action>
<acceptance_criteria>
Chart displays time labels on X-axis and data values on hover.
</acceptance_criteria>
</task>

## Requirements Covered
- **STAT-02**: Visualization of speed data.
- **STAT-04**: Enhanced visual dashboard reporting.

## must_haves
- [ ] Smooth 24h speed curve with gradient fill.
- [ ] Last 7 days usage summary.
- [ ] Responsive chart resizing.
- [ ] Efficient data loading (no UI lag).
