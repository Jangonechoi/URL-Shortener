from sqlalchemy import Column, String, Integer, DateTime
from app.database import Base
import datetime

class URL(Base):
    __tablename__ = 'urls'
    
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String(2048), nullable=False)
    short_key = Column(String(50), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    click_count = Column(Integer, default=0)  # 기본값을 0으로 설정

