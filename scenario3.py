import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from pool_helpers import Metrics, setup_listeners, client_work


CLIENTS = 10
POOL_SIZE = 3
MAX_OVERFLOW = 3
POOL_TIMEOUT = 2.0
HOLD_DURATION = 2.0


async def main():
    print("\n" + "=" * 60)
    print("SCENARIO 3: POOL EXHAUSTION")
    print("=" * 60)
    print(f"Clients: {CLIENTS}")
    print(f"Pool: size={POOL_SIZE}, max_overflow={MAX_OVERFLOW}")
    print("=" * 60 + "\n")

    database_url = os.getenv("DATABASE_URL")
    metrics = Metrics()

    engine = create_async_engine(
        database_url,
        pool_size=POOL_SIZE,
        max_overflow=MAX_OVERFLOW,
        pool_timeout=POOL_TIMEOUT,
    )

    setup_listeners(engine, metrics)

    tasks = [client_work(i, engine, metrics=metrics, hold_duration=HOLD_DURATION) for i in range(CLIENTS)]
    await asyncio.gather(*tasks)

    await engine.dispose()
    metrics.finalize()
    metrics.summary()


if __name__ == "__main__":
    asyncio.run(main())
