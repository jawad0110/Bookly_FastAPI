from sqlmodel import select
from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi import status
from .schemas import ReviewCreateModel, ReviewUpdateModel
from src.db.models import Review

book_service = BookService()
user_service = UserService()

class ReviewService:
    async def get_review_by_uid(self, review_uid: str, session: AsyncSession):
        statement = select(Review).where(Review.uid == review_uid)
        result = await session.exec(statement)
        
        review = result.first()
        return review
    
    async def add_review_to_book(self, user_email: str, book_uid: str, review_data: ReviewCreateModel,session: AsyncSession):
        try:
            book = await book_service.get_book(
                book_uid=book_uid,
                session=session
            )
            user = await user_service.get_user_by_email(
                email=user_email,
                session=session
            )
            
            review_data_dict =review_data.model_dump()
            new_review = Review(
                **review_data_dict
            )
            
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found."
                )
                
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Please Login to Review the Book."
                )
            
            new_review.user = user
            new_review.book = book
            session.add(new_review)
            await session.commit()
            
            return new_review
        
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ooops, something went wrong. Please try again later."
            )
            
    async def update_book_review(self, review_uid: str, review_data: ReviewUpdateModel, session: AsyncSession):
        # Get the review by its unique identifier
        review_to_update = await self.get_review_by_uid(review_uid, session)
        
        # If the review is not found, raise a 404 error
        if not review_to_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found."
            )
        
        # If the review is found, update its fields
        if review_to_update is not None:
            # Convert the review update data to a dictionary
            review_data_dict = review_data.model_dump()
            
            # Update each field of the review with the new data
            for k, v in review_data_dict.items():
                # `setattr` is a built-in Python function that sets a property (like a variable) on an object to a new value.
                setattr(review_to_update, k, v) # "k" stands for key and "v" stands for value,
                                                # and that means we are setting the value of the key to the new value
            # Commit the changes to the database
            await session.commit()
            
            return review_to_update
        
        return None
    
    async def delete_book_review(self, review_uid: str, session: AsyncSession):
        review_to_delete = await self.get_review_by_uid(review_uid, session)
        if review_to_delete is not None:
            await session.delete(review_to_delete)
            
            await session.commit()
            return {}
        
        return None