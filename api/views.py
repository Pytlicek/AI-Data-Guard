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


from checkers.robots_checker import check_robots_domain, check_robots_url


@api.get(
    "/check/robots/by_domain_name",
    response=schemas.CheckRobotsResult,
    tags=["check"],
)
def get_check_robots_by_domain_name(request, domain_name: str):
    """
    **Search for text**
    <br><br>
    **Try fe.** `amazon.com`
    """
    check_domain = check_robots_domain(domain_name)
    print("check_domain:", check_domain)
    check_result = {
        "domain_name": domain_name,
        "gptbot_is_allowed": check_domain["gptbot_is_allowed"],
        "gptbot_definition_explicit": check_domain[
            "gptbot_definition_explicit"]
    }
    return check_result


@api.get(
    "/check/robots/by_url",
    response={200: schemas.CheckRobotsResultURL, 400: schemas.ErrorSchema},
    tags=["check"],
)
def get_check_robots_by_url(request, url: str):
    """
    **Search for text**
    <br><br>
    **Try fe.** `https://amazon.com/`
    """
    try:
        check_domain = check_robots_url(url)
        print("check_domain:", check_domain)
        check_result = {
            "url": url,
            "domain_name": check_domain["domain_name"],
            "gptbot_is_allowed": check_domain["gptbot_is_allowed"],
            "gptbot_definition_explicit": check_domain[
                "gptbot_definition_explicit"]
        }
        return 200, check_result
    except Exception as e:
        return 400, schemas.ErrorSchema(error=str(e))
