from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles

from webapp.routers import router


app = FastAPI(debug=True)
app.include_router(router)
# app.mount("/static", StaticFiles(directory=config.STATIC), name="static")
