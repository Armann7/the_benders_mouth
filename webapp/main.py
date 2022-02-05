from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import fastapi.logger
from pydantic import BaseSettings
import asyncio
import logging

from app.conversation import Conversation
import webapp.model

logging.basicConfig(level=logging.DEBUG)


class Settings(BaseSettings):
    openapi_url: str = "/data/api/openapi-0.1.0.json"


settings = Settings()
app = FastAPI(debug=True, openapi_url=settings.openapi_url)
templates = Jinja2Templates(directory=r"data/templates")
log = logging.getLogger("The Bender's Mouth")
conversation = Conversation()


async def get_answer(phrase: str) -> str:
    """
    Блокирующий запрос внутри асинхронного
    :param phrase:
    :return:
    """
    loop = asyncio.get_event_loop()
    future_request = loop.run_in_executor(None, conversation.answer, phrase)
    text = await future_request
    return text


# API
#
@app.post("/api/answer",
          response_description="Bender's answer",
          description="Get Bender's answer")
async def answer(data):
    log.info("API call, input phrase: {phrase}".format(phrase=phrase))
    text = await get_answer(phrase)
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
    return templates.TemplateResponse("index.html", {"request": request, "conversation": conversation   .history})
