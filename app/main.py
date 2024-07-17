from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app import models, schemas, crud, database
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import datetime

app = FastAPI()

# Middleware 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터베이스 초기화
models.Base.metadata.create_all(bind=database.engine)

@app.on_event("startup")
async def startup():
    await database.database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.database.disconnect()

# 종속성 주입
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/shorten", response_model=schemas.URLResponse)
def create_short_url(url: schemas.URLCreate, db: Session = Depends(get_db)):
    db_url = crud.create_short_url(db, url)
    short_url = f"http://localhost:8000/{db_url.short_key}"
    return {"short_url": short_url}

@app.get("/{short_key}")
def redirect_url(short_key: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_short_key(db, short_key)
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    if db_url.expires_at and db_url.expires_at < datetime.datetime.utcnow():
        raise HTTPException(status_code=404, detail="URL has expired")
    crud.update_click_count(db, short_key)
    return RedirectResponse(db_url.original_url)

@app.get("/stats/{short_key}", response_model=schemas.URLStats)
def get_url_stats(short_key: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_short_key(db, short_key)
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"short_key": db_url.short_key, "click_count": db_url.click_count}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

