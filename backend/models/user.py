from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    uid: str
    email: EmailStr
    display_name: Optional[str] = None
