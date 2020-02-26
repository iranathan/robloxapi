class NotFound(Exception):
    """Raised when something is not found."""
    pass


class RoleError(Exception):
    """Raised when a role is too high."""
    pass


class BadStatus(Exception):
    """Raised when a status is not 200."""
    pass


class NotAuthenticated(Exception):
    """Raised when a user is not authenticated."""
    pass


class AuthenticationError(Exception):
    """Raised when a password or username is incorrect."""
    pass


class CaptchaEncountered(Exception):
    """Raised when captcha is encountered."""
    pass

