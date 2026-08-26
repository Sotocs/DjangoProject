from django.urls import include, path

from catalog.apps import CatalogConfig
from catalog.views import (
    ContactsView,
    HomeView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductUpdateView,
    UnpublishProductView,
    ProductsByCategoryView,
)

app_name = CatalogConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("product/create/", ProductCreateView.as_view(), name="product_create"),
    path(
        "product/update/<int:pk>/", ProductUpdateView.as_view(), name="product_update"
    ),
    path(
        "product/delete/<int:pk>/", ProductDeleteView.as_view(), name="product_delete"
    ),
    path(
        "product/<int:pk>/unpublish/",
        UnpublishProductView.as_view(),
        name="product_unpublish",
    ),
    path(
        "products/category/<int:pk>/",
        ProductsByCategoryView.as_view(),
        name="products_by_category",
    ),
]
