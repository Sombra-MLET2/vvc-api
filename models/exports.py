from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import mapped_column, relationship, Mapped

from infra.database.database import Base
from models.category import Category
from models.country import Country


class Export(Base):
    __tablename__ = 'exports'

    id = Column(Integer, autoincrement=True, primary_key=True)
    quantity = Column(Integer)
    value = Column(Float)
    year = Column(Integer, nullable=False)

    category_id = mapped_column(Integer, ForeignKey('categories.id'), nullable=False)
    category: Mapped["Category"] = relationship()

    country_id = mapped_column(Integer, ForeignKey('countries.id'), nullable=False)
    country: Mapped["Country"] = relationship()
