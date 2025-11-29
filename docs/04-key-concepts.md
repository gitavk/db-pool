# Key Concepts Demonstrated

## 1. Connection Pool Basics

The demo shows how SQLAlchemy creates a pool of reusable database connections instead of opening a new connection for each query. This includes:

- Initial pool creation with a specified size
- Connection reuse across multiple operations
- Automatic connection management

## 2. Pool Configuration Parameters

### Pool Size
- **pool_size**: Maximum number of permanent connections (default: 5)
- Determines how many connections are kept alive in the pool

### Max Overflow
- **max_overflow**: Additional temporary connections beyond pool_size (default: 10)
- Total possible connections = pool_size + max_overflow

### Pool Timeout
- **pool_timeout**: Seconds to wait for an available connection (default: 30)
- Raises TimeoutError if no connection available within timeout

### Pool Recycle
- **pool_recycle**: Seconds before recycling connections (default: -1, disabled)
- Prevents stale connections and handles server-side timeouts

### Pool Pre-ping
- **pool_pre_ping**: Test connections before use (default: False)
- Ensures connection validity before returning from pool

## 3. Connection Lifecycle Events

The demo tracks and displays:

- **connect**: New connection created
- **checkout**: Connection borrowed from pool
- **checkin**: Connection returned to pool
- **close**: Connection permanently closed
- **detach**: Connection removed from pool
- **invalidate**: Connection marked as invalid

## 4. Usage Patterns

### Sequential Operations
Demonstrates a single client performing multiple database operations sequentially, showing how connections are reused efficiently.

### Concurrent Operations
Simulates multiple clients accessing the database simultaneously, illustrating:
- Connection distribution among clients
- Pool saturation behavior
- Queue waiting times

### Long-Running Transactions
Shows impact of holding connections for extended periods:
- Pool depletion
- Other clients waiting for available connections
- Potential timeout scenarios

### Connection Leaks
Demonstrates what happens when connections aren't properly released:
- Pool exhaustion
- Application blocking
- Detection and recovery strategies

---

[← Previous: Architecture](03-architecture.md) | [Table of Contents](../README.md) | [Next: Demo Scenarios →](05-scenarios.md)
