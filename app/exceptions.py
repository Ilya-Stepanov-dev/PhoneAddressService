from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

class BaseError(Exception):
    def __init__(self, details: str, status_code: int):
        self.details = details
        self.status_code = status_code
        super().__init__(self.details)

class PhoneNotFoundError(BaseError):
    def __init__(self, phone: str):
        self.phone = phone
        self.details = f"Phone '{phone}' not found"
        self.status_code = status.HTTP_404_NOT_FOUND
        super().__init__(self.details, self.status_code)


class PhoneAlreadyExistsError(BaseError):
    def __init__(self, phone: str):
        self.phone = phone
        self.details = f"Phone '{phone}' already exists"
        self.status_code = status.HTTP_409_CONFLICT
        super().__init__(self.details, self.status_code)


class InvalidPhoneFormatError(BaseError):
    def __init__(self, phone: str, details: str | None= None):
        self.phone = phone
        self.details = f"{details}. Number - {phone}" or f"Invalid phone format: '{phone}'."
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(self.details, self.status_code)


class RedisConnectionError(BaseError):
    def __init__(self, details: str):
        self.details = f"Failed to connect to Redis. Error: {details}"
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        super().__init__(self.details, self.status_code)


def register_exceptions_handlers(app: FastAPI):
    @app.exception_handler(BaseError)
    async def error_handler(_, exc: BaseError):

        return JSONResponse(
            status_code=exc.status_code,
            content={"details": exc.details}
        )

