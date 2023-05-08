from rest_framework import permissions

from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_swagger.views import get_swagger_view
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from inventario.urls import routers

schema_view = get_schema_view(
    openapi.Info(
        title="API Title",
        default_version='v1',
        description="API description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@xyz.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [

    path('api/v1/',include('inventario.urls')),

    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
