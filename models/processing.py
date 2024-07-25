from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped

from infra.database.database import Base
from models.category import Category


class Processing(Base):
    __tablename__ = 'processing'

    id = Column(Integer, autoincrement=True, primary_key=True)
    cultivation = Column(String, unique=False, nullable=False)
    year = Column(Integer, nullable=False)
    quantity = Column(Integer)

    grape_class_id = mapped_column(Integer, ForeignKey('categories.id'), nullable=False)
    grape_class: Mapped["Category"] = relationship(foreign_keys=[grape_class_id])

    category_id = mapped_column(Integer, ForeignKey('categories.id'), nullable=False)
    category: Mapped["Category"] = relationship(foreign_keys=[category_id])
