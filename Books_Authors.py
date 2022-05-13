import sqlalchemy
from db import Base
from sqlalchemy import orm


class Books_Authors(Base):
    __tablename__ = "Books_Authors"
    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True)
    isbn = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Books.isbn"), nullable=False)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Authors.author_id"), nullable=False)
