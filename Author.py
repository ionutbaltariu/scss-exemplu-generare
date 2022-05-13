import sqlalchemy
from db import Base


class Author(Base):
    __tablename__ = "authors"
    author_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True)
    first_name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    last_name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    sqlalchemy.UniqueConstraint("author_id",  name="one_to_one_constr")
