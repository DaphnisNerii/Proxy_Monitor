# Research: SQLite Optimization for Proxy Monitor

## Use Case
- Frequency: ~60 seconds per write.
- Data Volume: Small (KB range).
- Concurrency: Background thread writes, UI thread reads.

## Key Findings

### 1. Concurrency (WAL Mode)
- **Problem**: Default SQLite journaling locks the whole DB on write.
- **Solution**: Enable `PRAGMA journal_mode=WAL;`. This allows readers (UI) to access data while the writer (Monitor) is active.
- **Implementation**: Set once via connection init.

### 2. Threading in Python `sqlite3`
- **Constraint**: `sqlite3` connections cannot be shared across threads by default (`check_same_thread=True`).
- **Patterns**:
  - **A. One Connection per Thread**: UI thread has its own, Monitor thread has its own.
  - **B. Re-opening**: Open, write, close. (Higher overhead, but simplest for 60s frequency).
- **Decision**: **Thread-Local Connections**. Use a singleton `DataService` that manages a local connection per thread.

### 3. Disk Performance
- **Tweak**: `PRAGMA synchronous = NORMAL;`.
- **Impact**: Reduces disk sync frequency without losing integrity in WAL mode.

### 4. Automatic Pruning
- **Trigger**: During insertion into `traffic_history`, check if `id % 100 == 0` (every 100 logs) to run a `DELETE` query for entries older than 30 days.

## Data Schema Recommendation
- `traffic_history`: High granularity for charts.
- `daily_stats`: One row per day.

## Migration Strategy
- On start, check for `traffic_state.json`.
- Read and insert into `daily_stats` and initial `traffic_history`.
- Rename `traffic_state.json` to `traffic_state.json.bak`.
