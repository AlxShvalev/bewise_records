from http import HTTPStatus

from fastapi import HTTPException


class NotFoundException(HTTPException):

    def __init__(self, obj, **params):
        self.status_code = HTTPStatus.NOT_FOUND
        self.detail = f"{obj} with {params} not found."


class UnauthorizedException(HTTPException):
    def __init__(self):
        self.status_code = HTTPStatus.UNAUTHORIZED
        self.detail = "User is not authorized or entered invalid token."


class AlreadyExistsException(HTTPException):

    def __init__(self, obj, **params):
        self.status_code = HTTPStatus.BAD_REQUEST
        self.detail = f"{obj} with {params} already exists."


class CouldntDecodeException(HTTPException):
    def __init__(self):
        self.status_code = HTTPStatus.BAD_REQUEST
        self.detail = "Please send correct WAV file."
