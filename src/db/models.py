from sqlmodel import Relationship, SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import date, datetime
from typing import List, Optional
import uuid


class User(SQLModel, table = True):
    __tablename__ = 'users'
    uid : uuid.UUID = Field(
        sa_column = Column(
            pg.UUID,
            nullable = False,
            primary_key = True,
            default = uuid.uuid4
        )
    )
    username : str
    email : str
    first_name : str
    last_name : str
    role : str = Field(sa_column=Column(
        pg.VARCHAR, nullable=False, server_default='user'
    ))
    is_verified : bool = Field(default = False)
    password_hash : str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: List["Book"] = Relationship(back_populates="user", sa_relationship_kwargs={'lazy':'selectin'})
    reviews: List["Review"] = Relationship(back_populates="user", sa_relationship_kwargs={'lazy':'selectin'}) # type: ignore
    tags: List["Tag"] = Relationship(back_populates="user", sa_relationship_kwargs={'lazy':'selectin'}) # type: ignore
    
    def __repr__(self):
        return f'<User {self.username}>'



class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional[User] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(back_populates="book", sa_relationship_kwargs={'lazy':'selectin'}) # type: ignore
    tags: List["Tag"] = Relationship(back_populates="book", sa_relationship_kwargs={'lazy':'selectin'}) # type: ignore
    

    def __repr__(self):
        return f"<Book {self.title}>"



class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    rating: int = Field(lt=6)
    review_text: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="books.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional[User] = Relationship(back_populates="reviews")
    book: Optional[Book] = Relationship(back_populates="reviews")


    def __repr__(self):
        return f"<Review for book {self.book_uid} by user {self.user_uid}>"


class Tag(SQLModel, table=True):
    __tablename__ = "tags"
    
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    tag_text: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="books.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional[User] = Relationship(back_populates="tags")
    book: Optional[Book] = Relationship(back_populates="tags")
    
    
    def __repr__(self):
        return f"<Tag for book {self.book_uid} by user {self.user_uid}>"