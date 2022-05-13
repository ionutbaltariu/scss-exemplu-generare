from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from model import get_all_books_authors_with_filters, get_books_authors_by_id, delete_books_authors_by_id, insert_books_authors, update_books_authors
from utils import GenericSuccess, get_error_body, BOOKS_AUTHORS_NOT_FOUND_BODY, GENERIC_SUCCESS_STATUS_BODY, CREATE_GENERIC_SUCCESS_STATUS_BODY
from view import Error, Books_Authors

router = APIRouter()


@router.get("/api/books_authors/",
            responses={200: {"model": List[Books_Authors]},
                       500: {"model": Error}},
            response_model=List[Books_Authors],
            tags=["books_authors"])
def get_books_authors(page: int = 1, items_per_page: int = 15):
    """
    Method that handles a generic GET request for all of the existent books_authors.
    """
    books_authors_list = []

    db_response = get_all_books_authors_with_filters()

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    else:
        status_code = 200
        for books_authors in db_response.payload:
            books_authors_list.append(Books_Authors.from_orm(books_authors).dict())
        response_body = books_authors_list[(page - 1) * items_per_page:page * items_per_page]

    return JSONResponse(status_code=status_code, content=response_body)


@router.get("/api/books_authors/{id}",
            responses={200: {"model": Books_Authors},
                       404: {"model": Error},
                       500: {"model": Error}},
            response_model=Books_Authors,
            tags=["books_authors"])
def get_books_authors(id: str):
    """
    Method that handles a GET request for a books_authors by the 'id' field.
    """
    db_response = get_books_authors_by_id(str(id))

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    elif not db_response.completed_operation:
        status_code = 404
        response_body = BOOKS_AUTHORS_NOT_FOUND_BODY
    else:
        status_code = 200
        response_body = Books_Authors.from_orm(db_response.payload).dict()

    return JSONResponse(status_code=status_code, content=response_body)


@router.delete("/api/books_authors/{id}",
               response_model=GenericSuccess,
               responses={500: {"model": Error},
                          404: {"model": Error},
                          200: {"model": GenericSuccess}},
               tags=["books_authors"])
def delete_books_authors(id: str):
    """
    Method that handles a DELETE request for a books_authors by the 'id' field.
    """
    db_response = delete_books_authors_by_id(str(id))

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    elif not db_response.completed_operation:
        status_code = 404
        response_body = BOOKS_AUTHORS_NOT_FOUND_BODY
    else:
        status_code = 200
        response_body = GENERIC_SUCCESS_STATUS_BODY

    return JSONResponse(status_code=status_code, content=response_body)


@router.post("/api/books_authors/",
             responses={201: {"model": GenericSuccess},
                        500: {"model": Error}},
             response_model=GenericSuccess,
             tags=["books_authors"])
def post_books_authors(books_authors: Books_Authors):
    """
    Method that handles a POST request for a books_authors.
    """

    books_authors_dict = books_authors.dict()
    del books_authors_dict["links"]

    db_response = insert_books_authors(**books_authors_dict)

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    else:
        status_code = 201
        response_body = CREATE_GENERIC_SUCCESS_STATUS_BODY

    return JSONResponse(status_code=status_code, content=response_body)


@router.put("/api/books_authors/{id}",
            responses={200: {"model": GenericSuccess},
                       201: {"model": GenericSuccess},
                       500: {"model": Error},
                       406: {"model": Error}},
            response_model=GenericSuccess,
            tags=["books_authors"])
def put_books_authors(id: str, books_authors: Books_Authors):
    """
    Method that handles a PUT request for a(n) books_authors by its 'id' field.
    Creates the books_authors if it doesn't already exist.
    """
    request_body = books_authors.dict()
    del request_body["links"]

    db_response = update_books_authors(id, request_body)

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    elif db_response.completed_operation is False:
        db_response = insert_books_authors(**request_body)

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