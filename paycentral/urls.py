from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api_schema/", get_schema_view(
        title="PayCentral API", description="Curates Payment Options",
        version=1.0
    ), name="api_schema"),

    path("api_docs/", TemplateView.as_view(
        template_name="swagger-ui.html",
        extra_context={
            "schema_url": "api_schema"
        })),

    path("account/", include("account.urls")),
    path("", include("paymentoptions.urls")),
    path("", include("countries.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
