from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, Field

class TagModel(BaseModel):
    uid: uuid.UUID
    tag_text: str
    user_uid: Optional[uuid.UUID]
    book_uid: Optional[uuid.UUID]
    created_at: datetime
    update_at: datetime

    
class TagCreateModel(BaseModel):
    tag_text: str
    

class TagUpdateModel(BaseModel):
    tag_text: str
