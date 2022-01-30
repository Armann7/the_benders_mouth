from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.conversation import Conversation
import webapp.model


app = FastAPI(title="Bender's mouth")
templates = Jinja2Templates(directory=r"data/templates")


# API
#
@app.post("/api/answer",
          response_description="Bender's answer",
          description="Get Bender's answer")
async def answer(data: webapp.model.PhraseInput):
    return {"answer": Conversation().answer(data.phrase)}


# Web interface
# На /answer приходит post запрос с фразой, после получения ответа редиректим в корень,
# а затем перезагружаем страницу
#
@app.get("/favicon.ico")
async def favicon():
    return FileResponse(r"data/static/favicon.ico")


@app.post("/answer",
          response_description="Bender's answer",
          description="Get Bender's answer")
async def answer_form(phrase: str = Form(...)):
    Conversation().answer(phrase)
    return RedirectResponse("/")


@app.post("/")
async def main_post(request: Request):
    return await main(request)


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "conversation": Conversation().history})
