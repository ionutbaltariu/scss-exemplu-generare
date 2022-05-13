import uvicorn
from fastapi import FastAPI
from fastapi_hypermodel import HyperModel
import book_router
import author_router
import books_authors_router


app = FastAPI()

app.include_router(book_router.router)
app.include_router(author_router.router)
app.include_router(books_authors_router.router)

HyperModel.init_app(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=5555, reload=True, debug=True)