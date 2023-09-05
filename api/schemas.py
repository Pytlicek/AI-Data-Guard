from ninja import Schema
from typing import Optional


class SearchResult(Schema):
    search_query: str
    search_response: Optional[str]
    search_metadata: Optional[str]
