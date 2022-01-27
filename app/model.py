import typing
from pydantic import BaseModel, Field


class PhraseInput(BaseModel):
    phrase: str = Field(title="Text", description="Text of phrase", max_lengh=200)


class PhraseOutput(BaseModel):
    phrase: typing.Optional[str] = None
