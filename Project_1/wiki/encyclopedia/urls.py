from django.urls import path
from . import views


urlpatterns = [
    path("wiki/", views.index, name="index"),
    path("new_page/", views.new_page, name="new_page"),
    path("rand_page/", views.rand_page, name="rand_page"),
    path("wiki/<str:title>/", views.view, name="view"),
    path("search/", views.search, name="search"),
    path("edit/<str:title>/", views.edit, name="edit")
]
