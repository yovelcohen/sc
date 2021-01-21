from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView

from api.admin import consumer_admin
from common.base.views import PermittedSwagger, PermittedReDoc
from config.config import SILK

admin.autodiscover()
admin.site.enable_nav_sidebar = False

urlpatterns = [
    # ADMIN
    path('admin/', consumer_admin.urls),
    # DOCS
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/swagger', PermittedSwagger.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/redoc/', PermittedReDoc.as_view(url_name='schema'), name='redoc'),
    # AUTH
    url(r'auth/', include('users.urls')),
    # ENDPOINTS
    url(r'api/', include('api.urls')),
    url(r'management/', include('account_management_api.urls'))
]

if SILK is True:
    urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]
