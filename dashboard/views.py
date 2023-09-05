from django.shortcuts import render


def index(request):
    return render(request, "dashboard/index.html")


def tools(request):
    return render(request, "dashboard/tools.html")
