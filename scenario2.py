import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
from pool_helpers import Metrics, setup_listeners, client_work

load_dotenv()


async def main():
    print("\n" + "="*60)
    print("SCENARIO 2: POOL SATURATION")
    print("="*60)
    print("Clients: 10")
    print("Pool: size=5, max_overflow=10")
    print("="*60 + "\n")

    database_url = os.getenv("DATABASE_URL")
    metrics = Metrics()

    engine = create_async_engine(
        database_url,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30.0,
    )

    setup_listeners(engine, metrics)

    tasks = [client_work(i, engine, duration=3.0) for i in range(10)]
    await asyncio.gather(*tasks)

    await engine.dispose()
    metrics.summary()


if __name__ == "__main__":
    asyncio.run(main())
