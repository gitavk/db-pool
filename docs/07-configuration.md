# Configuration Examples

## Conservative (Low-traffic application)
- pool_size: 5
- max_overflow: 5
- pool_timeout: 30
- pool_recycle: 3600

## Moderate (Medium-traffic application)
- pool_size: 10
- max_overflow: 20
- pool_timeout: 60
- pool_recycle: 1800

## Aggressive (High-traffic application)
- pool_size: 20
- max_overflow: 30
- pool_timeout: 120
- pool_recycle: 900

---

[← Previous: Monitoring & Metrics](06-monitoring.md) | [Table of Contents](../README.md) | [Next: Environment Variables →](08-environment-variables.md)
