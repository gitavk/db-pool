# PostgreSQL Server Configuration

For optimal demo experience, consider these PostgreSQL settings:

- `max_connections`: Should be higher than your application's total pool connections
- `idle_in_transaction_session_timeout`: Prevents stuck transactions
- `statement_timeout`: Prevents runaway queries

Recommended: `max_connections` ≥ (application instances × (pool_size + max_overflow)) + 20

---

[← Previous: Common Issues](12-common-issues.md) | [Table of Contents](../README.md) | [Next: Learning Path →](14-learning-path.md)
