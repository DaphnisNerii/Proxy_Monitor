# Plan: Phase 5 - Data Persistence & History

## Goal
Implement SQLite-based data persistence with a 30-day retention policy and automatic migration from JSON.

## Wave 1: Data Service & Schema
<task id="05-W1-01" read_first="[]" autonomous="true">
<action>
Create `data_service.py` with `DataService` singleton. Implement schema initialization for `traffic_history` and `daily_stats`.
</action>
<acceptance_criteria>
data_service.py exists and creates traffic.db with correct tables in WAL mode.
</acceptance_criteria>
</task>

<task id="05-W1-02" read_first="data_service.py" autonomous="true">
<action>
Implement `record_traffic(delta, used, remaining)` in `DataService`.
</action>
<acceptance_criteria>
Calling record_traffic inserts a row into traffic_history and updates/inserts into daily_stats for current date.
</acceptance_criteria>
</task>

## Wave 2: Monitor Service Integration
<task id="05-W2-01" read_first="monitor_service.py, data_service.py" autonomous="true">
<action>
Modify `TrafficMonitor` in `monitor_service.py` to use `DataService` instead of writing to JSON.
</action>
<acceptance_criteria>
run_loop calls data_service.record_traffic instead of json.dump.
</acceptance_criteria>
</task>

<task id="05-W2-02" read_first="main.pyw" autonomous="true">
<action>
Modify `main.pyw` to initialize `DataService` on startup.
</action>
<acceptance_criteria>
App starts without error, and DataService is passed or accessible.
</acceptance_criteria>
</task>

## Wave 3: Migration & Pruning
<task id="05-W3-01" read_first="data_service.py" autonomous="true">
<action>
Implement `migrate_from_json(json_path)` in `DataService`.
</action>
<acceptance_criteria>
If traffic_state.json exists, values are imported into DB and file is renamed to .bak.
</acceptance_criteria>
</task>

<task id="05-W3-02" read_first="data_service.py" autonomous="true">
<action>
Implement `prune_old_data(days=30)` in `DataService` and call it periodically.
</action>
<acceptance_criteria>
Records older than 30 days are removed from both tables.
</acceptance_criteria>
</task>

## Wave 4: Integration Test
<task id="05-W4-01" read_first="[]" autonomous="true">
<action>
Create a test script `test_persistence.py` in `scratch/` to verify DB reads/writes and pruning.
</action>
<acceptance_criteria>
Test script runs and confirms data integrity.
</acceptance_criteria>
</task>

## Requirements Covered
- **STAT-02**: SQLite logging.
- **STAT-03**: Historical data retention.

## must_haves
- [ ] SQLite WAL mode enabled.
- [ ] Thread-safe database access (Connections per thread).
- [ ] 30-day auto-pruning active.
- [ ] JSON data migrated on first run.
