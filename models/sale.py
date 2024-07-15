from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped

from infra.database.database import Base
from models.category import Category


class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    quantity = Column(Integer)
    year = Column(Integer, nullable=False)

    category_id = mapped_column(Integer, ForeignKey('categories.id'), nullable=False)
    category: Mapped["Category"] = relationship()
