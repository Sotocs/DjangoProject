from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

import catalog
from catalog.views import ContactsView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("catalog.urls", namespace="catalog")),
    path("contacts/", ContactsView.as_view(), name="contacts"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
