from pydantic import BaseModel
from typing import Optional
import datetime

class URLCreate(BaseModel):
    url: str
    expires_at: Optional[datetime.datetime] = None

class URLResponse(BaseModel):
    short_url: str

    class Config:
        from_attributes = True

class URLStats(BaseModel):
    short_key: str
    click_count: int  # 정수 타입 확인

