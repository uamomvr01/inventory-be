from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime

class UserSchema(BaseModel):
    id: UUID4
    email: EmailStr
    full_name: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True