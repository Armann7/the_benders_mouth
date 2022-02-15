import pathlib

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse


import config
import app.talk_api as talk_api


router = APIRouter()
templates = Jinja2Templates(directory=config.TEMPLATES)


@router.get("/favicon.ico")
async def favicon() -> FileResponse:
    return FileResponse(pathlib.Path(config.STATIC, "favicon.ico"))


@router.get("/answer", response_description="Bender's answer", description="Get Bender's answer")
async def answer_form(phrase: str) -> RedirectResponse:
    phrase = phrase.strip()
    config.log.info(f"Web call, input phrase: {phrase}")
    await talk_api.response(phrase)
    return RedirectResponse("/")


@router.get("/", response_class=HTMLResponse)
async def main(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse("index.html", {"request": request, "conversation": talk_api.history()})
