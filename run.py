from app import app
from db import db

db.init_app(app)

# Erstellung von Datenbank
@app.before_first_request
def create_tables():
    if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
        with sqlalchemy.create_engine(
            'postgresql:///postgres',
                isolation_level='AUTOCOMMIT').connect() as connection:
            connection.execute('CREATE DATABASE data')
    db.create_all()
