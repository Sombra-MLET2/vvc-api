from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship

from infra.database.database import Base


class Processing(Base):
    __tablename__ = 'processings'

    id = Column(Integer, autoincrement=True, primary_key=True)
    grape_class = Column(String, unique=True, nullable=False)
    cultivation = Column(String, unique=True, nullable=False)
    year = Column(Integer, nullable=False)
    quantity = Column(Integer)

    category_id = mapped_column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship()
