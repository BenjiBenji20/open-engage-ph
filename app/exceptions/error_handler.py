from fastapi import Request
from app.exceptions.customed_exceptions import *
from app.utils.error_response import error_response

async def internal_server_error_handler(request: Request, exc: InternalServerError):
  return error_response(exc.detail, exc.error_code, 500)

# handles db unique constraints
async def duplicate_entry_exception_handler(request: Request, exc: DuplicateEntryException):
  return error_response(exc.detail, exc.error_code, 400)


async def resource_not_found_handler(request: Request, exc: ResourceNotFoundException):
  return error_response(exc.detail, exc.error_code, 404)


async def unauthorized_access_handler(request: Request, exc: UnauthorizedAccessException):
  return error_response(exc.detail, exc.error_code, 401)


async def forbidden_access_handler(request: Request, exc: ForbiddenAccessException):
  return error_response(exc.detail, exc.error_code, 403)


async def invalid_token_handler(request: Request, exc: InvalidTokenException):
  return error_response(exc.detail, exc.error_code, 401)

async def unprocessible_content_handler(request: Request, exc: UnprocessibleContentException):
  return error_response(exc.detail, exc.error_code, 422)

async def invalid_request_handler(request: Request, exc: InvalidRequestException):
  return error_response(exc.detail, exc.error_code, 401)
