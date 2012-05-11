from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from imagekit.admin import AdminThumbnail
from feincms.admin import editor

from galeria.forms import AlbumAdminForm
from galeria.models import Album, Picture


# Hack to easier translate some strings from FeinCMS
OPEN_TREE_STR = _('Expand tree')
COLLAPSE_TREE_STR = _('Collapse tree')


class PictureAdmin(admin.ModelAdmin):
    list_display = ('admin_thumbnail', 'title', 'album', 'date_added', 'is_public')
    list_display_links = ['title']
    list_filter = ['date_added', 'album', 'is_public']
    list_per_page = 20
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'slug', 'description')

    admin_thumbnail = AdminThumbnail(
        image_field='thumbnail_image',
        template='galeria/admin/thumbnail.html'
    )
    admin_thumbnail.short_description = _('thumbnail')

admin.site.register(Picture, PictureAdmin)


class InlinePictureAdmin(admin.TabularInline):
    extra = 1
    model = Picture
    prepopulated_fields = {'slug': ('title',)}

class AlbumAdmin(editor.TreeEditor):
    form = AlbumAdminForm
    inlines = [InlinePictureAdmin]
    list_display = ('title', 'album_cover', 'is_public', 'order')
    list_filter = ['is_public']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'slug', 'description')
    #mptt_level_indent = 20

    def album_cover(self, obj):
        cover = obj.available_cover
        if not cover:
            return _('<em>Not defined</em>')
        return '<img src="%s" alt="%s" style="width: 42px;" />' % (cover.cover_image.url, cover.title)
    album_cover.allow_tags = True
    album_cover.short_description = _('cover')

admin.site.register(Album, AlbumAdmin)
