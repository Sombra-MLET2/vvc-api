import os

ENV = os.getenv('VVC_ENV') if os.getenv('VVC_ENV') else 'dev'
SQLALCHEMY_DATABASE_URL = os.getenv('VVC_DATABASE_URL') if os.getenv('VVC_DATABASE_URL') else "sqlite:///./vvc-fiap.db"
