import asyncio

from pool_helpers import create_engine, client_work, logger


async def main():
    logger.info("=" * 80)
    logger.info("POOL CONFIGURATION")
    logger.info("=" * 80)
    logger.info("Pool Size:        5")
    logger.info("Max Overflow:     10")
    logger.info("Total Capacity:   15")
    logger.info("Pool Timeout:     30s")
    logger.info("Pool Recycle:     Disabled")
    logger.info("Pool Pre-ping:    False")
    logger.info("=" * 80)
    logger.info("SCENARIO 1: NORMAL OPERATION")
    logger.info("=" * 80)
    logger.info("Running 3 concurrent clients")
    logger.info("Each client will execute 3 queries")
    logger.info("Expected: Smooth operation, connection reuse, no waiting")
    logger.info("=" * 80)

    async with create_engine(pool_size=5, max_overflow=10, pool_timeout=30) as (engine, stats):
        tasks = []
        for i in range(1, 4):
            logger.info(f"Starting Client {i}")
            tasks.append(asyncio.create_task(client_work(i, engine)))

        await asyncio.gather(*tasks)

        logger.info("=" * 80)
        logger.info("SCENARIO 1 COMPLETED")
        logger.info("=" * 80)

        stats.print_stats()


if __name__ == "__main__":
    asyncio.run(main())
