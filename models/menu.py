from typing import List
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Mapped
from infra.database.database import Base
from models.sub_menu import SubMenu


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, unique=True,  nullable=False)
    csv_url = Column(String,  nullable=True)
    sub_menu: Mapped[List["SubMenu"]] = relationship()
