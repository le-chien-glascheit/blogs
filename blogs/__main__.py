import uvicorn

from blogs.main import app
from blogs.settings import settings

if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host=settings.host,
        port=settings.port,
    )
