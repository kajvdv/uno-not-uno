from pydantic import BaseModel, Field, model_validator, constr


class GameCreate(BaseModel):
    name: str
    size: int = Field(ge=2, le=6)
    aiCount: int = 0
    jokerCount: int = 0
    two: str = ""
    three: str = ""
    four: str = ""
    five: str = ""
    six: str = ""
    seven: str = ""
    eight: str = ""
    nine: str = ""
    ten: str = ""
    jack: str = ""
    queen: str = ""
    king: str = ""
    ace: str = ""
    joker: str = ""

    @model_validator(mode='after')
    def check_ai_count(self):
        if self.aiCount >= self.size:
            raise ValueError("There are too many AI's")
        return self


class GamePublic(BaseModel):
    url: str
    id: str = constr(max_length=24)
    size: int
    capacity: int
    creator: str
    players: list[str]