from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

import catalog
from catalog.views import ContactsView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls", namespace="blog")),
    path("", include("catalog.urls", namespace="catalog")),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("accounts/", include("users.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
