import logging

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./vvc-fiap.db"

logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


# Forcando SQLite a verificar foreign keys
def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('PRAGMA foreign_keys=ON')


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

event.listen(engine, 'connect', _fk_pragma_on_connect)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Method used to get a SQLAlchemy database session.

    FastApi will inject this into a method parameter via:<br/>
        <i>db: Session = Depends(get_db)</i>

    :return: SessionLocal db session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
