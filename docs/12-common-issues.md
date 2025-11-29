# Common Issues Demonstrated

## Issue 1: "QueuePool limit exceeded"
- Cause: More clients than available connections
- Solution: Increase pool_size or max_overflow, or reduce client concurrency

## Issue 2: "Connection timeout"
- Cause: All connections in use, timeout reached
- Solution: Optimize query performance, reduce transaction duration, increase timeout

## Issue 3: "Lost connection to MySQL/PostgreSQL server"
- Cause: Stale connections due to server timeout
- Solution: Enable pool_recycle or pool_pre_ping

## Issue 4: Memory growth
- Cause: Too many overflow connections created
- Solution: Reduce max_overflow, investigate connection leaks

---

[← Previous: Running Scenarios](11-running-scenarios.md) | [Table of Contents](../README.md) | [Next: PostgreSQL Configuration →](13-postgres-config.md)
