# -*- coding: utf-8 -*-

import os
import zipfile

from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from mptt.forms import TreeNodeChoiceField

from galeria.models import Album, Picture


class AlbumForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # Set available cover choices for a album
        super(AlbumForm, self).__init__(*args, **kwargs)
        descendants_set = self.instance.get_descendants(include_self=True)
        descendants_ids = descendants_set.filter(is_public=True).values('id')
        picture_set = Picture.objects.public().filter(album__in=descendants_ids)
        self.fields['cover'].queryset = picture_set.order_by('-date_added')

    class Meta:
        model = Album


class ZipUploadForm(forms.Form):
    zip_archive = forms.FileField(
        label=_('ZIP archive'),
        help_text=_('Invalid or corrupted image files inside the ZIP archive '
                    'are ignored.')
    )
    album = TreeNodeChoiceField(
        label=_('Album'),
        queryset=Album.objects.all(),
        empty_label=''
    )

    def clean_zip_archive(self):
        zip_archive = self.cleaned_data.get('zip_archive')
        if zip_archive:
            try:
                zfile = zipfile.ZipFile(zip_archive)
                if zfile.testzip():
                    raise zipfile.BadZipfile
                zfile.close()
            except zipfile.BadZipfile:
                error_msg = _('File is not a ZIP archive or is corrupted.')
                raise forms.ValidationError(error_msg)
        return zip_archive

    def process_zip_archive(self):
        album = self.cleaned_data.get('album')
        zip_archive = self.cleaned_data.get('zip_archive')
        if not zip_archive:
            return

        zfile = zipfile.ZipFile(zip_archive)
        picture_list = []

        for filename in zfile.namelist():
            title = os.path.basename(os.path.splitext(filename)[0])
            slug = slugify(title)
            picture = Picture(title=title, slug=slug, is_public=False, album=album)
            try:
                content = zfile.read(filename)
                image_file = SimpleUploadedFile(filename, content)
                picture.original_image = forms.ImageField().clean(image_file)
            except forms.ValidationError:
                continue
            else:
                picture_list.append(picture)

        return picture_list
