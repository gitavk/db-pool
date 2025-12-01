import asyncio

from pool_helpers import create_engine, client_work, logger


async def main():
    logger.info("=" * 80)
    logger.info("POOL CONFIGURATION")
    logger.info("=" * 80)
    logger.info("Pool Size:        3")
    logger.info("Max Overflow:     3")
    logger.info("Total Capacity:   6")
    logger.info("Pool Timeout:     30s")
    logger.info("Pool Recycle:     Disabled")
    logger.info("Pool Pre-ping:    False")
    logger.info("=" * 80)
    logger.info("PostgreSQL max_connections: 8")
    logger.info("=" * 80)
    logger.info("SCENARIO 2: POOL SATURATION")
    logger.info("=" * 80)
    logger.info("Running 6 concurrent clients")
    logger.info("Each client will execute 3 queries")
    logger.info("Expected: Some clients wait, overflow connections created, queue formation")
    logger.info("=" * 80)

    async with create_engine(pool_size=3, max_overflow=3, pool_timeout=30) as (engine, stats):
        tasks = []
        for i in range(1, 7):
            logger.info(f"Starting Client {i}")
            tasks.append(asyncio.create_task(client_work(i, engine)))

        await asyncio.gather(*tasks)

        logger.info("=" * 80)
        logger.info("SCENARIO 2 COMPLETED")
        logger.info("=" * 80)

        stats.print_stats()


if __name__ == "__main__":
    asyncio.run(main())
