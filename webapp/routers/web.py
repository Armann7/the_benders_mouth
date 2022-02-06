from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import config
import app.talk_api as talk_api


router = APIRouter()
templates = Jinja2Templates(directory=r"data/templates")


# На /answer приходит post запрос с фразой, после получения ответа редиректим в корень,
# а затем перезагружаем страницу
#
@router.get("/favicon.ico")
async def favicon():
    return FileResponse(r"data/static/favicon.ico")


@router.post("/answer", response_description="Bender's answer", description="Get Bender's answer")
async def answer_form(phrase: str = Form(...)):
    config.log.info("Web call, input phrase: {phrase}".format(phrase=phrase))
    await talk_api.response(phrase)
    return RedirectResponse("/")


@router.post("/")
async def main_post(request: Request):
    return await main(request)


@router.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "conversation": talk_api.history()})
