from fastapi import APIRouter, Depends, HTTPException, status
from src.db.models import User
from src.db.main import get_session
from src.auth.dependencies import get_current_user
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import TagCreateModel, TagUpdateModel
from .service import TagService

tag_service = TagService()
tag_router = APIRouter()

@tag_router.post("/book/{book_uid}")
async def add_tag_to_book(
    book_uid: str,
    tag_data: TagCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    new_tag = await tag_service.create_book_tag(
        user_email= current_user.email,
        tag_data= tag_data,
        book_uid= book_uid,
        session= session
    )
    return new_tag

@tag_router.patch("/{tag_uid}")
async def update_tag_by_uid(tag_uid: str, tag_data: TagUpdateModel, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await tag_service.update_book_tag(tag_uid, tag_data, session)

@tag_router.delete("/{tag_uid}")
async def delete_tag_by_uid(tag_uid: str, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await tag_service.delete_book_tag(tag_uid, session)