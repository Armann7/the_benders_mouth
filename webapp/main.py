from fastapi import FastAPI

from webapp.routers import router


app = FastAPI(debug=True)
app.include_router(router)
