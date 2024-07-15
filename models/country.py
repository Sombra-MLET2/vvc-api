from sqlalchemy import Column, Integer, String

from infra.database.database import Base


class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, unique=True, nullable=False)
