from typing import Optional, List

from pydantic import BaseModel, Field


class ScrapSubmitRequest(BaseModel):
    query: str = Field(description="Search query", examples=["Mumbai restaurant menu card"])
    use_cse_papi: bool = Field(description="Whether to use Google programmable api or basic search", default=True)
    max_links: int = Field(description="Max images link to fetch from search", default=10)


class BasicResponse(BaseModel):
    success: bool
    message: Optional[str]


class ScrapResponse(BasicResponse):
    data: Optional[dict]


class ScrapAllTasksResponse(BasicResponse):
    data: Optional[List]
