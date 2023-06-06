class CardboardException(Exception):
    """
    Exception raised for other Cardboard-API exceptions, that don't fall under defined exceptions.

    Also the base exception class.
    """
    pass


class Forbidden(CardboardException):
    """
    Exception raised when there is insufficient permissions.
    """
    pass


class Unauthorized(CardboardException):
    """
    Exception raised when the request lacks valid authentication credentials.
    """
    pass


class NotFound(CardboardException):
    """
    Exception raised when a requested resource is not found.
    """
    pass


class InternalServerError(CardboardException):
    """
    Exception raised when the server encounters an internal error.

    Likely because the API is down.
    """
    pass


class RateLimited(CardboardException):
    """
    Exception raised when the rate limit for requests has been exceeded.
    """
    pass

class BadRequest(CardboardException):
    """
    Exception raised when a bad request is sent.

    Likely invalid data was posted.
    """
    pass


CardboardForbidden = Forbidden
CardboardUnauthorized = Unauthorized
CardboardNotFound = NotFound
CardboardInternalServerError = InternalServerError
CardboardRateLimited = RateLimited
CardboardBadRequest = BadRequest