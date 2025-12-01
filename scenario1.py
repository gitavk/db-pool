import asyncio

from pool_helpers import create_engine, client_work, logger, log_pool_config


CLIENTS = 10
POOL_SIZE = 3
MAX_OVERFLOW = 3
POOL_TIMEOUT = 3


async def main():
    log_pool_config(POOL_SIZE, MAX_OVERFLOW, POOL_TIMEOUT)

    logger.info("=" * 80)
    logger.info("SCENARIO 1: NORMAL OPERATION")
    logger.info("=" * 80)
    logger.info(f"Running {CLIENTS} clients with concurrent batch {POOL_SIZE}")
    logger.info("Each client will execute 1 queries")
    logger.info("Expected: Smooth operation, connection reuse, no waiting")
    logger.info("=" * 80)

    async with create_engine(pool_size=POOL_SIZE, max_overflow=MAX_OVERFLOW, pool_timeout=POOL_TIMEOUT) as (engine, stats):
        i = 0
        all_results = []
        while i < CLIENTS:
            tasks = []
            for _ in range(POOL_SIZE):
                if i >= CLIENTS:
                    break
                logger.debug(f"Starting Client {i}")
                tasks.append(asyncio.create_task(client_work(i, engine)))
                i += 1
            results = await asyncio.gather(*tasks, return_exceptions=True)
            all_results.extend(results)

        timeout_errors = sum(1 for result in all_results if isinstance(result, Exception))

        logger.debug("=" * 80)

        stats.print_stats(
            total_clients=CLIENTS,
            successful_clients=CLIENTS - timeout_errors,
            failed_clients=timeout_errors
        )


if __name__ == "__main__":
    asyncio.run(main())
