# Demo Scenarios

## Scenario 1: Normal Operation
- Pool size: 3
- Max overflow: 3
- Total clients: 10
- Concurrent batch: 3
- Pool timeout: 3s
- Expected behavior: Smooth operation, connection reuse, no waiting

## Scenario 2: Pool Saturation
- Pool size: 3
- Max overflow: 3
- Total clients: 10
- Concurrent batch: 6 (pool_size + max_overflow)
- Pool timeout: 3s
- Expected behavior: Some clients wait, overflow connections created, queue formation

## Scenario 3: Pool Exhaustion
- Pool size: 1
- Max overflow: 2
- Total clients: 10
- Concurrent: All clients at once
- Pool timeout: 2s
- Expected behavior: TimeoutError for clients exceeding total capacity (3)

## Scenario 4: Connection Leak Detection
- Pool size: 3
- Max overflow: 0
- Total clients: 10
- Leaked connections: 2
- Pool timeout: 3s
- Expected behavior: Phase 1 leaks 2 connections, Phase 2 shows pool exhaustion for remaining 8 clients

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
