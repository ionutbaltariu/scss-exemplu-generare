from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from model import get_all_books_with_filters, get_book_by_isbn, delete_book_by_isbn, insert_book, update_book
from utils import GenericSuccess, get_error_body, BOOK_NOT_FOUND_BODY, GENERIC_SUCCESS_STATUS_BODY, CREATE_GENERIC_SUCCESS_STATUS_BODY
from view import Error, Book

router = APIRouter()


@router.get("/api/books/",
            responses={200: {"model": List[Book]},
                       500: {"model": Error}},
            response_model=List[Book],
            tags=["books"])
def get_books(page: int = 1, items_per_page: int = 15):
    """
    Method that handles a generic GET request for all of the existent books.
    """
    book_list = []

    db_response = get_all_books_with_filters()

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    else:
        status_code = 200
        for book in db_response.payload:
            book_list.append(Book.from_orm(book).dict())
        response_body = book_list[(page - 1) * items_per_page:page * items_per_page]

    return JSONResponse(status_code=status_code, content=response_body)


@router.get("/api/books/{isbn}",
            responses={200: {"model": Book},
                       404: {"model": Error},
                       500: {"model": Error}},
            response_model=Book,
            tags=["books"])
def get_book(isbn: str):
    """
    Method that handles a GET request for a books by the 'isbn' field.
    """
    db_response = get_book_by_isbn(str(isbn))

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    elif not db_response.completed_operation:
        status_code = 404
        response_body = BOOK_NOT_FOUND_BODY
    else:
        status_code = 200
        response_body = Book.from_orm(db_response.payload).dict()

    return JSONResponse(status_code=status_code, content=response_body)


@router.delete("/api/books/{isbn}",
               response_model=GenericSuccess,
               responses={500: {"model": Error},
                          404: {"model": Error},
                          200: {"model": GenericSuccess}},
               tags=["books"])
def delete_book(isbn: str):
    """
    Method that handles a DELETE request for a books by the 'isbn' field.
    """
    db_response = delete_book_by_isbn(str(isbn))

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    elif not db_response.completed_operation:
        status_code = 404
        response_body = BOOK_NOT_FOUND_BODY
    else:
        status_code = 200
        response_body = GENERIC_SUCCESS_STATUS_BODY

    return JSONResponse(status_code=status_code, content=response_body)


@router.post("/api/books/",
             responses={201: {"model": GenericSuccess},
                        500: {"model": Error}},
             response_model=GenericSuccess,
             tags=["books"])
def post_book(book: Book):
    """
    Method that handles a POST request for a book.
    """

    book_dict = book.dict()
    del book_dict["links"]

    db_response = insert_book(**book_dict)

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    else:
        status_code = 201
        response_body = CREATE_GENERIC_SUCCESS_STATUS_BODY

    return JSONResponse(status_code=status_code, content=response_body)


@router.put("/api/books/{isbn}",
            responses={200: {"model": GenericSuccess},
                       201: {"model": GenericSuccess},
                       500: {"model": Error},
                       406: {"model": Error}},
            response_model=GenericSuccess,
            tags=["books"])
def put_book(isbn: str, book: Book):
    """
    Method that handles a PUT request for a(n) book by its 'isbn' field.
    Creates the book if it doesn't already exist.
    """
    request_body = book.dict()
    del request_body["links"]

    db_response = update_book(isbn, request_body)

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    elif db_response.completed_operation is False:
        db_response = insert_book(**request_body)

        if db_response.error:
            status_code = 500
            response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
        else:
            status_code = 201
            response_body = CREATE_GENERIC_SUCCESS_STATUS_BODY
    else:
        status_code = 200
        response_body = GENERIC_SUCCESS_STATUS_BODY

    return JSONResponse(status_code=status_code, content=response_body)