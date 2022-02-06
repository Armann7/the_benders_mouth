from fastapi import APIRouter

import config
import app.talk_api as talk_api


router = APIRouter()


@router.get("", response_description="It's response from Bender", description="Talk with Bender")
async def answer(phrase: str):
    config.log.info("API call, input phrase: {phrase}".format(phrase=phrase))
    text = await talk_api.response(phrase)
    return {"response": text}
