import asyncio

from pool_helpers import create_engine, client_work


async def main():
    print("=" * 80)
    print("POOL CONFIGURATION")
    print("=" * 80)
    print("Pool Size:        5")
    print("Max Overflow:     10")
    print("Total Capacity:   15")
    print("Pool Timeout:     30s")
    print("Pool Recycle:     Disabled")
    print("Pool Pre-ping:    False")
    print("=" * 80)
    print("SCENARIO 1: NORMAL OPERATION")
    print("=" * 80)
    print("Running 3 concurrent clients")
    print("Each client will execute 3 queries")
    print("Expected: Smooth operation, connection reuse, no waiting")
    print("=" * 80)

    async with create_engine(pool_size=5, max_overflow=10, pool_timeout=30) as (engine, stats):
        tasks = []
        for i in range(1, 4):
            print(f"\nStarting Client {i}")
            tasks.append(asyncio.create_task(client_work(i, engine)))

        await asyncio.gather(*tasks)

        print("\n" + "=" * 80)
        print("SCENARIO 1 COMPLETED")
        print("=" * 80)

        stats.print_stats()


if __name__ == "__main__":
    asyncio.run(main())
