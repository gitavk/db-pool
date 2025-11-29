# Demo Scenarios

## Scenario 1: Normal Operation
- Pool size: 5
- Concurrent clients: 3
- Expected behavior: Smooth operation, connection reuse, no waiting

## Scenario 2: Pool Saturation
- Pool size: 5
- Concurrent clients: 10
- Expected behavior: Some clients wait, overflow connections created, queue formation

## Scenario 3: Pool Exhaustion
- Pool size: 5, max_overflow: 5
- Concurrent clients: 15
- Expected behavior: TimeoutError for clients exceeding total capacity

## Scenario 4: Connection Leak Detection
- Pool size: 5
- Simulated leak: Connections not returned
- Expected behavior: Pool exhaustion, monitoring alerts, recovery after timeout

## Scenario 5: Connection Recycling
- Pool size: 5, pool_recycle: 3600
- Long-running application
- Expected behavior: Periodic connection refresh, stale connection prevention

## Scenario 6: Pre-ping Validation
- Pool size: 5, pool_pre_ping: True
- Simulated database restart
- Expected behavior: Invalid connections detected and recreated automatically

---

[← Previous: Key Concepts](04-key-concepts.md) | [Table of Contents](../README.md) | [Next: Monitoring & Metrics →](06-monitoring.md)
