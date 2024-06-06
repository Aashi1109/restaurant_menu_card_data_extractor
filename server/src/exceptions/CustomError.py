class CustomError(Exception):
    message = None
    status = None
    detail = None

    def __init__(self, status_code: int, message: str, detail: str = None):
        super().__init__(message)
        self.message = message
        self.status = status_code
        self.detail = detail
