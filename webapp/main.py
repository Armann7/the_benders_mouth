from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from app.conversation import Conversation
import model


app = FastAPI(title="Bender's mouth")
templates = Jinja2Templates(directory=r"data/templates")


# API
#
@app.get("/api/answer",
         response_description="Bender's answer",
         description="Get Bender's answer")
async def answer(data: model.PhraseInput):
    return {"phrase": data.phrase}


# Web interface
#
@app.get("/favicon.ico")
async def favicon():
    return FileResponse(r"data/static/favicon.ico")


@app.post("/answer",
          response_description="Bender's answer",
          description="Get Bender's answer")
async def answer_form(request: Request, phrase: str = Form(...)):
    Conversation().answer(phrase)
    # request.scope["path"] = r"/"
    request.url.path = r"/"
    return await main(request)


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "conversation": Conversation().history})
