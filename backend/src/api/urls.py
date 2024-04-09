from django.urls import path
from rest_framework import permissions
# from rest_framework.schemas import get_schema_view  # TODO
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views

# TODO
schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)

urlpatterns = [
    path('swagger<format>/',
         schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/',
         schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    path('sic-codes/', views.SICCodeList.as_view()),
    path('sic-codes/<int:sic_code>', views.SICCodeDetail.as_view()),
    path('naics-codes/', views.NAICSCodeList.as_view()),
    path('naics-codes/<int:pk>', views.NAICSCodeDetail.as_view()),
    path('ten-k/', views.TenKList.as_view()),
    path('ten-k/<int:cik>/<str:filing_date>', views.TenKDetail.as_view()),
]
