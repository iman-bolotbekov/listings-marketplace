from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Listing API",
      default_version='v-0.1-alpha',
      description="API for interacting with Listing API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="listing@gmail.com"),
      license=openapi.License(name="No Licence"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/listing/', include('marketplace.urls')),
    path('auth/user/', include('user.urls')),

    # documentation URL
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_doc'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc_doc'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )