from fastapi import APIRouter, Depends, HTTPException, status
from src.db.models import User
from src.db.main import get_session
from src.auth.dependencies import get_current_user
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ReviewCreateModel, ReviewUpdateModel
from .service import ReviewService

review_service = ReviewService()
review_router = APIRouter()

@review_router.post('/book/{book_uid}')
async def add_review_to_books(
    book_uid: str,
    review_data:ReviewCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    new_review = await review_service.add_review_to_book(
        user_email = current_user.email,
        review_data = review_data,
        book_uid = book_uid,
        session = session
    )
    
    return new_review


@review_router.patch('/{review_uid}')
async def update_review_by_uid(review_uid: str, review_data: ReviewUpdateModel, session: AsyncSession = Depends(get_session)):
    update_review_by_uid = await review_service.update_book_review(review_uid, review_data, session)
    return update_review_by_uid

@review_router.delete('/{review_uid}')
async def delete_review_by_uid(review_uid: str, session: AsyncSession = Depends(get_session)):
    delete_review_by_uid = await review_service.delete_book_review(review_uid, session)
    
    if delete_review_by_uid is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "book Review not found"
        )
        
    return {}