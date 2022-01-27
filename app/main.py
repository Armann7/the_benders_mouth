from fastapi import FastAPI

import model

app = FastAPI(title="Bender's mouth")


@app.post("/answer",
          response_description="Bender's answer",
          description="Get Bender's answer")
def answer(data: model.PhraseInput):
    return {"phrase": data.phrase}


@app.get("/")
def main():
    return "main"
