from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from infra.database.database import Base


class SubMenu(Base):
    __tablename__ = 'sub_menu'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, unique=True,  nullable=False)
    csv_url = Column(String,  nullable=True)
    menu_id: Mapped[String] = mapped_column(ForeignKey("menu.id"))
