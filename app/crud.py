from sqlalchemy.orm import Session
from app import models, schemas
import shortuuid

def get_url_by_short_key(db: Session, short_key: str):
    db_url = db.query(models.URL).filter(models.URL.short_key == short_key).first()
    if db_url and db_url.click_count is None:
        db_url.click_count = 0
    return db_url

def create_short_url(db: Session, url_create: schemas.URLCreate):
    short_key = shortuuid.ShortUUID().random(length=6)
    db_url = models.URL(
        original_url=url_create.url,
        short_key=short_key,
        expires_at=url_create.expires_at,
        click_count=0  # 클릭 카운트 초기화
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def update_click_count(db: Session, short_key: str):
    db_url = get_url_by_short_key(db, short_key)
    if db_url:
        db_url.click_count += 1
        db.commit()
        db.refresh(db_url)
    return db_url



