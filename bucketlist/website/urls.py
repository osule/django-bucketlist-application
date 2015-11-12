from django.conf.urls import url  
import website.views as views


urlpatterns = [
        url(r'^(?P<filename>(robots.txt)|(humans.txt))$',
            views.RootFilesView.as_view(), name='app.files'),
    ]

urlpatterns += [    
    url(r'^$',
        views.RootView.as_view(),
        name='app.index'),
    url(r'^login$',
        views.LoginView.as_view(),
        name='app.login'),
    url(r'^signup/$',
        views.SignUpView.as_view(),
        name='app.signup'),
    url(r'^logout/$',
        views.LogoutView.as_view(),
        name='app.logout'),
    url(r'^dashboard/$',
        views.DashboardView.as_view(),
        name='app.dashboard'),

    url(r'^bucketlists/$',
        views.BucketlistListView.as_view(),
        name='app.bucketlists'),
    url(r'^bucketlists/(?P<pk>[0-9]+)/$',
        views.BucketlistDetailView.as_view(),
        name='app.bucketlist'),

    url(r'^bucketlists/create/$',
        views.BucketlistCreateView.as_view(),
        name='app.bucketlist.create'),
    url(r'^bucketlists/(?P<pk>[0-9]+)/delete/$',
        views.BucketlistDeleteView.as_view(),
        name='app.bucketlist.delete'),
    url(r'^bucketlists/(?P<pk>[0-9]+)/update/$',
        views.BucketlistUpdateView.as_view(),
        name='app.bucketlist.update'),

    url(r'^bucketlists/(?P<pk>[0-9]+)/items/$',
        views.BucketlistItemListView.as_view(),
        name='app.bucketlist.items'),
    url(r'^bucketlists/(?P<pk>[0-9]+)/items/(?P<pk_item>[0-9]+)$',
        views.BucketlistItemDetailView.as_view(),
        name='app.bucketlist.item'),

    url(r'^bucketlists/(?P<pk>[0-9]+)/items/create/$',
        views.BucketlistItemCreateView.as_view(),
        name='app.bucketlist.item.create'),
    url(r'^bucketlists/(?P<pk>[0-9]+)/items/(?P<pk_item>[0-9]+)/delete/$',
        views.BucketlistItemDeleteView.as_view(),
        name='app.bucketlist.item.delete'),
    url(r'^bucketlists/(?P<pk>[0-9]+)/items/(?P<pk_item>[0-9]+)/update/$',
        views.BucketlistItemUpdateView.as_view(),
        name='app.bucketlist.item.update'),
                        
    url(r'^/bucketlists?q=(?P<query_string>[^\r\n]+)',
        views.BucketlistListView.as_view())    
]
