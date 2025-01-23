from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, func

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    comment = Column(String)
    comment_date = Column(DateTime, server_default=func.now())
    is_active = Column(Boolean, default=True)
