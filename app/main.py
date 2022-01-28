from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse


import model

app = FastAPI(title="Bender's mouth")


@app.get("/answer",
         response_description="Bender's answer",
         description="Get Bender's answer")
async def answer(data: model.PhraseInput):
    return {"phrase": data.phrase}


@app.get("/answer",
         response_description="Bender's answer",
         description="Get Bender's answer")
async def answer_form(phrase: str = Form(...)):
    return {"phrase": phrase}


@app.get("/", response_class=HTMLResponse)
async def main():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)