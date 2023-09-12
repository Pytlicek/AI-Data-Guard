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
    response=schemas.CheckRobotsResult,
    tags=["check"],
)
def get_check_robots_by_domain_name(request, domain_name: str):
    """
    **Endpoint to check robots.txt rules for a given Domain name**
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
    **Endpoint to check robots.txt rules for a given URL.**
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
