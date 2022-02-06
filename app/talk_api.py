import asyncio
import app.talk


talk = app.talk.Talk()


async def response(phrase: str) -> str:
    """
    Блокирующий запрос внутри асинхронного
    :param phrase:
    :return:
    """
    loop = asyncio.get_event_loop()
    future_request = loop.run_in_executor(None, talk.answer, phrase)
    text = await future_request
    return text


def history():
    """
    История разговора
    :return:
    """
    return talk.history
