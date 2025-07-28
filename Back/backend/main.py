from fastapi import FastAPI
from src.api import auth,sessions,messages

app = FastAPI()

app.include_router(auth.router,prefix = "/auth",tags=["authenticate user"])
app.include_router(sessions.router,prefix = "/sessions",tags=["user session"])
app.include_router(messages.router,prefix = "/messages",tags=["message part"])