from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    def __init__(self, message: str, code: str = "internal_error", status_code: int = 500):
        self.message = message
        self.code = code
        self.status_code = status_code


class NotFoundException(AppException):
    def __init__(self, entity: str, entity_id: int | str | None = None):
        msg = f"{entity} not found" + (f": {entity_id}" if entity_id else "")
        super().__init__(message=msg, code="not_found", status_code=404)


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Not authenticated"):
        super().__init__(message=message, code="unauthorized", status_code=401)


class ForbiddenException(AppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message=message, code="forbidden", status_code=403)


class ConflictException(AppException):
    def __init__(self, message: str):
        super().__init__(message=message, code="conflict", status_code=409)


class ValidationException(AppException):
    def __init__(self, message: str):
        super().__init__(message=message, code="validation_error", status_code=422)


class RateLimitException(AppException):
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message=message, code="rate_limited", status_code=429)


_EXCEPTION_HANDLERS: dict[type[Exception], callable] = {}


def _make_handler(cls: type[AppException]):
    async def handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message, "code": exc.code},
        )

    return handler


def register_exception_handlers(app: FastAPI):
    for cls in [
        NotFoundException,
        UnauthorizedException,
        ForbiddenException,
        ConflictException,
        ValidationException,
        RateLimitException,
        AppException,
    ]:
        app.add_exception_handler(cls, _make_handler(cls))
