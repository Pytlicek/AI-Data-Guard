from checkers.robots_checker import check_robots_domain, check_robots_url
from dataguard.settings import env
from django.shortcuts import redirect
from ninja import NinjaAPI
from . import schemas

api = NinjaAPI(title="AI DataGuard API", description="DG API Endpoints",
               version="1.0.0")


@api.get("/", include_in_schema=False)
def hello(request):
    return redirect("./docs#/")


@api.get(
    "/check/robots/by_domain_name",
    response={200: schemas.CheckRobotsResult, 400: schemas.ErrorSchema},
    tags=["check"],
)
def get_check_robots_by_domain_name(request, domain_name: str, user_agent: str = None):
    """
    **Endpoint to check robots.txt rules for a given Domain name**
    <br><br>
    **Try fe.** `amazon.com`
    """
    try:
        check_domain = check_robots_domain(domain_name, user_agent)
        print("check_domain:", check_domain, "user_agent:", user_agent)
        check_result = {
            "domain_name": domain_name,
            "gptbot_is_allowed": check_domain["gptbot_is_allowed"],
            "gptbot_definition_explicit": check_domain[
                "gptbot_definition_explicit"]
        }
        return check_result
    except Exception as e:
        return 400, schemas.ErrorSchema(error=str(e))


@api.get(
    "/check/robots/by_url",
    response={200: schemas.CheckRobotsResultURL, 400: schemas.ErrorSchema},
    tags=["check"],
)
def get_check_robots_by_url(request, url: str, user_agent: str = None):
    """
    **Endpoint to check robots.txt rules for a given URL.**
    <br><br>
    **Try fe.** `https://amazon.com/`
    """
    try:
        check_domain = check_robots_url(url, user_agent=user_agent)
        print("url:", url, "user_agent:", user_agent)
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
