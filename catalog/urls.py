from django.urls import include, path

from catalog import views
from catalog.apps import CatalogConfig
from catalog.views import home

app_name = CatalogConfig.name

urlpatterns = [
    path("", views.home, name="home"),
    path("contacts/", views.contacts, name="contacts"),
    path('product/<int:pr_id>/', views.product_detail, name='product_detail'),
]
