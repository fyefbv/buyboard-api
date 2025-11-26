import uvicorn
from fastapi import FastAPI

from app.core import setup_system_exception_handlers
from app.modules import api_router, setup_user_exception_handlers

app = FastAPI(title="Buyboard API")

app.include_router(api_router)

setup_system_exception_handlers(app)
setup_user_exception_handlers(app)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
