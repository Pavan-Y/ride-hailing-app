import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/paymentsdb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PORT=os.getenv('PORT',7000)
