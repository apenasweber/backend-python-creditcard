from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None

class UserCreateSchema(UserBase):
    password: str

class UserUpdateSchema(UserBase):
    password: Optional[str] = None
