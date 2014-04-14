class BadRequestException(Exception):
    """The API returned a status of 400 (Bad Request)."""


class NotFoundException(Exception):
    """The resource could not be found."""


class NotInitializedException(Exception):
    """The resource has not been initialized"""


class UnauthorizedException(Exception):
    """The request authentication failed. The OAuth credentials that the client supplied were missing or invalid."""


class ForbiddenException(Exception):
    """The request credentials authenticated, but the requesting user or client app is not authorized to access the given resource."""


class InvalidObjectException(Exception):
    """The object you attempted to create or update was invalid."""


class InvalidSearchArgumentsException(Exception):
    """Invalid arguments were passed when searching."""


class InvalidSizeException(Exception):
    """Invalid size."""


class InternalServerErrorException(Exception):
    """There was an error while processing your request."""


class ValidatorException(Exception):
    """There was an error creating the validator."""


class AttributeNotFoundException(Exception):
    """The attribute you requested does not exist."""
