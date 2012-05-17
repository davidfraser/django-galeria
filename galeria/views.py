from django.views import generic

from galeria.models import Album, Picture


class AlbumDetail(generic.detail.DetailView):
    model = Album


class AlbumList(generic.list.ListView):
    model = Album
    paginate_by = 20


class PictureDetail(generic.detail.DetailView):
    model = Picture
