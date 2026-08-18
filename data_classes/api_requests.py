from pydantic import BaseModel


class SyncRequest(BaseModel):
    game: bool
