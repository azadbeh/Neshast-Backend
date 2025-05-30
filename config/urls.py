from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/organization/", include("apps.organizations.urls", namespace="organizations")),
    path("api/v1/users/", include("apps.users.urls", namespace="users")),
    path("api/v1/events/", include("apps.events.urls", namespace="events")),
    path("api/v1/news/", include("apps.news.urls", namespace="news")),
    path("api/v1/swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("api/v1/swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/v1/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
