from django.conf.urls import patterns, url

from galeria import views


urlpatterns = patterns('',
    url(
        '^(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        views.PictureDetail.as_view(),
        name='galeria-picture'
    ),
    url(
        '^album/(?P<slug>[-\w]+)/$',
        views.AlbumDetail.as_view(),
        name='galeria-album'
    ),
    url('^$', views.AlbumList.as_view(), name='galeria-album-list'),
)
