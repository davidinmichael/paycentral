from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

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

    path("", include("paymentoptions.urls")),
    path("", include("countries.urls")),
]
