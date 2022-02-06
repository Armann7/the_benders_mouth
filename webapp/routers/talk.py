from fastapi import APIRouter

import config
import app.talk_api as talk_api
from webapp.models.common import Version

router = APIRouter()


@router.get("", response_description="It's response from Bender", description="Talk with Bender")
async def response(version: Version, phrase: str):
    config.log.info("API/{version} call, input phrase: {phrase}".format(version=version, phrase=phrase))
    text = await talk_api.response(phrase)
    return {"response": text}
