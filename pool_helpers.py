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


class PoolStats:
    def __init__(self):
        self.connections_created = 0
        self.checkout_count = 0
        self.seen_connections = set()

    def on_new_connection(self, conn_id):
        self.connections_created += 1
        self.seen_connections.add(conn_id)

    def on_checkout(self, conn_id):
        self.checkout_count += 1

    def print_stats(self):
        total_checkouts = self.checkout_count
        new_conn_queries = self.connections_created
        reused_queries = total_checkouts - new_conn_queries

        logger.info("POOL STATISTICS")
        logger.info("=" * 80)
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


async def client_work(client_id, engine):
    logger.debug(f"Client {client_id} | Query 1 | Requesting connection...")
    async with engine.connect() as conn:
        await conn.execute(text("SELECT pg_sleep(0.5)"))

    logger.debug(f"Client {client_id} | Query 2 | Requesting connection...")
    async with engine.connect() as conn:
        await conn.execute(text("SELECT pg_sleep(0.5)"))

    logger.debug(f"Client {client_id} | Query 3 | Requesting connection...")
    async with engine.connect() as conn:
        await conn.execute(text("SELECT pg_sleep(0.5)"))

    logger.debug(f"Client {client_id} | Completed")
