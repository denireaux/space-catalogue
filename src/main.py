from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy import text
from datetime import datetime, timezone
from src.utils import get_logger, get_db_conn, sync_engine
from src.poller import login, BackgroundScheduler, poll_and_upsert

log = get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("API started")
    login()
    scheduler = BackgroundScheduler()
    scheduler.add_job(poll_and_upsert, "interval", hours=1, args=[sync_engine], next_run_time=datetime.now(timezone.utc))
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/messages/all")
async def get_messages(conn = Depends(get_db_conn)):
    result = await conn.execute(text("SELECT * FROM gp ORDER BY epoch DESC LIMIT 100"))
    return [dict(row._mapping) for row in result]
