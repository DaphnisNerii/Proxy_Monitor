# Research: Flet LineChart for Analytics

## Implementation Details

### 1. Chart Configuration
- **Control**: `ft.LineChart`.
- **Interactivity**: `interactive=True` for tooltips.
- **Smoothing**: `curved=True` and `curve_smoothness=0.35` on `LineChartData` for a premium, non-jagged look.
- **Visuals**: `below_line_gradient` with a vertical linear gradient (Theme Color -> Transparent).

### 2. Data Transformation
- **X-Axis**: Timestamps converted to numerical values (e.g., minutes from 24h ago).
- **Y-Axis**: Traffic delta (formatted reasonably).
- **Downsampling**: For the 24h view (~1440 points), I will use simple aggregation (averaging points) if the Flet Chart performance is an issue, but standard Flet charts can often handle 1k points smoothly.

### 3. Axis Formatting
- **Bottom Labels**: Show time (e.g., 14:00, 16:00) using `get_bottom_labels()` callback.
- **Left Labels**: Show traffic units (e.g., 2.5 MB).

## Code Snippet (Template)
```python
chart = ft.LineChart(
    data_series=[
        ft.LineChartData(
            points=[ft.LineChartDataPoint(x, y), ...],
            curved=True,
            below_line_gradient=ft.LinearGradient(...)
        )
    ],
    bottom_axis=ft.ChartAxis(labels=[...]),
    interactive=True
)
```
