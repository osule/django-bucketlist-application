from django.conf.urls import url, include
import api.views as views


urlpatterns = [    

    url(r'^bucketlists/$',
        views.BucketlistList.as_view(),
        name='api.bucketlists'),
    
    url(r'^bucketlists/(?P<pk>[0-9]+)/$',
        views.BucketlistDetail.as_view(),
        name='api.bucketlist'),
    
    url(r'^bucketlists/(?P<pk>[0-9]+)/items/$',
        views.BucketlistItemCreate.as_view(),
        name='api.bucketlist.create'),
               
    url(r'^bucketlists/(?P<pk>[0-9]+)/items/(?P<pk_item>[0-9]+)$',
        views.BucketlistItemDetail.as_view(),
        name='api.bucketlist.item'),

    url(r'^auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
    
    url(r'', include('rest_framework.urls', namespace='rest_framework')),
    
]
