"""bucketlist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
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

urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': STATIC_ROOT}),
    )