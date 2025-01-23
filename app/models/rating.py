from sqlalchemy.orm import relationship
from app.backend.db import Base
from sqlalchemy import Integer, Column, ForeignKey, Boolean, Float

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    grade = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    review_id = Column(Integer, ForeignKey("reviews.id"))
    is_active = Column(Boolean, default=True)

    product = relationship("Product", back_populates="rating_table")
