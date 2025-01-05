from typing import Any, Callable
from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

class BooklyException(Exception):
    """This is the base class for all bookly errors"""
    pass


class InvalidToken(BooklyException):
    """User has been provided an invalid or expired token"""
    pass


class RevokedToken(BooklyException):
    """User has been provided a token that has been revoked"""
    pass


class AccessTokenRequired(BooklyException):
    """User has been provided a refresh token when an access token is needed"""
    pass


class RefreshTokenRequired(BooklyException):
    """User has been provided an access token when an access token is needed"""
    pass


class UserAlreadyExists(BooklyException):
    """User has been provided an email for a user who exists during sign up."""
    pass


class InvalidCredentials(BooklyException):
    """User has been provided wrong email password during login."""
    pass


class InsufficientPermission(BooklyException):
    """User has been provided a refresh token when an access token is needed"""
    pass


class BookNotFound(BooklyException):
    """Book not found."""
    pass


class TagNotFound(BooklyException):
    """Tag not found."""
    pass

class TagAlreadyExists(BooklyException):
    """Tag Already Exists."""
    pass


class UserNotFound(BooklyException):
    """User not found."""
    pass


class AccountNotVerified(Exception):
    """Account not verified yet."""
    pass


def create_exception_handler(status_code: int, initial_detail: Any) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: BooklyException):
        return JSONResponse(
            content=initial_detail,
            status_code=status_code
        )
        
    return exception_handler



def register_all_errors(app: FastAPI):
    #  User Already Exists
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "User with this email already exists",
                "error_code": "user_exists"
            }
        )
    )

    #  Book Not Found
    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Book not found",
                "error_code": "book_does_not_exists"
            }
        )
    )
    
    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Account is not verified yet",
                "error_code": "account_not_verified",
                "resolution": "Check your email for verification link"
            }
        )
    )


    # User Not Found
    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "User with this email does not exists",
                "error_code": "user_does_not_exists"
            }
        )
    )

    # Access Token Required
    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Access token is required",
                "error_code": "access_token_required"
            }
        )
    )

    # Invalid Token
    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "you provided an invalid or expired token",
                "error_code": "invalid_token"
            }
        )
    )

    # Refresh Token Required
    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Refresh token is required",
                "error_code": "refresh_token_required"
            }
        )
    )

    # Revoked Token
    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "you provided a revoked token",
                "error_code": "rekoved_token"
            }
        )
    )

    # Invalid Credentials
    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Invalid email or password",
                "error_code": "invalid_credentials"
            }
        )
    )

    # Insufficient Permission
    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "You do not have sufficient permission",
                "error_code": "insufficient_permission"
            }
        )
    )
    
    # Tag Not Found
    app.add_exception_handler(
        TagNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Book Tag not found",
                "error_code": "tag_does_not_exists"
            }
        )
    )

    @app.exception_handler(500)
    async def enternal_server_error_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Opps, Something went wrong. Please try again later",
                "error_code": "server_error"
            }
        )

