import sqlalchemy
from db import Base
from sqlalchemy import orm


class Author(Base):
    __tablename__ = "Authors"
    author_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True)
    first_name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    last_name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
