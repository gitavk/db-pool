import asyncio

from pool_helpers import create_engine, logger, log_pool_config
from sqlalchemy import text


CLIENTS = 10
POOL_SIZE = 3
MAX_OVERFLOW = 0
POOL_TIMEOUT = 3
LEAK_CONNECTIONS = 2


async def leaky_client_work(client_id, engine, leak=False, leaked_connections=None):
    logger.debug(f"Client {client_id} | Requesting connection...")
    conn = await engine.connect()

    try:
        await conn.execute(text("SELECT pg_sleep(1)"))
        logger.debug(f"Client {client_id} | Query executed")

        if leak:
            logger.debug(f"Client {client_id} | LEAKING connection (not closing)")
            if leaked_connections is not None:
                leaked_connections.append(conn)
        else:
            await conn.close()
            logger.debug(f"Client {client_id} | Connection returned to pool")
    except Exception as e:
        await conn.close()
        raise e


async def main():
    log_pool_config(POOL_SIZE, MAX_OVERFLOW, POOL_TIMEOUT)

    logger.info("=" * 80)
    logger.info("SCENARIO 4: CONNECTION LEAK DETECTION")
    logger.info("=" * 80)
    logger.info(f"Running {CLIENTS} clients total")
    logger.info(f"First {LEAK_CONNECTIONS} clients will leak connections")
    logger.info(f"Remaining {CLIENTS - LEAK_CONNECTIONS} clients will try to get connections")
    logger.info("Expected: Pool exhaustion, timeouts, leaked connections never returned")
    logger.info("=" * 80)

    async with create_engine(pool_size=POOL_SIZE, max_overflow=MAX_OVERFLOW, pool_timeout=POOL_TIMEOUT) as (engine, stats):
        all_results = []
        leaked_connections = []

        logger.debug(f"--- Phase 1: Leaking {LEAK_CONNECTIONS} connections ---")
        leak_tasks = []
        for i in range(LEAK_CONNECTIONS):
            logger.debug(f"Starting Leaky Client {i}")
            leak_tasks.append(asyncio.create_task(
                leaky_client_work(i, engine, leak=True, leaked_connections=leaked_connections)
            ))

        leak_results = await asyncio.gather(*leak_tasks, return_exceptions=True)
        all_results.extend(leak_results)

        logger.debug(f"Phase 1 complete: {LEAK_CONNECTIONS} connections leaked")

        logger.debug(f"--- Phase 2: Attempting {CLIENTS - LEAK_CONNECTIONS} normal operations ---")
        normal_tasks = []
        for i in range(LEAK_CONNECTIONS, CLIENTS):
            logger.debug(f"Starting Normal Client {i}")
            normal_tasks.append(asyncio.create_task(leaky_client_work(i, engine, leak=False)))

        normal_results = await asyncio.gather(*normal_tasks, return_exceptions=True)
        all_results.extend(normal_results)

        timeout_errors = sum(1 for result in all_results if isinstance(result, Exception))

        logger.debug("=" * 80)
        logger.debug(f"\nPhase 2 complete")
        logger.debug("=" * 80)
        logger.debug(f"WARNING: {len(leaked_connections)} connections were leaked and never returned!")
        logger.debug("=" * 80)

        stats.print_stats(
            total_clients=CLIENTS,
            successful_clients=CLIENTS - timeout_errors,
            failed_clients=timeout_errors
        )

        logger.debug(f"\nCleaning up {len(leaked_connections)} leaked connections...")
        for conn in leaked_connections:
            await conn.close()
        logger.debug("Leaked connections cleaned up")


if __name__ == "__main__":
    asyncio.run(main())
