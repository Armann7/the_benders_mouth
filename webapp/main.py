from dataclasses import dataclass

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates


import model


app = FastAPI(title="Bender's mouth")
templates = Jinja2Templates(directory="data/templates")


@dataclass
class Phrase:
    text: str = ""
    answer: str = ""

conversation = list()
conversation.append(Phrase("Hi! How are you?", "I'm fine, thanks you"))


"""
API
"""


@app.get("/api/answer",
         response_description="Bender's answer",
         description="Get Bender's answer")
async def answer(data: model.PhraseInput):
    return {"phrase": data.phrase}


"""
Web interface
"""


@app.post("/answer",
          response_description="Bender's answer",
          description="Get Bender's answer")
async def answer_form(request: Request, phrase: str = Form(...)):
    global conversation
    conversation.insert(0, Phrase(phrase, "my big answer"))
    return await main(request)


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    global conversation
    return templates.TemplateResponse("index.html", {"request": request, "conversation": conversation})
