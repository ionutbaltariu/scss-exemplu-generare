from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from model import get_all_authors_with_filters, get_author_by_author_id, delete_author_by_author_id, insert_author, update_author
from utils import GenericSuccess, get_error_body, AUTHOR_NOT_FOUND_BODY, GENERIC_SUCCESS_STATUS_BODY, CREATE_GENERIC_SUCCESS_STATUS_BODY
from view import Error, Author

router = APIRouter()


@router.get("/api/authors/",
            responses={200: {"model": List[Author]},
                       500: {"model": Error}},
            response_model=List[Author],
            tags=["authors"])
def get_authors(page: int = 1, items_per_page: int = 15):
    """
    Method that handles a generic GET request for all of the existent authors.
    """
    author_list = []

    db_response = get_all_authors_with_filters()

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    else:
        status_code = 200
        for author in db_response.payload:
            author_list.append(Author.from_orm(author).dict())
        response_body = author_list[(page - 1) * items_per_page:page * items_per_page]

    return JSONResponse(status_code=status_code, content=response_body)


@router.get("/api/authors/{author_id}",
            responses={200: {"model": Author},
                       404: {"model": Error},
                       500: {"model": Error}},
            response_model=Author,
            tags=["authors"])
def get_author(author_id: str):
    """
    Method that handles a GET request for a authors by the 'author_id' field.
    """
    db_response = get_author_by_author_id(str(author_id))

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    elif not db_response.completed_operation:
        status_code = 404
        response_body = AUTHOR_NOT_FOUND_BODY
    else:
        status_code = 200
        response_body = Author.from_orm(db_response.payload).dict()

    return JSONResponse(status_code=status_code, content=response_body)


@router.delete("/api/authors/{author_id}",
               response_model=GenericSuccess,
               responses={500: {"model": Error},
                          404: {"model": Error},
                          200: {"model": GenericSuccess}},
               tags=["authors"])
def delete_author(author_id: str):
    """
    Method that handles a DELETE request for a authors by the 'author_id' field.
    """
    db_response = delete_author_by_author_id(str(author_id))

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    elif not db_response.completed_operation:
        status_code = 404
        response_body = AUTHOR_NOT_FOUND_BODY
    else:
        status_code = 200
        response_body = GENERIC_SUCCESS_STATUS_BODY

    return JSONResponse(status_code=status_code, content=response_body)


@router.post("/api/authors/",
             responses={201: {"model": GenericSuccess},
                        500: {"model": Error}},
             response_model=GenericSuccess,
             tags=["authors"])
def post_author(author: Author):
    """
    Method that handles a POST request for a author.
    """

    author_dict = author.dict()
    del author_dict["links"]

    db_response = insert_author(**author_dict)

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    else:
        status_code = 201
        response_body = CREATE_GENERIC_SUCCESS_STATUS_BODY

    return JSONResponse(status_code=status_code, content=response_body)


@router.put("/api/authors/{author_id}",
            responses={200: {"model": GenericSuccess},
                       201: {"model": GenericSuccess},
                       500: {"model": Error},
                       406: {"model": Error}},
            response_model=GenericSuccess,
            tags=["authors"])
def put_author(author_id: str, author: Author):
    """
    Method that handles a PUT request for a(n) author by its 'author_id' field.
    Creates the author if it doesn't already exist.
    """
    request_body = author.dict()
    del request_body["links"]

    db_response = update_author(author_id, request_body)

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    elif db_response.completed_operation is False:
        db_response = insert_author(**request_body)

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