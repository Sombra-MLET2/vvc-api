from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped

from infra.database.database import Base
from models.category import Category


class Production(Base):
    __tablename__ = 'productions'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer)
    year = Column(Integer, nullable=False)
    category: Mapped["Category"] = relationship()
    category_id = mapped_column(Integer, ForeignKey('categories.id'), nullable=False)

    def __repr__(self):
        return f"Production [id={self.id}, name={self.name}, quantity={self.quantity}, year={self.year}, category={self.category}, category_id={self.category_id}]"