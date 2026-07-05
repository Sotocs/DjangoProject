from django.urls import include, path

from catalog import views
from catalog.apps import CatalogConfig
from catalog.views import home

app_name = CatalogConfig.name

urlpatterns = [
    path("", views.home, name="home"),
    path("/contacts/", views.contacts, name="contacts"),
]
