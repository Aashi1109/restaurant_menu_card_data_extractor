from pydantic import BaseModel


class ScrapRequest(BaseModel):
    query: str
    use_cse_papi: bool = False
    max_links: int = 20
