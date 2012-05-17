from django import forms
from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from imagekit.admin import AdminThumbnail
from mptt.admin import MPTTModelAdmin

from galeria.forms import AlbumForm
from galeria.models import Album, Picture


class PictureAdmin(admin.ModelAdmin):
    change_list_template = 'galeria/admin/change_list.html'
    list_display = ('thumbnail', 'title', 'is_public', 'album', 'date_added')
    list_display_links = ('title',)
    list_editable = ('album', 'is_public')
    list_filter = ('date_added', 'album', 'is_public')
    list_per_page = 20
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'slug', 'description')

    thumbnail = AdminThumbnail(
        image_field='thumbnail_image',
        template='galeria/admin/thumbnail.html'
    )
    thumbnail.short_description = _('thumbnail')

admin.site.register(Picture, PictureAdmin)


class InlinePictureAdmin(admin.TabularInline):
    extra = 1
    model = Picture
    ordering = ('-date_added',)
    prepopulated_fields = {'slug': ('title',)}
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows':3,'cols':30})}
    }

class AlbumAdmin(MPTTModelAdmin):
    change_list_template = 'galeria/admin/change_list.html'
    form = AlbumForm
    inlines = [InlinePictureAdmin]
    list_display = ('title', 'album_cover', 'is_public', 'order')
    list_editable = ('is_public', 'order')
    list_filter = ['is_public']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'slug', 'description')

    def album_cover(self, obj):
        cover = obj.available_cover
        if not cover:
            return _('<em>Not defined</em>')
        html = '<img src="%s" alt="%s" style="width: 42px;" />'
        return html % (cover.cover_image.url, cover.title)
    album_cover.allow_tags = True
    album_cover.short_description = _('cover')

admin.site.register(Album, AlbumAdmin)
