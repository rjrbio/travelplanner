class ServiceError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def format_error(exc: Exception) -> dict:
    return {"error": str(exc)}
