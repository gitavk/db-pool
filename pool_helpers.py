import asyncio
from datetime import datetime
from sqlalchemy import event, text


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
        self.max_overflow_used = 0
        self.query_count = 0
        self.total_query_time = 0.0
        self.start_time = datetime.now()

    def log(self, event_type, details=""):
        log_print(f"{event_type}: {details}")

    def record_query(self, duration):
        self.query_count += 1
        self.total_query_time += duration

    def finalize(self):
        self.end_time = datetime.now()

    def summary(self):
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Created:           {self.created}")
        print(f"Closed:            {self.closed}")
        print(f"Checkouts:         {self.checkouts}")
        print(f"Checkins:          {self.checkins}")
        print(f"Active:            {self.active}")
        print(f"Max Overflow Used: {self.max_overflow_used}")
        print("="*60)

        if self.query_count > 0:
            avg_query_time = self.total_query_time / self.query_count
            print("SQL QUERY PERFORMANCE:")
            print(f"Total Queries:     {self.query_count}")
            print(f"Total Time:        {self.total_query_time:.4f}s")
            print(f"Average Time:      {avg_query_time:.4f}s")
            print("="*60)


def setup_listeners(engine, metrics):
    @event.listens_for(engine.sync_engine.pool, "connect")
    def on_connect(dbapi_conn, conn_record):
        metrics.created += 1
        metrics.active += 1
        pool = engine.sync_engine.pool
        overflow = pool.overflow()
        if overflow > metrics.max_overflow_used:
            metrics.max_overflow_used = overflow
        metrics.log("CONNECT", f"total={metrics.created}, overflow={overflow}")

    @event.listens_for(engine.sync_engine.pool, "close")
    def on_close(dbapi_conn, conn_record):
        metrics.closed += 1
        metrics.active -= 1
        metrics.log("CLOSE", f"active={metrics.active}")

    @event.listens_for(engine.sync_engine.pool, "checkout")
    def on_checkout(dbapi_conn, conn_record, conn_proxy):
        metrics.checkouts += 1
        pool = engine.sync_engine.pool
        metrics.log("CHECKOUT", f"checkout #{metrics.checkouts}, pool={pool.size()}, overflow={pool.overflow()}")

    @event.listens_for(engine.sync_engine.pool, "checkin")
    def on_checkin(dbapi_conn, conn_record):
        metrics.checkins += 1
        metrics.log("CHECKIN", f"checkin #{metrics.checkins}")


async def client_work(client_id, engine, metrics=None):
    try:
        log_print(f"Client {client_id}: requesting connection")

        query_start = datetime.now()
        async with engine.connect() as conn:
            log_print(f"Client {client_id}: got connection, working...")

            result = await conn.execute(text(
                "SELECT count(*) as connections, state FROM pg_stat_activity "
                "WHERE datname = 'demo_db' GROUP BY state ORDER BY state"
            ))
            rows = result.fetchall()
            query_duration = (datetime.now() - query_start).total_seconds()

            if metrics:
                metrics.record_query(query_duration)

            conn_info = ", ".join([f"{row[1]}={row[0]}" for row in rows])
            log_print(f"Client {client_id}: connections [{conn_info}]")
            log_print(f"Client {client_id}: done")

    except Exception as e:
        log_print(f"Client {client_id}: ERROR - {e}")
