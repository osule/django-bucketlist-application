# bucketlist URL Configuration

from django.conf.urls import include, url, patterns
from django.contrib import admin
from settings.base import STATIC_ROOT
from website import urls as website_urls
from api import urls as api_urls

urlpatterns = [
             url('^', include(website_urls)),
             url('^api/', include(api_urls)),
             url(r'^docs/', include('rest_framework_swagger.urls')),
    ]


urlpatterns += patterns(
    '', url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns(
    '',
    (
        r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': STATIC_ROOT}
    ),
)
