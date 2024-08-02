from fastapi import FastAPI, HTTPException, Request

from blogs.exceptions import BlogsError
from blogs.routes import post_router, user_router

app = FastAPI(
    title='ApiBlogs',
    description='hello',
)

app.include_router(user_router)
app.include_router(post_router)


@app.exception_handler(BlogsError)
def handle_file_not_found_error(request: Request, exception: BlogsError):
    raise HTTPException(
        status_code=exception.status,
        detail=exception.description,
    )
