from server.src.exceptions.CustomError import CustomError


class NotFoundError(CustomError):
    def __init__(self, message, detail: str = None):
        super().__init__(404, message, detail)
