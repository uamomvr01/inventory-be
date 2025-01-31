from pydantic import BaseModel, UUID4
from datetime import datetime

class ProfileBase(BaseModel):
    full_name: str

class ProfileCreate(ProfileBase):
    pass

class ProfileSchema(ProfileBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True