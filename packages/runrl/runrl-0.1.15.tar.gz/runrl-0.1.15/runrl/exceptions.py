class RunRLError(Exception):
    """Base exception class for RunRL client errors."""
    pass

class AuthenticationError(RunRLError):
    """Raised for authentication failures (e.g., invalid API key)."""
    pass

class PermissionError(RunRLError):
    """Raised when the user does not have permission for an action."""
    pass

class NotFoundError(RunRLError):
    """Raised when a requested resource is not found."""
    pass

class RequestError(RunRLError):
    """Raised for general client-side errors (e.g., bad request, 4xx errors)."""
    pass

class APIServerError(RunRLError):
    """Raised for server-side errors (5xx errors)."""
    pass 