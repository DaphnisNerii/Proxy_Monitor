# Phase 5 Context: Data Persistence & History

## Goal
Implement SQLite-based traffic data persistence to support historical analytics and dashboard visualization.

## Decisions

### 1. Database Schema (SQLite)
- **Database**: `traffic.db` (root directory).
- **Table: `traffic_history`**
  - Columns: `id` (PK), `timestamp` (TEXT), `delta_bytes` (INTEGER), `used_bytes` (INTEGER), `remaining_bytes` (INTEGER).
  - Purpose: Real-time chart data (last 30 days).
- **Table: `daily_stats`**
  - Columns: `date` (TEXT, PK), `total_used` (INTEGER), `max_rate` (INTEGER), `warned` (BOOLEAN).
  - Purpose: Long-term audit and day-over-day tracking.

### 2. Retention Policy
- Clear `traffic_history` entries older than 30 days automatically.
- Clear `daily_stats` entries older than 30 days automatically.

### 3. Architecture: Data Service
- Create `data_service.py` to centralize all DB operations.
- Use **WAL (Write-Ahead Logging)** mode for better concurrent performance (Monitor thread writes, UI thread reads).

### 4. Logic Changes (Monitor Service)
- Replace JSON file reads/writes with `DataService` calls.
- `traffic_state.json` will be migrated and deleted/archived on the first run of the new version.

## Canonical Refs
- `j:/Project/Proxy_Monitor/monitor_service.py` (Current data producer)
- `j:/Project/Proxy_Monitor/.planning/REQUIREMENTS.md` (STAT-02, STAT-03)
