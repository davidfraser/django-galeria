# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from galeria import views


urlpatterns = patterns('',
    url(
        '^(?P<album_slug>[-\w]+)/(?P<pk>[0-9]+)/(?P<slug>[-\w]+)/$',
        views.PictureDetail.as_view(),
        name='galeria-picture'
    ),
    url(
        '^(?P<slug>[-\w]+)/$',
        views.AlbumDetail.as_view(),
        name='galeria-album'
    ),
    url('^$', views.AlbumList.as_view(), name='galeria-album-list'),
)
