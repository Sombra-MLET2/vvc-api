from sqlalchemy import Column, Integer, String

from infra.database.database import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    meta_name = Column(String, unique=True, nullable=True)
