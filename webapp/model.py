from pydantic import BaseModel, Field


class PhraseInput(BaseModel):
    phrase: str = Field(title="Text", description="Text of phrase", max_lengh=200)
