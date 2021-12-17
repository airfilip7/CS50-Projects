from django.urls import path, register_converter
from . import views
from auctions import converters
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

register_converter(converters.EmptyOrSlug, 'emptyorslug')

urlpatterns = [
    path("", views.index, name="index"),
    path("view/<str:title>", views.view, name="view"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register1", views.register1, name="register1"),
    path("categories/", views.categories, kwargs={'filter': ''},  name="categories"),
    path("categories/<str:filter>", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create", views.create, name="create"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



