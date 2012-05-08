from django.views import generic

from galeria.models import Album, Picture


class AlbumDetail(generic.detail.DetailView):
    model = Album


class AlbumList(generic.list.ListView):
    model = Album
    paginate_by = 20


class PictureDetail(generic.dates.DateDetailView):
    date_field = 'date_added'
    model = Picture
    month_format = '%m'
    slug_field = 'slug'
