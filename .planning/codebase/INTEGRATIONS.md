# External Integrations

**Analysis Date:** 2026-04-11

## Overview

The Proxy Monitor integrates with external network services for traffic data retrieval and user notifications.

## 1. Proxy Subscription APIs

- **Type:** HTTP GET Request
- **Frequency:** Polling (default 60s)
- **Data Source:** User-provided subscription URL (Clash/v2ray format).
- **Mechanism:** Extracts traffic data from the `subscription-userinfo` HTTP response header.
- **Fields Collected:** `upload`, `download`, `total`, `expire`.
- **User Agent:** Impersonates `ClashforWindows/0.19.23` to ensure compatibility with providers.

## 2. ServerChan (SCTAPI)

- **Type:** Webhook (POST Request)
- **Purpose:** Sending push notifications to the user's mobile device.
- **Service URL:** `https://sctapi.ftqq.com/{sendkey}.send`
- **Triggers:**
  - Daily traffic limit exceeded.
  - Burst traffic rate limit exceeded (spike detection).

## 3. Windows Registry

- **Type:** Local OS Integration
- **Purpose:** Managing application auto-start.
- **Key Path:** `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
- **Action:** Sets/removes a registry value pointing to the `.pyw` script.

## 4. Local Persistence

- **File System:**
  - `config.json`: Stores user-defined URLs, keys, and thresholds.
  - `traffic_state.json`: Tracked traffic usage and dates to persist state across restarts.
  - `monitor.log`: Circular logging of stdout/stderr.

---

*Integration mapping: 2026-04-11*
*Update when adding new push services or data providers*
