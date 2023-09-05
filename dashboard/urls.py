from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="dashboard_index"),
    path("tools", views.tools, name="tools"),
]
