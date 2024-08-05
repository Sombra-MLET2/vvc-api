import os

ENV = os.getenv('VVC_ENV') if os.getenv('VVC_ENV') else 'dev'
SQLALCHEMY_DATABASE_URL = os.getenv('VVC_DATABASE_URL') if os.getenv('VVC_DATABASE_URL') else "sqlite:///./vvc-fiap.db"
JWT_ALGORITHM = 'HS256'
JWT_SECRET = os.getenv('JWT_SECRET') if os.getenv('JWT_SECRET') else '8e8e092f6c6d48839b5b514b3edb7d57'
JWT_EXPIRY = os.getenv('JWT_EXPIRY') if os.getenv('JWT_EXPIRY') else 30
