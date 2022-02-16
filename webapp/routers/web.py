"""
 Роуты веб интерфейса
"""
import pathlib

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse


import config
from app import talk_api


router = APIRouter()
templates = Jinja2Templates(directory=config.TEMPLATES)


@router.get("/favicon.ico")
async def favicon() -> FileResponse:
    """
    Отдаем favicon
    """
    return FileResponse(pathlib.Path(config.STATIC, "favicon.ico"))


@router.get("/answer",
            response_description="Bender's answer",
            description="Get Bender's answer")
async def answer_form(phrase: str) -> RedirectResponse:
    """
    Обработка формы
    :param phrase:
    :return:
    """
    phrase = phrase.strip()
    config.log.info("Web call, input phrase: %s", phrase)
    await talk_api.response(phrase)
    return RedirectResponse("/")


@router.get("/", response_class=HTMLResponse)
async def main(request: Request) -> _TemplateResponse:
    """
    Корневая страничка
    """
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "conversation": talk_api.history()})
