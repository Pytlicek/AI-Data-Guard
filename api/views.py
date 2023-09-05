from django.shortcuts import redirect
from ninja import NinjaAPI
from . import schemas
from dataguard.settings import env

api = NinjaAPI(title="AI DataGuard API", description="DG API Endpoints", version="1.0.0")


@api.get("/", include_in_schema=False)
def hello(request):
    return redirect("./docs#/")


@api.get(
    "/search/{str:search_query}",
    response=schemas.SearchResult,
    tags=["search"],
)
def get_search(request, search_query: str):
    """
    **Search for text**
    <br><br>
    **Try fe.** `Test`
    """
    example_variable_from_env = env(
        "API_USERNAME",
        default="ENV1",
    )
    search_result = {
        "search_query": search_query,
        "search_response": f"example search_response for: {search_query}",
        "search_metadata": example_variable_from_env,
    }
    return search_result
