from sqlmodel import select
from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi import status
from .schemas import TagCreateModel, TagUpdateModel
from src.db.models import Tag
from src.errors import TagNotFound, BookNotFound, UserNotFound


book_service = BookService()
user_service = UserService()

class TagService:
    async def get_tag_by_id(self, tag_uid:str, session: AsyncSession):
        statement = select(Tag).where(Tag.uid == tag_uid)
        result = await session.exec(statement)
        
        tag = result.first()
        
        return tag
    
    async def create_book_tag(self, user_email: str, book_uid: str, tag_data: TagCreateModel, session: AsyncSession):
        try:
            book = await book_service.get_book(
                book_uid= book_uid,
                session= session
            )
            
            user = await user_service.get_user_by_email(
                email= user_email,
                session= session
            )
            
            
            tag_data_dict = tag_data.model_dump()
            new_tag = Tag(
                **tag_data_dict
            )
            
            if not book:
                raise BookNotFound()

                
            if not user:
                raise UserNotFound()
                
            new_tag.user = user
            new_tag.book = book
            session.add(new_tag)
            await session.commit()
            
            return new_tag
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Opps, Something went wronge. Pleas try again later."
            )
    
    
    async def update_book_tag(self, tag_uid: str, tag_data: TagUpdateModel, session: AsyncSession):
        tag_to_update = await self.get_tag_by_id(tag_uid, session)
        if not tag_to_update:
            raise TagNotFound()
            
        if tag_to_update is not None:
            tag_data_dict = tag_data.model_dump()
            
            for k, v in tag_data_dict.items():
                setattr(tag_to_update, k, v)
                
            await session.commit()
            return tag_to_update
        
        return None
    
    async def delete_book_tag(self, tag_uid: str, session: AsyncSession):
        tag_to_delete = await self.get_tag_by_id(tag_uid, session)
        if tag_to_delete is not None:
            await session.delete(tag_to_delete)
            await session.commit()
            
            return {"message": "Tag deleted successfully."}

        raise TagNotFound()  