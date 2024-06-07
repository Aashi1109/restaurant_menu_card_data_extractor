from typing import Optional

from pydantic import BaseModel, Field


class ScrapSubmitRequest(BaseModel):
    query: str = Field(description="Search query", examples=["Mumbai restaurant images .."])
    use_cse_papi: bool = Field(description="Whether to use Google programmable api or basic search", default=True)
    max_links: int = Field(description="Max images link to fetch from search", default=10)


class ScrapResponse(BaseModel):
    success: bool
    message: Optional[str]
    data: Optional[dict]
