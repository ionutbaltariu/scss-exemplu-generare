from fastapi_hypermodel import HyperModel, LinkSet, HALFor
from pydantic import constr, BaseModel


class Book(HyperModel):
    isbn: constr(min_length=1, max_length=100)
    title: constr(min_length=1, max_length=100)
    year_of_publishing: int

    links = LinkSet(
        {
            "self": HALFor("get_book",
                          { "isbn": "<isbn>"},
                          "Get the book"),
        }
    )

    class Config:
        orm_mode = True

class Author(HyperModel):
    author_id: int
    first_name: constr(min_length=1, max_length=100)
    last_name: constr(min_length=1, max_length=100)

    links = LinkSet(
        {
            "self": HALFor("get_author",
                          { "author_id": "<author_id>"},
                          "Get the author"),
        }
    )

    class Config:
        orm_mode = True

class Books_Authors(HyperModel):
    id: int
    isbn: int
    author_id: int

    links = LinkSet(
        {
            "self": HALFor("get_books_authors",
                          { "id": "<id>"},
                          "Get the books_authors"),
        }
    )

    class Config:
        orm_mode = True


class Error(BaseModel):
    error_code: int
    error_source: str
    error_reason: str