"""
Роуты API
"""
from fastapi import APIRouter

import config
from app import talk_api
from webapp.models.common import Version

router = APIRouter()


@router.get("",
            response_description="It's response from Bender",
            description="Talk with Bender")
async def response(version: Version, phrase: str) -> dict:
    """
    Получаем фразу и формируем ответ
    :param version:
    :param phrase:
    :return:
    """
    config.log.info("API/%s call, input phrase: %s", version, phrase)
    text = await talk_api.response(phrase)
    return {"response": text}


@router.get("/history",
            response_description="History of talk",
            description="History of talk")
async def history(version: Version) -> dict:
    """
    История разговора
    :param version:
    :return:
    """
    config.log.info("API/%s call, get history", version)
    return {"history": talk_api.history()}
