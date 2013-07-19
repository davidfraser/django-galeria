# -*- coding: utf-8 -*-

from django import forms
from django import http
from django.conf.urls import patterns, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db import models
from django.template.response import TemplateResponse
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _
from mptt.admin import MPTTModelAdmin

from galeria.forms import AlbumForm, ZipUploadForm
from galeria.models import Album, Picture


class PictureAdmin(admin.ModelAdmin):
    change_list_template = 'galeria/admin/change_list.html'
    list_display = ('title', 'is_public', 'album', 'date_added')
    list_display_links = ('title',)
    list_editable = ('album', 'is_public')
    list_filter = ('date_added', 'album', 'is_public')
    list_per_page = 20
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'slug', 'description')

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.module_name
        default_patterns = super(PictureAdmin, self).get_urls()
        custom_patterns = patterns('', url(
            r'^zip_upload/$',
            self.admin_site.admin_view(self.zip_upload_view),
            name='%s_%s_zip_upload' % info
        ))
        return custom_patterns + default_patterns

    def zip_upload_view(self, request, template='galeria/admin/zip_upload_form.html'):
        model = self.model
        opts = model._meta
        form = ZipUploadForm()

        if request.method == 'POST':
            form = ZipUploadForm(request.POST, request.FILES)
            if form.is_valid():
                album = form.cleaned_data['album']
                picture_list = form.process_zip_archive()
                model.objects.bulk_create(picture_list)

                # Send user to album change view to edit the uploaded pictures
                if request.user.has_perm('galeria.change_album', album):
                    url_ = reverse('admin:galeria_album_change', args=[album.pk])
                    return http.HttpResponseRedirect(url_ + '#pictures-group')
                url_ = reverse('admin:galeria_picture_changelist')
                return http.HttpResponseRedirect(url_)

        context = {
            'app_label': opts.app_label,
            'has_add_permission': self.has_add_permission(request),
            'has_change_permission': self.has_change_permission(request),
            'module_name': force_unicode(opts.verbose_name_plural),
            'opts': opts,
            'title': _('ZIP Upload'),
            'form': form,
        }
        return TemplateResponse(request, template, context, current_app=self.admin_site.name)

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
    list_display = ('title', 'is_public', 'order')
    list_editable = ('is_public', 'order')
    list_filter = ['is_public']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'slug', 'description')

admin.site.register(Album, AlbumAdmin)
