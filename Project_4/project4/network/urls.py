
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register1", views.register1, name="register1"),
    path("profile/<str:username>", views.profile, name="profile"),
    
    #API fetch routes
    path("add", views.add, name="add"),
    path("profile/<str:username>/follow", views.profile, name="follow"),
    path("edit", views.edit, name="edit"),
    path("like", views.like, name="like"),
    path("following", views.following, name="following"),

]
