from pydantic import BaseModel


class Config(BaseModel):
    mcmod_search_seq: bool = False
