from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import user_router, loan_router
from app.db import models
from app.db.sqldb import engine


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


models.Base.metadata.create_all(bind=engine)
app = get_application()

app.include_router(user_router.router, prefix="/users", tags=["user"])
app.include_router(loan_router.router, prefix="/loans", tags=["loan"])
