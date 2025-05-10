from sqlalchemy import Column, Integer, String, Float, Boolean, ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Ad(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    category = Column(String, nullable=False)
    type = Column(String, nullable=False)
    target_keywords = Column(ARRAY(String), default=list)
    ctr = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True) 