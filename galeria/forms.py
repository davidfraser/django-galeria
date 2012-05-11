from django import forms
from galeria.models import Album, Picture


class AlbumAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AlbumAdminForm, self).__init__(*args, **kwargs)
        descendants_set = self.instance.get_descendants(include_self=True).filter(is_public=True)
        descendants_ids = descendants_set.values('id')
        picture_set = Picture.objects.public().filter(album__in=descendants_ids).order_by('-date_added')
        self.fields['cover'].queryset = picture_set

    class Meta:
        model = Album
