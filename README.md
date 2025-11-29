# PostgreSQL Connection Pool Utilization Demo with SQLAlchemy

This demo application demonstrates how PostgreSQL database connection pooling works with SQLAlchemy in Python. It provides a practical understanding of connection pool behavior, lifecycle, and resource management.

## Documentation

Complete documentation is available in the `docs/` directory:

1. [Overview](docs/01-overview.md) - Project overview and purpose
2. [Prerequisites](docs/02-prerequisites.md) - System requirements and dependencies
3. [Architecture](docs/03-architecture.md) - Application components and structure
4. [Key Concepts](docs/04-key-concepts.md) - Pool configuration and lifecycle events
5. [Demo Scenarios](docs/05-scenarios.md) - Six scenarios demonstrating pool behavior
6. [Monitoring & Metrics](docs/06-monitoring.md) - Real-time statistics and performance tracking
7. [Configuration Examples](docs/07-configuration.md) - Configuration for different traffic levels
8. [Environment Variables](docs/08-environment-variables.md) - Configuration via environment
9. [Expected Outcomes](docs/09-expected-outcomes.md) - Learning goals and best practices
10. [Visualization](docs/10-visualization.md) - Output and visualization features
11. [Running Scenarios](docs/11-running-scenarios.md) - Command-line options for scenarios
12. [Common Issues](docs/12-common-issues.md) - Troubleshooting guide
13. [PostgreSQL Configuration](docs/13-postgres-config.md) - Server configuration recommendations
14. [Learning Path](docs/14-learning-path.md) - Recommended learning progression

## Quick Start

```bash
# Install dependencies
pip install sqlalchemy asyncpg python-dotenv

# Set up environment variables
export DATABASE_URL="postgresql://user:password@localhost/dbname"
export POOL_SIZE=5
export MAX_OVERFLOW=10
```

## License

This demo application is provided for educational purposes.
