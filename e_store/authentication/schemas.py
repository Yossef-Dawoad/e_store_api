from pydantic import BaseModel


class TokenPublic(BaseModel):
    access_token: str
    refresh_token: str
    extra: dict | None = None
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: str | None = None


class LogInUser(BaseModel):
    username: str
    password: str
