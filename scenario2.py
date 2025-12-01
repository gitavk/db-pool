import asyncio

from pool_helpers import create_engine, client_work


async def main():
    print("=" * 80)
    print("POOL CONFIGURATION")
    print("=" * 80)
    print("Pool Size:        3")
    print("Max Overflow:     3")
    print("Total Capacity:   6")
    print("Pool Timeout:     30s")
    print("Pool Recycle:     Disabled")
    print("Pool Pre-ping:    False")
    print("=" * 80)
    print("DATABASE LIMITS")
    print("=" * 80)
    print("PostgreSQL max_connections: 8")
    print("=" * 80)
    print("SCENARIO 2: POOL SATURATION")
    print("=" * 80)
    print("Running 6 concurrent clients")
    print("Each client will execute 3 queries")
    print("Expected: Some clients wait, overflow connections created, queue formation")
    print("=" * 80)

    async with create_engine(pool_size=3, max_overflow=3, pool_timeout=30) as (engine, stats):
        tasks = []
        for i in range(1, 7):
            print(f"\nStarting Client {i}")
            tasks.append(asyncio.create_task(client_work(i, engine)))

        await asyncio.gather(*tasks)

        print("\n" + "=" * 80)
        print("SCENARIO 2 COMPLETED")
        print("=" * 80)

        stats.print_stats()


if __name__ == "__main__":
    asyncio.run(main())
