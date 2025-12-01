import asyncio

from pool_helpers import create_engine, client_work, logger, log_pool_config


CLIENTS = 10
POOL_SIZE = 1
MAX_OVERFLOW = 2
POOL_TIMEOUT = 2


async def main():
    log_pool_config(POOL_SIZE, MAX_OVERFLOW, POOL_TIMEOUT)

    logger.info("=" * 80)
    logger.info("SCENARIO 3: POOL EXHAUSTION")
    logger.info("=" * 80)
    logger.info(f"Running {CLIENTS} clients concurrently")
    logger.info("Each client will execute 1 queries")
    logger.info("Expected: TimeoutError for clients exceeding total capacity")
    logger.info("=" * 80)

    async with create_engine(pool_size=POOL_SIZE, max_overflow=MAX_OVERFLOW, pool_timeout=POOL_TIMEOUT) as (engine, stats):
        tasks = []
        for i in range(CLIENTS):
            logger.debug(f"Starting Client {i}")
            tasks.append(asyncio.create_task(client_work(i, engine)))

        # Gather with return_exceptions to catch TimeoutErrors
        results = await asyncio.gather(*tasks, return_exceptions=True)

        timeout_errors = 0
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                timeout_errors += 1
                logger.debug(f"Client {i} | Error: {type(result).__name__}")

        logger.debug("=" * 80)
        stats.print_stats(
            total_clients=CLIENTS,
            successful_clients=CLIENTS - timeout_errors,
            failed_clients=timeout_errors
        )


if __name__ == "__main__":
    asyncio.run(main())
