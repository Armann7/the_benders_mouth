from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import asyncio
import logging

from app.conversation import Conversation
import webapp.model


app = FastAPI(title="Bender's mouth")
templates = Jinja2Templates(directory=r"data/templates")
log = logging.getLogger("The Bender's Mouth")


async def get_answer(phrase: str) -> str:
    """
    Блокирующий запрос внутри асинхронного
    :param phrase:
    :return:
    """
    loop = asyncio.get_event_loop()
    future_request = loop.run_in_executor(None, Conversation().answer, phrase)
    text = await future_request
    return text


# API
#
@app.post("/api/answer",
          response_description="Bender's answer",
          description="Get Bender's answer")
async def answer(data: webapp.model.PhraseInput):
    log.info("API call, input phrase: {phrase}".format(phrase=data.phrase))
    text = await get_answer(data.phrase)
    return {"answer": text}


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
    log.info("Web call, input phrase: {phrase}".format(phrase=phrase))
    await get_answer(phrase)
    return RedirectResponse("/")


@app.post("/")
async def main_post(request: Request):
    return await main(request)


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "conversation": Conversation().history})
