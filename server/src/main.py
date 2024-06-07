class FastAPIServer:
    def __init__(self):
        try:
            self.app = FastAPI()
            self.app.include_router(router=embedding_router, tags=["Embeddings"])
            self.app.include_router(router=tokens_router, tags=["Tokens"])
            self.app.include_router(router=query_router, tags=["Query"])
            self.__exception_middlewares()
        except Exception as e:
            logger.error(str(e), exc_info=True)

    def __exception_middlewares(self):
        @self.app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request: Request, exc: RequestValidationError):
            logger.error(f"Validation on request: {request.url} error: {exc.errors()}", exc_info=True)
            errors = exc.errors()
            error_message = "Validation error"
            if errors:
                error_message = errors[0]["msg"] + " location: " + f"{errors[0]["loc"][1]}"
            return JSONResponse(status_code=400,
                                content={"message": error_message,
                                         "success": False})

        @self.app.exception_handler(Exception)
        async def custom_exception_handler(request: Request, exception):
            logger.error(str(exception), exc_info=True)
            if isinstance(exception, CustomError):
                return JSONResponse(content={"message": exception.message, "status": False},
                                    status_code=exception.status)
            return JSONResponse(content={"message": "Internal server error", "status": False}, status_code=500)

    def run(self, host: str, port: int):
        uvicorn.run(self.app, host=host, port=port)
