import asyncio
import os
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import event, text
from dotenv import load_dotenv

load_dotenv()


def get_timestamp():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


def log_print(message):
    print(f"[{get_timestamp()}] {message}")


class Metrics:
    def __init__(self):
        self.created = 0
        self.closed = 0
        self.checkouts = 0
        self.checkins = 0
        self.active = 0

    def log(self, event_type, details=""):
        log_print(f"{event_type}: {details}")

    def summary(self):
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Created:   {self.created}")
        print(f"Closed:    {self.closed}")
        print(f"Checkouts: {self.checkouts}")
        print(f"Checkins:  {self.checkins}")
        print(f"Active:    {self.active}")
        print("="*60)


metrics = Metrics()


def setup_listeners(engine):
    @event.listens_for(engine.sync_engine.pool, "connect")
    def on_connect(dbapi_conn, conn_record):
        metrics.created += 1
        metrics.active += 1
        metrics.log("CONNECT", f"total={metrics.created}")

    @event.listens_for(engine.sync_engine.pool, "close")
    def on_close(dbapi_conn, conn_record):
        metrics.closed += 1
        metrics.active -= 1
        metrics.log("CLOSE", f"active={metrics.active}")

    @event.listens_for(engine.sync_engine.pool, "checkout")
    def on_checkout(dbapi_conn, conn_record, conn_proxy):
        metrics.checkouts += 1
        metrics.log("CHECKOUT", f"checkout #{metrics.checkouts}")

    @event.listens_for(engine.sync_engine.pool, "checkin")
    def on_checkin(dbapi_conn, conn_record):
        metrics.checkins += 1
        metrics.log("CHECKIN", f"checkin #{metrics.checkins}")


async def client_work(client_id, engine, duration=2.0):
    try:
        log_print(f"Client {client_id}: requesting connection")

        async with engine.connect() as conn:
            log_print(f"Client {client_id}: got connection, working...")
            await conn.execute(text("SELECT 1"))
            await asyncio.sleep(duration)
            log_print(f"Client {client_id}: done")

    except Exception as e:
        log_print(f"Client {client_id}: ERROR - {e}")


async def main():
    print("\n" + "="*60)
    print("SCENARIO 1: NORMAL OPERATION")
    print("="*60)
    print("Clients: 3")
    print("Pool: size=5, max_overflow=10")
    print("="*60 + "\n")

    database_url = os.getenv("DATABASE_URL")

    engine = create_async_engine(
        database_url,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30.0,
    )

    setup_listeners(engine)

    tasks = [client_work(i, engine) for i in range(3)]
    await asyncio.gather(*tasks)

    await engine.dispose()
    metrics.summary()


if __name__ == "__main__":
    asyncio.run(main())
