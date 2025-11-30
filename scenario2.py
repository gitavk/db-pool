import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
from pool_helpers import Metrics, setup_listeners, client_work

load_dotenv()

CLIENTS = 5
POOL_SIZE = 3
MAX_OVERFLOW = 4
POOL_TIMEOUT = 30.0
WORK_DURATION = 3.0


async def main():
    print("\n" + "="*60)
    print("SCENARIO 2: POOL SATURATION")
    print("="*60)
    print(f"Clients: {CLIENTS}")
    print(f"Pool: size={POOL_SIZE}, max_overflow={MAX_OVERFLOW}")
    print("="*60 + "\n")

    database_url = os.getenv("DATABASE_URL")
    metrics = Metrics()

    engine = create_async_engine(
        database_url,
        pool_size=POOL_SIZE,
        max_overflow=MAX_OVERFLOW,
        pool_timeout=POOL_TIMEOUT,
    )

    setup_listeners(engine, metrics)

    tasks = [client_work(i, engine, duration=WORK_DURATION) for i in range(CLIENTS)]
    await asyncio.gather(*tasks)

    await engine.dispose()
    metrics.summary()


if __name__ == "__main__":
    asyncio.run(main())
