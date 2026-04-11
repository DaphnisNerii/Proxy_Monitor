# Plan: Phase 4 - UI Framework Migration & System Integration

## Goal
Replace Tkinter with Flet, implement the UI Bridge, and ensure seamless system tray integration.

## Wave 1: Infrastructure & Decoupling
<task id="04-W1-01" read_first="requirements.txt" autonomous="true">
<action>
Add `flet` to `requirements.txt`.
</action>
<acceptance_criteria>
requirements.txt contains flet
</acceptance_criteria>
</task>

<task id="04-W1-02" read_first="[]" autonomous="true">
<action>
Create `ui_bridge.py` containing the `UIBridge` class to mediate between UI and Logic.
</action>
<acceptance_criteria>
ui_bridge.py exists and exposes UIBridge class
</acceptance_criteria>
</task>

## Wave 2: Core Loop & Tray Integration
<task id="04-W2-01" read_first="tray_app.py" autonomous="true">
<action>
Update `tray_app.py` to use `UIBridge` instead of directly calling logic or monitor.
</action>
<acceptance_criteria>
ProxyTrayIcon constructor takes bridge as an argument
</acceptance_criteria>
</task>

<task id="04-W2-02" read_first="main.pyw" autonomous="true">
<action>
Refactor `main.pyw` to remove Tkinter root and replace it with Flet and the UI Bridge.
</action>
<acceptance_criteria>
main.pyw no longer imports tkinter (except for error fallbacks) and calls ft.app
</acceptance_criteria>
</task>

## Wave 3: Flet UI Implementation
<task id="04-W3-01" read_first="[]" autonomous="true">
<action>
Create `flet_ui.py` with the modern sidebar layout and settings page.
</action>
<acceptance_criteria>
flet_ui.py contains the FletUI class with at least Dashboard and Settings tabs
</acceptance_criteria>
</task>

<task id="04-W3-02" read_first="flet_ui.py, ui_bridge.py" autonomous="true">
<action>
Wire the Save button in Flet settings to bridge.save_config().
</action>
<acceptance_criteria>
Clicking save in UI triggers config update in config_manager
</acceptance_criteria>
</task>

## Wave 4: Cleanup & Verification
<task id="04-W4-01" read_first="ui_components.py" autonomous="true">
<action>
Remove `ui_components.py` (Tkinter-based).
</action>
<acceptance_criteria>
ui_components.py no longer exists
</acceptance_criteria>
</task>

<task id="04-W4-02" read_first="main.pyw" autonomous="true">
<action>
Final Integration Test: Run the app and verify tray + Flet UI works.
</action>
<acceptance_criteria>
App runs without errors, UI settings match config.json
</acceptance_criteria>
</task>

## Requirements Covered
- **UI-MOD-01**: Flet migration and visual enhancement.
- **ARCH-EXP-04**: MVP/Bridge pattern implementation.
- **ARCH-EXP-05**: Modernized tray-UI threading.

## must_haves
- [ ] No Tkinter dependencies in main loop.
- [ ] UI Bridge singleton mediating all cross-thread config updates.
- [ ] Tray icon remains responsive during UI interaction.
