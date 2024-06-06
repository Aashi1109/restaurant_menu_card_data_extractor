from src.exceptions.CustomError import CustomError


class ClientError(CustomError):
    def __init__(self, message: str, detail: str = None):
        super().__init__(400, message, detail)
