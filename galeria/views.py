from django.views import generic

from galeria.models import Album, Picture


class AlbumDetail(generic.detail.DetailView):
    model = Album
    queryset = Album.objects.public()


class AlbumList(generic.list.ListView):
    model = Album
    queryset = Album.objects.public()
    paginate_by = 20


class PictureDetail(generic.detail.DetailView):
    model = Picture
    queryset = Picture.objects.public()
