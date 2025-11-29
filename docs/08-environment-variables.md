# Environment Variables

The demo uses environment variables for configuration:

- `DATABASE_URL`: PostgreSQL connection string
- `POOL_SIZE`: Number of permanent connections
- `MAX_OVERFLOW`: Additional overflow connections
- `POOL_TIMEOUT`: Connection wait timeout in seconds
- `POOL_RECYCLE`: Connection recycle time in seconds
- `POOL_PRE_PING`: Enable connection pre-ping validation
- `ECHO_POOL`: Enable SQLAlchemy pool logging
- `LOG_LEVEL`: Application logging level

---

[← Previous: Configuration Examples](07-configuration.md) | [Table of Contents](../README.md) | [Next: Expected Outcomes →](09-expected-outcomes.md)
