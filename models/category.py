from sqlalchemy import Column, Integer, String

from infra.database.database import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    meta_name = Column(String, unique=True, nullable=True)

    def __repr__(self):
        return f"Category [id={self.id}, name={self.name}, meta_name={self.meta_name}]"