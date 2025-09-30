from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    age: int
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    hashed_password: str

    class Config:
        from_attributes = True