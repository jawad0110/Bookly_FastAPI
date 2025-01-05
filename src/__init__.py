from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tag_router
from src.db.main import init_db
from .errors import register_all_errors
from .middleware import register_middleware

version = "v1"

app = FastAPI(
    title = "Bookly",
    description = " A REST API for a book review web service",
    version = version,
    docs_url=f"/api/{version}/docs",
    redoc_url=f"/api/{version}/doc",
    openapi_url=f"/api/{version}/openapi.json",
    contact={
        "email": "jawadcoder0@gmail.com"
    }
)

register_all_errors(app)

register_middleware(app)

app.include_router(book_router, prefix=f"/api/{version}/books", tags = ['books'])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags = ['auth'])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags = ['reviews'])
app.include_router(tag_router, prefix=f"/api/{version}/tags", tags = ['tags'])