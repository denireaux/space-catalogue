from fastapi import FastAPI, Depends
from sqlalchemy import text
from src.utils import get_logger, database_init, get_db_conn
from src.poller import login, BackgroundScheduler, poll_and_upsert

log = get_logger()
app = FastAPI()
engine, SessionLocal = database_init()

@app.on_event("startup")
def startup_event():
    log.info("API started")
    login()
    scheduler = BackgroundScheduler()
    scheduler.add_job(poll_and_upsert, "interval", hours=1, args=[engine])
    scheduler.start()
    poll_and_upsert(engine)

@app.get("/gps")
def get_last_fifty_gps(conn = Depends(get_db_conn), limit: int = 50):
    result = conn.execute(text("SELECT * FROM gp ORDER BY epoch DESC LIMIT :l"), {"l": limit})
    return [dict(row._mapping) for row in result]

@app.get("/starlinks")
def get_starlinks(conn = Depends(get_db_conn)):
    result = conn.execute(text("SELECT * FROM gp WHERE object_name ILIKE '%STARLINK%';"))
    return [dict(row._mapping) for row in result]