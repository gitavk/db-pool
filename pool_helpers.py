import datetime as dt
import os
import logging
from contextlib import asynccontextmanager
from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import create_async_engine


logging.basicConfig(
    format='[%(asctime)s.%(msecs)03d] %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def log_pool_config(pool_size, max_overflow, pool_timeout):
    """Log pool configuration details"""
    logger.debug("=" * 80)
    logger.debug("POOL CONFIGURATION")
    logger.debug("=" * 80)
    logger.debug(f"Pool Size:        {pool_size}")
    logger.debug(f"Max Overflow:     {max_overflow}")
    logger.debug(f"Total Capacity:   {pool_size + max_overflow}")
    logger.debug(f"Pool Timeout:     {pool_timeout}s")
    logger.debug("Pool Recycle:     Disabled")
    logger.debug("Pool Pre-ping:    False")
    logger.debug("PostgreSQL max_connections: 8")
    logger.debug("=" * 80)


class PoolStats:
    def __init__(self):
        self.connections_created = 0
        self.checkout_count = 0
        self.seen_connections = set()
        self.start_time = dt.datetime.now()

    def on_new_connection(self, conn_id):
        self.connections_created += 1
        self.seen_connections.add(conn_id)

    def on_checkout(self, conn_id):
        self.checkout_count += 1

    def print_stats(self, total_clients=None, successful_clients=None, failed_clients=None):
        total_checkouts = self.checkout_count
        new_conn_queries = self.connections_created
        reused_queries = total_checkouts - new_conn_queries
        elapsed_time = (dt.datetime.now() - self.start_time).total_seconds()

        logger.info("POOL STATISTICS")
        logger.info("=" * 80)
        logger.info(f"Total time elapsed:            {elapsed_time:.2f}s")

        # Client statistics (optional)
        if total_clients is not None:
            logger.info(f"Total clients:                 {total_clients}")
        if successful_clients is not None:
            logger.info(f"Successful clients:            {successful_clients}")
        if failed_clients is not None:
            logger.info(f"Failed clients (timeout):      {failed_clients}")

        logger.info(f"Total connections created:     {self.connections_created}")
        logger.info(f"Total checkouts:               {total_checkouts}")
        logger.info(f"Queries with new connection:   {new_conn_queries}")
        logger.info(f"Queries reusing connection:    {reused_queries}")
        if total_checkouts > 0:
            reuse_percent = (reused_queries / total_checkouts) * 100
            logger.info(f"Connection reuse rate:         {reuse_percent:.1f}%")
        logger.info("=" * 80)


def setup_listeners(engine, stats):
    pool = engine.sync_engine.pool

    @event.listens_for(pool, "connect")
    def on_connect(dbapi_conn, conn_record):
        conn_id = id(dbapi_conn)
        stats.on_new_connection(conn_id)
        logger.debug(f"CONNECT Created, overflow={pool.overflow()}")

    @event.listens_for(pool, "close")
    def on_close(dbapi_conn, conn_record):
        logger.debug("CLOSE active")

    @event.listens_for(pool, "checkout")
    def on_checkout(dbapi_conn, conn_record, conn_proxy):
        conn_id = id(dbapi_conn)
        stats.on_checkout(conn_id)
        logger.debug(
            f"CHECKOUT checkout pool={pool.size()}, overflow={pool.overflow()}",
        )

    @event.listens_for(pool, "checkin")
    def on_checkin(dbapi_conn, conn_record):
        logger.debug("CHECKIN checkin ")


@asynccontextmanager
async def create_engine(pool_size, max_overflow, pool_timeout):
    database_url = os.getenv("DATABASE_URL")
    engine = create_async_engine(
        database_url,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_timeout=pool_timeout,
    )
    stats = PoolStats()
    setup_listeners(engine, stats)
    try:
        yield engine, stats
    finally:
        await engine.dispose()

SQL_STATMENT = text("SELECT pg_sleep(1)")

async def client_work(client_id, engine):
    logger.debug(f"Client {client_id} | Requesting connection...")
    async with engine.connect() as conn:
        await conn.execute(SQL_STATMENT)

    logger.debug(f"Client {client_id} | Completed")
