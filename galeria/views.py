from django import http
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from galeria.forms import ZipUploadForm
from galeria.models import Album, Picture


class AlbumDetail(generic.detail.DetailView):
    model = Album


class AlbumList(generic.list.ListView):
    model = Album
    paginate_by = 20


class PictureDetail(generic.detail.DetailView):
    model = Picture


@login_required
def zip_upload(request, template='galeria/admin/zip_upload_form.html'):
    if not request.user.has_perm('galeria.add_picture'):
        raise PermissionDenied

    form = ZipUploadForm()

    if request.method == 'POST':
        form = ZipUploadForm(request.POST, request.FILES)
        if form.is_valid():
            picture_list = form.process_zip_archive()
            Picture.objects.bulk_create(picture_list)

            # Send user to album change view to edit the uploaded pictures
            album = form.cleaned_data['album']
            url = reverse('admin:galeria_album_change', args=[album.pk])
            return http.HttpResponseRedirect(url + '#pictures-group')

    context = {
        'title': _('ZIP Upload'),
        'zip_upload_form': form
    }
    return render_to_response(template, context, context_instance=RequestContext(request))
