import asyncio

import app.talk


TALK = app.talk.Talk()


async def response(phrase: str) -> str:
    """
    Блокирующий запрос внутри асинхронного
    :param phrase:
    :return:
    """
    loop = asyncio.get_event_loop()
    future_request = loop.run_in_executor(None, TALK.answer, phrase)
    return await future_request


def history() -> list:
    """
    История разговора
    """
    hist = list()
    for line in TALK.history:
        hist.append([f'{line.timestamp:%Y-%m-%d %H:%M}', line.phrase, line.response])
    return hist
