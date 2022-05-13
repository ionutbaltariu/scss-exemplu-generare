from Book import Book
from Author import Author
from Books_Authors import Books_Authors
from db import Session, engine


class OperationResponseWrapper:
    def __init__(self, payload=None, error=None, completed_operation=True):
        self.payload = payload
        self.error = error
        self.completed_operation = completed_operation


def get_all_entities(entity, **kwargs):
    """
    Wrapper for a generic ORM call that is retrieving all instances of
    any entity also using some filter parameters.
    :param entity: the type of the entity that is to be retrieved
    :param kwargs: the parameters by which the filters will be made
    """
    with Session(bind=engine) as session:
        response = OperationResponseWrapper()

        try:
            response.payload = session.query(entity).filter_by(**kwargs).all()
            response.completed_operation = True
        except Exception as e:
            session.rollback()
            response.error = e
            response.completed_operation = False

        return response


def get_entity_by_identifier(entity, identifier_name, identifier_value):
    """
    Wrapper for a generic ORM call that is retrieving an Entity by an identifier.
    :param entity: the type of the entity that is to be retrieved
    :param identifier_name: the column/field by which the identifier will be searched
    :param identifier_value: the value of the identifier column
    """
    with Session(bind=engine) as session:
        response = OperationResponseWrapper()

        try:
            response.payload = session\
                .query(entity)\
                .filter(getattr(entity, identifier_name) == identifier_value)\
                .first()
            if not response.payload:
                response.completed_operation = False
            else:
                response.completed_operation = True
        except Exception as e:
            session.rollback()
            response.error = e
            response.completed_operation = False

        return response


def delete_entity_by_identifier(entity, identifier_name, identifier_value):
    """
    Wrapper for a generic ORM call that is deleting an Entity by an identifier.
    :param entity: the type of the entity that is to be deleted
    :param identifier_name: the column/field by which the identifier will be searched and deleted
    :param identifier_value: the value of the identifier column
    """
    with Session(bind=engine) as session:
        response = OperationResponseWrapper()

        try:
            entity_to_delete = session\
                .query(entity)\
                .filter(getattr(entity, identifier_name) == identifier_value)\
                .first()

            if entity_to_delete:
                session.delete(entity_to_delete)
                session.commit()
            else:
                response.completed_operation = False

        except Exception as e:
            session.rollback()
            response.completed_operation = False
            response.error = e

        return response


def update_entity_by_identifier(entity, identifier_name, identifier_value, updated_entity_fields):
    """
    Wrapper for a generic ORM call that is updating an Entity by an identifier.
    :param entity: the type of the entity that is to be updated
    :param identifier_name: the column/field by which the identifier will be searched
    :param identifier_value: the value of the identifier column
    :param updated_entity_fields: a dictionary that contains the new values of the entity
    """
    with Session(bind=engine) as session:
        response = OperationResponseWrapper()

        try:
            entity_to_update = session\
                .query(entity)\
                .filter(getattr(entity, identifier_name) == identifier_value)\
                .first()

            if entity_to_update:
                for field in updated_entity_fields:
                    setattr(entity_to_update, field, updated_entity_fields[field])

                session.add(entity_to_update)
                session.commit()
                response.completed_operation = True
                response.payload = entity_to_update
            else:
                response.completed_operation = False
        except Exception as e:
            session.rollback()
            response.completed_operation = False
            response.error = e

        return response

def insert_entity(entity, **kwargs):
    """
    Wrapper for an ORM call that inserts a book into the database.
    :param entity: the type of the entity
    :param kwargs: the attributes of the entity
    """
    with Session(bind=engine) as session:
        response = OperationResponseWrapper()

        entity_to_insert = entity(**kwargs)
        try:
            session.add(entity_to_insert)
            session.commit()
            response.completed_operation = True
            response.payload = entity_to_insert
        except Exception as e:
            session.rollback()
            response.completed_operation = False
            response.error = e

        return response


def get_book_by_isbn(isbn):
    """
    Wrapper for an ORM call that is retrieving a(n) entity by its isbn.
    :param isbn: TODO
    """
    return get_entity_by_identifier(Book, "isbn", isbn)

def get_author_by_author_id(author_id):
    """
    Wrapper for an ORM call that is retrieving a(n) entity by its author_id.
    :param author_id: TODO
    """
    return get_entity_by_identifier(Author, "author_id", author_id)

def get_books_authors_by_id(id):
    """
    Wrapper for an ORM call that is retrieving a(n) entity by its id.
    :param id: TODO
    """
    return get_entity_by_identifier(Books_Authors, "id", id)


def get_all_books_with_filters(**kwargs):
    """
    Wrapper for an ORM call that is retrieving all books by isbn
    :param kwargs: the parameters by which the filters will be made
    """
    return get_all_entities(Book, **kwargs)
def get_all_authors_with_filters(**kwargs):
    """
    Wrapper for an ORM call that is retrieving all authors by author_id
    :param kwargs: the parameters by which the filters will be made
    """
    return get_all_entities(Author, **kwargs)
def get_all_books_authors_with_filters(**kwargs):
    """
    Wrapper for an ORM call that is retrieving all books_authors by id
    :param kwargs: the parameters by which the filters will be made
    """
    return get_all_entities(Books_Authors, **kwargs)


def update_book(isbn, book):
    """
    Wrapper for an ORM call that updates a(n) book in the database.
    :param isbn: the identifier of the Book
    :param book: a dictionary containing the fields of the book - can be partial
    """
    return update_entity_by_identifier(Book, "isbn", isbn, book)
def update_author(author_id, author):
    """
    Wrapper for an ORM call that updates a(n) author in the database.
    :param author_id: the identifier of the Author
    :param author: a dictionary containing the fields of the author - can be partial
    """
    return update_entity_by_identifier(Author, "author_id", author_id, author)
def update_books_authors(id, books_authors):
    """
    Wrapper for an ORM call that updates a(n) books_authors in the database.
    :param id: the identifier of the Books_Authors
    :param books_authors: a dictionary containing the fields of the books_authors - can be partial
    """
    return update_entity_by_identifier(Books_Authors, "id", id, books_authors)


def delete_book_by_isbn(isbn):
    """
    Wrapper for an ORM call that is deleting a(n) book by its isbn.
    :param isbn: isbn of the book that is to be deleted
    """
    return delete_entity_by_identifier(Book, "isbn", isbn)
def delete_author_by_author_id(author_id):
    """
    Wrapper for an ORM call that is deleting a(n) author by its author_id.
    :param author_id: author_id of the author that is to be deleted
    """
    return delete_entity_by_identifier(Author, "author_id", author_id)
def delete_books_authors_by_id(id):
    """
    Wrapper for an ORM call that is deleting a(n) books_authors by its id.
    :param id: id of the books_authors that is to be deleted
    """
    return delete_entity_by_identifier(Books_Authors, "id", id)


def insert_book(**kwargs):
    """
    Wrapper for an ORM call that is creating a(n) book.
    :param kwargs: the attributes of the Book that is to be created
    """
    return insert_entity(Book, **kwargs)
def insert_author(**kwargs):
    """
    Wrapper for an ORM call that is creating a(n) author.
    :param kwargs: the attributes of the Author that is to be created
    """
    return insert_entity(Author, **kwargs)
def insert_books_authors(**kwargs):
    """
    Wrapper for an ORM call that is creating a(n) books_authors.
    :param kwargs: the attributes of the Books_Authors that is to be created
    """
    return insert_entity(Books_Authors, **kwargs)

