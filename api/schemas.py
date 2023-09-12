from ninja import Schema
from typing import Optional


class SearchResult(Schema):
    search_query: str
    search_response: Optional[str]
    search_metadata: Optional[str]


class CheckRobotsResult(Schema):
    domain_name: str
    gptbot_is_allowed: bool
    gptbot_definition_explicit: bool


class CheckRobotsResultURL(Schema):
    domain_name: str
    url: str
    gptbot_is_allowed: bool
    gptbot_definition_explicit: bool


class ErrorSchema(Schema):
    error: str
