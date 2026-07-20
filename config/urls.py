from django.contrib import admin
from django.urls import include, path

import catalog

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("catalog.urls", namespace="catalog")),
    path("contacts/", catalog.views.contacts, name="contacts"),
]
