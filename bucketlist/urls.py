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
from website import views

urlpatterns = [
    url(r'^(?P<filename>(robots.txt)|(humans.txt))$',
        views.RootFilesView.as_view(), name='app.files'),
]

urlpatterns += patterns(
    '',
    url(r'^$', views.RootView.as_view(), name='app.index'),
    url(r'^login$', views.LoginView.as_view(), name='app.login'),
    url(r'^accounts/login/$', views.RootView.as_view(), name='app.index'),
    url(r'^signup$', views.SignUpView.as_view(), name='app.signup'),
    url(r'^logout$', views.LogoutView.as_view(), name='app.logout'),
    url(r'^dashboard$', views.DashboardView.as_view(),
        name='app.dashboard'),
    url(r'^bucketlists$', views.BucketlistView.as_view(),
        name='app.bucketlists'),
    url(r'^bucketlists/(?P<id>[0-9]+)/', views.BucketlistEditView.as_view(),
        name='app.bucketlist'),
    url(r'^bucketlists/(?P<id>[0-9]+)/items$',
        views.BucketlistView.as_view(),
        name='app.bucketlist.items'),

    url(r'^bucketlists/(?P<id>[0-9]+)/items/(?P<item_id>[0-9]+)$',
        views.BucketlistItemEditView.as_view(),
        name='app.bucketlist.item'),
)

urlpatterns += patterns(
    '', url(r'^admin/', include(admin.site.urls)),
)
